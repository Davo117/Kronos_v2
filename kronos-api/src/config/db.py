from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fuente de verdad para la conexión
DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/kronos_db"

engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    isolation_level="REPEATABLE READ" 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Generador de sesiones para inyección de dependencias."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()