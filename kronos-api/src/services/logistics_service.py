r"""
Servicio de Logística - KronosSystem.
"""
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from src.modules.logistics import models, schemas
from src.modules.production.models import OrdenCompra

def crear_contenedor(db: Session, datos: schemas.EmpaqueCreate):
    """
    Registra una caja jalando el peso teórico de la Ficha Técnica vinculada.
    """
    orden = db.query(OrdenCompra).filter(OrdenCompra.id == datos.id_orden).first()
    if not orden:
        raise ValueError(f"Orden ID {datos.id_orden} no existe.")

    # El peso teórico viene de la configuración de empaque de la FT
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

def registrar_peso_y_evaluar(db: Session, contenedor_id: int, peso_real: Decimal):
    """
    Evalúa el pesaje con precisión Decimal siguiendo la directiva 2026-03-09.
    """
    contenedor = db.query(models.EmpaqueContenedor).filter(
        models.EmpaqueContenedor.id == contenedor_id
    ).with_for_update().first()

    if not contenedor:
        raise ValueError("Contenedor no localizado.")
    
    orden = db.query(OrdenCompra).filter(OrdenCompra.id == contenedor.id_orden).first()
    
    # Conversiones explícitas a Decimal para seguridad en el cálculo
    peso_teorico = Decimal(str(contenedor.peso_teorico))
    tolerancia = Decimal(str(orden.version_ft.config_empaque.tolerancia_porcentaje))
    
    contenedor.peso_bascula = peso_real
    
    # Margen = Peso_Teórico * (Tolerancia / 100)
    margen = peso_teorico * (tolerancia / Decimal("100"))
    
    # Aprobado si la diferencia absoluta es menor o igual al margen
    contenedor.aprobado = abs(peso_teorico - peso_real) <= margen
    
    db.commit()
    db.refresh(contenedor)
    return contenedor