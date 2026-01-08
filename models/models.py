from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instancia de la base de datos (normalmente esto va en tu app.py o extensions.py)
db = SQLAlchemy()

# -------------------------------------------------------------------
# 1. CATÁLOGOS BASE (Para estandarizar entradas)
# -------------------------------------------------------------------

class TipoMaterial(db.Model):
    """
    Define si es TINTA, SUSTRATO, LAMINADO, BARNIZ, etc.
    Esto reemplaza la lógica rígida del sistema anterior.
    """
    __tablename__ = 'tipos_material'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True) # Ej: "Sustrato", "Tinta UV"
    descripcion = db.Column(db.String(100))
    
    # Relación para acceder a los materiales de este tipo
    materiales = db.relationship('Material', backref='tipo', lazy=True)

    def __repr__(self):
        return f'<TipoMaterial {self.nombre}>'

# -------------------------------------------------------------------
# 2. INVENTARIO (INSUMOS)
# -------------------------------------------------------------------

class Material(db.Model):
    """
    El inventario real. Aquí viven tanto el 'Papel Bond' como el 'Barniz Mate'.
    """
    __tablename__ = 'materiales'

    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.String(30), unique=True, nullable=False) # El SKU de la empresa
    descripcion = db.Column(db.String(200), nullable=False)
    
    # Foreign Key al catálogo de tipos
    tipo_material_id = db.Column(db.Integer, db.ForeignKey('tipos_material.id'), nullable=False)
    
    # IMPORTANTE: Usamos Numeric (DECIMAL) para evitar errores de redondeo de FLOAT
    stock_actual = db.Column(db.Numeric(10, 4), default=0) 
    unidad_medida = db.Column(db.String(10), nullable=False) # 'kg', 'mts', 'lts'
    
    costo_unitario = db.Column(db.Numeric(10, 2)) # Para reportes financieros
    
    activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Material {self.codigo_interno} - {self.descripcion}>'

# -------------------------------------------------------------------
# 3. PRODUCTO TERMINADO (HEADER)
# -------------------------------------------------------------------

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    
    # Dimensiones
    ancho_mm = db.Column(db.Numeric(10, 2))
    alto_mm = db.Column(db.Numeric(10, 2))
    
    activo = db.Column(db.Boolean, default=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship('Cliente', backref='productos_asignados')

# -------------------------------------------------------------------
# 4. MATERIALES Y RECEtas
# -------------------------------------------------------------------

class ProductoReceta(db.Model):
    """
    Tabla intermedia que conecta Producto con Materiales.
    Define CÓMO se fabrica la etiqueta.
    """
    __tablename__ = 'producto_recetas'

    id = db.Column(db.Integer, primary_key=True)
    
    # Vínculos
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materiales.id'), nullable=False)
    
    # Definición técnica
    cantidad_consumo = db.Column(db.Numeric(10, 6), nullable=False) # Cuánto gasta por unidad de producto
    
    # Orden de aplicación (Vital para producción)
    # 1 = Sustrato, 2 = Tinta Fondo, 3 = Tinta Detalle, 4 = Laminado, 5 = Corte
    orden_aplicacion = db.Column(db.Integer, nullable=False)
    
    # Relación para acceder a los datos del material desde la receta
    material = db.relationship('Material')

    def __repr__(self):
        return f'<Receta {self.producto.codigo_interno} -> {self.material.descripcion}>'
    
# -------------------------------------------------------------------
# 5. USUARIOS Y SEGURIDAD
# -------------------------------------------------------------------

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100))
    puesto = db.Column(db.String(100))
    # Relación inversa con Usuario
    usuario = db.relationship('Usuario', backref='empleado', uselist=False)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Guardaremos hash, no texto plano
    rol = db.Column(db.String(20), default='user') # admin, logistica, produccion
    activo = db.Column(db.Boolean, default=True)
    
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))


# -------------------------------------------------------------------
# 6. LOGÍSTICA Y PEDIDOS
# -------------------------------------------------------------------

class Ciudad(db.Model):
    __tablename__ = 'ciudades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False) # Ej. Monterrey
    estado = db.Column(db.String(100), nullable=False) # Ej. Nuevo León
    pais = db.Column(db.String(100), default='México')
    
    # Relaciones para saber qué clientes/sucursales hay en esta ciudad
    clientes = db.relationship('Cliente', backref='ciudad_ref', lazy=True)
    sucursales = db.relationship('Sucursal', backref='ciudad_ref', lazy=True)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre_fiscal = db.Column(db.String(200), nullable=False)
    rfc = db.Column(db.String(20))
    telefono = db.Column(db.String(20))
    
    # Dirección Fiscal
    direccion = db.Column(db.String(255)) # Calle y Número
    colonia = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    
    # Relación con Ciudad
    ciudad_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'))
    
    # Relación con sus sucursales
    sucursales = db.relationship('Sucursal', backref='cliente', lazy=True)

class Sucursal(db.Model):
    __tablename__ = 'sucursales'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    nombre = db.Column(db.String(100), nullable=False) # Ej: "Planta Norte"
    
    # Dirección de Entrega (Puede ser distinta a la fiscal)
    direccion = db.Column(db.String(255))
    colonia = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    telefono_sucursal = db.Column(db.String(20))
    transporte = db.Column(db.String(100)) # Ej: "Transportes Castores", "Propio", etc.
    
    # Relación con Ciudad
    ciudad_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'))
    
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)

    # Datos Generales
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursales.id')) # NUEVO

    folio_interno = db.Column(db.String(20), unique=True) # Generado por nosotros (ej: PED-001)
    numero_orden_cliente = db.Column(db.String(50)) # El folio que ellos nos dan (ej: OC-9988)

    # Fechas Clave
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow) # Cuándo se capturó en sistema
    fecha_documento = db.Column(db.Date) # La fecha del documento del cliente
    fecha_recepcion = db.Column(db.Date) # Cuando nos llegó el documento
    fecha_entrega_pactada = db.Column(db.Date) # Cuando prometimos entregar

    estatus = db.Column(db.String(20), default='BORRADOR') 

    # Relación con los productos
    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)
    cliente = db.relationship('Cliente', backref='pedidos')
    sucursal = db.relationship('Sucursal', backref='pedidos')

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))

    cantidad_solicitada = db.Column(db.Numeric(10, 2))
    unidad_medida = db.Column(db.String(20)) # Guardamos la unidad por si cambia el producto después
    notas = db.Column(db.String(255)) # "Lote prioritario", etc.

    cantidad_entregada = db.Column(db.Numeric(10, 2), default=0)
    producto = db.relationship('Producto', backref='detalles_pedido')

# -------------------------------------------------------------------
# 7. PRODUCCIÓN 
# -------------------------------------------------------------------

class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'
    id = db.Column(db.Integer, primary_key=True)
    folio_op = db.Column(db.String(20), unique=True) # Ej: OP-5599
    pedido_detalle_id = db.Column(db.Integer, db.ForeignKey('detalles_pedido.id'))
    
    cantidad_meta = db.Column(db.Numeric(10, 2))
    estatus = db.Column(db.String(20), default='PENDIENTE') # EN_PROCESO, DETENIDO, CERRADO

class BitacoraProduccion(db.Model):
    """
    Esta es la tabla MÁGICA que reemplaza a tbproimpresion, tbprocorte, etc.
    """
    __tablename__ = 'bitacora_produccion'
    id = db.Column(db.Integer, primary_key=True)
    orden_produccion_id = db.Column(db.Integer, db.ForeignKey('ordenes_produccion.id'))
    
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    
    # Aquí definimos qué se hizo 
    proceso = db.Column(db.String(50), nullable=False) 
    
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    
    cantidad_entrada = db.Column(db.Numeric(10, 2))
    cantidad_salida_buena = db.Column(db.Numeric(10, 2))
    merma_cantidad = db.Column(db.Numeric(10, 2))
    
    observaciones = db.Column(db.Text)
    