from flask import Blueprint, request, jsonify
from models.models import db, Cliente, Sucursal, Producto, Pedido, DetallePedido
from datetime import datetime

logistica_bp = Blueprint('logistica', __name__)

# 1. Obtener lista de clientes 
@logistica_bp.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    resultado = []
    for c in clientes:
        sucursales = [{'id': s.id, 'nombre': s.nombre} for s in c.sucursales]
        resultado.append({
            'id': c.id,
            'nombre': c.nombre_fiscal,
            'sucursales': sucursales
        })
    return jsonify(resultado)

# 2. Obtener lista de productos para el buscador
@logistica_bp.route('/api/productos-catalogo', methods=['GET'])
def get_productos_catalogo():
    productos = Producto.query.filter_by(activo=True).all()
    resultado = [{'id': p.id, 'nombre': p.nombre, 'codigo': p.codigo_interno} for p in productos]
    return jsonify(resultado)

# 3. Guardar el pedido
@logistica_bp.route('/api/pedidos', methods=['POST'])
def crear_pedido():
    data = request.json
    print("📦 Payload recibido:", data) # Esto te servirá para ver en la terminal qué llega

    try:
        # 1. Limpieza de Datos (Vital para evitar errores de tipo)
        # Convertimos cadenas vacías "" a None (NULL en base de datos)
        def clean(value):
            if value == "" or value is None:
                return None
            return value

        # 2. Parseo de Fechas seguro
        def parse_date(date_str):
            if not date_str: return None
            return datetime.strptime(date_str, '%Y-%m-%d').date()

        nuevo_pedido = Pedido(
            cliente_id=data['cliente_id'], # Este sí es obligatorio
            sucursal_id=clean(data.get('sucursal_id')), 
            numero_orden_cliente=clean(data.get('numero_orden_cliente')),
            fecha_documento=parse_date(data.get('fecha_documento')),
            fecha_recepcion=parse_date(data.get('fecha_recepcion')),
            fecha_entrega_pactada=parse_date(data.get('fecha_entrega_pactada')),
            folio_interno=f"TEMP-{int(datetime.now().timestamp())}", 
            estatus='CONFIRMADO'
        )
        
        db.session.add(nuevo_pedido)
        db.session.flush() # Generamos el ID
        
        # Guardar Detalles
        for item in data['productos']:
            if not item['productoId']: continue 
            
            detalle = DetallePedido(
                pedido_id=nuevo_pedido.id,
                producto_id=item['productoId'],
                cantidad_solicitada=float(item['cantidad']) if item['cantidad'] else 0,
                unidad_medida=item['unidad'],
                notas=item['notas']
            )
            db.session.add(detalle)
            
        db.session.commit()
        return jsonify({'mensaje': 'Pedido creado exitosamente', 'id': nuevo_pedido.id}), 201

    except Exception as e:
        db.session.rollback()
        print("ERROR EN BACKEND:", str(e))
        return jsonify({'error': str(e)}), 500