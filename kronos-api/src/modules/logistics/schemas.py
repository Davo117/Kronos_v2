"""
Esquemas de validación Pydantic para el módulo de Logística.
Define la estructura para contenedores, embarques y asignaciones de carga.
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class EmpaqueBase(BaseModel):
    id_orden: int = Field(..., gt=0)
    id_operario: int = Field(..., gt=0)

class EmpaqueCreate(EmpaqueBase):
    """
    Atributos requeridos para crear un nuevo contenedor. 
    No se incluye peso_teorico porque el servicio lo jala de la Ficha Técnica.
    """
    pass

class EmpaqueUpdatePeso(BaseModel):
    """Atributos para la actualización tras el pesaje en báscula."""
    peso_bascula: Decimal = Field(..., gt=0)

    @field_validator('peso_bascula')
    @classmethod
    def validar_precision(cls, v: Decimal) -> Decimal:
        """Asegura una precisión estándar de 4 decimales."""
        return round(v, 4)

class EmpaqueResponse(EmpaqueBase):
    """Representación de salida completa de un contenedor."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    peso_teorico: Decimal
    peso_bascula: Optional[Decimal] = None
    aprobado: bool
    id_embarque: Optional[int] = None
    fecha_creacion: datetime