"""
Modelos del módulo de Producción.
Gestiona la persistencia de Órdenes de Compra y UPIDs.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint, Numeric, BigInteger
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from src.config.db import Base

class OrdenCompra(Base):
    """
    Representa una orden de fabricación.
    Relaciona la sucursal del cliente con la versión técnica aprobada.
    """
    __tablename__ = "orden_compra"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"), nullable=False)
    id_version_ft = Column(Integer, ForeignKey("ft_version.id"), nullable=False)
    cantidad_solicitada = Column(Integer, nullable=False)
    empaque_seleccionado = Column(String(10), nullable=False)

    # Relaciones para navegación ORM
    version_ft = relationship("FTVersion", back_populates="ordenes")
    unidades = relationship("UPID", back_populates="orden")

class UPID(Base):
    """
    Unidad de Producción Individual (Identificador Único).
    Almacena los valores teóricos calculados por ingeniería para validación.
    """
    __tablename__ = "upid"
    codigo_upid = Column(String(50), primary_key=True)
    id_orden = Column(Integer, ForeignKey("orden_compra.id"), nullable=False)
    longitud_teorica = Column(Numeric(10, 4), comment="Metros lineales calculados")
    peso_teorico = Column(Numeric(10, 4), comment="Masa calculada en Kg")
    piezas_estimadas = Column(Integer, comment="Cantidad de etiquetas por unidad")
    
    orden = relationship("OrdenCompra", back_populates="unidades")
    eventos = relationship("EventoProceso", back_populates="unidad")

class EventoProceso(Base):
    """
    Registro de trazabilidad en planta.
    Garantiza que una unidad no pase dos veces por el mismo proceso (UniqueConstraint).
    """
    __tablename__ = "evento_proceso"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_upid = Column(String(50), ForeignKey("upid.codigo_upid"), nullable=False)
    id_proceso = Column(TINYINT, ForeignKey("proceso_maestro.id"), nullable=False)
    id_empleado = Column(Integer, ForeignKey("empleado.id"), nullable=False)
    id_maquina = Column(Integer, ForeignKey("maquina.id"), nullable=False)
    fecha_hora = Column(DateTime, server_default=func.now())
    
    unidad = relationship("UPID", back_populates="eventos")

    # Validación de concurrencia a nivel de base de datos
    __table_args__ = (UniqueConstraint('id_upid', 'id_proceso', name='_upid_proceso_uc'),)