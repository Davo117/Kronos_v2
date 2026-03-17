"""
Esquemas de validación Pydantic para el módulo de Logística.
Define la estructura para contenedores, embarques y asignaciones de carga.
Documentado bajo directiva 2026-03-09.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
protected_namespaces = ()
from decimal import Decimal
from datetime import datetime

class EmpaqueBase(BaseModel):
    """Base para la gestión de contenedores físicos."""
    id_orden: int
    peso_teorico: Decimal = Field(..., gt=0)
    id_operario: int

class EmpaqueCreate(EmpaqueBase):
    """Atributos requeridos para crear un nuevo contenedor."""
    pass

class EmpaqueUpdatePeso(BaseModel):
    """Atributos para la actualización tras el pesaje en báscula."""
    peso_bascula: Decimal = Field(..., gt=0)

class EmpaqueResponse(EmpaqueBase):
    """Representación de salida de un contenedor con su estado de aprobación."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    peso_bascula: Optional[Decimal] = None
    aprobado: bool
    id_embarque: Optional[int] = None
    fecha_creacion: datetime

class EmbarqueCreate(BaseModel):
    """Datos necesarios para registrar una unidad de transporte."""
    transporte: str = Field(..., min_length=3, max_length=100)

class EmbarqueResponse(EmbarqueCreate):
    """Detalle del embarque generado."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    fecha_salida: datetime

class AsignacionEmbarque(BaseModel):
    """
    Esquema para la vinculación masiva de contenedores a un embarque.
    Corrigiendo el AttributeError detectado en la recolección de tests.
    """
    contenedor_ids: List[int] = Field(..., min_length=1)