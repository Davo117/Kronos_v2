"""
Modelos del módulo de Logística.
Gestiona la agrupación física de unidades y el despacho de mercancía.
Actualizado para corregir DeprecationWarning de datetime.utcnow().
Documentación conforme a directiva 2026-03-09.
"""
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Boolean
from datetime import datetime, timezone
from src.config.db import Base

class EmpaqueContenedor(Base):
    """
    Agrupación física con validación de cumplimiento de peso.
    Vincula órdenes de producción con operarios y embarques finales.
    Utiliza datetime.now(timezone.utc) para evitar advertencias de depreciación.
    """
    __tablename__ = "empaque_contenedor"
    id = Column(Integer, primary_key=True)
    id_orden = Column(Integer, ForeignKey("orden_compra.id"), nullable=False)
    peso_teorico = Column(Numeric(10, 3), nullable=False)
    peso_bascula = Column(Numeric(10, 3))
    aprobado = Column(Boolean, default=False)
    id_operario = Column(Integer, ForeignKey("empleado.id"), nullable=False)
    id_embarque = Column(Integer, ForeignKey("embarque.id"), nullable=True)
    # Se utiliza una función lambda para asegurar la generación del timestamp al momento de la inserción
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Embarque(Base):
    """
    Registro de salida de mercancía.
    Almacena información del transporte y fecha de despacho.
    """
    __tablename__ = "embarque"
    id = Column(Integer, primary_key=True)
    transporte = Column(String(100), nullable=False)
    fecha_salida = Column(DateTime, default=lambda: datetime.now(timezone.utc))