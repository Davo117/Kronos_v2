from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class ProductionStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    RELEASED = "RELEASED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"

# AQUI ESTA LA CORRECCION:
# Ya no son niveles jerárquicos, son TIPO DE PRESENTACION.
class UnitPresentation(str, enum.Enum):
    ROLL = "ROLL"       # El producto es una Bobina (Rollo continuo)
    BOX = "BOX"         # El producto es Corte (Caja con fajillas/paquetes dentro)
    PALLET = "PALLET"   # Agrupación logística (Tarima)

class ProductionOrder(Base):
    __tablename__ = "production_order"
    
    id = Column(Integer, primary_key=True, index=True)
    operation_number = Column(String(50), unique=True, index=True, nullable=False)
    order_item_id = Column(Integer, nullable=False, index=True)
    product_version_id = Column(Integer, nullable=False)
    
    # Meta de Produccion
    quantity_planned = Column(Integer, nullable=False) # Total etiquetas
    quantity_produced = Column(Integer, default=0)     # Total etiquetas reportadas
    
    machine_id = Column(String(50), nullable=True)
    status = Column(Enum(ProductionStatus), default=ProductionStatus.PLANNED)
    
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=True)

    units = relationship("ProductionUnit", back_populates="production_order")


class ProductionUnit(Base):
    """
    La Unidad de Producto Terminado (Lo que cuenta Don Chuy).
    
    - Si es Bobina: Se crea un registro tipo 'ROLL'. 
      (El rollo ES el producto).
      
    - Si es Corte: Se crea un registro tipo 'BOX'. 
      (La caja ES el producto, los paquetes de adentro son irrelevantes para la BD).
    """
    __tablename__ = "production_unit"

    id = Column(Integer, primary_key=True, index=True)
    
    # Codigo Unico (PT-5040-001)
    code = Column(String(100), unique=True, index=True, nullable=False)
    
    production_order_id = Column(Integer, ForeignKey("production_order.id"), nullable=False)
    
    # Agrupacion Logistica (Solo para Tarimas)
    # Un Rollo puede ir en una Tarima. Una Caja puede ir en una Tarima.
    pallet_id = Column(Integer, ForeignKey("production_unit.id"), nullable=True)
    
    presentation = Column(Enum(UnitPresentation), nullable=False)
    
    # Contenido Neto
    quantity_units = Column(Integer, default=0)  # Cuantas etiquetas van aqui?
    weight_kg = Column(Float, default=0.0)       # Cuanto pesa esto?
    length_mts = Column(Float, default=0.0)      # Cuantos metros (Solo si es Rollo)
    
    # Trazabilidad
    source_material_lot_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=True)
    
    is_defective = Column(Boolean, default=False)
    is_shipped = Column(Boolean, default=False)

    # Relaciones
    production_order = relationship("ProductionOrder", back_populates="units")
    
    # Para acceder a los hijos de una tarima (sean rollos o cajas)
    children = relationship("ProductionUnit", 
                          backref=relationship("ProductionUnit", remote_side=[id]),
                          uselist=True)