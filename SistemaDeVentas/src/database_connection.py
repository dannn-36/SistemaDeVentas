import mysql.connector

class DatabaseConnection:
    # Valores por defecto
  
    host = 'localhost'
    port = 3306
    database = 'sistemadeventas'

    @classmethod
    def set_credentials(cls, user, password):
        cls.user = user
        cls.password = password

    @staticmethod
    def conexionBaseDeDatos():
        try:
            
            conexion = mysql.connector.connect(
                user=DatabaseConnection.user,
                password=DatabaseConnection.password,
                host=DatabaseConnection.host,
                port=DatabaseConnection.port,
                database=DatabaseConnection.database
            )
            print("Conexión correcta")
            return conexion
        except mysql.connector.Error as error:
            print(f"Error al conectarse a la base de datos: {error}")
            return None
