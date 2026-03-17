"""
Esquemas de validación (Pydantic) para el módulo Common.
Define las estructuras de datos para clientes, sucursales, empleados y materiales.
Actualizado a Pydantic V2 con ConfigDict y documentado según directiva 2026-03-09.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Generic, TypeVar
from decimal import Decimal

T = TypeVar("T")

class BaseSchema(BaseModel):
    """
    Clase base que habilita la compatibilidad con modelos de SQLAlchemy.
    Sustituye la clase Config interna por model_config.
    """
    model_config = ConfigDict(from_attributes=True)

# --- ESQUEMAS DE UTILIDAD ---

class ResponseWrapper(BaseSchema, Generic[T]):
    """Estructura genérica para respuestas de API."""
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None

class PaginatedResponse(BaseSchema, Generic[T]):
    """Estructura para resultados paginados."""
    total: int
    page: int
    size: int
    items: List[T]

# --- ESQUEMAS DE DATOS MAESTROS ---

class ProcesoResponse(BaseSchema):
    """Estructura de salida para procesos maestros."""
    id: int
    nombre_proceso: str
    sigla: str

class MaquinaCreate(BaseModel):
    """Estructura para registro de nueva maquinaria."""
    descripcion: str = Field(..., min_length=3)
    id_proceso: int

class MaquinaResponse(BaseSchema):
    """Estructura de salida para maquinaria."""
    id: int
    codigo_maquina: str
    descripcion: str
    id_proceso: int

class SustratoCreate(BaseModel):
    """Atributos técnicos para dar de alta un material."""
    descripcion: str
    codigo_interno: str
    altura_material: Decimal
    gramaje: Decimal
    espesor: Optional[Decimal] = None

class SustratoResponse(BaseSchema):
    """Información completa de un sustrato del catálogo."""
    id: int
    descripcion: str
    codigo_interno: str
    altura_material: Decimal
    gramaje: Decimal
    espesor: Optional[Decimal]

class ClienteCreate(BaseModel):
    """Datos para registro de cliente con sucursal matriz inicial."""
    nombre: str = Field(..., min_length=2)
    direccion_matriz: str

class ClienteResponse(BaseSchema):
    """Información básica del cliente."""
    id: int
    nombre: str

class SucursalCreate(BaseModel):
    """Datos para crear sucursales adicionales."""
    id_cliente: int
    nombre_sucursal: str
    direccion_completa: str

class EmpleadoCreate(BaseModel):
    """Datos de identificación de personal de planta."""
    nombre: str
    numero_empleado: str

class EmpleadoResponse(BaseSchema):
    """Información del empleado registrado."""
    id: int
    nombre: str
    numero_empleado: str

# --- ESQUEMAS DE APOYO (INGENIERÍA INICIAL) ---

class CilindroCreate(BaseModel):
    """Estructura base para juegos de cilindros."""
    desarrollo_mm: Decimal
    repeticion: int
    tipo_engrane: str

class CirelCreate(BaseModel):
    """Estructura base para placas cirel."""
    espesor: Decimal
    lineaje: int
    descripcion: str