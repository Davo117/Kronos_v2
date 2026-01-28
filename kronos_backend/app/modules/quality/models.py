from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base import Base

# Definición de Enums
class InspectionResult(str, enum.Enum):
    PASS = "PASS"               # Aprobado
    FAIL = "FAIL"               # Rechazado (Scrap)
    CONDITIONAL = "CONDITIONAL" # Aprobado con reserva (Ej: Cliente acepta con descuento)

class DefectSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"       # Detener máquina inmediatamente
    MAJOR = "MAJOR"             # Producto no funcional
    MINOR = "MINOR"             # Defecto estético leve

class DefectType(Base):
    """
    Catálogo de Defectos.
    Ejemplos: "Fuera de Registro", "Manchas de Tinta", "Mal Corte".
    """
    __tablename__ = "defect_type"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False) # Ej: DEF-01
    name = Column(String(100), nullable=False) 
    severity = Column(Enum(DefectSeverity), default=DefectSeverity.MAJOR)
    
    is_active = Column(Boolean, default=True)


class QualityInspection(Base):
    """
    Auditoría de Calidad.
    Se conecta dinámicamente con Inventarios o Producción.
    """
    __tablename__ = "quality_inspection"

    id = Column(Integer, primary_key=True, index=True)
    
    # OPCIÓN A: Inspección de Materia Prima (Inventory)
    material_lot_id = Column(Integer, nullable=True) 
    
    # OPCIÓN B: Inspección de Producto Terminado (Production)
    # Puede ser un Rollo ('ROLL') o una Caja ('BOX')
    production_unit_id = Column(Integer, nullable=True)
    
    inspector_id = Column(Integer, nullable=False) # ID del usuario
    result = Column(Enum(InspectionResult), nullable=False)
    
    notes = Column(Text, nullable=True)
    evidence_url = Column(String(255), nullable=True) # URL de foto en S3/Local
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    defects = relationship("InspectionDefect", back_populates="inspection")


class InspectionDefect(Base):
    """
    Detalle de los defectos encontrados en una inspección.
    """
    __tablename__ = "inspection_defect"

    id = Column(Integer, primary_key=True, index=True)
    
    inspection_id = Column(Integer, ForeignKey("quality_inspection.id"), nullable=False)
    defect_type_id = Column(Integer, ForeignKey("defect_type.id"), nullable=False)
    
    quantity_affected = Column(Float, default=0) # Metros o Piezas dañadas
    
    # Relaciones
    inspection = relationship("QualityInspection", back_populates="defects")
    defect = relationship("DefectType")


class UnpackLog(Base):
    """
    Bitácora de 'Desempaquetado' / 'Rotura de Caja'.
    Aunque ya no rastreamos paquetes individuales en la BD, 
    seguimos necesitando registrar cuando una Caja Cerrada (UnitType='BOX')
    es abierta/destruida para re-trabajar su contenido.
    """
    __tablename__ = "unpack_log"

    id = Column(Integer, primary_key=True, index=True)
    
    # Código de la unidad contenedora (Caja o Tarima)
    container_code = Column(String(100), nullable=False) 
    
    user_id = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True) # Ej: "Etiqueta incorrecta", "Revisión interna"
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())