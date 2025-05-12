from database_connection import DatabaseConnection

class DistritoCRUD:
    @staticmethod
    def menu_crud_distritos():
        while True:
            print("\n--- Menú CRUD Distrito ---")
            print("1. Listar Distritos")
            print("2. Insertar Distrito")
            print("3. Actualizar Distrito")
            print("4. Eliminar Distrito")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                DistritoCRUD.listar_distritos()
            elif opcion == "2":
                DistritoCRUD.insertar_distrito()
            elif opcion == "3":
                DistritoCRUD.actualizar_distrito()
            elif opcion == "4":
                DistritoCRUD.eliminar_distrito()
            elif opcion == "5":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")


    @staticmethod
    def listar_distritos():
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DISTRITO")
            distritos = cursor.fetchall()
            print("\n--- Lista de distritos ---")
            for dist in distritos:
                print(dist)
            conexion.close()


    @staticmethod
    def insertar_distrito():
        cod_dis = input("Código del distrito ")
        nom_dis = input("Nombre del distrito: ")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO DISTRITO (COD_DIS, NOM_DIS)
                    VALUES(%s, %s)
                """
                valores = (cod_dis, nom_dis)
                cursor.execute(sql, valores)
                conexion.commit()
                print("distrito insertado correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")
            finally:
                conexion.close()

    @staticmethod
    def actualizar_distrito():
        cod_dis = input("Código del distrito que desea actualizar")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM DISTRITO WHERE COD_DIS = %s",(cod_dis))
            distrito = cursor.fetchone()

            if distrito:
                print("Deja en blanco si no deseas cambiar un valor.")
                nom_dis = input(f"nombre del distrito [{distrito[1]}]") or distrito[1]
                
                try:
                    sql= """
                        UPDATE DISTRITO SET NOM_DIS = %s
                    """
                    valores = (nom_dis)
                    cursor.execute(sql, valores)
                    conexion.commit()
                    print("distrito actualizado correctamente")
                except Exception as e:
                    print(f"Error al acutalizar: {e}")
            else:
                print("Distrito no encontrado")
            conexion.close()
    
    @staticmethod
    def eliminar_distrito():
        cod_dis = input("Código del distrito que desea eliminar")
        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM DISTRITO WHERE COD_DIS = %s", (cod_dis,))
                conexion.commit()
                if cursor.rowcount > 0:
                    print("Distrito eliminado correctamente.")
                else:
                    print("Distrito no encontrado.")
            except Exception as e:
                print(f"Error al eliminar: {e}")
            finally:
                conexion.close()

