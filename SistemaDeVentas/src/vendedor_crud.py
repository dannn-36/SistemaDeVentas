import mysql.connector
from database_connection import DatabaseConnection

class VendedorCRUD:
    @staticmethod
    def agregar_vendedor(cod_ven, nom_ven, ape_ven, sue_ven, fin_ven, tip_ven, cod_dis):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            query = "INSERT INTO VENDEDOR (COD_VEN, NOM_VEN, APE_VEN, SUE_VEN, FIN_VEN, TIP_VEN, COD_DIS) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (cod_ven, nom_ven, ape_ven, sue_ven, fin_ven, tip_ven, cod_dis)

            cursor.execute(query, values)
            conexion.commit()
            return True, "Vendedor agregado exitosamente."

        except mysql.connector.Error as error:
            return False, f"Error al agregar vendedor: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def mostrar_vendedores():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM VENDEDOR")
            vendedores = cursor.fetchall()
            return vendedores
        except mysql.connector.Error as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_vendedor(cod_ven, nom_ven=None, ape_ven=None, sue_ven=None, fin_ven=None, tip_ven=None, cod_dis=None):
        try:
            if not cod_ven or not cod_ven.startswith("V") or not cod_ven[1:].isdigit():
                raise ValueError("Código de vendedor inválido. Debe comenzar con 'V' seguido de números (ej: V01).")
            if nom_ven and any(char.isdigit() for char in nom_ven):
                raise ValueError("El nombre no debe contener números.")
            if ape_ven and any(char.isdigit() for char in ape_ven):
                raise ValueError("El apellido no debe contener números.")
            if sue_ven and (not sue_ven.isdigit() or "." in sue_ven or "," in sue_ven):
                raise ValueError("El sueldo debe contener solo números sin puntos ni comas.")
            if tip_ven and not tip_ven.isdigit():
                raise ValueError("El tipo de vendedor debe contener solo números.")
            if cod_dis and (not cod_dis.startswith("D") or not cod_dis[1:].isdigit()):
                raise ValueError("Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01).")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if nom_ven:
                campos.append("NOM_VEN = %s")
                valores.append(nom_ven)
            if ape_ven:
                campos.append("APE_VEN = %s")
                valores.append(ape_ven)
            if sue_ven:
                campos.append("SUE_VEN = %s")
                valores.append(float(sue_ven))
            if fin_ven:
                campos.append("FIN_VEN = %s")
                valores.append(fin_ven)
            if tip_ven:
                campos.append("TIP_VEN = %s")
                valores.append(tip_ven)
            if cod_dis:
                campos.append("COD_DIS = %s")
                valores.append(cod_dis)

            if campos:
                query = f"UPDATE VENDEDOR SET {', '.join(campos)} WHERE COD_VEN = %s"
                valores.append(cod_ven)
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Vendedor actualizado correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al actualizar vendedor: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_vendedor(cod_ven):
        try:
            if not cod_ven or not cod_ven.startswith("V") or not cod_ven[1:].isdigit():
                raise ValueError("Código de vendedor inválido. Debe comenzar con 'V' seguido de números (ej: V01).")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM VENDEDOR WHERE COD_VEN = %s", (cod_ven,))
            conexion.commit()
            return True, "Vendedor eliminado correctamente."
        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al eliminar vendedor: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def obtener_distritos():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            query = "SELECT COD_DIS FROM distrito"
            cursor.execute(query)
            # Ensure the result is a list of strings
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as ex:
            print(f"Error al obtener distritos: {ex}")
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
