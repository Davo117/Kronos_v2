"""
Test de Diagnóstico de Ingeniería - KronosSystem.
Usa IDs dinámicos para evitar colisiones de integridad (Error 400).
Documentado bajo directiva 2026-03-09.
"""
import pytest
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_diagnostico_ingenieria():
    # Generamos un sufijo único basado en el tiempo para evitar el error "ya existe"
    uid = str(int(time.time()))[-4:]
    
    # 1. Crear Empleado
    print(f"\n[1/5] Registrando empleado E_{uid}...")
    r_emp = client.post("/catalogos/empleados", json={
        "nombre": f"DAVE_{uid}", 
        "numero_employee": f"E_{uid}" # <-- Esto garantiza que no se repita
    })
    assert r_emp.status_code == 200, f"Error en Empleado: {r_emp.json()}"
    emp_id = r_emp.json()["id"]

    # 2. Crear Cliente
    print(f"[2/5] Registrando cliente CLI_{uid}...")
    r_cli = client.post("/catalogos/clientes", json={
        "nombre": f"CLIENTE_{uid}", 
        "direccion_matriz": "AV CENTRAL 1"
    })
    assert r_cli.status_code == 200, f"Error en Cliente: {r_cli.json()}"
    cli_id = r_cli.json()["id"]

    # 3. Catálogos Técnicos
    print("[3/5] Registrando catálogos técnicos...")
    r_sus = client.post("/catalogos/sustratos", json={
        "descripcion": "BOPP", "codigo_interno": f"B_{uid}", 
        "altura_material": 100, "gramaje": 40
    })
    assert r_sus.status_code == 200

    r_cil = client.post("/ingenieria/cilindros", json={
        "desarrollo_mm": 300, "repeticion": 1, "tipo_engrane": "CP"
    })
    cil_id = r_cil.json()["id"]

    r_cir = client.post("/ingenieria/cireles", json={
        "espesor": 1.14, "lineaje": 133, "descripcion": "TEST"
    })
    cir_id = r_cir.json()["id"]

    # 4. Crear Ficha Maestra
    print("[4/5] Creando Ficha Maestra...")
    r_ft = client.post("/ingenieria/fichas", json={
        "id_cliente": cli_id, 
        "nombre_disenio": f"DISEÑO_{uid}"
    })
    assert r_ft.status_code == 200
    ft_id = r_ft.json()["id"]

    # 5. Crear Versión
    print("[5/5] Creando Versión...")
    r_v = client.post("/ingenieria/versiones", json={
        "id_ficha": ft_id, 
        "pistas": 1, 
        "avance_paso": 100,
        "id_sustrato": r_sus.json()["id"], 
        "id_juego_cilindro": cil_id, 
        "id_cirel": cir_id, 
        "id_creador_logistica": emp_id
    })
    
    assert r_v.status_code == 200, f"Fallo en Versión: {r_v.json()}"
    print(f"✅ Ciclo completado para Versión ID: {r_v.json()['id']}")