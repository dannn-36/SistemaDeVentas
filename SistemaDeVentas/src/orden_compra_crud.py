from database_connection import DatabaseConnection
import re
from datetime import datetime

class OrdenCompraCRUD:
    @staticmethod
    def validar_orden_compra(num_oco, fec_oco, cod_prv, fat_oco, est_oco):
        if not re.match(r"^OC\d{3}$", num_oco):
            return False, "Número de orden de compra inválido. Debe tener el formato 'OC' seguido de tres números (ej: OC001)."
        if OrdenCompraCRUD.orden_compra_existe(num_oco):
            return False, "El número de orden de compra ya existe. Por favor, use un número diferente."
        try:
            datetime.strptime(fec_oco, "%Y-%m-%d")
        except ValueError:
            return False, "Fecha de orden de compra inválida. Debe tener el formato YYYY-MM-DD."
        if not re.match(r"^PR\d{2}$", cod_prv):
            return False, "Código de proveedor inválido. Debe tener el formato 'PR' seguido de dos números (ej: PR01)."
        if not OrdenCompraCRUD.proveedor_existe(cod_prv):
            return False, "El código de proveedor no existe en la base de datos."
        try:
            datetime.strptime(fat_oco, "%Y-%m-%d")
        except ValueError:
            return False, "Fecha de facturación inválida. Debe tener el formato YYYY-MM-DD."
        if not est_oco.isdigit() or int(est_oco) not in [1, 2, 3]:
            return False, "Estado de orden de compra inválido. Debe ser un número (1, 2 o 3)."
        return True, ""

    @staticmethod
    def orden_compra_existe(num_oco):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM ORDEN_COMPRA WHERE NUM_OCO = %s", (num_oco,))
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def proveedor_existe(cod_prv):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM PROVEEDOR WHERE COD_PRV = %s", (cod_prv,))
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def listar_ordenes_compra():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ORDEN_COMPRA")
            ordenes = cursor.fetchall()
            return ordenes
        except Exception as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def insertar_orden_compra(num_oco, fec_oco, cod_prv, fat_oco, est_oco):
        valid, msg = OrdenCompraCRUD.validar_orden_compra(num_oco, fec_oco, cod_prv, fat_oco, est_oco)
        if not valid:
            return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            query = """
                INSERT INTO ORDEN_COMPRA (NUM_OCO, FEC_OCO, COD_PRV, FAT_OCO, EST_OCO)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (num_oco, fec_oco, cod_prv, fat_oco, est_oco)
            cursor.execute(query, valores)
            conexion.commit()
            return True, "Orden de compra insertada correctamente."
        except Exception as error:
            return False, f"Error al insertar orden de compra: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_orden_compra(num_oco, fec_oco=None, cod_prv=None, fat_oco=None, est_oco=None):
        if fec_oco or cod_prv or fat_oco or est_oco:
            valid, msg = OrdenCompraCRUD.validar_orden_compra(num_oco, fec_oco or "2000-01-01", cod_prv or "PR01", fat_oco or "2000-01-01", est_oco or "1")
            if not valid:
                return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if fec_oco:
                campos.append("FEC_OCO = %s")
                valores.append(fec_oco)
            if cod_prv:
                campos.append("COD_PRV = %s")
                valores.append(cod_prv)
            if fat_oco:
                campos.append("FAT_OCO = %s")
                valores.append(fat_oco)
            if est_oco:
                campos.append("EST_OCO = %s")
                valores.append(est_oco)

            if campos:
                query = f"UPDATE ORDEN_COMPRA SET {', '.join(campos)} WHERE NUM_OCO = %s"
                valores.append(num_oco)
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Orden de compra actualizada correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."
        except Exception as error:
            return False, f"Error al actualizar orden de compra: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_orden_compra(num_oco):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM ORDEN_COMPRA WHERE NUM_OCO = %s", (num_oco,))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Orden de compra eliminada correctamente."
            else:
                return False, "Orden de compra no encontrada."
        except Exception as error:
            return False, f"Error al eliminar orden de compra: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
