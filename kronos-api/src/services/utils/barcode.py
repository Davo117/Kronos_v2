"""
Generador de Identificadores Únicos de Producción (UPID).
"""
from sqlalchemy.orm import Session
from src.modules.production.models import UPID
from datetime import datetime

def generar_upid_inmutable(db: Session) -> str:
    """
    Genera código UPYYXXXXXX con bloqueo de fila.
    """
    anio_prefix = f"UP{datetime.now().strftime('%y')}"
    
    ultimo = db.query(UPID)\
               .filter(UPID.codigo_upid.like(f"{anio_prefix}%"))\
               .with_for_update()\
               .order_by(UPID.codigo_upid.desc())\
               .first()

    nuevo_folio = 1
    if ultimo:
        try:
            nuevo_folio = int(ultimo.codigo_upid[4:]) + 1
        except (ValueError, IndexError):
            nuevo_folio = 1

    return f"{anio_prefix}{str(nuevo_folio).zfill(6)}"