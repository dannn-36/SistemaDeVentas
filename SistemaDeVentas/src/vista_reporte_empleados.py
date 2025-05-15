import flet as ft

def vista_reporte_empleados(page: ft.Page):
    cantidad_field = ft.TextField(label="Cantidad de empleados a mostrar", width=250)
    resultado_text = ft.Text("")

    def mostrar_empleados(e):
        try:
            cantidad = int(cantidad_field.value)
            if cantidad <= 0:
                resultado_text.value = "Ingrese un número mayor a 0."
            else:
                resultado_text.value = f"Mostrando {cantidad} empleados con ventas más bajas."
        except ValueError:
            resultado_text.value = "Ingrese un número válido."
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
