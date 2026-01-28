import os
from typing import List, ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuracion global del sistema.
    Lee variables de entorno o usa valores por defecto para desarrollo.
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Kronos System v2"
    
    # SEGURIDAD
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CLAVE_TEMPORAL_SUPER_SECRETA_DEV_123")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 Dias


    # BASE DE DATOS (MySQL)
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")   
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "") 
    MYSQL_DB: str = os.getenv("MYSQL_DB", "kronos_db")
    SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}"

    # LISTA ESTATICA DE ESTADOS (MEXICO) - Requerimiento Logistica
    MEXICO_STATES: ClassVar[List[str]] = [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", 
        "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", "Colima", 
        "Durango", "Estado de México", "Guanajuato", "Guerrero", "Hidalgo", 
        "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", 
        "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", 
        "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
    ]

    class Config:
        case_sensitive = True

settings = Settings()