from database_connection import DatabaseConnection

class FacturaCRUD:
    @staticmethod
    def menu_crud_facturas():
        while True:
            print("\n--- Menú CRUD Factura ---")
            print("1. Listar Facturas")
            print("2. Insertar Factura")
            print("3. Actualizar Factura")
            print("4. Eliminar Factura")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                FacturaCRUD.listar_facturas()
            elif opcion == "2":
                FacturaCRUD.insertar_factura()
            elif opcion == "3":
                FacturaCRUD.actualizar_factura()
            elif opcion == "4":
                FacturaCRUD.eliminar_factura()
            elif opcion == "5":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    @staticmethod
    def listar_facturas():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM FACTURA")
            facturas = cursor.fetchall()
            print("\n--- Lista de facturas ---")
            for factura in facturas:
                print(factura)
            conexion.close()

    @staticmethod
    def insertar_factura():
        num_fac = input("Número de factura: ")
        fec_fac = input("Fecha de factura (YYYY-MM-DD): ")
        cod_cli = input("Código del cliente: ")
        fec_can = input("Fecha de cancelación (YYYY-MM-DD): ")
        est_fac = input("Estado de la factura: ")
        cod_ven = input("Código del vendedor: ")
        por_igv = input("Porcentaje de IGV: ")

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO FACTURA (NUM_FAC, FEC_FAC, COD_CLI, FEC_CAN, EST_FAC, COD_VEN, POR_IGV)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                valores = (num_fac, fec_fac, cod_cli, fec_can, est_fac, cod_ven, por_igv)
                cursor.execute(sql, valores)
                conexion.commit()
                print("Factura insertada correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_factura():
        num_fac = input("Número de factura que desea actualizar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM FACTURA WHERE NUM_FAC = %s", (num_fac,))
            factura = cursor.fetchone()

            if factura:
                print("Deja en blanco si no deseas cambiar un valor.")
                fec_fac = input(f"Fecha de factura [{factura[1]}]: ") or factura[1]
                cod_cli = input(f"Código del cliente [{factura[2]}]: ") or factura[2]
                fec_can = input(f"Fecha de cancelación [{factura[3]}]: ") or factura[3]
                est_fac = input(f"Estado de la factura [{factura[4]}]: ") or factura[4]
                cod_ven = input(f"Código del vendedor [{factura[5]}]: ") or factura[5]
                por_igv = input(f"Porcentaje de IGV [{factura[6]}]: ") or factura[6]

                try:
                    sql = """
                        UPDATE FACTURA
                        SET FEC_FAC = %s, COD_CLI = %s, FEC_CAN = %s, EST_FAC = %s, COD_VEN = %s, POR_IGV = %s
                        WHERE NUM_FAC = %s
                    """
                    valores = (fec_fac, cod_cli, fec_can, est_fac, cod_ven, por_igv, num_fac)
                    cursor.execute(sql, valores)
                    conexion.commit()
                    print("Factura actualizada correctamente.")
                except Exception as e:
                    print(f"Error al actualizar: {e}")
            else:
                print("Factura no encontrada.")
            conexion.close()

    @staticmethod
    def eliminar_factura():
        num_fac = input("Número de factura que desea eliminar: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM FACTURA WHERE NUM_FAC = %s", (num_fac,))
                conexion.commit()
                if cursor.rowcount > 0:
                    print("Factura eliminada correctamente.")
                else:
                    print("Factura no encontrada.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conexion.close()
