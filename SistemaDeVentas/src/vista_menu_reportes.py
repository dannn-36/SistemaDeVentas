import flet as ft

def vista_menu_reportes(page: ft.Page):
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=20,
        bgcolor=ft.Colors.INDIGO,
        color=ft.Colors.WHITE,
        overlay_color=ft.Colors.INDIGO
    )

    return ft.View(
        "/reportes",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Menú Reportes", size=36, weight="bold", text_align="center"),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Reporte Tabla Auditoría",
                            icon=ft.Icons.TABLE_CHART,
                            style=button_style,
                            on_click=lambda _: page.go("/reporte_auditoria")
                        ),
                        ft.ElevatedButton(
                            "Empleados con ventas más bajas",
                            icon=ft.Icons.ARROW_DOWNWARD,
                            style=button_style,
                            on_click=lambda _: page.go("/reporte_empleados")
                        ),
                        ft.ElevatedButton(
                            "Volver al Menú Principal",
                            icon=ft.Icons.ARROW_BACK,
                            style=button_style,
                            on_click=lambda _: page.go("/menu")
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=30,
                width=500,
                bgcolor="white",
                border_radius=20,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.GREY_400,
                    offset=ft.Offset(0, 6),
                ),
                alignment=ft.alignment.center,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
