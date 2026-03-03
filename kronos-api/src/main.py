from src.config.db import engine, Base
# Importación obligatoria para el registro de metadatos
from src.modules.common.models import Sustrato, Pantone, ProcesoMaestro, Cliente, Sucursal, Empleado
from src.modules.engineering.models import FichaTecnica, FTVersion, FTColor, FTEmpaqueOpcion
from src.modules.production.models import OrdenCompra, UnidadProduccion, EventoProceso
from src.modules.logistics.models import EmpaqueContenedor, Embarque

def init_db():
    """
    Sincroniza los modelos de SQLAlchemy con la base de datos física.
    ADVERTENCIA: Esta implementación incluye validaciones de concurrencia 
    en la tabla 'evento_proceso' para evitar duplicidad de registros en planta.
    """
    try:
        print("Iniciando creación de tablas modularizadas...")
        Base.metadata.create_all(bind=engine)
        print("Base de datos sincronizada exitosamente.")
    except Exception as e:
        print(f"Error crítico en la creación de la base de datos: {e}")

if __name__ == "__main__":
    init_db()
