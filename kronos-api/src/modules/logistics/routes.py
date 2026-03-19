"""
Router de Logística - KronosSystem.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.modules.logistics import schemas
from src.services import logistics_service

router = APIRouter(prefix="/logistica", tags=["Logística"])

@router.post("/contenedores", response_model=schemas.EmpaqueResponse)
def crear_caja(request: schemas.EmpaqueCreate, db: Session = Depends(get_db)):
    # El ValueError interno de crear_contenedor será capturado por el handler global
    return logistics_service.crear_contenedor(db, request)

@router.patch("/contenedores/{id}/pesar", response_model=schemas.EmpaqueResponse)
def pesar_caja(id: int, request: schemas.EmpaqueUpdatePeso, db: Session = Depends(get_db)):
    # Se pasa el Decimal directamente desde el esquema validado
    return logistics_service.registrar_peso_y_evaluar(db, id, request.peso_bascula)