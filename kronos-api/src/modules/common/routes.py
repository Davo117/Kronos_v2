"""
Router de Catálogos Maestros - KronosSystem.
Define los puntos de entrada para la gestión de personal, clientes y materiales.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.modules.common import schemas
from src.services import catalog_service

router = APIRouter(prefix="/catalogos", tags=["Catálogos"])

@router.post("/empleados", response_model=schemas.EmpleadoResponse)
def crear_empleado(request: schemas.EmpleadoCreate, db: Session = Depends(get_db)):
    """Registra personal en el catálogo maestro."""
    try:
        return catalog_service.registrar_empleado(db, request.nombre, request.numero_empleado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/clientes", response_model=schemas.ClienteResponse)
def crear_cliente(request: schemas.ClienteCreate, db: Session = Depends(get_db)):
    """Alta de cliente y sucursal matriz."""
    try:
        return catalog_service.registrar_cliente_con_matriz(db, request.nombre, request.direccion_matriz)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sustratos", response_model=schemas.SustratoResponse)
def crear_sustrato(request: schemas.SustratoCreate, db: Session = Depends(get_db)):
    """Registro de materiales base con validación física."""
    try:
        return catalog_service.gestionar_sustrato(db, **request.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))