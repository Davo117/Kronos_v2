"""
Servicio de Producción - KronosSystem.
Este servicio centraliza la lógica de orquestación para la creación de órdenes
de compra y el registro de trazabilidad (escaneos) en planta.

Funciones principales:
1. Programación de órdenes con desglose matemático de UPIDs.
2. Registro inmutable de eventos de proceso con validación de concurrencia.

"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.modules.production import models, schemas
from src.services.utils import barcode, calculator

def generar_orden_y_upids(db: Session, data: schemas.OrdenCompraCreate):
    """
    Registra una orden de compra y genera automáticamente sus unidades físicas (UPIDs).
    
    Proceso:
    1. Crea el encabezado de la OrdenCompra.
    2. Recupera la Ficha Técnica y el Sustrato para obtener constantes físicas.
    3. Calcula la longitud (metros) y el peso (Kg) teórico por cada unidad.
    4. Genera folios únicos e inmutables mediante el servicio de barcode.
    
    Args:
        db (Session): Conexión activa a la base de datos.
        data (OrdenCompraCreate): Esquema con la cantidad solicitada y unidades.
        
    Returns:
        models.OrdenCompra: La orden creada con sus unidades relacionadas.
    """
    try:
        # Instanciación de la cabecera de la orden
        nueva_orden = models.OrdenCompra(
            id_sucursal=data.id_sucursal,
            id_version_ft=data.id_version_ft,
            cantidad_solicitada=data.cantidad_solicitada,
            empaque_seleccionado=data.empaque_seleccionado
        )
        db.add(nueva_orden)
        
        # flush() es necesario para que SQLAlchemy obtenga el ID de la orden
        # y permita que las relaciones de 'version_ft' se carguen correctamente.
        db.flush() 

        # Acceso a datos técnicos mediante navegación ORM
        version = nueva_orden.version_ft
        sustrato = version.sustrato
        
        # --- CÁLCULOS INDUSTRIALES ---
        # Determinamos cuántas piezas van en cada bulto/rollo
        piezas_por_upid = data.cantidad_solicitada // data.cantidad_unidades
        
        # Calculamos los metros lineales usando el avance de paso y las pistas
        metros_teoricos = calculator.calcular_longitud_lineal(
            piezas_por_upid, version.pistas, version.avance_paso
        )
        
        # Calculamos el peso teórico basado en el área del material y su gramaje
        peso_teorico = calculator.calcular_peso_teorico(
            metros_teoricos, sustrato.altura_material, sustrato.gramaje
        )

        # --- GENERACIÓN DE UNIDADES (UPIDs) ---
        for _ in range(data.cantidad_unidades):
            # Obtención de folio inmutable con bloqueo pesimista en DB
            codigo = barcode.generar_upid_inmutable(db)
            
            nueva_unidad = models.UPID(
                codigo_upid=codigo,
                id_orden=nueva_orden.id,
                longitud_teorica=metros_teoricos,
                peso_teorico=peso_teorico,
                piezas_estimadas=piezas_por_upid
            )
            db.add(nueva_unidad)
        
        # Consolidación de la transacción atómica
        db.commit()
        db.refresh(nueva_orden)
        return nueva_orden
        
    except Exception as e:
        # En caso de error (ej. falta de datos técnicos), revertimos todo.
        db.rollback()
        raise ValueError(f"Fallo en motor de programación: {str(e)}")

def registrar_evento_planta(db: Session, evento_data: schemas.ScanEventRequest):
    """
    Registra el paso de un UPID por una estación de trabajo (proceso/máquina).
    
    Validaciones:
    - Evita que un operador registre dos veces la misma unidad en el mismo proceso
      capturando el IntegrityError de la base de datos (Race Condition).
    
    Args:
        db (Session): Conexión activa a la base de datos.
        evento_data (ScanEventRequest): Datos del escaneo (UPID, Empleado, Máquina).
        
    Returns:
        models.EventoProceso: El registro del evento exitoso.
    """
    try:
        # Creación del evento con timestamp en formato UTC para consistencia
        nuevo_evento = models.EventoProceso(
            id_upid=evento_data.id_upid,
            id_empleado=evento_data.id_empleado,
            id_maquina=evento_data.id_maquina,
            id_proceso=evento_data.id_proceso,
            fecha_hora=datetime.now(timezone.utc)
        )
        db.add(nuevo_evento)
        
        # El flush() dispara la validación de UniqueConstraint en MySQL
        db.flush()
        db.commit()
        db.refresh(nuevo_evento)
        return nuevo_evento
        
    except IntegrityError:
        # Captura de error de duplicidad (Unique Key Violation)
        db.rollback()
        raise ValueError("Conflicto de trazabilidad: El UPID ya fue registrado en este proceso.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error inesperado al registrar evento: {str(e)}")