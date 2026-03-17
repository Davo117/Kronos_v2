"""
Servicio Maestro de Catálogos - KronosSystem.
Centraliza la lógica de negocio para Infraestructura, Comercial, Materiales, 
RRHH (Seguridad) y Herramental.

"""
import re
from sqlalchemy.orm import Session
from src.modules.common import models as c_models
from src.modules.engineering import models as e_models
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

# --- INFRAESTRUCTURA (PROCESOS Y MÁQUINAS) ---

def registrar_proceso(db: Session, nombre: str):
    """
    Crea un proceso maestro generando una sigla única de 2 caracteres.
    Absorbe la lógica del antiguo process_service.
    """
    # Limpieza de nombre para generar sigla (solo letras)
    nombre_limpio = re.sub(r'[^a-zA-Z]', '', nombre).upper()
    if len(nombre_limpio) < 2:
        raise ValueError("Nombre demasiado corto para generar sigla.")

    # Algoritmo de generación de sigla única
    fijo = nombre_limpio[0]
    nueva_sigla = None
    for i in range(1, len(nombre_limpio)):
        candidata = fijo + nombre_limpio[i]
        existe = db.query(c_models.ProcesoMaestro).filter(c_models.ProcesoMaestro.sigla == candidata).first()
        if not existe:
            nueva_sigla = candidata
            break
    
    if not nueva_sigla:
        raise RuntimeError(f"No hay combinaciones únicas disponibles para: {nombre}")

    nuevo_proceso = c_models.ProcesoMaestro(nombre_proceso=nombre.upper(), sigla=nueva_sigla)
    db.add(nuevo_proceso)
    try:
        db.commit()
        db.refresh(nuevo_proceso)
        return nuevo_proceso
    except IntegrityError:
        db.rollback()
        raise ValueError("Race condition: El proceso o sigla ya fue creado por otro usuario.")

def registrar_maquina(db: Session, descripcion: str, id_proceso: int):
    """
    Registra una nueva máquina y genera un código técnico: MT-[SIGLA]-[ID].
    """
    proceso = db.query(c_models.ProcesoMaestro).filter(c_models.ProcesoMaestro.id == id_proceso).first()
    if not proceso:
        raise ValueError("El proceso especificado no existe.")

    nueva_maquina = c_models.Maquina(
        descripcion=descripcion.upper(),
        id_proceso=id_proceso,
        codigo_maquina="TEMP"
    )
    db.add(nueva_maquina)
    db.flush() 

    nueva_maquina.codigo_maquina = f"MT-{proceso.sigla}-{str(nueva_maquina.id).zfill(3)}"
    
    try:
        db.commit()
        db.refresh(nueva_maquina)
        return nueva_maquina
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad: El código de máquina ya existe.")

# --- RRHH Y SEGURIDAD (ROLES Y USUARIOS) ---

def registrar_rol(db: Session, nombre: str, descripcion: str = None):
    """Define facultades de acceso en el sistema."""
    nuevo_rol = c_models.Rol(nombre=nombre.upper(), descripcion=descripcion)
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

def crear_usuario(db: Session, id_empleado: int, id_rol: int, username: str, password_hash: str):
    """
    Vincula un empleado con credenciales de acceso administrativo.
    ADVERTENCIA: La contraseña debe llegar ya hasheada a esta función.
    """
    nuevo_usuario = c_models.Usuario(
        id_empleado=id_empleado,
        id_rol=id_rol,
        username=username.lower(),
        password_hash=password_hash,
        activo=True
    )
    db.add(nuevo_usuario)
    try:
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except IntegrityError:
        db.rollback()
        raise ValueError("El nombre de usuario ya está en uso o el empleado ya tiene cuenta.")

def registrar_empleado(db: Session, nombre: str, numero_empleado: str):
    """Alta de personal de planta para trazabilidad de UPIDs."""
    nuevo_e = c_models.Empleado(nombre=nombre.upper(), numero_empleado=numero_empleado)
    db.add(nuevo_e)
    try:
        db.commit()
        db.refresh(nuevo_e)
        return nuevo_e
    except IntegrityError:
        db.rollback()
        raise ValueError(f"El número de empleado '{numero_empleado}' ya existe.")

# --- COMERCIAL ---

def registrar_cliente_con_matriz(db: Session, nombre: str, direccion_matriz: str):
    """Crea cliente y sucursal matriz de forma atómica."""
    try:
        nuevo_cliente = c_models.Cliente(nombre=nombre.upper())
        db.add(nuevo_cliente)
        db.flush() 

        nueva_sucursal = c_models.Sucursal(
            id_cliente=nuevo_cliente.id,
            nombre_sucursal="MATRIZ",
            direccion_completa=direccion_matriz
        )
        db.add(nueva_sucursal)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente
    except Exception as e:
        db.rollback()
        raise ValueError(f"Fallo en registro atómico: {str(e)}")

# --- MATERIALES Y HERRAMENTAL ---

def gestionar_sustrato(db: Session, descripcion: str, codigo_interno: str, altura_material: Decimal, gramaje: Decimal, espesor: Decimal = None):
    """Alta de sustratos con validación física."""
    if altura_material <= 0 or gramaje <= 0:
        raise ValueError("Altura y gramaje deben ser valores positivos.")
    
    nuevo_s = c_models.Sustrato(
        descripcion=descripcion.upper(),
        codigo_interno=codigo_interno.upper(),
        altura_material=altura_material,
        gramaje=gramaje,
        espesor=espesor
    )
    db.add(nuevo_s)
    try:
        db.commit()
        db.refresh(nuevo_s)
        return nuevo_s
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Código interno '{codigo_interno}' ya registrado.")

def registrar_pantone(db: Session, codigo_hex: str, descripcion: str, codigo_pantone: str):
    """Registro de colores para formulación."""
    nuevo_p = c_models.Pantone(
        codigo_hex=codigo_hex.upper(), 
        descripcion=descripcion.upper(), 
        codigo_pantone=codigo_pantone.upper()
    )
    db.add(nuevo_p)
    try:
        db.commit()
        db.refresh(nuevo_p)
        return nuevo_p
    except IntegrityError:
        db.rollback()
        raise ValueError("Código Pantone o HEX ya registrados.")

def registrar_cilindro(db: Session, desarrollo_mm: Decimal, repeticion: int, tipo_engrane: str):
    """Registra juegos de cilindros en el catálogo de ingeniería."""
    nuevo_c = e_models.JuegoCilindro(
        desarrollo_mm=desarrollo_mm, 
        repeticion=repeticion, 
        tipo_engrane=tipo_engrane.upper()
    )
    db.add(nuevo_c)
    db.commit()
    db.refresh(nuevo_c)
    return nuevo_c

def registrar_cirel(db: Session, espesor: Decimal, lineaje: int, descripcion: str):
    """Registra grabados flexográficos."""
    nuevo_cr = e_models.Cirel(
        espesor=espesor, 
        lineaje=lineaje, 
        descripcion=descripcion.upper()
    )
    db.add(nuevo_cr)
    db.commit()
    db.refresh(nuevo_cr)
    return nuevo_cr