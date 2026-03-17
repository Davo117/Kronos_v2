"""
Router de Logística - KronosSystem.
Gestiona el pesaje de cajas y despacho.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.modules.logistics import schemas
from src.services import logistics_service

router = APIRouter(prefix="/logistica", tags=["Logística"])

@router.post("/contenedores", response_model=schemas.EmpaqueResponse)
def crear_caja(request: schemas.EmpaqueCreate, db: Session = Depends(get_db)):
    try:
        return logistics_service.crear_contenedor(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/contenedores/{id}/pesar", response_model=schemas.EmpaqueResponse)
def pesar_caja(id: int, request: schemas.EmpaqueUpdatePeso, db: Session = Depends(get_db)):
    try:
        return logistics_service.registrar_peso_y_evaluar(db, id, float(request.peso_bascula))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))