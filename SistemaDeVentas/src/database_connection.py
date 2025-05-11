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
            print("4. CRUD de productos")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                from client_crud import ClienteCRUD
                ClienteCRUD.menu_crud_clientes()
            elif opcion == "2":
                from provider_crud import ProveedorCRUD
                ProveedorCRUD.menu_crud_proveedores()
                break
            elif opcion == "3":
                from district_crud import DistritoCRUD
                DistritoCRUD.menu_crud_distritos()
                break
            elif opcion == "4":
                from product_crud import ProductoCRUD
                ProductoCRUD.menu_crud_productos()
                break
            else:
                print("Opción inválida. Intente nuevamente.")

# Ejecutar el menú principal
if __name__ == "__main__":
    DatabaseConnection.menu_principal()