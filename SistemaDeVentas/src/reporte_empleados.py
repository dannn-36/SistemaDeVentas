from database_connection import DatabaseConnection

def obtener_vendedores_menos_ventas(limit=None):
    conn = DatabaseConnection.conexionBaseDeDatos()
    cursor = conn.cursor()
    query = "SELECT COD_VEN, NOMBRE_COMPLETO, TOTAL_VENTAS FROM VENDEDORES_MENOS_VENTAS"
    if limit is not None:
        query += " LIMIT %s"
        cursor.execute(query, (limit,))
    else:
        cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados
