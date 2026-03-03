from sqlalchemy import Column, Integer, String, Decimal, ForeignKey, Enum
from src.config.db import Base

class FichaTecnica(Base):
    __tablename__ = "ficha_tecnica"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, nullable=False)
    nombre_disenio = Column(String(255), nullable=False)

class FTVersion(Base):
    __tablename__ = "ft_version"
    id = Column(Integer, primary_key=True, index=True)
    id_ficha = Column(Integer, ForeignKey("ficha_tecnica.id"))
    numero_version = Column(Integer, nullable=False)
    pistas = Column(Integer, default=1)
    avance_paso = Column(Decimal(10, 4), nullable=False)
    id_sustrato = Column(Integer, ForeignKey("sustrato.id"))
    margen_tolerancia_peso = Column(Decimal(5, 2), default=0.05)

class FTColor(Base):
    __tablename__ = "ft_color"
    id_version = Column(Integer, ForeignKey("ft_version.id"), primary_key=True)
    id_pantone = Column(String(7), ForeignKey("pantone.codigo_hex"), primary_key=True)
    orden_tinta = Column(Integer, nullable=False)

class FTEmpaqueOpcion(Base):
    __tablename__ = "ft_empaque_opcion"
    id = Column(Integer, primary_key=True, index=True)
    id_version = Column(Integer, ForeignKey("ft_version.id"))
    tipo_empaque = Column(Enum('ROLLO', 'CAJA'), nullable=False)
    piezas_por_unidad = Column(Integer, nullable=False)