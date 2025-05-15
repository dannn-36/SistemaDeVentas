import flet as ft

def vista_menu(page: ft.Page):
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=20,
        bgcolor=ft.Colors.INDIGO,
        color=ft.Colors.WHITE,
        overlay_color=ft.Colors.INDIGO
    )

    return ft.View(
        "/menu",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Menú Principal", size=36, weight="bold", text_align="center"),
                        ft.Divider(),
                        ft.ElevatedButton(" Ir a Proveedores", icon=ft.Icons.PEOPLE, style=button_style, on_click=lambda _: page.go("/proveedor")),
                        ft.ElevatedButton(" Ir a Productos", icon=ft.Icons.INVENTORY, style=button_style, on_click=lambda _: page.go("/producto")),
                        ft.ElevatedButton(" Ir a Vendedores", icon=ft.Icons.BADGE, style=button_style, on_click=lambda _: page.go("/vendedor")),
                        ft.ElevatedButton(" Ir a Facturas", icon=ft.Icons.RECEIPT, style=button_style, on_click=lambda _: page.go("/factura")),
                        ft.ElevatedButton(" Ir a Detalles de Factura", icon=ft.Icons.LIST_ALT, style=button_style, on_click=lambda _: page.go("/detalle_factura")),
                        ft.ElevatedButton(" Ir a Órdenes de Compra", icon=ft.Icons.SHOPPING_CART, style=button_style, on_click=lambda _: page.go("/orden_compra")),
                        ft.ElevatedButton(" Ir a Detalles de Compra", icon=ft.Icons.LIST, style=button_style, on_click=lambda _: page.go("/detalle_compra")),
                        ft.ElevatedButton(" Ir a Abastecimiento", icon=ft.Icons.WAREHOUSE, style=button_style, on_click=lambda _: page.go("/abastecimiento")),
                        ft.ElevatedButton(" Ir a Distritos", icon=ft.Icons.LOCATION_CITY, style=button_style, on_click=lambda _: page.go("/distrito")),
                        ft.ElevatedButton(" Ir a Clientes", icon=ft.Icons.PERSON, style=button_style, on_click=lambda _: page.go("/cliente")),
                        ft.ElevatedButton(" Ir a Reportes", icon=ft.Icons.INSERT_CHART, style=button_style, on_click=lambda _: page.go("/reportes")),
                        ft.ElevatedButton(" Cerrar sesión", icon=ft.Icons.EXIT_TO_APP, style=button_style, on_click=lambda _: page.go("/")),
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
