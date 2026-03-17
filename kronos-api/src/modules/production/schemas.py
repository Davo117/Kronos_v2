"""
Esquemas Pydantic para el módulo de Producción.
Define las reglas de validación para entrada y salida de datos.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal

class OrdenCompraCreate(BaseModel):
    """Atributos necesarios para programar una nueva orden."""
    id_sucursal: int = Field(..., gt=0)
    id_version_ft: int = Field(..., gt=0)
    cantidad_solicitada: int = Field(..., gt=0)
    cantidad_unidades: int = Field(..., gt=0, description="Número de bultos/rollos a generar")
    empaque_seleccionado: str = Field(..., pattern='^(ROLLO|CAJA)$')

class ScanEventRequest(BaseModel):
    """Datos requeridos por la terminal de escaneo en planta."""
    id_upid: str = Field(..., min_length=1)
    id_proceso: int = Field(..., gt=0)
    id_empleado: int = Field(..., gt=0)
    id_maquina: int = Field(..., gt=0)

class UPIDResponse(BaseModel):
    """Estructura de respuesta para la consulta de unidades."""
    model_config = ConfigDict(from_attributes=True)
    
    codigo_upid: str
    id_orden: int
    piezas_estimadas: Optional[int] = None
    longitud_teorica: Optional[Decimal] = None
    peso_teorico: Optional[Decimal] = None