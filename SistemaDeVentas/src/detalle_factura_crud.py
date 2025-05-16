from database_connection import DatabaseConnection
import re

class DetalleFacturaCRUD:
    @staticmethod
    def validar_detalle_factura(num_fac, cod_pro, can_ven, pre_ven):
        if not re.match(r"^FA\d{3}$", num_fac):
            return False, "Número de factura inválido. Debe tener el formato 'FA' seguido de tres números (ej: FA001)."
        if not re.match(r"^P\d{3}$", cod_pro):
            return False, "Código de producto inválido. Debe tener el formato 'P' seguido de tres números (ej: P001)."
        if not isinstance(can_ven, int) or can_ven <= 0:
            return False, "Cantidad vendida inválida. Debe ser un número entero mayor que 0."
        if not isinstance(pre_ven, (int, float)) or pre_ven <= 0:
            return False, "Precio de venta inválido. Debe ser un número mayor que 0."
        return True, ""

    @staticmethod
    def listar_detalles_factura():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DETALLE_FACTURA")
            detalles = cursor.fetchall()
            return detalles
        except Exception as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def verificar_existencia_factura(num_fac):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM FACTURA WHERE NUM_FAC = %s", (num_fac,))
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def verificar_existencia_producto(cod_pro):
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
    def insertar_detalle_factura(num_fac, cod_pro, can_ven, pre_ven):
        # Verificar existencia de factura y producto
        if not DetalleFacturaCRUD.verificar_existencia_factura(num_fac):
            return False, "El número de factura no existe en la base de datos."
        if not DetalleFacturaCRUD.verificar_existencia_producto(cod_pro):
            return False, "El código de producto no existe en la base de datos."

        valid, msg = DetalleFacturaCRUD.validar_detalle_factura(num_fac, cod_pro, can_ven, pre_ven)
        if not valid:
            return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            query = """
                INSERT INTO DETALLE_FACTURA (NUM_FAC, COD_PRO, CAN_VEN, PRE_VEN)
                VALUES (%s, %s, %s, %s)
            """
            valores = (num_fac, cod_pro, can_ven, pre_ven)
            cursor.execute(query, valores)
            conexion.commit()
            return True, "Detalle de factura insertado correctamente."
        except Exception as error:
            return False, f"Error al insertar detalle de factura: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_detalle_factura(num_fac, cod_pro, can_ven=None, pre_ven=None):
        # Verificar existencia de factura y producto
        if not DetalleFacturaCRUD.verificar_existencia_factura(num_fac):
            return False, "El número de factura no existe en la base de datos."
        if not DetalleFacturaCRUD.verificar_existencia_producto(cod_pro):
            return False, "El código de producto no existe en la base de datos."

        if can_ven or pre_ven:
            valid, msg = DetalleFacturaCRUD.validar_detalle_factura(num_fac, cod_pro, can_ven or 1, pre_ven or 1.0)
            if not valid:
                return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if can_ven:
                campos.append("CAN_VEN = %s")
                valores.append(can_ven)
            if pre_ven:
                campos.append("PRE_VEN = %s")
                valores.append(pre_ven)

            if campos:
                query = f"UPDATE DETALLE_FACTURA SET {', '.join(campos)} WHERE NUM_FAC = %s AND COD_PRO = %s"
                valores.extend([num_fac, cod_pro])
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Detalle de factura actualizado correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."
        except Exception as error:
            return False, f"Error al actualizar detalle de factura: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_detalle_factura(num_fac, cod_pro):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM DETALLE_FACTURA WHERE NUM_FAC = %s AND COD_PRO = %s", (num_fac, cod_pro))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Detalle de factura eliminado correctamente."
            else:
                return False, "Detalle de factura no encontrado."
        except Exception as error:
            return False, f"Error al eliminar detalle de factura: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
