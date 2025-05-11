from database_connection import DatabaseConnection

class ClienteCRUD:
    @staticmethod
    def menu_crud_clientes():
        while True:
            print("\n--- Menú CRUD de Clientes ---")
            print("1. Crear Cliente")
            print("2. Leer Clientes")
            print("3. Actualizar Cliente")
            print("4. Eliminar Cliente")
            print("5. Volver al Menú Principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                cod_cli = input("Ingrese el código del cliente: ")
                rso_cli = input("Ingrese la razón social: ")
                dir_cli = input("Ingrese la dirección: ")
                tlf_cli = input("Ingrese el teléfono: ")
                ruc_cli = input("Ingrese el RUC: ")
                cod_dis = input("Ingrese el código del distrito: ")
                fec_reg = input("Ingrese la fecha de registro (YYYY-MM-DD): ")
                tip_cli = input("Ingrese el tipo de cliente: ")
                con_cli = input("Ingrese la condición del cliente: ")
                ClienteCRUD.crear_cliente(cod_cli, rso_cli, dir_cli, tlf_cli, ruc_cli, cod_dis, fec_reg, tip_cli, con_cli)

            elif opcion == "2":
                ClienteCRUD.leer_clientes()

            elif opcion == "3":
                cod_cli = input("Ingrese el código del cliente a actualizar: ")
                rso_cli = input("Ingrese la nueva razón social (o presione Enter para omitir): ")
                dir_cli = input("Ingrese la nueva dirección (o presione Enter para omitir): ")
                tlf_cli = input("Ingrese el nuevo teléfono (o presione Enter para omitir): ")
                ruc_cli = input("Ingrese el nuevo RUC (o presione Enter para omitir): ")
                cod_dis = input("Ingrese el nuevo código del distrito (o presione Enter para omitir): ")
                fec_reg = input("Ingrese la nueva fecha de registro (YYYY-MM-DD) (o presione Enter para omitir): ")
                tip_cli = input("Ingrese el nuevo tipo de cliente (o presione Enter para omitir): ")
                con_cli = input("Ingrese la nueva condición del cliente (o presione Enter para omitir): ")
                ClienteCRUD.actualizar_cliente(cod_cli, rso_cli, dir_cli, tlf_cli, ruc_cli, cod_dis, fec_reg, tip_cli, con_cli)

            elif opcion == "4":
                cod_cli = input("Ingrese el código del cliente a eliminar: ")
                ClienteCRUD.eliminar_cliente(cod_cli)

            elif opcion == "5":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    @staticmethod
    def crear_cliente(cod_cli, rso_cli, dir_cli, tlf_cli, ruc_cli, cod_dis, fec_reg, tip_cli, con_cli):
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    INSERT INTO cliente (COD_CLI, RSO_CLI, DIR_CLI, TLF_CLI, RUC_CLI, COD_DIS, FEC_REG, TIP_CLI, CON_CLI)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (cod_cli, rso_cli, dir_cli, tlf_cli, ruc_cli, cod_dis, fec_reg, tip_cli, con_cli))
                conexion.commit()
                print("Cliente creado exitosamente.")
            except Exception as e:
                print(f"Error al crear cliente: {e}")
            finally:
                conexion.close()

    @staticmethod
    def leer_clientes():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT * FROM cliente"
                cursor.execute(query)
                resultados = cursor.fetchall()
                for cliente in resultados:
                    print(cliente)
            except Exception as e:
                print(f"Error al leer clientes: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_cliente(cod_cli, rso_cli=None, dir_cli=None, tlf_cli=None, ruc_cli=None, cod_dis=None, fec_reg=None, tip_cli=None, con_cli=None):
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                fields = []
                values = []

                if rso_cli:
                    fields.append("RSO_CLI = %s")
                    values.append(rso_cli)
                if dir_cli:
                    fields.append("DIR_CLI = %s")
                    values.append(dir_cli)
                if tlf_cli:
                    fields.append("TLF_CLI = %s")
                    values.append(tlf_cli)
                if ruc_cli:
                    fields.append("RUC_CLI = %s")
                    values.append(ruc_cli)
                if cod_dis:
                    fields.append("COD_DIS = %s")
                    values.append(cod_dis)
                if fec_reg:
                    fields.append("FEC_REG = %s")
                    values.append(fec_reg)
                if tip_cli:
                    fields.append("TIP_CLI = %s")
                    values.append(tip_cli)
                if con_cli:
                    fields.append("CON_CLI = %s")
                    values.append(con_cli)

                if fields:
                    query = f"UPDATE cliente SET {', '.join(fields)} WHERE COD_CLI = %s"
                    values.append(cod_cli)
                    cursor.execute(query, tuple(values))
                    conexion.commit()
                    print("Cliente actualizado exitosamente.")
                else:
                    print("No se proporcionaron datos para actualizar.")
            except Exception as e:
                print(f"Error al actualizar cliente: {e}")
            finally:
                conexion.close()

    @staticmethod
    def eliminar_cliente(cod_cli):
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "DELETE FROM cliente WHERE COD_CLI = %s"
                cursor.execute(query, (cod_cli,))
                conexion.commit()
                print("Cliente eliminado exitosamente.")
            except Exception as e:
                print(f"Error al eliminar cliente: {e}")
            finally:
                conexion.close()