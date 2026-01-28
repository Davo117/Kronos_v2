from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.api.api_v1 import api_router
from app.db.session import engine
from app.db.base import Base

# --- IMPORTANTE: Importar TODOS los modelos para que SQLAlchemy los detecte ---

from app.modules.logistics import models as logistics_models
from app.modules.engineering import models as engineering_models
from app.modules.production import models as production_models
from app.modules.inventory import models as inventory_models
from app.modules.quality import models as quality_models

def create_tables():
    """
    Verifica los modelos definidos y crea las tablas en MySQL si no existen.
    NOTA: En produccion usaremos Alembic migraciones, pero para desarrollo 
    esto es mas rapido para empezar.
    """
    print("--- Creando Tablas en Base de Datos ---")
    Base.metadata.create_all(bind=engine)
    print("--- Tablas Creadas Exitosamente ---")

def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Configuracion CORS (Permitir trafico del Frontend)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # En produccion cambiar por la URL real del frontend
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar Rutas
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = get_application()

# Evento de inicio: Crear tablas
@app.on_event("startup")
async def startup_event():
    create_tables()

# Bloque para ejecutar como script directo (python main.py)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)