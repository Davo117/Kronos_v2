"""
Pruebas de integración para Producción - KronosSystem.
Valida la generación de UPIDs y la trazabilidad con datos dinámicos.
Documentado bajo directiva 2026-03-09.
"""
import pytest
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_programacion_y_trazabilidad_upid():
    uid = str(int(time.time()))[-4:]
    
    # 1. SETUP: Crear prerequisitos para que existan IDs válidos
    # Empleado
    r_emp = client.post("/catalogos/empleados", json={"nombre": f"OPERARIO_{uid}", "numero_empleado": f"E_{uid}"})
    emp_id = r_emp.json()["id"]
    
    # Cliente y Sucursal
    r_cli = client.post("/catalogos/clientes", json={"nombre": f"CLIENTE_{uid}", "direccion_matriz": "DIR TEST"})
    cli_id = r_cli.json()["id"]
    
    # Sustrato, Cilindro y Cirel
    r_sus = client.post("/catalogos/sustratos", json={"descripcion": "BOPP", "codigo_interno": f"S_{uid}", "altura_material": 100, "gramaje": 40})
    sus_id = r_sus.json()["id"]
    r_cil = client.post("/ingenieria/cilindros", json={"desarrollo_mm": 300, "repeticion": 1, "tipo_engrane": "CP"})
    cil_id = r_cil.json()["id"]
    r_cir = client.post("/ingenieria/cireles", json={"espesor": 1.14, "lineaje": 133, "descripcion": "TEST"})
    cir_id = r_cir.json()["id"]

    # 2. INGENIERÍA: Crear Ficha y Versión (Debe ser la versión que usará la orden)
    r_ft = client.post("/ingenieria/fichas", json={"id_cliente": cli_id, "nombre_disenio": f"DISEÑO_{uid}"})
    ft_id = r_ft.json()["id"]
    
    r_v = client.post("/ingenieria/versiones", json={
        "id_ficha": ft_id, "pistas": 1, "avance_paso": 100,
        "id_sustrato": sus_id, "id_juego_cilindro": cil_id, 
        "id_cirel": cir_id, "id_creador_logistica": emp_id
    })
    version_id = r_v.json()["id"]

    # 3. PRODUCCIÓN: Crear Orden usando los IDs recién generados
    order_data = {
        "id_sucursal": 1, # La sucursal MATRIZ creada por registrar_cliente_con_matriz suele ser ID 1 o cercana
        "id_version_ft": version_id, 
        "cantidad_solicitada": 10000,
        "cantidad_unidades": 2,
        "empaque_seleccionado": "ROLLO"
    }
    
    resp_order = client.post("/produccion/ordenes", json=order_data)
    assert resp_order.status_code == 200, f"Fallo en Orden: {resp_order.json()}"
    
    upid_code = resp_order.json()["codigo_upid"]

    # 4. TRAZABILIDAD: Registro de evento en planta
    scan_data = {
        "id_upid": upid_code, "id_empleado": emp_id, "id_maquina": 1, "id_proceso": 1
    }
    resp_scan = client.post("/produccion/escanear", json=scan_data)
    assert resp_scan.status_code == 200

    # 5. CONCURRENCIA: Intento de duplicado
    resp_dup = client.post("/produccion/escanear", json=scan_data)
    assert resp_dup.status_code == 400
    assert "Conflicto de trazabilidad" in resp_dup.json()["detail"]