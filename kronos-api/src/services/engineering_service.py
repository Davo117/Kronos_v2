"""
Servicio de Gestión de Ingeniería - KronosSystem.
Administra el ciclo de vida de las Fichas Técnicas (FT) y sus versiones.
Flujo: BORRADOR -> PEND_EMPAQUE -> PEND_CALIDAD -> APROBADA.

"""
from sqlalchemy.orm import Session
from src.modules.engineering import models, schemas
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

def crear_ficha_maestra(db: Session, id_cliente: int, nombre_disenio: str):
    """
    Registra un nuevo producto (Ficha Maestra) en el catálogo.
    """
    nueva_ficha = models.FichaTecnica(
        id_cliente=id_cliente,
        nombre_disenio=nombre_disenio.upper()
    )
    db.add(nueva_ficha)
    try:
        db.commit()
        db.refresh(nueva_ficha)
        return nueva_ficha
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al crear ficha maestra: {str(e)}")

def registrar_nueva_version(db: Session, data: schemas.FTVersionCreate):
    """
    Genera una iteración técnica en estado BORRADOR.
    Calcula el número de versión automáticamente.
    """
    # Consulta de la versión más reciente para autoincrementar
    ultima_v = db.query(models.FTVersion)\
        .filter(models.FTVersion.id_ficha == data.id_ficha)\
        .order_by(models.FTVersion.numero_version.desc())\
        .first()
    
    siguiente_num = (ultima_v.numero_version + 1) if ultima_v else 1

    nueva_version = models.FTVersion(
        id_ficha=data.id_ficha,
        numero_version=siguiente_num,
        pistas=data.pistas,
        avance_paso=data.avance_paso,
        id_sustrato=data.id_sustrato,
        id_juego_cilindro=data.id_juego_cilindro,
        id_cirel=data.id_cirel,
        id_creador_logistica=data.id_creador_logistica,
        estado='BORRADOR'
    )
    
    db.add(nueva_version)
    try:
        db.commit()
        db.refresh(nueva_version)
        return nueva_version
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad: Verifique que los IDs de sustrato/herramental existen.")

def configurar_empaque_y_avanzar(db: Session, id_version: int, empaque_data: schemas.FTConfigEmpaqueCreate):
    """
    Establece la configuración de empaque y mueve la versión a PEND_CALIDAD.
    Solo el personal de Empaque debe ejecutar esta acción.
    """
    version = db.query(models.FTVersion).filter(models.FTVersion.id == id_version).first()
    if not version:
        raise ValueError("La versión técnica no existe.")

    # Crear o actualizar configuración de empaque
    config = models.FTConfigEmpaque(
        id_version=id_version,
        **empaque_data.model_dump()
    )
    
    db.add(config)
    version.estado = 'PEND_CALIDAD'
    
    db.commit()
    db.refresh(version)
    return version

def dictaminar_version(db: Session, id_version: int, id_aprobador: int, aprobado: bool):
    """
    Aprobación o Rechazo final por parte de Calidad (QC).
    Si se aprueba, la FT queda liberada para Producción.
    """
    version = db.query(models.FTVersion).filter(models.FTVersion.id == id_version).first()
    if not version:
        raise ValueError("La versión técnica no existe.")

    if aprobado:
        version.estado = 'APROBADA'
        version.fecha_aprobacion = datetime.now(timezone.utc)
    else:
        version.estado = 'RECHAZADA'
    
    version.id_aprobador_qc = id_aprobador
    db.commit()
    db.refresh(version)
    return version