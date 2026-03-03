from sqlalchemy import Column, Integer, String, Decimal, ForeignKey, DateTime, Boolean
from datetime import datetime
from src.config.db import Base

class EmpaqueContenedor(Base):
    """
    Consolidación de unidades y validación de peso.
    """
    __tablename__ = "empaque_contenedor"
    id = Column(Integer, primary_key=True, index=True)
    id_orden = Column(Integer, ForeignKey("orden_compra.id"), nullable=False)
    peso_teorico = Column(Decimal(10, 3), nullable=False)
    peso_bascula = Column(Decimal(10, 3), nullable=True)
    aprobado = Column(Boolean, default=False)
    id_operario = Column(Integer, ForeignKey("empleado.id"), nullable=False)
    id_embarque = Column(Integer, ForeignKey("embarque.id"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Embarque(Base):
    """
    Gestiona el despacho final de los paquetes hacia las sucursales.
    """
    __tablename__ = "embarque"
    id = Column(Integer, primary_key=True, index=True)
    transporte = Column(String(100), nullable=False)
    guia_rastreo = Column(String(100), nullable=True)
    fecha_salida = Column(DateTime, default=datetime.utcnow)