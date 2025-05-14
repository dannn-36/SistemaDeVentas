from database_connection import DatabaseConnection
import re

class DetalleCompraCRUD:
    @staticmethod
    def validar_detalle_compra(num_oco, cod_pro, can_det):
        if not re.match(r"^OC\d{3}$", num_oco):
            return False, "Número de orden de compra inválido. Debe tener el formato 'OC' seguido de tres números (ej: OC001)."
        if not DetalleCompraCRUD.orden_compra_existe(num_oco):
            return False, "El número de orden de compra no existe en la base de datos."
        if not re.match(r"^P\d{3}$", cod_pro):
            return False, "Código de producto inválido. Debe tener el formato 'P' seguido de tres números (ej: P001)."
        if not DetalleCompraCRUD.producto_existe(cod_pro):
            return False, "El código de producto no existe en la base de datos."
        if not isinstance(can_det, int) or can_det <= 0:
            return False, "Cantidad del detalle inválida. Debe ser un número entero mayor que 0."
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
    def producto_existe(cod_pro):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM PRODUCTO WHERE COD_PRO = %s", (cod_pro,))
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def listar_detalles_compra():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DETALLE_COMPRA")
            detalles = cursor.fetchall()
            return detalles
        except Exception as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def insertar_detalle_compra(num_oco, cod_pro, can_det):
        valid, msg = DetalleCompraCRUD.validar_detalle_compra(num_oco, cod_pro, can_det)
        if not valid:
            return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            query = """
                INSERT INTO DETALLE_COMPRA (NUM_OCO, COD_PRO, CAN_DET)
                VALUES (%s, %s, %s)
            """
            valores = (num_oco, cod_pro, can_det)
            cursor.execute(query, valores)
            conexion.commit()
            return True, "Detalle de compra insertado correctamente."
        except Exception as error:
            return False, f"Error al insertar detalle de compra: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_detalle_compra(num_oco, cod_pro, can_det=None):
        if can_det:
            valid, msg = DetalleCompraCRUD.validar_detalle_compra(num_oco, cod_pro, can_det)
            if not valid:
                return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if can_det:
                campos.append("CAN_DET = %s")
                valores.append(can_det)

            if campos:
                query = f"UPDATE DETALLE_COMPRA SET {', '.join(campos)} WHERE NUM_OCO = %s AND COD_PRO = %s"
                valores.extend([num_oco, cod_pro])
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Detalle de compra actualizado correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."
        except Exception as error:
            return False, f"Error al actualizar detalle de compra: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_detalle_compra(num_oco, cod_pro):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM DETALLE_COMPRA WHERE NUM_OCO = %s AND COD_PRO = %s", (num_oco, cod_pro))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Detalle de compra eliminado correctamente."
            else:
                return False, "Detalle de compra no encontrado."
        except Exception as error:
            return False, f"Error al eliminar detalle de compra: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
