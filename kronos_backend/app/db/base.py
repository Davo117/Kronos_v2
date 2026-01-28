from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    """
    Clase base para todos los modelos SQLAlchemy.
    Convierte automaticamente nombres de clase CamelCase a tablas snake_case.
    """
    id: Any
    __name__: str

    # Genera el nombre de la tabla automaticamente
    # Ejemplo: class OrdenCompra -> tabla "orden_compra"
    @declared_attr
    def __tablename__(cls) -> str:
        import re
        name = cls.__name__
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()