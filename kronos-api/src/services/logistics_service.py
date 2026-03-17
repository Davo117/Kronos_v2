r"""
Servicio de Logística - KronosSystem.
"""
from sqlalchemy.orm import Session
from typing import List
from src.modules.logistics import models, schemas
from src.modules.production.models import OrdenCompra
from datetime import datetime, timezone

def crear_contenedor(db: Session, datos: schemas.EmpaqueCreate):
    """Registra una caja jalando el peso teórico de ingeniería."""
    orden = db.query(OrdenCompra).filter(OrdenCompra.id == datos.id_orden).first()
    if not orden:
        raise ValueError(f"Orden ID {datos.id_orden} no existe.")

    config = orden.version_ft.config_empaque
    if not config:
        raise ValueError("La FT no tiene configuración de empaque aprobada.")

    nuevo = models.EmpaqueContenedor(
        id_orden=datos.id_orden,
        peso_teorico=config.peso_teorico_kg,
        id_operario=datos.id_operario
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def registrar_peso_y_evaluar(db: Session, contenedor_id: int, peso_real: float):
    r"""
    Actualiza peso y evalúa con la fórmula:
    $$ \text{Aprobado} = | \text{Peso}_{\text{Báscula}} - \text{Peso}_{\text{Teórico}} | \le \left( \text{Peso}_{\text{Teórico}} \times \frac{\text{Tolerancia}}{100} \right) $$
    """
    contenedor = db.query(models.EmpaqueContenedor).filter(
        models.EmpaqueContenedor.id == contenedor_id
    ).with_for_update().first()

    if not contenedor:
        raise ValueError("Contenedor no localizado.")
    
    orden = db.query(OrdenCompra).filter(OrdenCompra.id == contenedor.id_orden).first()
    tolerancia = orden.version_ft.config_empaque.tolerancia_porcentaje
    
    contenedor.peso_bascula = peso_real
    margen = float(contenedor.peso_teorico) * (float(tolerancia) / 100)
    
    contenedor.aprobado = abs(float(contenedor.peso_teorico) - peso_real) <= margen
    db.commit()
    db.refresh(contenedor)
    return contenedor

def crear_embarque(db: Session, datos: schemas.EmbarqueCreate):
    """Registra transporte."""
    nuevo = models.Embarque(transporte=datos.transporte.upper())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def asignar_contenedores_a_embarque(db: Session, embarque_id: int, contenedor_ids: List[int]):
    """Asignación masiva de cajas aprobadas."""
    embarque = db.query(models.Embarque).filter(models.Embarque.id == embarque_id).first()
    if not embarque:
        raise ValueError("Embarque no encontrado.")

    contenedores = db.query(models.EmpaqueContenedor).filter(
        models.EmpaqueContenedor.id.in_(contenedor_ids)
    ).all()

    for cont in contenedores:
        if not cont.aprobado or cont.id_embarque:
            raise ValueError(f"Contenedor {cont.id} no elegible para envío.")
        cont.id_embarque = embarque_id

    db.commit()
    return {"status": "ok", "items": len(contenedores)}