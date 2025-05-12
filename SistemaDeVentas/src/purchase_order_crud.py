from database_connection import DatabaseConnection

class OrdenCompraCRUD:
    @staticmethod
    def menu_crud_ordenes_compra():
        while True:
            print("\n--- Menú CRUD Orden de Compra ---")
            print("1. Listar Órdenes de Compra")
            print("2. Insertar Orden de Compra")
            print("3. Actualizar Orden de Compra")
            print("4. Eliminar Orden de Compra")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                OrdenCompraCRUD.listar_ordenes_compra()
            elif opcion == "2":
                OrdenCompraCRUD.insertar_orden_compra()
            elif opcion == "3":
                OrdenCompraCRUD.actualizar_orden_compra()
            elif opcion == "4":
                OrdenCompraCRUD.eliminar_orden_compra()
            elif opcion == "5":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    @staticmethod
    def listar_ordenes_compra():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ORDEN_COMPRA")
            ordenes = cursor.fetchall()
            print("\n--- Lista de órdenes de compra ---")
            for orden in ordenes:
                print(orden)
            conexion.close()

    @staticmethod
    def insertar_orden_compra():
        num_oc = input("Número de orden de compra: ")
        fec_oc = input("Fecha de orden de compra (YYYY-MM-DD): ")
        cod_pr = input("Código del proveedor: ")
        fec_ent = input("Fecha de entrega (YYYY-MM-DD): ")
        est_oc = input("Estado de la orden de compra: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO ORDEN_COMPRA (NUM_OC, FEC_OC, COD_PR, FEC_ENT, EST_OC)
                    VALUES (%s, %s, %s, %s, %s)
                """
                valores = (num_oc, fec_oc, cod_pr, fec_ent, est_oc)
                cursor.execute(sql, valores)
                conexion.commit()
                print("Orden de compra insertada correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_orden_compra():
        num_oc = input("Número de orden de compra que desea actualizar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ORDEN_COMPRA WHERE NUM_OC = %s", (num_oc,))
            orden = cursor.fetchone()

            if orden:
                print("Deja en blanco si no deseas cambiar un valor.")
                fec_oc = input(f"Fecha de orden de compra [{orden[1]}]: ") or orden[1]
                cod_pr = input(f"Código del proveedor [{orden[2]}]: ") or orden[2]
                fec_ent = input(f"Fecha de entrega [{orden[3]}]: ") or orden[3]
                est_oc = input(f"Estado de la orden de compra [{orden[4]}]: ") or orden[4]

                try:
                    sql = """
                        UPDATE ORDEN_COMPRA
                        SET FEC_OC = %s, COD_PR = %s, FEC_ENT = %s, EST_OC = %s
                        WHERE NUM_OC = %s
                    """
                    valores = (fec_oc, cod_pr, fec_ent, est_oc, num_oc)
                    cursor.execute(sql, valores)
                    conexion.commit()
                    print("Orden de compra actualizada correctamente.")
                except Exception as e:
                    print(f"Error al actualizar: {e}")
            else:
                print("Orden de compra no encontrada.")
            conexion.close()

    @staticmethod
    def eliminar_orden_compra():
        num_oc = input("Número de orden de compra que desea eliminar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM ORDEN_COMPRA WHERE NUM_OC = %s", (num_oc,))
                conexion.commit()
                if cursor.rowcount > 0:
                    print("Orden de compra eliminada correctamente.")
                else:
                    print("Orden de compra no encontrada.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conexion.close()
