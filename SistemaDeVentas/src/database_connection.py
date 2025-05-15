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

# Ejecutar el menú principal
if __name__ == "__main__":
    DatabaseConnection.menu_principal()