"""
Modelos del módulo de Ingeniería.
Sincronizado con el flujo de aprobación y estados de ficha técnica.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from src.config.db import Base

class JuegoCilindro(Base):
    __tablename__ = "juego_cilindro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    desarrollo_mm = Column(Numeric(10, 2), nullable=False)
    repeticion = Column(Integer, nullable=False)
    tipo_engrane = Column(String(50))

class Cirel(Base):
    __tablename__ = "cirel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    espesor = Column(Numeric(10, 3))
    lineaje = Column(Integer)
    descripcion = Column(String(100))

class FichaTecnica(Base):
    __tablename__ = "ficha_tecnica"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    nombre_disenio = Column(String(255), nullable=False)
    versiones = relationship("FTVersion", back_populates="ficha")

class FTVersion(Base):
    __tablename__ = "ft_version"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ficha = Column(Integer, ForeignKey("ficha_tecnica.id"), nullable=False)
    numero_version = Column(Integer, nullable=False)
    pistas = Column(Integer, nullable=False)
    avance_paso = Column(Numeric(10, 4), nullable=False)
    id_sustrato = Column(Integer, ForeignKey("sustrato.id"), nullable=False)
    id_juego_cilindro = Column(Integer, ForeignKey("juego_cilindro.id"), nullable=False)
    id_cirel = Column(Integer, ForeignKey("cirel.id"), nullable=False)
    
    # Nuevos campos para el ciclo de vida acordado
    estado = Column(Enum('BORRADOR', 'PEND_EMPAQUE', 'PEND_CALIDAD', 'APROBADA', 'RECHAZADA'), default='BORRADOR')
    id_creador_logistica = Column(Integer, ForeignKey("empleado.id"))
    id_aprobador_qc = Column(Integer, ForeignKey("empleado.id"))
    fecha_aprobacion = Column(DateTime)
    
    ficha = relationship("FichaTecnica", back_populates="versiones")
    config_empaque = relationship("FTConfigEmpaque", back_populates="version", uselist=False)
    ordenes = relationship("OrdenCompra", back_populates="version_ft")

class FTConfigEmpaque(Base):
    """Configuración de salida definitiva definida por el Encargado de Empaque."""
    __tablename__ = "ft_config_empaque"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_version = Column(Integer, ForeignKey("ft_version.id"), nullable=False)
    tipo_empaque = Column(Enum('ROLLO', 'CAJA'), nullable=False)
    etiquetas_por_caja = Column(Integer, nullable=False)
    peso_teorico_kg = Column(Numeric(10, 3), nullable=False)
    tolerancia_porcentaje = Column(Numeric(5, 2), default=1.00)
    
    version = relationship("FTVersion", back_populates="config_empaque")