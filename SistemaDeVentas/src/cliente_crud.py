import mysql.connector
from database_connection import DatabaseConnection

class ClienteCRUD:
    @staticmethod
    def agregar_cliente(cod_cli, rso_cli, dir_cli, tlf_cli, ruc_cli, cod_dis, fec_reg, tip_cli, con_cli):
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            query = """
                INSERT INTO CLIENTE (COD_CLI, RSO_CLI, DIR_CLI, TLF_CLI, RUC_CLI, COD_DIS, FEC_REG, TIP_CLI, CON_CLI)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (cod_cli, rso_cli, dir_cli, tlf_cli, ruc_cli, cod_dis, fec_reg, tip_cli, con_cli)

            cursor.execute(query, values)
            conexion.commit()
            return True, "Cliente agregado exitosamente."

        except mysql.connector.Error as error:
            return False, f"Error al agregar cliente: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def mostrar_clientes():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM CLIENTE")
            clientes = cursor.fetchall()
            return clientes
        except mysql.connector.Error as error:
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_cliente(cod_cli, rso_cli=None, dir_cli=None, tlf_cli=None, ruc_cli=None, cod_dis=None, fec_reg=None, tip_cli=None, con_cli=None):
        try:
            if not cod_cli or not cod_cli.startswith("C") or not cod_cli[1:].isdigit():
                raise ValueError("Código de cliente inválido. Debe comenzar con 'C' seguido de números (ej: C01).")
            if rso_cli and not rso_cli.strip():
                raise ValueError("La razón social no puede estar vacía.")
            if dir_cli and not dir_cli.strip():
                raise ValueError("La dirección no puede estar vacía.")
            if tlf_cli and not tlf_cli.isdigit():
                raise ValueError("El teléfono debe contener solo números.")
            if ruc_cli and not ruc_cli.isdigit():
                raise ValueError("El RUC debe contener solo números si se proporciona.")
            if cod_dis and (not cod_dis.startswith("D") or not cod_dis[1:].isdigit()):
                raise ValueError("Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01).")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            campos = []
            valores = []

            if rso_cli:
                campos.append("RSO_CLI = %s")
                valores.append(rso_cli)
            if dir_cli:
                campos.append("DIR_CLI = %s")
                valores.append(dir_cli)
            if tlf_cli:
                campos.append("TLF_CLI = %s")
                valores.append(tlf_cli)
            if ruc_cli:
                campos.append("RUC_CLI = %s")
                valores.append(ruc_cli)
            if cod_dis:
                campos.append("COD_DIS = %s")
                valores.append(cod_dis)
            if fec_reg:
                campos.append("FEC_REG = %s")
                valores.append(fec_reg)
            if tip_cli:
                campos.append("TIP_CLI = %s")
                valores.append(tip_cli)
            if con_cli:
                campos.append("CON_CLI = %s")
                valores.append(con_cli)

            if campos:
                query = f"UPDATE CLIENTE SET {', '.join(campos)} WHERE COD_CLI = %s"
                valores.append(cod_cli)
                cursor.execute(query, valores)
                conexion.commit()
                return True, "Cliente actualizado correctamente."
            else:
                return False, "No se proporcionaron campos para actualizar."

        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al actualizar cliente: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_cliente(cod_cli):
        try:
            if not cod_cli or not cod_cli.startswith("C") or not cod_cli[1:].isdigit():
                raise ValueError("Código de cliente inválido. Debe comenzar con 'C' seguido de números (ej: C01).")

            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM CLIENTE WHERE COD_CLI = %s", (cod_cli,))
            conexion.commit()
            return True, "Cliente eliminado correctamente."
        except ValueError as ve:
            return False, str(ve)
        except mysql.connector.Error as error:
            return False, f"Error al eliminar cliente: {error}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
