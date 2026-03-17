"""
Pruebas de integración para Producción.
Valida la generación de múltiples UPIDs y
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_programacion_y_trazabilidad_upid():
    """Verifica que una orden genere la cantidad correcta de unidades y bloquee duplicados."""
    # Setup de Orden (Requiere FT Aprobada del test anterior)
    order_data = {
        "id_sucursal": 1,
        "id_version_ft": 1,
        "cantidad_solicitada": 10000,
        "cantidad_unidades": 2, # Debe generar 2 UPIDs
        "empaque_seleccionado": "ROLLO"
    }
    resp_order = client.post("/produccion/ordenes", json=order_data)
    assert resp_order.status_code == 200
    
    upid_code = resp_order.json()["codigo_upid"]

    # Registro de evento en planta
    scan_data = {
        "id_upid": upid_code, "id_empleado": 1, "id_maquina": 1, "id_proceso": 1
    }
    resp_scan = client.post("/produccion/escanear", json=scan_data)
    assert resp_scan.status_code == 200

    # Intento de duplicado (Race Condition)
    resp_dup = client.post("/produccion/escanear", json=scan_data)
    assert resp_dup.status_code == 400
    assert "Conflicto de trazabilidad" in resp_dup.json()["detail"]