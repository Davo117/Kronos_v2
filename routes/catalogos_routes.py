from flask import Blueprint, request, jsonify
from models.models import db, Ciudad, Cliente, Sucursal, Producto

catalogos_bp = Blueprint('catalogos', __name__)

# -----------------------------------------------------------------------------
# 1. CIUDADES
# -----------------------------------------------------------------------------
@catalogos_bp.route('/api/ciudades', methods=['GET'])
def get_ciudades():
    ciudades = Ciudad.query.order_by(Ciudad.nombre.asc()).all()
    return jsonify([{
        'id': c.id, 
        'nombre': c.nombre, 
        'estado': c.estado, 
        'pais': c.pais
    } for c in ciudades])

@catalogos_bp.route('/api/ciudades', methods=['POST'])
def crear_ciudad():
    data = request.json
    
    if not data.get('nombre') or not data.get('estado'):
        return jsonify({'error': 'Nombre y Estado son obligatorios'}), 400

    nueva = Ciudad(
        nombre=data['nombre'],
        estado=data['estado'],
        pais=data.get('pais', 'México')
    )
    
    try:
        db.session.add(nueva)
        db.session.commit()
        return jsonify({'mensaje': 'Ciudad agregada correctamente', 'id': nueva.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# -----------------------------------------------------------------------------
# 2. CLIENTES 
# -----------------------------------------------------------------------------
@catalogos_bp.route('/api/clientes-completo', methods=['POST'])
def crear_cliente():
    data = request.json
    try:
        nuevo = Cliente(
            nombre_fiscal=data['nombre_fiscal'],
            rfc=data['rfc'],
            telefono=data.get('telefono'),
            
            # Dirección
            direccion=data.get('direccion'),
            colonia=data.get('colonia'),
            codigo_postal=data.get('codigo_postal'),
            
            # Relación: Convertimos a entero por seguridad
            ciudad_id=int(data['ciudad_id']) if data.get('ciudad_id') else None
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'mensaje': 'Cliente registrado exitosamente', 'id': nuevo.id})
    except Exception as e:
        db.session.rollback()
        print("Error creando cliente:", e)
        return jsonify({'error': str(e)}), 500

# -----------------------------------------------------------------------------
# 3. SUCURSALES
# -----------------------------------------------------------------------------
@catalogos_bp.route('/api/sucursales-completo', methods=['POST'])
def crear_sucursal():
    data = request.json
    try:
        if not data.get('cliente_id'):
             return jsonify({'error': 'La sucursal debe pertenecer a un cliente'}), 400

        nueva = Sucursal(
            cliente_id=int(data['cliente_id']),
            nombre=data['nombre'],
            telefono_sucursal=data.get('telefono'),
            transporte=data.get('transporte'), # Campo nuevo importante
            
            # Dirección
            direccion=data.get('direccion'),
            colonia=data.get('colonia'),
            codigo_postal=data.get('codigo_postal'),
            
            # Relación
            ciudad_id=int(data['ciudad_id']) if data.get('ciudad_id') else None
        )
        db.session.add(nueva)
        db.session.commit()
        return jsonify({'mensaje': 'Sucursal vinculada exitosamente', 'id': nueva.id})
    except Exception as e:
        db.session.rollback()
        print("Error creando sucursal:", e)
        return jsonify({'error': str(e)}), 500
    
# -----------------------------------------------------------------------------
# 4. PRODUCTOS 
# -----------------------------------------------------------------------------

# --- Se creo su propio archivo de rutas --- #


