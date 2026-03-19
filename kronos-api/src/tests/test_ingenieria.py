"""
Test de Diagnóstico de Ingeniería - KronosSystem.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_ficha_tecnica_completa():
    """Crea la base para que Logística tenga un peso teórico que consultar."""
    # 1. Crear Ficha Técnica
    ft_payload = {"nombre_producto": "Caja Galletas XL", "codigo_producto": "GAL-001"}
    response_ft = client.post("/ingenieria/fichas", json=ft_payload)
    assert response_ft.status_code == 200
    ft_id = response_ft.json()["id"]

    # 2. Crear Configuración de Empaque (Peso 10kg, Tolerancia 5%)
    config_payload = {"peso_teorico_kg": 10.0, "tolerancia_porcentaje": 5.0}
    response_config = client.post("/ingenieria/config-empaque", json=config_payload)
    assert response_config.status_code == 200
    config_id = response_config.json()["id"]

    # 3. Crear Versión y aprobarla
    version_payload = {
        "id_ficha_tecnica": ft_id,
        "version_numero": 1,
        "id_config_empaque": config_id,
        "estado": "aprobada"
    }
    response_ver = client.post("/ingenieria/versiones", json=version_payload)
    assert response_ver.status_code == 200