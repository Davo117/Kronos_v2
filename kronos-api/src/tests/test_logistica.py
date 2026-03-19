"""
Pruebas de integración para Logística.
Valida pesaje contra configuración de ingeniería y gestión de embarques.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from decimal import Decimal

client = TestClient(app)

def test_health_check():
    """Verifica que la API y la DB estén respondiendo correctamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"

def test_crear_contenedor_orden_inexistente():
    """Prueba que el manejador global capture el error 400 cuando la orden no existe."""
    payload = {
        "id_orden": 999999, # ID que no existe
        "id_operario": 1
    }
    response = client.post("/logistica/contenedores", json=payload)
    assert response.status_code == 400
    # Verificamos que nuestro handler global en main.py funcione
    assert response.json()["type"] == "ValidationError"