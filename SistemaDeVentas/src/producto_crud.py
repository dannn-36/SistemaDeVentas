import mysql.connector
from database_connection import DatabaseConnection

class ProductoCRUD:
    @staticmethod
    def agregar_producto(cod_pro, des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            query = """
            INSERT INTO PRODUCTO (COD_PRO, DES_PRO, PRE_PRO, SAC_PRO, SMI_PRO, UNI_PRO, LIN_PRO, IMP_PRO)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (cod_pro, des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro)

            cursor.execute(query, values)
            conexion.commit()
            return True, "Producto agregado exitosamente."

        except mysql.connector.Error as error:
            return False, f"Error al agregar producto: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def mostrar_productos():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PRODUCTO")
            productos = cursor.fetchall()
            return productos
        except mysql.connector.Error as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_producto(cod_pro, des_pro=None, pre_pro=None, sac_pro=None, smi_pro=None, uni_pro=None, lin_pro=None, imp_pro=None):
        try:
            if not cod_pro or not cod_pro.isalnum():
                raise ValueError("Código de producto inválido.")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if des_pro:
                campos.append("DES_PRO = %s")
                valores.append(des_pro)
            if pre_pro:
                campos.append("PRE_PRO = %s")
                valores.append(pre_pro)
            if sac_pro is not None:
                campos.append("SAC_PRO = %s")
                valores.append(sac_pro)
            if smi_pro is not None:
                campos.append("SMI_PRO = %s")
                valores.append(smi_pro)
            if uni_pro:
                campos.append("UNI_PRO = %s")
                valores.append(uni_pro)
            if lin_pro:
                campos.append("LIN_PRO = %s")
                valores.append(lin_pro)
            if imp_pro:
                campos.append("IMP_PRO = %s")
                valores.append(imp_pro)

            if campos:
                query = f"UPDATE PRODUCTO SET {', '.join(campos)} WHERE COD_PRO = %s"
                valores.append(cod_pro)
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Producto actualizado correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al actualizar producto: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_producto(cod_pro):
        try:
            if not cod_pro or not cod_pro.isalnum():
                raise ValueError("Código de producto inválido.")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM PRODUCTO WHERE COD_PRO = %s", (cod_pro,))
            conexion.commit()
            return True, "Producto eliminado correctamente."
        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al eliminar producto: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def existe_producto(cod_pro):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            query = "SELECT COUNT(*) FROM PRODUCTO WHERE COD_PRO = %s"
            cursor.execute(query, (cod_pro,))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as error:
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

