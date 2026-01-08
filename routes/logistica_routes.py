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
    print("Recibido:", data)

    try:
        # 1. Limpieza de Datos 
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

# 4. LISTAR PEDIDOS
@logistica_bp.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    
    pedidos = Pedido.query.order_by(Pedido.fecha_registro.desc()).all()
    
    resultado = []
    for p in pedidos:
        nombre_cliente = p.cliente.nombre_fiscal if p.cliente else "Sin Cliente"
        nombre_sucursal = p.sucursal.nombre if p.sucursal else "N/A"
        
        # Calculamos progreso (Por ahora dummy)
        progreso = 0 
        
        resultado.append({
            'id': p.id,
            'folio': p.folio_interno,
            'orden_cliente': p.numero_orden_cliente,
            'cliente': nombre_cliente,
            'sucursal': nombre_sucursal,
            'fecha_registro': p.fecha_registro.strftime('%Y-%m-%d'),
            'fecha_entrega': p.fecha_entrega_pactada.strftime('%Y-%m-%d') if p.fecha_entrega_pactada else 'Sin Fecha',
            'estatus': p.estatus,
            'items_count': len(p.detalles) 
        })
        
    return jsonify(resultado)

# 5. OBTENER UN PEDIDO POR ID 
# # (Para editar)
@logistica_bp.route('/api/pedidos/<int:id>', methods=['GET'])
def get_pedido_por_id(id):
    p = Pedido.query.get_or_404(id)

    detalles = []
    for d in p.detalles:
        detalles.append({
            'productoId': d.producto_id,
            'cantidad': float(d.cantidad_solicitada),
            'unidad': d.unidad_medida,
            'notas': d.notas
        })
        
    data = {
        'id': p.id,
        'cliente_id': p.cliente_id,
        'sucursal_id': p.sucursal_id,
        'numero_orden_cliente': p.numero_orden_cliente,
        'fecha_documento': p.fecha_documento.strftime('%Y-%m-%d') if p.fecha_documento else '',
        'fecha_recepcion': p.fecha_recepcion.strftime('%Y-%m-%d') if p.fecha_recepcion else '',
        'fecha_entrega_pactada': p.fecha_entrega_pactada.strftime('%Y-%m-%d') if p.fecha_entrega_pactada else '',
        'productos': detalles
    }

    return jsonify(data)

# 6. CANCELAR PEDIDO (Cambio de Estatus)
@logistica_bp.route('/api/pedidos/<int:id>/cancelar', methods=['PUT'])
def cancelar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    
    # Validacion, no cancelar si ya se entregó
    if pedido.estatus == 'ENTREGADO':
        return jsonify({'error': 'No se puede cancelar un pedido entregado'}), 400
        
    pedido.estatus = 'CANCELADO'
    db.session.commit()
    
    return jsonify({'mensaje': 'Pedido cancelado exitosamente'})

# 7. ACTUALIZAR PEDIDO COMPLETO (PUT)
@logistica_bp.route('/api/pedidos/<int:id>', methods=['PUT'])
def actualizar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    data = request.json

    try:
        # Funciones auxiliares para limpiar datos (igual que en crear)
        def clean(value):
            return None if value == "" or value is None else value
        
        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        # 1. Actualizar Datos Generales
        pedido.cliente_id = data['cliente_id']
        pedido.sucursal_id = clean(data.get('sucursal_id'))
        pedido.numero_orden_cliente = clean(data.get('numero_orden_cliente'))
        pedido.fecha_documento = parse_date(data.get('fecha_documento'))
        pedido.fecha_recepcion = parse_date(data.get('fecha_recepcion'))
        pedido.fecha_entrega_pactada = parse_date(data.get('fecha_entrega_pactada'))
        
        # 2. Actualizar Productos
        # Primero borramos los detalles actuales de esta orden
        DetallePedido.query.filter_by(pedido_id=id).delete()
        
        for item in data['productos']:
            if not item['productoId']: continue 
            
            detalle = DetallePedido(
                pedido_id=pedido.id,
                producto_id=item['productoId'],
                cantidad_solicitada=float(item['cantidad']) if item['cantidad'] else 0,
                unidad_medida=item['unidad'],
                notas=item['notas']
            )
            db.session.add(detalle)
            
        db.session.commit()
        return jsonify({'mensaje': 'Pedido actualizado correctamente'})

    except Exception as e:
        db.session.rollback()
        print(" ERROR ACTUALIZANDO:", str(e))
        return jsonify({'error': str(e)}), 500