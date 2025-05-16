import flet as ft
from reporte_empleados import obtener_vendedores_menos_ventas

def vista_reporte_empleados(page: ft.Page):
    cantidad_field = ft.TextField(label="Cantidad de empleados a mostrar", width=250)
    resultado_text = ft.Text("")
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Empleado N°")),  # Nueva columna
            ft.DataColumn(label=ft.Text("Código")),
            ft.DataColumn(label=ft.Text("Nombre Completo")),
            ft.DataColumn(label=ft.Text("Total Ventas")),
        ],
        rows=[]
    )

    def mostrar_empleados(e):
        try:
            cantidad = int(cantidad_field.value)
            if cantidad <= 0:
                resultado_text.value = "Ingrese un número mayor a 0."
                datatable.rows = []
            else:
                empleados = obtener_vendedores_menos_ventas(limit=cantidad)
                if not empleados:
                    resultado_text.value = "No hay empleados registrados."
                    datatable.rows = []
                else:
                    total_empleados = len(empleados)
                    if total_empleados < cantidad:
                        resultado_text.value = f"Solo existen {total_empleados} empleados en la base de datos."
                    else:
                        resultado_text.value = f"Mostrando {cantidad} empleados con ventas más bajas."
                    datatable.rows = [
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(idx + 1))),  # Número de empleado
                                ft.DataCell(ft.Text(str(emp[0]))),
                                ft.DataCell(ft.Text(str(emp[1]))),
                                ft.DataCell(ft.Text(str(emp[2]))),
                            ]
                        )
                        for idx, emp in enumerate(empleados)
                    ]
        except ValueError:
            resultado_text.value = "Ingrese un número válido."
            datatable.rows = []
        except Exception as ex:
            resultado_text.value = f"Error: {ex}"
            datatable.rows = []
        page.update()

    return ft.View(
        "/reporte_empleados",
        controls=[
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Volver al Menú de Reportes",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda _: page.go("/reportes"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.INDIGO,
                            color=ft.Colors.WHITE,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Empleados con ventas más bajas", size=24, weight="bold"),
                        cantidad_field,
                        ft.ElevatedButton("Mostrar", icon=ft.Icons.SEARCH, on_click=mostrar_empleados),
                        resultado_text,
                        ft.Container(
                            ft.Column(
                                [datatable],
                                scroll="auto",
                                expand=True,
                            ),
                            height=400,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
