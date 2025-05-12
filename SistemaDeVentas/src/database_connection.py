import mysql.connector  # Ensure this import is present

class DatabaseConnection:
    @staticmethod
    def conexionBaseDeDatos():
        try:
            conexion = mysql.connector.connect(
                user='root',
                password='2852',
                port=3306,
                host='localhost',
                database='sistemadeventas'
            )
            print("Conexión correcta")
            return conexion
        except mysql.connector.Error as error:
            print(f"Error al conectarse a la base de datos: {error}")
            return None

    @staticmethod
    def menu_principal():
        while True:
            print("\n--- Menú Principal ---")
            print("1. CRUD de Clientes")
            print("2. CRUD de Proovedores")
            print("3. CRUD de Distritos")
            print("4. CRUD de Productos")
            print("5. CRUD de Vendedores")
            print("6. CRUD de Facturas")
            print("7. CRUD de Órdenes de Compra")
            print("8. CRUD de Detalles de Factura")
            print("9. CRUD de Detalles de Compra")
            print("10. CRUD de Abastecimientos")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                from client_crud import ClienteCRUD
                ClienteCRUD.menu_crud_clientes()
            elif opcion == "2":
                from provider_crud import ProveedorCRUD
                ProveedorCRUD.menu_crud_proveedores()
                
            elif opcion == "3":
                from district_crud import DistritoCRUD
                DistritoCRUD.menu_crud_distritos()
            elif opcion == "4":
                from product_crud import ProductoCRUD
                ProductoCRUD.menu_crud_productos()
               
            elif opcion == "5":
                from seller_crud import VendedorCRUD
                VendedorCRUD.menu_crud_vendedores()
            elif opcion == "6":
                from invoice_crud import FacturaCRUD
                FacturaCRUD.menu_crud_facturas()
                
            elif opcion == "7":
                from purchase_order_crud import OrdenCompraCRUD
                OrdenCompraCRUD.menu_crud_ordenes_compra()
                
            elif opcion == "8":
                from invoice_detail_crud import DetalleFacturaCRUD
                DetalleFacturaCRUD.menu_crud_detalle_factura()
             
            elif opcion == "9":
                from purchase_detail_crud import DetalleCompraCRUD
                DetalleCompraCRUD.menu_crud_detalle_compra()
             
            elif opcion == "10":
                from supply_crud import AbastecimientoCRUD
                AbastecimientoCRUD.menu_crud_abastecimiento()
              
            else:
                print("Opción inválida. Intente nuevamente.")

# Ejecutar el menú principal
if __name__ == "__main__":
    DatabaseConnection.menu_principal()