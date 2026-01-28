from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    IN_PRODUCTION = "IN_PRODUCTION"
    COMPLETED = "COMPLETED"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"

class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False) # Razón Social
    rfc = Column(String(20), index=True, nullable=True)
    
    # Dirección (Aplanada y limpia)
    address = Column(String(200), nullable=True)
    colony = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(10), nullable=True)
    
    # Contacto
    contact_name = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    orders = relationship("Order", back_populates="client")

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    operation_number = Column(String(50), unique=True, index=True, nullable=False)
    
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    priority = Column(String(20), default="NORMAL")
    
    expected_delivery_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    client = relationship("Client", back_populates="orders")