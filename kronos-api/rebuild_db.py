"""
Script de Sincronización Estructural - KronosSystem.
Reconstruye las tablas basándose en los modelos de Python actuales.

"""
from src.config.db import engine, Base
# Importar todos los modelos para que Base los reconozca
from src.modules.common import models as common_models
from src.modules.engineering import models as engineering_models
from src.modules.production import models as production_models
from src.modules.logistics import models as logistics_models

def rebuild():
    print("--- Iniciando reconstrucción de Base de Datos ---")
    
    # 1. Limpieza total (por si no lo hiciste en phpMyAdmin)
    print("Eliminando tablas antiguas...")
    Base.metadata.drop_all(bind=engine)
    
    # 2. Creación con la nueva estructura (UPID, estados, etc.)
    print("Creando nuevas tablas y relaciones...")
    Base.metadata.create_all(bind=engine)
    
    print("--- ¡Base de Datos sincronizada con éxito! ---")

if __name__ == "__main__":
    rebuild()