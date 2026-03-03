from sqlalchemy import Column, Integer, String, Decimal, TEXT
from src.config.db import Base

class Sustrato(Base):
    __tablename__ = "sustrato"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100), nullable=False)
    codigo_interno = Column(String(50), unique=True)
    altura_material = Column(Decimal(10, 4), nullable=False)

class Pantone(Base):
    __tablename__ = "pantone"
    codigo_hex = Column(String(7), primary_key=True)
    descripcion = Column(String(50), nullable=False)
    codigo_pantone = Column(String(20), unique=True)

class ProcesoMaestro(Base):
    __tablename__ = "proceso_maestro"
    id = Column(Integer, primary_key=True)
    nombre_proceso = Column(String(50), nullable=False)

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)

class Sucursal(Base):
    __tablename__ = "sucursal"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, nullable=False) # Relación lógica
    nombre_sucursal = Column(String(255))
    direccion_completa = Column(TEXT, nullable=False)

class Empleado(Base):
    __tablename__ = "empleado"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    numero_empleado = Column(String(50), unique=True, nullable=False)