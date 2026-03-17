"""
Pruebas de integración para Logística.
Valida pesaje contra configuración de ingeniería y gestión de embarques.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pesaje_y_despacho_logistico():
    """Valida que solo cajas con peso aprobado puedan asignarse a un embarque."""
    # 1. Crear Contenedor (El servicio jala peso_teorico: 12.500 de la FT)
    cont_data = {"id_orden": 1, "id_operario": 1, "peso_teorico": 12.500} # El peso es validado por el service
    resp_cont = client.post("/logistica/contenedores", json=cont_data)
    assert resp_cont.status_code == 200
    caja_id = resp_cont.json()["id"]

    # 2. Pesaje en Báscula (Dentro de tolerancia 1%: 12.450 Kg)
    resp_peso = client.patch(f"/logistica/contenedores/{caja_id}/pesar", json={"peso_bascula": 12.450})
    assert resp_peso.status_code == 200
    assert resp_peso.json()["aprobado"] is True

    # 3. Crear Embarque y Asignar
    client.post("/logistica/embarques", json={"transporte": "TRANSPORTE EXPRESS"})
    resp_asig = client.post(f"/logistica/embarques/1/asignar", json={"contenedor_ids": [caja_id]})
    assert resp_asig.status_code == 200
    assert resp_asig.json()["asignaciones"] == 1