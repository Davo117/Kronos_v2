"""
Test de Diagnóstico de Ingeniería.
Detiene la ejecución en el primer fallo y muestra el error del servidor.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_diagnostico_ingenieria():
    # 1. Crear Empleado (Necesario para id_creador_logistica)
    print("\n[1/5] Registrando empleado...")
    r_emp = client.post("/catalogos/empleados", json={"nombre": "DAVE", "numero_empleado": "E001"})
    assert r_emp.status_code == 200, f"Error en Empleado: {r_emp.json()}"

    # 2. Crear Cliente
    print("[2/5] Registrando cliente...")
    r_cli = client.post("/catalogos/clientes", json={"nombre": "CLIENTE TEST", "direccion_matriz": "AV CENTRAL 1"})
    assert r_cli.status_code == 200, f"Error en Cliente: {r_cli.json()}"

    # 3. Crear Sustrato y Herramental
    print("[3/5] Registrando catálogos técnicos...")
    client.post("/catalogos/sustratos", json={"descripcion": "BOPP", "codigo_interno": "B01", "altura_material": 100, "gramaje": 40})
    client.post("/ingenieria/cilindros", json={"desarrollo_mm": 300, "repeticion": 1, "tipo_engrane": "CP"})
    client.post("/ingenieria/cireles", json={"espesor": 1.14, "lineaje": 133, "descripcion": "TEST"})

    # 4. Crear Ficha Maestra
    print("[4/5] Creando Ficha Maestra...")
    r_ft = client.post("/ingenieria/fichas", json={"id_cliente": 1, "nombre_disenio": "DISEÑO ALFA"})
    if r_ft.status_code != 200:
        print(f"❌ FALLO CRÍTICO EN FICHA: {r_ft.json()}")
    assert r_ft.status_code == 200

    # 5. Crear Versión
    print("[5/5] Creando Versión...")
    r_v = client.post("/ingenieria/versiones", json={
        "id_ficha": 1, "pistas": 1, "avance_paso": 100,
        "id_sustrato": 1, "id_juego_cilindro": 1, "id_cirel": 1, "id_creador_logistica": 1
    })
    if r_v.status_code != 200:
        print(f"❌ FALLO CRÍTICO EN VERSIÓN: {r_v.json()}")
    assert r_v.status_code == 200