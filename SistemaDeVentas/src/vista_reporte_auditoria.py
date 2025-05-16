import flet as ft
from reporte_auditoria import obtener_vendedores_menos_ventas

def vista_reporte_auditoria(page: ft.Page):
    # Obtener los datos de auditoría
    datos = obtener_vendedores_menos_ventas()

    # Encabezados de la tabla
    columnas = [
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Usuario")),
        ft.DataColumn(ft.Text("Fecha/Hora")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Operación")),
        ft.DataColumn(ft.Text("Llave Primaria")),
        ft.DataColumn(ft.Text("Detalle Tabla")),
    ]

    # Filas de la tabla
    filas = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(fila[0]))),
                ft.DataCell(ft.Text(str(fila[1]))),
                ft.DataCell(ft.Text(str(fila[2]))),
                ft.DataCell(ft.Text(str(fila[3]))),
                ft.DataCell(ft.Text(str(fila[4]))),
                ft.DataCell(ft.Text(str(fila[5]))),
                ft.DataCell(ft.Text(str(fila[6]))),
            ]
        )
        for fila in datos
    ]

    return ft.View(
        "/reporte_auditoria",
        controls=[
            ft.Text("Reporte de Auditoría", size=28, weight="bold"),
            ft.Divider(),
            ft.DataTable(
                columns=columnas,
                rows=filas,
                expand=True,
            ),
            ft.ElevatedButton(
                "Volver al menú",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: page.go("/menu"),
            ),
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
