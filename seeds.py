from app import app
from models.models import db, TipoMaterial, Material, Producto, ProductoReceta, Cliente, Sucursal, Pedido, DetallePedido, Ciudad

def run_seeds():
    with app.app_context():
        print("🌱 Iniciando siembra (Estructura Extendida)...")

        # Limpieza
        db.session.query(DetallePedido).delete()
        db.session.query(Pedido).delete()
        db.session.query(Sucursal).delete()
        db.session.query(Cliente).delete()
        db.session.query(Ciudad).delete() # <--- Borramos ciudades también
        db.session.query(ProductoReceta).delete()
        db.session.query(Producto).delete()
        db.session.query(Material).delete()
        db.session.query(TipoMaterial).delete()
        db.session.commit()

        # 1. CIUDADES
        mty = Ciudad(nombre='Monterrey', estado='Nuevo León')
        gdl = Ciudad(nombre='Guadalajara', estado='Jalisco')
        cdmx = Ciudad(nombre='CDMX', estado='CDMX')
        silao = Ciudad(nombre='Silao', estado='Guanajuato')
        db.session.add_all([mty, gdl, cdmx, silao])
        db.session.commit()

        # 2. CLIENTES (Ahora con dirección)
        cliente_coca = Cliente(
            nombre_fiscal='Coca Cola Femsa', 
            rfc='KOF980101', 
            direccion='Av. Alfonso Reyes 200', 
            colonia='Bella Vista', 
            codigo_postal='64440', 
            telefono='81815500', 
            ciudad_id=mty.id
        )
        cliente_farm = Cliente(
            nombre_fiscal='Farmacias Guadalajara', 
            rfc='FGU830930', 
            direccion='Av. Americas 100', 
            colonia='Ladrón de Guevara', 
            codigo_postal='44600', 
            telefono='33333333', 
            ciudad_id=gdl.id
        )
        db.session.add_all([cliente_coca, cliente_farm])
        db.session.commit()

        # 3. SUCURSALES (Ahora con transporte y ciudad)
        suc_norte = Sucursal(
            cliente_id=cliente_coca.id, 
            nombre='Planta Norte', 
            direccion='Av. Industrias 500', 
            colonia='Industrial', 
            codigo_postal='64000', 
            telefono_sucursal='81800000',
            transporte='Tráiler Propio',
            ciudad_id=mty.id
        )
        suc_bajio = Sucursal(
            cliente_id=cliente_coca.id, 
            nombre='CEDIS Bajío', 
            direccion='Carr. León-Silao Km 15', 
            colonia='Puerto Interior', 
            codigo_postal='36275', 
            telefono_sucursal='47770000',
            transporte='Castores',
            ciudad_id=silao.id
        )
        db.session.add_all([suc_norte, suc_bajio])
        db.session.commit()
        
        # 4. PRODUCTOS TERMINADOS (Asignados a clientes específicos)
        # Producto para Coca Cola
        prod1 = Producto(
            codigo_interno='ETQ-COCA-500', 
            nombre='Etiqueta Coca-Cola 500ml', 
            ancho_mm=100, alto_mm=50,
            cliente_id=cliente_coca.id  # 👈 ASIGNADO A COCA
        )
        
        # Producto para Farmacia (Para probar que se filtran)
        prod2 = Producto(
            codigo_interno='BLISTER-PARACETAMOL', 
            nombre='Aluminio Blister Paracetamol', 
            ancho_mm=200, alto_mm=100,
            cliente_id=cliente_farm.id  # 👈 ASIGNADO A FARMACIA
        )
        
        db.session.add_all([prod1, prod2])
        db.session.commit()
        print("✅ Base de datos actualizada con Ciudades y Direcciones.")

if __name__ == '__main__':
    run_seeds()