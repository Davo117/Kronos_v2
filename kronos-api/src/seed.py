"""
Script de carga de datos iniciales (Seed).
"""
from src.config.db import SessionLocal, engine, Base
from src.modules.common.models import Cliente, Sucursal
from src.modules.engineering.models import FichaTecnica, FTVersion, ConfigEmpaque
from src.modules.production.models import OrdenCompra
from decimal import Decimal

def run_seed():
    db = SessionLocal()
    try:
        # 1. Crear Cliente y Sucursal
        cliente = Cliente(nombre="Cliente de Prueba")
        db.add(cliente)
        db.flush()
        
        sucursal = Sucursal(id_cliente=cliente.id, nombre_sucursal="Planta 1", direccion_completa="Calle Falsa 123")
        db.add(sucursal)
        
        # 2. Crear Estructura de Ingeniería
        ft = FichaTecnica(nombre_producto="Producto Test", codigo_producto="TEST-001")
        db.add(ft)
        db.flush()
        
        # Configuración de empaque (Peso 10kg, 5% tolerancia)
        config = ConfigEmpaque(peso_teorico_kg=Decimal("10.00"), tolerancia_porcentaje=Decimal("5.00"))
        db.add(config)
        db.flush()
        
        version = FTVersion(id_ficha_tecnica=ft.id, version_numero=1, id_config_empaque=config.id, estado="aprobada")
        db.add(version)
        db.flush()
        
        # 3. Crear Orden de Compra
        orden = OrdenCompra(id_sucursal=sucursal.id, id_version_ft=version.id, numero_orden="OC-100", cantidad_solicitada=100)
        db.add(orden)
        
        db.commit()
        print("Seed completado: Orden ID 1 creada con éxito.")
    except Exception as e:
        db.rollback()
        print(f"Error en seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()