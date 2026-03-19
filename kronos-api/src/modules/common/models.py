"""
Modelos de infraestructura y maestros (Common).
Define las entidades compartidas por todos los módulos.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from src.config.db import Base

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, index=True) # Índice añadido
    sucursales = relationship("Sucursal", back_populates="cliente")

class Sucursal(Base):
    __tablename__ = "sucursal"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False, index=True)
    nombre_sucursal = Column(String(255), index=True) # Índice añadido
    direccion_completa = Column(Text, nullable=False)
    cliente = relationship("Cliente", back_populates="sucursales")

class Empleado(Base):
    __tablename__ = "empleado"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, index=True)
    numero_empleado = Column(String(50), unique=True, nullable=False, index=True)

class ProcesoMaestro(Base):
    __tablename__ = "proceso_maestro"
    id = Column(TINYINT, primary_key=True, autoincrement=True)
    nombre_proceso = Column(String(50), nullable=False)
    sigla = Column(String(2), unique=True, nullable=False)

class Maquina(Base):
    __tablename__ = "maquina"
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_maquina = Column(String(10), unique=True, nullable=False, index=True)
    descripcion = Column(String(100), nullable=False)
    id_proceso = Column(TINYINT, ForeignKey("proceso_maestro.id"), nullable=False)

class Sustrato(Base):
    __tablename__ = "sustrato"
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=False, index=True)
    codigo_interno = Column(String(50), unique=True, index=True)
    altura_material = Column(Numeric(10, 4), nullable=False, default=0.0000)
    gramaje = Column(Numeric(10, 4), nullable=False, default=0.0000)
    espesor = Column(Numeric(10, 2))

class Pantone(Base):
    __tablename__ = "pantone"
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_hex = Column(String(7), nullable=False)
    descripcion = Column(String(50), nullable=False, index=True)
    codigo_pantone = Column(String(20), unique=True, index=True)