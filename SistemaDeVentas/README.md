# CRUD Clientes

Este proyecto implementa un sistema de gestión de clientes utilizando operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en una base de datos MySQL.

## Estructura del Proyecto

```
crud-clientes
├── src
│   ├── database_connection.py  # Clase para la conexión a la base de datos
│   ├── client_crud.py          # Implementación de operaciones CRUD para clientes
│   └── models
│       └── client.py           # Modelo de datos para el cliente
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación del proyecto
```

## Requisitos

Asegúrate de tener instalado Python y MySQL en tu sistema. Este proyecto requiere la biblioteca `mysql-connector-python`. Puedes instalarla ejecutando:

```
pip install -r requirements.txt
```

## Uso

1. **Conexión a la Base de Datos**: La clase `DatabaseConnection` en `src/database_connection.py` maneja la conexión a la base de datos. Asegúrate de que los parámetros de conexión (usuario, contraseña, puerto, host y base de datos) sean correctos.

2. **Operaciones CRUD**:
   - **Crear Cliente**: Utiliza la función `create_client` en `src/client_crud.py` para agregar un nuevo cliente a la base de datos.
   - **Leer Cliente**: Usa `read_client` para obtener información de un cliente específico.
   - **Actualizar Cliente**: Modifica los datos de un cliente existente con `update_client`.
   - **Eliminar Cliente**: Elimina un cliente de la base de datos utilizando `delete_client`.

## Ejemplo de Uso

```python
from src.database_connection import DatabaseConnection
from src.client_crud import create_client, read_client, update_client, delete_client

# Conectar a la base de datos
conexion = DatabaseConnection.conexionBaseDeDatos()

# Crear un nuevo cliente
create_client(conexion, "Juan Pérez", "juan@example.com", "123456789")

# Leer información de un cliente
cliente = read_client(conexion, 1)
print(cliente)

# Actualizar información de un cliente
update_client(conexion, 1, "Juan Pérez", "juan.perez@example.com", "987654321")

# Eliminar un cliente
delete_client(conexion, 1)
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, por favor abre un issue o envía un pull request.