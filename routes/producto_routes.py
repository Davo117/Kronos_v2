from flask import Blueprint, request, jsonify
from models.models import db, Producto, Cliente

producto_bp = Blueprint('producto_ing', __name__)

# -----------------------------------------------------------------------------
# GESTIÓN DE PRODUCTO
# -----------------------------------------------------------------------------

# 1. LISTA DE PRODUCTOS
@producto_bp.route('/api/productos', methods=['GET'])
def get_productos():
    cliente_id = request.args.get('cliente_id')
    
    query = Producto.query.filter_by(activo=True)
    
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
        
    productos = query.order_by(Producto.nombre.asc()).all()

    resultado = []
    for p in productos:
        cliente_nombre = p.cliente.nombre_fiscal if p.cliente else "Sin Asignar"
        resultado.append({
            'id': p.id,
            'codigo': p.codigo_interno,
            'nombre': p.nombre,
            'cliente_id': p.cliente_id,
            'cliente': cliente_nombre,
            'ancho': float(p.ancho_mm),
            'alto': float(p.alto_mm)
        })

    return jsonify(resultado)

# 2. CREAR NUEVO PRODUCTO
@producto_bp.route('/api/productos', methods=['POST'])
def crear_producto():
    data = request.json
    
    # Validaciones
    if not data.get('cliente_id') or not data.get('nombre') or not data.get('codigo'):
        return jsonify({'error': 'Cliente, Nombre y Código son obligatorios'}), 400

    try:
        nuevo_prod = Producto(
            cliente_id=int(data['cliente_id']),
            codigo_interno=data['codigo'],
            nombre=data['nombre'],
            ancho_mm=float(data['ancho']) if data.get('ancho') else 0,
            alto_mm=float(data['alto']) if data.get('alto') else 0,
            activo=True
        )
        
        db.session.add(nuevo_prod)
        db.session.commit()
        return jsonify({'mensaje': 'Producto diseñado exitosamente', 'id': nuevo_prod.id})
        
    except Exception as e:
        db.session.rollback()
        if "Duplicate entry" in str(e):
             return jsonify({'error': 'El código interno ya existe'}), 400
        return jsonify({'error': str(e)}), 500