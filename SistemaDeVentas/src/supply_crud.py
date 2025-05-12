from database_connection import DatabaseConnection

class AbastecimientoCRUD:
    @staticmethod
    def menu_crud_abastecimiento():
        while True:
            print("\n--- Menú CRUD Abastecimiento ---")
            print("1. Listar Abastecimientos")
            print("2. Insertar Abastecimiento")
            print("3. Actualizar Abastecimiento")
            print("4. Eliminar Abastecimiento")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                AbastecimientoCRUD.listar_abastecimientos()
            elif opcion == "2":
                AbastecimientoCRUD.insertar_abastecimiento()
            elif opcion == "3":
                AbastecimientoCRUD.actualizar_abastecimiento()
            elif opcion == "4":
                AbastecimientoCRUD.eliminar_abastecimiento()
            elif opcion == "5":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    @staticmethod
    def listar_abastecimientos():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ABASTECIMIENTO")
            abastecimientos = cursor.fetchall()
            print("\n--- Lista de abastecimientos ---")
            for abastecimiento in abastecimientos:
                print(abastecimiento)
            conexion.close()

    @staticmethod
    def insertar_abastecimiento():
        cod_prv = input("Código del proveedor: ")
        cod_pro = input("Código del producto: ")
        pre_aba = input("Precio de abastecimiento: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO ABASTECIMIENTO (COD_PRV, COD_PRO, PRE_ABA)
                    VALUES (%s, %s, %s)
                """
                valores = (cod_prv, cod_pro, pre_aba)
                cursor.execute(sql, valores)
                conexion.commit()
                print("Abastecimiento insertado correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_abastecimiento():
        cod_prv = input("Código del proveedor del abastecimiento que desea actualizar: ")
        cod_pro = input("Código del producto del abastecimiento que desea actualizar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ABASTECIMIENTO WHERE COD_PRV = %s AND COD_PRO = %s", (cod_prv, cod_pro))
            abastecimiento = cursor.fetchone()

            if abastecimiento:
                print("Deja en blanco si no deseas cambiar un valor.")
                pre_aba = input(f"Precio de abastecimiento [{abastecimiento[2]}]: ") or abastecimiento[2]

                try:
                    sql = """
                        UPDATE ABASTECIMIENTO
                        SET PRE_ABA = %s
                        WHERE COD_PRV = %s AND COD_PRO = %s
                    """
                    valores = (pre_aba, cod_prv, cod_pro)
                    cursor.execute(sql, valores)
                    conexion.commit()
                    print("Abastecimiento actualizado correctamente.")
                except Exception as e:
                    print(f"Error al actualizar: {e}")
            else:
                print("Abastecimiento no encontrado.")
            conexion.close()

    @staticmethod
    def eliminar_abastecimiento():
        cod_prv = input("Código del proveedor del abastecimiento que desea eliminar: ")
        cod_pro = input("Código del producto del abastecimiento que desea eliminar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM ABASTECIMIENTO WHERE COD_PRV = %s AND COD_PRO = %s", (cod_prv, cod_pro))
                conexion.commit()
                if cursor.rowcount > 0:
                    print("Abastecimiento eliminado correctamente.")
                else:
                    print("Abastecimiento no encontrado.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conexion.close()
