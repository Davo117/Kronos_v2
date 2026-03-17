"""
KronosSystem API - Punto de Entrada Principal.
Documentado bajo directiva 2026-03-09.
"""
from fastapi import FastAPI
from src.config.db import engine, Base
# Importación obligatoria de modelos para generación de tablas
from src.modules.common import models as common_models
from src.modules.engineering import models as engineering_models
from src.modules.production import models as production_models
from src.modules.logistics import models as logistics_models

# Routers
from src.modules.common.routes import router as common_router
from src.modules.engineering.routes import router as engineering_router
from src.modules.production.routes import router as production_router
from src.modules.logistics.routes import router as logistics_router

# Inicialización de base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KronosSystem API", version="1.1.0")

app.include_router(common_router)
app.include_router(engineering_router)
app.include_router(production_router)
app.include_router(logistics_router)

@app.get("/")
def health_check():
    return {"status": "online", "system": "KronosSystem"}