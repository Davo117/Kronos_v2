"""
Router de Producción - KronosSystem.
Mapea los endpoints de programación y trazabilidad al servicio unificado.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.modules.production import schemas
from src.services import production_service

router = APIRouter(prefix="/produccion", tags=["Producción"])

@router.post("/ordenes", response_model=schemas.UPIDResponse)
def programar_produccion(request: schemas.OrdenCompraCreate, db: Session = Depends(get_db)):
    """
    Crea una orden y genera masivamente sus UPIDs con cálculos industriales.
    """
    try:
        orden = production_service.generar_orden_y_upids(db, request)
        # Retorna el primer UPID generado para validación de flujo
        return orden.unidades[0]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/escanear")
def registrar_paso(request: schemas.ScanEventRequest, db: Session = Depends(get_db)):
    """
    Registra un evento de trazabilidad en planta.
    Valida la restricción de unicidad por proceso.
    """
    try:
        return production_service.registrar_evento_planta(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))