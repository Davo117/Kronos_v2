from fastapi import APIRouter

# Aqui importaremos los routers de cada modulo cuando los creemos.
# from app.modules.logistics import router as logistics_router
# from app.modules.production import router as production_router

api_router = APIRouter()

@api_router.get("/health", tags=["Status"])
def health_check():
    """
    Endpoint basico para verificar que el servidor esta corriendo.
    """
    return {"status": "ok", "system": "Kronos v2 Running"}

# A futuro, aqui registraremos las rutas:
# api_router.include_router(logistics_router.router, prefix="/logistics", tags=["Logistics"])