from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

# --- ENUMS (Reglas de negocio) ---
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    IN_PRODUCTION = "IN_PRODUCTION"
    COMPLETED = "COMPLETED"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"

# --- CLIENT SCHEMAS ---

class ClientBase(BaseModel):
    """
    Datos base del cliente.
    Hecho basándonos en la necesidad operativa real, 
    descartando campos basura del sistema viejo.
    """
    name: str = Field(..., min_length=1, title="Razón Social / Nombre")
    rfc: Optional[str] = Field(None, min_length=12, max_length=13, title="RFC")
    
    # Dirección (Mantenemos la estructura desglosada para mejor logística)
    address: Optional[str] = Field(None, title="Calle y Número") 
    colony: Optional[str] = Field(None, title="Colonia")
    city: Optional[str] = Field(None, title="Ciudad")
    state: Optional[str] = Field(None, title="Estado")
    zip_code: Optional[str] = Field(None, max_length=10, title="Código Postal")
    
    # Contacto
    phone: Optional[str] = Field(None, title="Teléfono")
    contact_name: Optional[str] = Field(None, title="Nombre de Contacto")
    email: Optional[EmailStr] = Field(None, title="Correo Electrónico")
    
    is_active: bool = True

class ClientCreate(ClientBase):
    pass 

class ClientUpdate(ClientBase):
    name: Optional[str] = None 
    is_active: Optional[bool] = None

class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- ORDER SCHEMAS ---

class OrderBase(BaseModel):
    client_id: int
    expected_delivery_date: Optional[datetime] = None
    priority: str = "NORMAL"
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    expected_delivery_date: Optional[datetime] = None

class OrderResponse(OrderBase):
    id: int
    operation_number: str
    status: OrderStatus
    created_at: datetime
    
    class Config:
        from_attributes = True