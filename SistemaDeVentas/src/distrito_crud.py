import mysql.connector
from database_connection import DatabaseConnection

class DistritoCRUD:

    @staticmethod
    def insertar_distrito(cod_dis, nom_dis):
        try:
            if not cod_dis.startswith("D") or not cod_dis[1:].isdigit():
                raise ValueError("Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01).")
            if any(char.isdigit() for char in nom_dis):
                raise ValueError("El nombre del distrito no debe contener números.")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            query = "INSERT INTO DISTRITO (COD_DIS, NOM_DIS) VALUES (%s, %s)"
            cursor.execute(query, (cod_dis, nom_dis))
            conexion.commit()
            return True, "Distrito insertado correctamente."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al insertar distrito: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def listar_distritos():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DISTRITO")
            distritos = cursor.fetchall()
            return distritos
        except mysql.connector.Error as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_distrito(cod_dis, nom_dis=None):
        try:
            if not cod_dis.startswith("D") or not cod_dis[1:].isdigit():
                raise ValueError("Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01).")
            if nom_dis and any(char.isdigit() for char in nom_dis):
                raise ValueError("El nombre del distrito no debe contener números.")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            # Verificar si existe
            cursor.execute("SELECT * FROM DISTRITO WHERE COD_DIS = %s", (cod_dis,))
            distrito = cursor.fetchone()
            if not distrito:
                return False, "Distrito no encontrado."

            if nom_dis:
                query = "UPDATE DISTRITO SET NOM_DIS = %s WHERE COD_DIS = %s"
                cursor.execute(query, (nom_dis, cod_dis))
                conexion.commit()
                return True, "Distrito actualizado correctamente."
            else:
                return False, "No se proporcionó un nuevo nombre para actualizar."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al actualizar distrito: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_distrito(cod_dis):
        try:
            if not cod_dis.startswith("D") or not cod_dis[1:].isdigit():
                raise ValueError("Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01).")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM DISTRITO WHERE COD_DIS = %s", (cod_dis,))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Distrito eliminado correctamente."
            else:
                return False, "Distrito no encontrado."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al eliminar distrito: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
