from database_connection import DatabaseConnection

class DetalleCompraCRUD:
    @staticmethod
    def menu_crud_detalle_compra():
        while True:
            print("\n--- Menú CRUD Detalle Compra ---")
            print("1. Listar Detalles de Compra")
            print("2. Insertar Detalle de Compra")
            print("3. Actualizar Detalle de Compra")
            print("4. Eliminar Detalle de Compra")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                DetalleCompraCRUD.listar_detalles_compra()
            elif opcion == "2":
                DetalleCompraCRUD.insertar_detalle_compra()
            elif opcion == "3":
                DetalleCompraCRUD.actualizar_detalle_compra()
            elif opcion == "4":
                DetalleCompraCRUD.eliminar_detalle_compra()
            elif opcion == "5":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    @staticmethod
    def listar_detalles_compra():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DETALLE_COMPRA")
            detalles = cursor.fetchall()
            print("\n--- Lista de detalles de compra ---")
            for detalle in detalles:
                print(detalle)
            conexion.close()

    @staticmethod
    def insertar_detalle_compra():
        num_oco = input("Número de orden de compra: ")
        cod_pro = input("Código del producto: ")
        can_det = input("Cantidad del detalle: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO DETALLE_COMPRA (NUM_OCO, COD_PRO, CAN_DET)
                    VALUES (%s, %s, %s)
                """
                valores = (num_oco, cod_pro, can_det)
                cursor.execute(sql, valores)
                conexion.commit()
                print("Detalle de compra insertado correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_detalle_compra():
        num_oco = input("Número de orden de compra del detalle que desea actualizar: ")
        cod_pro = input("Código del producto del detalle que desea actualizar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DETALLE_COMPRA WHERE NUM_OCO = %s AND COD_PRO = %s", (num_oco, cod_pro))
            detalle = cursor.fetchone()

            if detalle:
                print("Deja en blanco si no deseas cambiar un valor.")
                can_det = input(f"Cantidad del detalle [{detalle[2]}]: ") or detalle[2]

                try:
                    sql = """
                        UPDATE DETALLE_COMPRA
                        SET CAN_DET = %s
                        WHERE NUM_OCO = %s AND COD_PRO = %s
                    """
                    valores = (can_det, num_oco, cod_pro)
                    cursor.execute(sql, valores)
                    conexion.commit()
                    print("Detalle de compra actualizado correctamente.")
                except Exception as e:
                    print(f"Error al actualizar: {e}")
            else:
                print("Detalle de compra no encontrado.")
            conexion.close()

    @staticmethod
    def eliminar_detalle_compra():
        num_oco = input("Número de orden de compra del detalle que desea eliminar: ")
        cod_pro = input("Código del producto del detalle que desea eliminar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM DETALLE_COMPRA WHERE NUM_OCO = %s AND COD_PRO = %s", (num_oco, cod_pro))
                conexion.commit()
                if cursor.rowcount > 0:
                    print("Detalle de compra eliminado correctamente.")
                else:
                    print("Detalle de compra no encontrado.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conexion.close()
