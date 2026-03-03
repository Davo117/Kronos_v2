from sqlalchemy import Column, Integer, String, Decimal, ForeignKey, DateTime, Enum, UniqueConstraint
from datetime import datetime
from src.config.db import Base

class OrdenCompra(Base):
    __tablename__ = "orden_compra"
    id = Column(Integer, primary_key=True, index=True)
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))
    id_version_ft = Column(Integer, ForeignKey("ft_version.id"))
    cantidad_piezas_total = Column(Integer, nullable=False)
    empaque_seleccionado = Column(Enum('ROLLO', 'CAJA'), nullable=False)

class UnidadProduccion(Base):
    """
    Representa el objeto físico. 
    Contiene la FK id_empaque para permitir la agrupación en Logística.
    """
    __tablename__ = "unidad_produccion"
    codigo_barras = Column(String(64), primary_key=True)
    id_orden = Column(Integer, ForeignKey("orden_compra.id"))
    id_empaque = Column(Integer, ForeignKey("empaque_contenedor.id"), nullable=True)
    longitud_real = Column(Decimal(10, 2))
    peso_real = Column(Decimal(10, 3))
    piezas_estimadas = Column(Integer)

class EventoProceso(Base):
    """
    Validación de concurrencia mediante UniqueConstraint.
    """
    __tablename__ = "evento_proceso"
    id = Column(Integer, primary_key=True)
    id_unidad = Column(String(64), ForeignKey("unidad_produccion.codigo_barras"))
    id_proceso = Column(Integer, ForeignKey("proceso_maestro.id"))
    id_empleado = Column(Integer, ForeignKey("empleado.id"))
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('id_unidad', 'id_proceso', name='idx_unidad_proceso'),)