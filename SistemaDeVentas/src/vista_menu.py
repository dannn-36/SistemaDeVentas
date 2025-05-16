import flet as ft

def vista_menu(page: ft.Page):
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=15,
        bgcolor=ft.Colors.INDIGO,
        color=ft.Colors.WHITE,
        overlay_color=ft.Colors.INDIGO_300,
    )

    BUTTON_WIDTH = 200  # Ancho fijo para todos los botones

    def menu_button(texto, icono, ruta):
        return ft.ElevatedButton(
            texto,
            icon=icono,
            style=button_style,
            on_click=lambda _: page.go(ruta),
            width=BUTTON_WIDTH
        )

    def card_seccion(titulo, botones):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(titulo, size=20, weight="bold", color=ft.Colors.INDIGO_700),
                    ft.Divider(thickness=1),
                    *botones
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            width=BUTTON_WIDTH + 40,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.GREY_300,
                offset=ft.Offset(0, 4),
            ),
        )

    return ft.View(
        "/menu",
        controls=[
            # Encabezado
            ft.Row(
                [ft.Text("Menú Principal", size=36, weight="bold")],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Divider(thickness=2),

            # Secciones centradas en la mitad
            ft.Container(
                content=ft.Row(
                    controls=[
                        card_seccion("Entidades", [
                            menu_button("Proveedores", ft.Icons.PEOPLE, "/proveedor"),
                            menu_button("Productos", ft.Icons.INVENTORY, "/producto"),
                            menu_button("Vendedores", ft.Icons.BADGE, "/vendedor"),
                            menu_button("Clientes", ft.Icons.PERSON, "/cliente"),
                            menu_button("Distritos", ft.Icons.LOCATION_CITY, "/distrito"),
                        ]),
                        card_seccion("Transacciones", [
                            menu_button("Facturas", ft.Icons.RECEIPT, "/factura"),
                            menu_button("Detalles Factura", ft.Icons.LIST_ALT, "/detalle_factura"),
                            menu_button("Órdenes Compra", ft.Icons.SHOPPING_CART, "/orden_compra"),
                            menu_button("Detalles Compra", ft.Icons.LIST, "/detalle_compra"),
                            menu_button("Abastecimiento", ft.Icons.WAREHOUSE, "/abastecimiento"),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=60,
                ),
                alignment=ft.alignment.center,
                margin=ft.Margin(0, 30, 0, 0),
            ),

            # Sección inferior
            ft.Container(
                content=card_seccion("Utilidades", [
                    menu_button("Reportes", ft.Icons.INSERT_CHART, "/reportes"),
                    menu_button("Cerrar sesión", ft.Icons.EXIT_TO_APP, "/"),
                ]),
                alignment=ft.alignment.center,
                margin=ft.Margin(0, 30, 0, 0),
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        padding=30,
    )
