from database_connection import DatabaseConnection
import re
from datetime import datetime

class FacturaCRUD:
    @staticmethod
    def validar_factura(num_fac, fec_fac, cod_cli, fec_can, est_fac, cod_ven, por_igv):
        if not re.match(r"^FA\d{3}$", num_fac):
            return False, "Número de factura inválido. Debe tener el formato 'FA' seguido de tres números (ej: FA001)."
        try:
            datetime.strptime(fec_fac, "%Y-%m-%d")
        except ValueError:
            return False, "Fecha de factura inválida. Debe tener el formato YYYY-MM-DD."
        if not re.match(r"^C\d{3}$", cod_cli):
            return False, "Código de cliente inválido. Debe tener el formato 'C' seguido de tres números (ej: C001)."
        try:
            datetime.strptime(fec_can, "%Y-%m-%d")
        except ValueError:
            return False, "Fecha de cancelación inválida. Debe tener el formato YYYY-MM-DD."
        if not est_fac.isdigit() or int(est_fac) not in [1, 2, 3]:
            return False, "Estado de factura inválido. Debe ser un número (1, 2 o 3)."
        if not re.match(r"^V\d{2}$", cod_ven):
            return False, "Código de vendedor inválido. Debe tener el formato 'V' seguido de dos números (ej: V01)."
        if not FacturaCRUD.vendedor_existe(cod_ven):
            return False, "El código de vendedor no existe en la base de datos."
        try:
            por_igv = float(por_igv)
            if por_igv < 0 or por_igv > 1:
                return False, "Porcentaje de IGV inválido. Debe ser un número entre 0 y 1 (ej: 0.19)."
        except ValueError:
            return False, "Porcentaje de IGV inválido. Debe ser un número decimal (ej: 0.19)."
        return True, ""

    @staticmethod
    def vendedor_existe(cod_ven):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM VENDEDOR WHERE COD_VEN = %s", (cod_ven,))
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def listar_facturas():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM FACTURA")
            facturas = cursor.fetchall()
            return facturas
        except Exception as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def insertar_factura(num_fac, fec_fac, cod_cli, fec_can, est_fac, cod_ven, por_igv=0.19):
        valid, msg = FacturaCRUD.validar_factura(num_fac, fec_fac, cod_cli, fec_can, est_fac, cod_ven, por_igv)
        if not valid:
            return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            query = """
                INSERT INTO FACTURA (NUM_FAC, FEC_FAC, COD_CLI, FEC_CAN, EST_FAC, COD_VEN, POR_IGV)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (num_fac, fec_fac, cod_cli, fec_can, est_fac, cod_ven, por_igv)
            cursor.execute(query, valores)
            conexion.commit()
            return True, "Factura insertada correctamente."
        except Exception as error:
            return False, f"Error al insertar factura: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_factura(num_fac, fec_fac=None, cod_cli=None, fec_can=None, est_fac=None, cod_ven=None, por_igv=None):
        if fec_fac or cod_cli or fec_can or est_fac or cod_ven or por_igv:
            valid, msg = FacturaCRUD.validar_factura(num_fac, fec_fac or "2000-01-01", cod_cli or "C001", fec_can or "2000-01-01", est_fac or "1", cod_ven or "V01", por_igv or 0.19)
            if not valid:
                return False, msg
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if fec_fac:
                campos.append("FEC_FAC = %s")
                valores.append(fec_fac)
            if cod_cli:
                campos.append("COD_CLI = %s")
                valores.append(cod_cli)
            if fec_can:
                campos.append("FEC_CAN = %s")
                valores.append(fec_can)
            if est_fac:
                campos.append("EST_FAC = %s")
                valores.append(est_fac)
            if cod_ven:
                campos.append("COD_VEN = %s")
                valores.append(cod_ven)
            if por_igv:
                campos.append("POR_IGV = %s")
                valores.append(por_igv)

            if campos:
                query = f"UPDATE FACTURA SET {', '.join(campos)} WHERE NUM_FAC = %s"
                valores.append(num_fac)
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Factura actualizada correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."
        except Exception as error:
            return False, f"Error al actualizar factura: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_factura(num_fac):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM FACTURA WHERE NUM_FAC = %s", (num_fac,))
            conexion.commit()
            if cursor.rowcount > 0:
                return True, "Factura eliminada correctamente."
            else:
                return False, "Factura no encontrada."
        except Exception as error:
            return False, f"Error al eliminar factura: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
