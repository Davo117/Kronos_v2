"""
Modelos del módulo de Logística - KronosSystem.
Gestiona la agrupación física de unidades y el despacho de mercancía.
"""
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.config.db import Base

class EmpaqueContenedor(Base):
    """
    Agrupación física con validación de cumplimiento de peso.
    Vincula órdenes de producción con operarios y embarques finales.
    """
    __tablename__ = "empaque_contenedor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_orden = Column(Integer, ForeignKey("orden_compra.id"), nullable=False)
    peso_teorico = Column(Numeric(10, 3), nullable=False)
    peso_bascula = Column(Numeric(10, 3))
    aprobado = Column(Boolean, default=False)
    id_operario = Column(Integer, ForeignKey("empleado.id"), nullable=False)
    id_embarque = Column(Integer, ForeignKey("embarque.id"), nullable=True)
    
    # Campo de auditoría necesario para reportes de logística
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Navegación ORM para facilitar cálculos en el servicio
    orden = relationship("src.modules.production.models.OrdenCompra")
    operario = relationship("src.modules.common.models.Empleado")
    embarque = relationship("Embarque", back_populates="contenedores")

class Embarque(Base):
    """
    Registro de salida de mercancía.
    Almacena información del transporte y fecha de despacho.
    """
    __tablename__ = "embarque"
    id = Column(Integer, primary_key=True, autoincrement=True)
    transporte = Column(String(100), nullable=False)
    fecha_salida = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación para ver todos los contenedores asignados a este transporte
    contenedores = relationship("EmpaqueContenedor", back_populates="embarque")