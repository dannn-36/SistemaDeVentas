import mysql.connector
from database.database_connection import DatabaseConnection

class VendedorCRUD:
    @staticmethod
    def menu_crud_vendedores():
        while True:
            print("\n--- CRUD de Vendedores ---")
            print("1. Agregar vendedor")
            print("2. Mostrar vendedores")
            print("3. Actualizar vendedor")
            print("4. Eliminar vendedor")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                VendedorCRUD.agregar_vendedor()
            elif opcion == "2":
                VendedorCRUD.mostrar_vendedores()
            elif opcion == "3":
                VendedorCRUD.actualizar_vendedor()
            elif opcion == "4":
                VendedorCRUD.eliminar_vendedor()
            elif opcion == "5":
                break
            else:
                print("Opción inválida.")

    @staticmethod
    def agregar_vendedor():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            cod_ven = input("Código del vendedor: ")
            nom_ven = input("Nombre del vendedor: ")
            ape_ven = input("Apellido del vendedor: ")
            sue_ven = float(input("Sueldo: "))
            fin_ven = input("Fecha de ingreso (YYYY-MM-DD): ")
            tip_ven = input("Tipo de vendedor: ")
            cod_dis = input("Código del distrito: ")

            query = "INSERT INTO VENDEDOR (COD_VEN, NOM_VEN, APE_VEN, SUE_VEN, FIN_VEN, TIP_VEN, COD_DIS) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (cod_ven, nom_ven, ape_ven, sue_ven, fin_ven, tip_ven, cod_dis)

            cursor.execute(query, values)
            conexion.commit()
            print("Vendedor agregado exitosamente.")

        except mysql.connector.Error as error:
            print(f"Error al agregar vendedor: {error}")
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
            for v in vendedores:
                print(v)
        except mysql.connector.Error as error:
            print(f"Error al mostrar vendedores: {error}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_vendedor():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()

            cod_ven = input("Código del vendedor a actualizar: ")

            print("Deje vacío cualquier campo que no desea actualizar.")
            nom_ven = input("Nuevo nombre: ")
            ape_ven = input("Nuevo apellido: ")
            sue_ven = input("Nuevo sueldo: ")
            fin_ven = input("Nueva fecha de ingreso (YYYY-MM-DD): ")
            tip_ven = input("Nuevo tipo de vendedor: ")
            cod_dis = input("Nuevo código de distrito: ")

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
                print("Vendedor actualizado correctamente.")
            else:
                print("No se proporcionaron campos para actualizar.")

        except mysql.connector.Error as error:
            print(f"Error al actualizar vendedor: {error}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_vendedor():
        try:
            conexion = DatabaseConnection.conexionBaseDeDatos()
            cursor = conexion.cursor()
            cod_ven = input("Código del vendedor a eliminar: ")
            cursor.execute("DELETE FROM VENDEDOR WHERE COD_VEN = %s", (cod_ven,))
            conexion.commit()
            print("Vendedor eliminado correctamente.")
        except mysql.connector.Error as error:
            print(f"Error al eliminar vendedor: {error}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
