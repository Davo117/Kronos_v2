from sqlalchemy import Column, DateTime, Integer, String, Boolean, Float, ForeignKey, JSON, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base import Base

# Tipos de Producto soportados (segun tus archivos: Termoencogible, Flexo, Holograma)
class ProductType(str, enum.Enum):
    SHRINK_SLEEVE = "SHRINK_SLEEVE" # Termoencogible
    FLEXO_LABEL = "FLEXO_LABEL"     # Etiqueta Autoadherible
    HOLOGRAPHIC = "HOLOGRAPHIC"     # Holograma

class Product(Base):
    """
    Catálogo Maestro de Productos (SKUs).
    Define QUÉ vendemos, pero no CÓMO se fabrica (eso va en la Version).
    """
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False) # El codigo interno (Ej: PT-500)
    name = Column(String(200), nullable=False) # Descripcion comercial
    
    product_type = Column(Enum(ProductType), nullable=False)
    
    # Auditoria
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    versions = relationship("ProductVersion", back_populates="product")


class ProductVersion(Base):
    """
    La 'Ficha Técnica' o 'Ingeniería' del producto.
    Si cambias el diseño o el material, creas una NUEVA versión (v1, v2),
    no sobrescribes la anterior. Esto garantiza trazabilidad histórica.
    """
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    
    version_number = Column(Integer, nullable=False, default=1)
    description = Column(String(255), nullable=True) # Ej: "Cambio de arte 2026"
    
    # --- ESPECIFICACIONES DINAMICAS (JSON) ---
    # Aqui guardamos: ancho, alto, sustrato, tipo de barniz, etc.
    # Evita tener 50 columnas con NULL.
    # Ejemplo: {"width": 100, "height": 50, "substrate_type": "PET-G"}
    specs = Column(JSON, nullable=False)
    
    # Archivos adjuntos (Rutas a PDFs de Arte/Planos)
    art_file_path = Column(String(255), nullable=True)
    
    is_approved = Column(Boolean, default=False) # Solo versiones aprobadas se pueden producir
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    product = relationship("Product", back_populates="versions")
    bom_items = relationship("BillOfMaterial", back_populates="version")
    tooling_configs = relationship("ToolingConfig", back_populates="version")


class Tooling(Base):
    """
    Inventario de Herramentales (Cilindros, Suajes, Placas).
    Reemplaza a 'juegoscilindros' y 'showCilindros.php'.
    """
    id = Column(Integer, primary_key=True, index=True)
    serial_code = Column(String(50), unique=True, nullable=False) # Identificador fisico
    
    # Datos Tecnicos para las formulas de rendimiento
    type = Column(String(50)) # Ej: "CILINDRO", "SUAJE", "ANILOX"
    teeth_count = Column(Integer, nullable=True) # Z (Dientes)
    repetition_around = Column(Integer, nullable=True) # Repeticiones al giro (repAlGiro)
    repetition_across = Column(Integer, nullable=True) # Repeticiones al paso (repAlPaso)
    
    # Medidas fisicas
    diameter = Column(Float, nullable=True) # Para calcular perimetro
    width = Column(Float, nullable=True)
    
    # Vida Util (Gestion de desgaste)
    guaranteed_turns = Column(Integer, default=1000000) # Vida garantizada
    current_turns = Column(Integer, default=0) # Acumulado real
    
    status = Column(String(20), default="AVAILABLE") # AVAILABLE, IN_MAINTENANCE, DISCARDED


class ToolingConfig(Base):
    """
    Tabla puente: Qué herramentales necesita ESTA versión de producto.
    """
    id = Column(Integer, primary_key=True, index=True)
    product_version_id = Column(Integer, ForeignKey("product_version.id"))
    tooling_id = Column(Integer, ForeignKey("tooling.id"))
    
    # Relaciones
    version = relationship("ProductVersion", back_populates="tooling_configs")
    tooling = relationship("Tooling")


class BillOfMaterial(Base):
    """
    La 'Receta' del producto (BOM).
    Define tintas, sustratos y cajas necesarias.
    Reemplaza la separacion absurda de 'consumos' vs 'pantonepcapa'.
    """
    id = Column(Integer, primary_key=True, index=True)
    product_version_id = Column(Integer, ForeignKey("product_version.id"))
    
    # Referencia al Inventario (Materia Prima).
    # Usamos ID directo para evitar ciclo de importacion con modulo Inventory
    material_id = Column(Integer, nullable=False) 
    
    quantity_per_unit = Column(Float, nullable=False) # Cuanto gasto por cada 1000 etiquetas?
    unit_measure = Column(String(20), nullable=False) # "KG", "MTS", "LT"
    
    # Tipo de insumo (Para agrupar en reportes)
    type = Column(String(20), nullable=False) # "INK", "SUBSTRATE", "VARNISH", "PACKAGING"

    # Relaciones
    version = relationship("ProductVersion", back_populates="bom_items")