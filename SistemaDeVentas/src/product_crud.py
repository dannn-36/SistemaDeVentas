from SistemaDeVentas.src.database_connection import DatabaseConnection

class ProductoCRUD:
    @staticmethod
    def menu_crud_productos():
        while True:
            print("\n--- Menú CRUD de Productos ---")
            print("1. Crear Producto")
            print("2. Leer Productos")
            print("3. Actualizar Producto")
            print("4. Eliminar Producto")
            print("5. Volver al Menú Principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                cod_pro = input("Código del producto: ")
                des_pro = input("Descripción: ")
                pre_pro = float(input("Precio: "))
                sac_pro = int(input("Stock actual: "))
                smi_pro = int(input("Stock mínimo: "))
                uni_pro = input("Unidad: ")
                lin_pro = input("Línea: ")
                imp_pro = input("Impuesto (ej. IGV): ")
                ProductoCRUD.crear_producto(cod_pro, des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro)

            elif opcion == "2":
                ProductoCRUD.leer_productos()

            elif opcion == "3":
                cod_pro = input("Código del producto a actualizar: ")
                print("Ingrese los nuevos valores:")
                des_pro = input("Descripción: ")
                pre_pro = float(input("Precio: "))
                sac_pro = int(input("Stock actual: "))
                smi_pro = int(input("Stock mínimo: "))
                uni_pro = input("Unidad: ")
                lin_pro = input("Línea: ")
                imp_pro = input("Impuesto: ")
                ProductoCRUD.actualizar_producto(cod_pro, des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro)

            elif opcion == "4":
                cod_pro = input("Código del producto a eliminar: ")
                ProductoCRUD.eliminar_producto(cod_pro)

            elif opcion == "5":
                break
            else:
                print("Opción inválida.")

    @staticmethod
    def crear_producto(cod_pro, des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro):
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    INSERT INTO producto (COD_PRO, DES_PRO, PRE_PRO, SAC_PRO, SMI_PRO, UNI_PRO, LIN_PRO, IMP_PRO)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (cod_pro, des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro))
                conexion.commit()
                print("Producto creado exitosamente.")
            except Exception as e:
                print(f"Error al crear producto: {e}")
            finally:
                conexion.close()

    @staticmethod
    def leer_productos():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM producto")
                for producto in cursor.fetchall():
                    print(producto)
            except Exception as e:
                print(f"Error al leer productos: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_producto(cod_pro, des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro):
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    UPDATE producto
                    SET DES_PRO=%s, PRE_PRO=%s, SAC_PRO=%s, SMI_PRO=%s,
                        UNI_PRO=%s, LIN_PRO=%s, IMP_PRO=%s
                    WHERE COD_PRO=%s
                """
                cursor.execute(query, (des_pro, pre_pro, sac_pro, smi_pro, uni_pro, lin_pro, imp_pro, cod_pro))
                conexion.commit()
                print("Producto actualizado exitosamente.")
            except Exception as e:
                print(f"Error al actualizar producto: {e}")
            finally:
                conexion.close()

    @staticmethod
    def eliminar_producto(cod_pro):
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM producto WHERE COD_PRO = %s", (cod_pro,))
                conexion.commit()
                print("Producto eliminado exitosamente.")
            except Exception as e:
                print(f"Error al eliminar producto: {e}")
            finally:
                conexion.close()
