"""
KronosSystem API - Punto de Entrada Principal.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.config.db import engine, Base

# Importación de modelos para asegurar creación de tablas
from src.modules.common import models as common_models
from src.modules.engineering import models as engineering_models
from src.modules.production import models as production_models
from src.modules.logistics import models as logistics_models

# Routers
from src.modules.common.routes import router as common_router
from src.modules.engineering.routes import router as engineering_router
from src.modules.production.routes import router as production_router
from src.modules.logistics.routes import router as logistics_router

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KronosAPI")

# Sincronización de base de datos
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Base de datos sincronizada correctamente.")
except Exception as e:
    logger.error(f"Error al sincronizar la base de datos: {e}")

app = FastAPI(title="KronosSystem API", version="1.1.0")

# --- Manejadores Globales de Errores ---

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Captura errores de lógica de negocio (ej. IDs no encontrados)."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "ValidationError"}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador para errores internos inesperados."""
    logger.error(f"Error crítico: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor", "type": "ServerError"}
    )

app.include_router(common_router)
app.include_router(engineering_router)
app.include_router(production_router)
app.include_router(logistics_router)

@app.get("/")
def health_check():
    return {"status": "online", "system": "KronosSystem", "database": "connected"}