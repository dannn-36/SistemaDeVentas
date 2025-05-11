import mysql.connector

class DatabaseConnection:
    @staticmethod
    def conexionBaseDeDatos():
        try:
            conexion = mysql.connector.connect(
                user='root',
                password='2852',
                port=3306,
                host='127.0.0.1',
                database='sistemadeventas'
            )
            print("Conexión correcta")
            return conexion

        except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos: {}".format(error))
            return None

    conexionBaseDeDatos()