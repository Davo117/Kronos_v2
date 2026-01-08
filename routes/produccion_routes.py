from flask import Blueprint, jsonify
from models.models import db, Pedido

produccion_bp = Blueprint('produccion', __name__)

@produccion_bp.route('/api/produccion/dashboard', methods=['GET'])
def get_dashboard_data():
    # Buscamos ordenes que Logistica ya aprobo
    ordenes = Pedido.query.filter(
        Pedido.estatus.in_(['CONFIRMADO', 'PRODUCCION'])
    ).order_by(Pedido.fecha_entrega_pactada.asc()).all()

    lista_ordenes = []
    pendientes_cola = 0

    for p in ordenes:
        # Logica simple para el avance: Si esta en PRODUCCION lleva 50%, si no 0%
        avance_calculado = 50 if p.estatus == 'PRODUCCION' else 0
        
        # Tomamos el primer producto como referencia principal
        producto_principal = "Varios"
        if p.detalles and len(p.detalles) > 0:
            producto_principal = p.detalles[0].producto.nombre

        lista_ordenes.append({
            'folio': p.folio_interno,
            'cliente': p.cliente.nombre_fiscal if p.cliente else "N/A",
            'producto': producto_principal,
            'fecha_entrega': p.fecha_entrega_pactada.strftime('%Y-%m-%d') if p.fecha_entrega_pactada else 'Sin fecha',
            'estatus': p.estatus,
            'avance': avance_calculado
        })
        
        if p.estatus == 'CONFIRMADO':
            pendientes_cola += 1

    # Datos para los indicadores de arriba (KPIs)
    kpis = {
        'eficiencia': 92,     # Dato simulado por ahora
        'metros_hoy': 15400,  # Dato simulado
        'en_cola': pendientes_cola,
        'merma': 3.5          # Dato simulado
    }

    return jsonify({
        'kpis': kpis,
        'ordenes': lista_ordenes
    })