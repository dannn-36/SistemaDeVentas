from database_connection import DatabaseConnection

class DetalleFacturaCRUD:
    @staticmethod
    def menu_crud_detalle_factura():
        while True:
            print("\n--- Menú CRUD Detalle Factura ---")
            print("1. Listar Detalles de Factura")
            print("2. Insertar Detalle de Factura")
            print("3. Actualizar Detalle de Factura")
            print("4. Eliminar Detalle de Factura")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                DetalleFacturaCRUD.listar_detalles_factura()
            elif opcion == "2":
                DetalleFacturaCRUD.insertar_detalle_factura()
            elif opcion == "3":
                DetalleFacturaCRUD.actualizar_detalle_factura()
            elif opcion == "4":
                DetalleFacturaCRUD.eliminar_detalle_factura()
            elif opcion == "5":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")


    @staticmethod
    def listar_detalles_factura():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DETALLE_FACTURA")
            detalles = cursor.fetchall()
            print("\n--- Lista de detalles de factura ---")
            for detalle in detalles:
                print(detalle)
            conexion.close()

    @staticmethod
    def insertar_detalle_factura():
        num_fac = input("Número de factura: ")
        cod_pro = input("Código del producto: ")
        can_ven = input("Cantidad vendida: ")
        pre_ven = input("Precio de venta: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO DETALLE_FACTURA (NUM_FAC, COD_PRO, CAN_VEN, PRE_VEN)
                    VALUES (%s, %s, %s, %s)
                """
                valores = (num_fac, cod_pro, can_ven, pre_ven)
                cursor.execute(sql, valores)
                conexion.commit()
                print("Detalle de factura insertado correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_detalle_factura():
        num_fac = input("Número de factura del detalle que desea actualizar: ")
        cod_pro = input("Código del producto del detalle que desea actualizar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DETALLE_FACTURA WHERE NUM_FAC = %s AND COD_PRO = %s", (num_fac, cod_pro))
            detalle = cursor.fetchone()

            if detalle:
                print("Deja en blanco si no deseas cambiar un valor.")
                can_ven = input(f"Cantidad vendida [{detalle[2]}]: ") or detalle[2]
                pre_ven = input(f"Precio de venta [{detalle[3]}]: ") or detalle[3]

                try:
                    sql = """
                        UPDATE DETALLE_FACTURA
                        SET CAN_VEN = %s, PRE_VEN = %s
                        WHERE NUM_FAC = %s AND COD_PRO = %s
                    """
                    valores = (can_ven, pre_ven, num_fac, cod_pro)
                    cursor.execute(sql, valores)
                    conexion.commit()
                    print("Detalle de factura actualizado correctamente.")
                except Exception as e:
                    print(f"Error al actualizar: {e}")
            else:
                print("Detalle de factura no encontrado.")
            conexion.close()

    @staticmethod
    def eliminar_detalle_factura():
        num_fac = input("Número de factura del detalle que desea eliminar: ")
        cod_pro = input("Código del producto del detalle que desea eliminar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM DETALLE_FACTURA WHERE NUM_FAC = %s AND COD_PRO = %s", (num_fac, cod_pro))
                conexion.commit()
                if cursor.rowcount > 0:
                    print("Detalle de factura eliminado correctamente.")
                else:
                    print("Detalle de factura no encontrado.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conexion.close()
