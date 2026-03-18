"""
Test de Diagnóstico de Ingeniería - KronosSystem.
Utiliza marcas de tiempo para garantizar la unicidad de los datos.
"""
import pytest
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_diagnostico_ingenieria():
    # Generar sufijo único para evitar errores de integridad (UNIQUE)
    uid = str(int(time.time()))[-4:]
    
    # 1. Registro de Empleado Único
    print(f"\n[1/5] Registrando empleado E_{uid}...")
    r_emp = client.post("/catalogos/empleados", json={
        "nombre": f"DAVE_{uid}", 
        "numero_empleado": f"E_{uid}"
    })
    assert r_emp.status_code == 200, f"Error en Empleado: {r_emp.json()}"
    emp_id = r_emp.json()["id"]

    # 2. Registro de Cliente Único
    print(f"[2/5] Registrando cliente CLI_{uid}...")
    r_cli = client.post("/catalogos/clientes", json={
        "nombre": f"CLIENTE_{uid}", 
        "direccion_matriz": "AV CENTRAL 1"
    })
    assert r_cli.status_code == 200
    cli_id = r_cli.json()["id"]

    # 3. Registro de Catálogos Técnicos
    client.post("/catalogos/sustratos", json={
        "descripcion": "BOPP", "codigo_interno": f"B_{uid}", 
        "altura_material": 100, "gramaje": 40
    })
    r_cil = client.post("/ingenieria/cilindros", json={
        "desarrollo_mm": 304.8, "repeticion": 1, "tipo_engrane": "CP"
    })
    r_cir = client.post("/ingenieria/cireles", json={
        "espesor": 1.14, "lineaje": 133, "descripcion": "TEST"
    })

    # 4. Creación de Ficha Maestra
    r_ft = client.post("/ingenieria/fichas", json={
        "id_cliente": cli_id, 
        "nombre_disenio": f"DISEÑO_{uid}"
    })
    assert r_ft.status_code == 200
    ft_id = r_ft.json()["id"]

    # 5. Creación de Versión
    r_v = client.post("/ingenieria/versiones", json={
        "id_ficha": ft_id, "pistas": 1, "avance_paso": 152.4,
        "id_sustrato": 1, "id_juego_cilindro": r_cil.json()["id"], 
        "id_cirel": r_cir.json()["id"], "id_creador_logistica": emp_id
    })
    assert r_v.status_code == 200
    print(f"Ciclo de ingeniería completado con éxito.")