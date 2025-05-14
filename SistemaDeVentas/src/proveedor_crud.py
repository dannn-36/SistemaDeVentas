import mysql.connector
from database_connection import DatabaseConnection

class ProveedorCRUD:
    @staticmethod
    def agregar_proveedor(cod_prv, rso_prv, dir_prv, tel_prv, cod_dis, rep_pro):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            # Verificar si el proveedor ya existe
            cursor.execute("SELECT COUNT(*) FROM PROVEEDOR WHERE COD_PRV = %s", (cod_prv,))
            if cursor.fetchone()[0] > 0:
                return False, "El código del proveedor ya existe. Por favor, elige otro."

            query = """
                INSERT INTO PROVEEDOR (COD_PRV, RSO_PRV, DIR_PRV, TEL_PRV, COD_DIS, REP_PRO)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (cod_prv, rso_prv, dir_prv, tel_prv, cod_dis, rep_pro)

            cursor.execute(query, values)
            conexion.commit()
            return True, "Proveedor agregado exitosamente."

        except mysql.connector.Error as error:
            return False, f"Error al agregar proveedor: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def mostrar_proveedores():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PROVEEDOR")
            proveedores = cursor.fetchall()
            return proveedores
        except mysql.connector.Error as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_proveedor(cod_prv, rso_prv=None, dir_prv=None, tel_prv=None, cod_dis=None, rep_pro=None):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if rso_prv:
                campos.append("RSO_PRV = %s")
                valores.append(rso_prv)
            if dir_prv:
                campos.append("DIR_PRV = %s")
                valores.append(dir_prv)
            if tel_prv:
                campos.append("TEL_PRV = %s")
                valores.append(tel_prv)
            if cod_dis:
                campos.append("COD_DIS = %s")
                valores.append(cod_dis)
            if rep_pro:
                campos.append("REP_PRO = %s")
                valores.append(rep_pro)

            if campos:
                query = f"UPDATE PROVEEDOR SET {', '.join(campos)} WHERE COD_PRV = %s"
                valores.append(cod_prv)
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Proveedor actualizado correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."

        except mysql.connector.Error as error:
            return False, f"Error al actualizar proveedor: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_proveedor(cod_prv):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM PROVEEDOR WHERE COD_PRV = %s", (cod_prv,))
            conexion.commit()
            return True, "Proveedor eliminado correctamente."
        except mysql.connector.Error as error:
            return False, f"Error al eliminar proveedor: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
