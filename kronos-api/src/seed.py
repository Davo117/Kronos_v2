"""
Script de población de datos maestros (Seeding).
Sincronizado con nombres de tabla oficiales y resolución de dependencias circulares.
"""
from sqlalchemy.orm import Session
from src.config.db import SessionLocal
from decimal import Decimal

# IMPORTANTE: Importar todos los modelos primero para registrarlos en Base.registry
from src.modules.common import models as c_models
from src.modules.production import models as p_models
from src.modules.engineering import models as e_models
from src.modules.logistics import models as l_models

def run_seed():
    """Ejecuta la carga de catálogos con validación de existencia previa."""
    db = SessionLocal()
    try:
        print("--> Iniciando carga de catálogos maestros con resolución de nombres...")

        # 1. Catálogos Base
        proceso = db.query(c_models.ProcesoMaestro).filter_by(sigla="IM").first()
        if not proceso:
            proceso = c_models.ProcesoMaestro(nombre_proceso="IMPRESION", sigla="IM")
            db.add(proceso)
            db.flush()

        maquina = db.query(c_models.Maquina).filter_by(codigo_maquina="IM-01").first()
        if not maquina:
            maquina = c_models.Maquina(codigo_maquina="IM-01", descripcion="PRENSA 1", id_proceso=proceso.id)
            db.add(maquina)

        cliente = db.query(c_models.Cliente).filter_by(nombre="PEPSI CO.").first()
        if not cliente:
            cliente = c_models.Cliente(nombre="PEPSI CO.")
            db.add(cliente)
            db.flush()

        sucursal = db.query(c_models.Sucursal).filter_by(id_cliente=cliente.id, nombre_sucursal="PLANTA NORTE").first()
        if not sucursal:
            sucursal = c_models.Sucursal(id_cliente=cliente.id, nombre_sucursal="PLANTA NORTE", direccion_completa="KM 15")
            db.add(sucursal)

        sustrato = db.query(c_models.Sustrato).filter_by(codigo_interno="BOPP-01").first()
        if not sustrato:
            sustrato = c_models.Sustrato(descripcion="BOPP", codigo_interno="BOPP-01", altura_material=Decimal("250.00"), gramaje=Decimal("60.00"))
            db.add(sustrato)

        empleado = db.query(c_models.Empleado).filter_by(numero_empleado="OP-001").first()
        if not empleado:
            empleado = c_models.Empleado(nombre="JUAN PEREZ", numero_empleado="OP-001")
            db.add(empleado)

        # 2. Ingeniería
        cilindro = db.query(e_models.JuegoCilindro).filter_by(desarrollo_mm=Decimal("320.00")).first()
        if not cilindro:
            cilindro = e_models.JuegoCilindro(desarrollo_mm=Decimal("320.00"), repeticion=4, tipo_engrane="CP")
            db.add(cilindro)
        
        cirel = db.query(e_models.Cirel).filter_by(lineaje=133).first()
        if not cirel:
            cirel = e_models.Cirel(espesor=Decimal("1.143"), lineaje=133, descripcion="HD")
            db.add(cirel)
        db.flush()

        ficha = db.query(e_models.FichaTecnica).filter_by(nombre_disenio="PEPSI 500ML").first()
        if not ficha:
            ficha = e_models.FichaTecnica(id_cliente=cliente.id, nombre_disenio="PEPSI 500ML")
            db.add(ficha)
            db.flush()

        version = db.query(e_models.FTVersion).filter_by(id_ficha=ficha.id, numero_version=1).first()
        if not version:
            version = e_models.FTVersion(
                id_ficha=ficha.id, numero_version=1, pistas=3, avance_paso=Decimal("150.50"),
                id_sustrato=sustrato.id, id_juego_cilindro=cilindro.id, id_cirel=cirel.id
            )
            db.add(version)
            db.flush()

        empaque = db.query(e_models.FTEmpaqueOpcion).filter_by(id_version=version.id, tipo_empaque="ROLLO").first()
        if not empaque:
            empaque = e_models.FTEmpaqueOpcion(id_version=version.id, tipo_empaque="ROLLO", piezas_por_unidad=5000)
            db.add(empaque)

        db.commit()
        print("--> Sincronización exitosa.")
    except Exception as e:
        db.rollback()
        print(f"!!! Error en seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()