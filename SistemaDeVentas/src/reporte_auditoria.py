from database_connection import DatabaseConnection

def obtener_vendedores_menos_ventas(limit=None):
    conn = DatabaseConnection.conexionBaseDeDatos()
    cursor = conn.cursor()
    query = "SELECT ID_AUD, USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE TABLA FROM AUDITORIA"
    if limit is not None:
        query += " LIMIT %s"
        cursor.execute(query, (limit,))
    else:
        cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados
