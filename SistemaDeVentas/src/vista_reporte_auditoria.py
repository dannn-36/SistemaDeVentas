import flet as ft

def vista_reporte_auditoria(page: ft.Page):
    return ft.View(
        "/reporte_auditoria",
        controls=[
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Volver al Menú Principal",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda _: page.go("/menu"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.INDIGO,
                            color=ft.Colors.WHITE,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Container(
                content=ft.Text("Reporte Tabla Auditoría (en blanco)"),
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
