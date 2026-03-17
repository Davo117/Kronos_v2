"""
Router de Ingeniería - KronosSystem.
Implementa el ciclo de vida de la Ficha Técnica (FT) y gestión de herramental.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.config.db import get_db
from src.modules.engineering import schemas, models
from src.services import engineering_service, catalog_service

router = APIRouter(prefix="/ingenieria", tags=["Ingeniería"])

# --- GESTIÓN DE HERRAMENTAL (CATÁLOGOS) ---

@router.post("/cilindros", response_model=schemas.CilindroResponse)
def crear_cilindro(request: schemas.CilindroCreate, db: Session = Depends(get_db)):
    """Registra un nuevo juego de cilindros en el catálogo."""
    return catalog_service.registrar_cilindro(db, **request.model_dump())

@router.get("/cilindros", response_model=List[schemas.CilindroResponse])
def listar_cilindros(db: Session = Depends(get_db)):
    """Obtiene la lista completa de cilindros registrados."""
    return db.query(models.JuegoCilindro).all()

@router.post("/cireles", response_model=schemas.CirelResponse)
def crear_cirel(request: schemas.CirelCreate, db: Session = Depends(get_db)):
    """Registra grabados cirel para procesos de impresión."""
    return catalog_service.registrar_cirel(db, **request.model_dump())

@router.get("/cireles", response_model=List[schemas.CirelResponse])
def listar_cireles(db: Session = Depends(get_db)):
    """Obtiene la lista completa de cireles registrados."""
    return db.query(models.Cirel).all()

# --- FLUJO DE FICHA TÉCNICA ---

@router.post("/fichas", response_model=schemas.FichaTecnicaResponse)
def crear_ficha_maestra(request: schemas.FichaTecnicaCreate, db: Session = Depends(get_db)):
    """Crea la cabecera de la ficha técnica para un cliente."""
    try:
        return engineering_service.crear_ficha_maestra(db, request.id_cliente, request.nombre_disenio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/versiones", response_model=schemas.FTVersionResponse)
def crear_version_tecnica(request: schemas.FTVersionCreate, db: Session = Depends(get_db)):
    """Genera una iteración técnica inicial en estado BORRADOR."""
    try:
        return engineering_service.registrar_nueva_version(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/versiones/{id}/empaque", response_model=schemas.FTVersionResponse)
def configurar_empaque(id: int, request: schemas.FTConfigEmpaqueCreate, db: Session = Depends(get_db)):
    """Define parámetros de salida física y avanza el flujo a PEND_CALIDAD."""
    try:
        return engineering_service.configurar_empaque_y_avanzar(db, id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/versiones/{id}/dictaminar", response_model=schemas.FTVersionResponse)
def dictaminar_ft(id: int, aprobado: bool, id_aprobador: int, db: Session = Depends(get_db)):
    """Aprobación o rechazo final de Calidad para liberar a Producción."""
    try:
        return engineering_service.dictaminar_version(db, id, id_aprobador, aprobado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/versiones/{id}", response_model=schemas.FTVersionResponse)
def obtener_detalle_version(id: int, db: Session = Depends(get_db)):
    """Consulta los parámetros técnicos de una versión por ID."""
    version = db.query(models.FTVersion).filter(models.FTVersion.id == id).first()
    if not version:
        raise HTTPException(status_code=404, detail="La versión técnica especificada no existe.")
    return version