from SistemaDeVentas.src.database_connection import DatabaseConnection

class ProveedorCRUD:

    @staticmethod
    def menu_crud_proveedores():
        while True:
            print("\n--- Menú CRUD Proveedor ---")
            print("1. Listar Proveedores")
            print("2. Insertar Proveedor")
            print("3. Actualizar Proveedor")
            print("4. Eliminar Proveedor")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                ProveedorCRUD.listar_proveedores()
            elif opcion == "2":
                ProveedorCRUD.insertar_proveedor()
            elif opcion == "3":
                ProveedorCRUD.actualizar_proveedor()
            elif opcion == "4":
                ProveedorCRUD.eliminar_proveedor()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    @staticmethod
    def listar_proveedores():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PROVEEDOR")
            proveedores = cursor.fetchall()
            print("\n--- Lista de Proveedores ---")
            for prov in proveedores:
                print(prov)
            conexion.close()

    @staticmethod
    def insertar_proveedor():
        cod_prv = input("Código del proveedor: ")
        rso_prv = input("Razón social: ")
        dir_prv = input("Dirección: ")
        tel_prv = input("Teléfono: ")
        cod_dis = input("Código de distrito: ")
        rep_pro = input("Representante: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO PROVEEDOR (COD_PRV, RSO_PRV, DIR_PRV, TEL_PRV, COD_DIS, REP_PRO)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (cod_prv, rso_prv, dir_prv, tel_prv, cod_dis, rep_pro)
                cursor.execute(sql, valores)
                conexion.commit()
                print("Proveedor insertado correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_proveedor():
        cod_prv = input("Código del proveedor a actualizar: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PROVEEDOR WHERE COD_PRV = %s", (cod_prv,))
            proveedor = cursor.fetchone()

            if proveedor:
                print("Deja en blanco si no deseas cambiar un valor.")
                rso_prv = input(f"Razón social [{proveedor[1]}]: ") or proveedor[1]
                dir_prv = input(f"Dirección [{proveedor[2]}]: ") or proveedor[2]
                tel_prv = input(f"Teléfono [{proveedor[3]}]: ") or proveedor[3]
                cod_dis = input(f"Código distrito [{proveedor[4]}]: ") or proveedor[4]
                rep_pro = input(f"Representante [{proveedor[5]}]: ") or proveedor[5]

                try:
                    sql = """
                        UPDATE PROVEEDOR SET RSO_PRV = %s, DIR_PRV = %s, TEL_PRV = %s, 
                        COD_DIS = %s, REP_PRO = %s WHERE COD_PRV = %s
                    """
                    valores = (rso_prv, dir_prv, tel_prv, cod_dis, rep_pro, cod_prv)
                    cursor.execute(sql, valores)
                    conexion.commit()
                    print("Proveedor actualizado correctamente.")
                except Exception as e:
                    print(f"Error al actualizar: {e}")
            else:
                print("Proveedor no encontrado.")
            conexion.close()

    @staticmethod
    def eliminar_proveedor():
        cod_prv = input("Código del proveedor a eliminar: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM PROVEEDOR WHERE COD_PRV = %s", (cod_prv,))
                conexion.commit()
                if cursor.rowcount > 0:
                    print("Proveedor eliminado correctamente.")
                else:
                    print("Proveedor no encontrado.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conexion.close()
