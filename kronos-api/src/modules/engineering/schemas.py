"""
Esquemas de validación Pydantic para el módulo de Ingeniería.
Define las estructuras para herramental, fichas técnicas y flujos de aprobación.

"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime

class EngineeringBase(BaseModel):
    """Configuración base para habilitar el modo ORM."""
    model_config = ConfigDict(from_attributes=True)

# --- HERRAMENTAL ---

class CilindroCreate(BaseModel):
    """Atributos para registrar un juego de cilindros."""
    desarrollo_mm: Decimal = Field(..., gt=0)
    repeticion: int = Field(..., gt=0)
    tipo_engrane: str

class CilindroResponse(EngineeringBase):
    """Estructura de salida para juegos de cilindros."""
    id: int
    desarrollo_mm: Decimal
    repeticion: int
    tipo_engrane: Optional[str]

class CirelCreate(BaseModel):
    """Atributos para registrar placas cirel."""
    espesor: Decimal = Field(..., gt=0)
    lineaje: int = Field(..., gt=0)
    descripcion: str

class CirelResponse(EngineeringBase):
    """Estructura de salida para placas cirel."""
    id: int
    espesor: Decimal
    lineaje: int
    descripcion: str

# --- CONFIGURACIÓN DE EMPAQUE ---

class FTConfigEmpaqueCreate(BaseModel):
    """Define los parámetros de empaque para una versión específica."""
    tipo_empaque: str = Field(..., pattern='^(ROLLO|CAJA)$')
    etiquetas_por_caja: int = Field(..., gt=0)
    peso_teorico_kg: Decimal = Field(..., gt=0)
    tolerancia_porcentaje: Decimal = Field(Decimal("1.00"), ge=0)

class FTConfigEmpaqueResponse(EngineeringBase):
    """Representación de la configuración de empaque asignada."""
    id: int
    tipo_empaque: str
    etiquetas_por_caja: int
    peso_teorico_kg: Decimal
    tolerancia_porcentaje: Decimal

# --- FICHAS Y VERSIONES ---

class FichaTecnicaCreate(BaseModel):
    """Atributos para registrar un nuevo producto en ingeniería."""
    id_cliente: int = Field(..., gt=0)
    nombre_disenio: str = Field(..., min_length=1)

class FichaTecnicaResponse(EngineeringBase):
    """Respuesta con los datos base de la ficha técnica."""
    id: int
    id_cliente: int
    nombre_disenio: str

class FTVersionCreate(BaseModel):
    """Esquema para generar una nueva iteración técnica."""
    id_ficha: int = Field(..., gt=0)
    pistas: int = Field(..., gt=0)
    avance_paso: Decimal = Field(..., gt=0)
    id_sustrato: int = Field(..., gt=0)
    id_juego_cilindro: int = Field(..., gt=0)
    id_cirel: int = Field(..., gt=0)
    id_creador_logistica: int = Field(..., gt=0)

class FTVersionResponse(EngineeringBase):
    """Representación detallada de la versión con su estado actual."""
    id: int
    id_ficha: int
    numero_version: int
    pistas: int
    avance_paso: Decimal
    id_sustrato: int
    id_juego_cilindro: int
    id_cirel: int
    estado: str
    id_creador_logistica: Optional[int]
    id_aprobador_qc: Optional[int]
    fecha_aprobacion: Optional[datetime]
    config_empaque: Optional[FTConfigEmpaqueResponse]