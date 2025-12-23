from app import app
from models.models import db, TipoMaterial, Material, Producto, ProductoReceta, Cliente, Sucursal, Pedido, DetallePedido

def run_seeds():
    with app.app_context():
        print("🌱 Iniciando la siembra de datos...")

        # 1. LIMPIEZA TOTAL (Borrando datos viejos para evitar duplicados)
        # Borramos en orden inverso a las dependencias
        db.session.query(DetallePedido).delete()
        db.session.query(Pedido).delete()
        db.session.query(Sucursal).delete()
        db.session.query(Cliente).delete()
        db.session.query(ProductoReceta).delete()
        db.session.query(Producto).delete()
        db.session.query(Material).delete()
        db.session.query(TipoMaterial).delete()
        db.session.commit()
        print("🧹 Limpieza completada.")

        # ------------------------------------------------------------------
        # 2. CLIENTES Y SUCURSALES (LOGÍSTICA)
        # ------------------------------------------------------------------
        cliente_coca = Cliente(nombre_fiscal='Coca Cola Femsa S.A.B. de C.V.', rfc='KOF980101')
        cliente_farm = Cliente(nombre_fiscal='Farmacias Guadalajara S.A. de C.V.', rfc='FGU830930')
        db.session.add_all([cliente_coca, cliente_farm])
        db.session.commit()

        # Sucursales Coca Cola
        suc_coca_norte = Sucursal(cliente_id=cliente_coca.id, nombre='Planta Norte', direccion='Av. Industrias 500, Monterrey', ciudad='Monterrey')
        suc_coca_bajio = Sucursal(cliente_id=cliente_coca.id, nombre='CEDIS Bajío', direccion='Carr. León-Silao Km 15', ciudad='Silao')
        
        # Sucursales Farmacia
        suc_farm_occidente = Sucursal(cliente_id=cliente_farm.id, nombre='CEDIS Occidente', direccion='Periférico Sur 4000', ciudad='Guadalajara')
        
        db.session.add_all([suc_coca_norte, suc_coca_bajio, suc_farm_occidente])
        db.session.commit()
        print("✅ Clientes y Sucursales creados.")

        # ------------------------------------------------------------------
        # 3. CATÁLOGOS TÉCNICOS
        # ------------------------------------------------------------------
        tipo_sustrato = TipoMaterial(nombre='SUSTRATO', descripcion='Papeles y películas')
        tipo_tinta = TipoMaterial(nombre='TINTA', descripcion='Tintas UV/Agua')
        db.session.add_all([tipo_sustrato, tipo_tinta])
        db.session.commit()

        # Materiales
        mat_papel = Material(codigo_interno='SUS-001', descripcion='Papel Semigloss 80g', tipo_material_id=tipo_sustrato.id, unidad_medida='mts', stock_actual=5000.00)
        mat_tinta = Material(codigo_interno='TIN-CYAN', descripcion='Tinta Cyan UV', tipo_material_id=tipo_tinta.id, unidad_medida='kg', stock_actual=20.0)
        db.session.add_all([mat_papel, mat_tinta])
        db.session.commit()

        # ------------------------------------------------------------------
        # 4. PRODUCTOS TERMINADOS
        # ------------------------------------------------------------------
        prod1 = Producto(codigo_interno='ETQ-COCA-500', nombre='Etiqueta Coca-Cola 500ml', ancho_mm=100, alto_mm=50)
        prod2 = Producto(codigo_interno='ETQ-FARM-BLISTER', nombre='Aluminio Blister Paracetamol', ancho_mm=200, alto_mm=100)
        
        db.session.add_all([prod1, prod2])
        db.session.commit()
        print(f"Productos creados: {prod1.nombre}, {prod2.nombre}")

        print("\n--- ¡TODO LISTO PARA LA DEMO! ---")

if __name__ == '__main__':
    run_seeds()