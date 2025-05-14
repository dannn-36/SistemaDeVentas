import mysql.connector
from database_connection import DatabaseConnection

class AbastecimientoCRUD:

    @staticmethod
    def insertar_abastecimiento(cod_prv, cod_pro, pre_aba):
        try:
            if not cod_prv.startswith("PR") or not cod_prv[2:].isdigit():
                raise ValueError("Código de proveedor inválido. Debe comenzar con 'PR' seguido de números (ej: PR01).")
            if not cod_pro.startswith("P") or not cod_pro[1:].isdigit():
                raise ValueError("Código de producto inválido. Debe comenzar con 'P' seguido de números (ej: P001).")
            if not isinstance(pre_aba, (int, float)) or float(pre_aba) <= 0:
                raise ValueError("Precio inválido, debe ser un número mayor que cero.")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            query = "INSERT INTO ABASTECIMIENTO (COD_PRV, COD_PRO, PRE_ABA) VALUES (%s, %s, %s)"
            cursor.execute(query, (cod_prv, cod_pro, pre_aba))
            conexion.commit()
            return True, "Abastecimiento insertado correctamente."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al insertar abastecimiento: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def listar_abastecimientos():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ABASTECIMIENTO")
            abastecimientos = cursor.fetchall()
            return abastecimientos
        except mysql.connector.Error as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_abastecimiento(cod_prv, cod_pro, nuevo_precio):
        try:
            if not cod_prv.startswith("PR") or not cod_prv[2:].isdigit():
                raise ValueError("Código de proveedor inválido.")
            if not cod_pro.startswith("P") or not cod_pro[1:].isdigit():
                raise ValueError("Código de producto inválido.")
            if not isinstance(nuevo_precio, (int, float)) or float(nuevo_precio) <= 0:
                raise ValueError("Precio inválido.")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            # Verificar si existe
            cursor.execute("SELECT * FROM ABASTECIMIENTO WHERE COD_PRV = %s AND COD_PRO = %s", (cod_prv, cod_pro))
            registro = cursor.fetchone()
            if not registro:
                return False, "Registro de abastecimiento no encontrado."

            query = "UPDATE ABASTECIMIENTO SET PRE_ABA = %s WHERE COD_PRV = %s AND COD_PRO = %s"
            cursor.execute(query, (nuevo_precio, cod_prv, cod_pro))
            conexion.commit()
            return True, "Abastecimiento actualizado correctamente."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al actualizar abastecimiento: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_abastecimiento(cod_prv, cod_pro):
        try:
            if not cod_prv.startswith("PR") or not cod_prv[2:].isdigit():
                raise ValueError("Código de proveedor inválido.")
            if not cod_pro.startswith("P") or not cod_pro[1:].isdigit():
                raise ValueError("Código de producto inválido.")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM ABASTECIMIENTO WHERE COD_PRV = %s AND COD_PRO = %s", (cod_prv, cod_pro))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Abastecimiento eliminado correctamente."
            else:
                return False, "Abastecimiento no encontrado."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al eliminar abastecimiento: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
