import flet as ft
import sys
from vista_proveedor import main as vista_proveedor
from vista_producto import main as vista_producto
from vista_vendedor import main as vista_vendedor
from vista_detalle_factura import main as vista_detalle_factura
from vista_factura import main as vista_factura
from vista_orden_compra import main as vista_orden_compra
from vista_detalle_compra import main as vista_detalle_compra
from vista_abastecimiento import main as vista_abastecimiento
from vista_distrito import main as vista_distrito
from vista_cliente import main as vista_cliente


def main(page: ft.Page):
    page.title = "Sistema de Gestión"
    page.theme_mode = "light"
    page.scroll = "auto"
    page.padding = 30
    page.bgcolor = "#f2f2f7"  # Fondo suave tipo iOS


    def route_change(e: ft.RouteChangeEvent):
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/menu",
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Menú Principal", size=36, weight="bold", text_align="center"),
                                    ft.Divider(),
                                    ft.ElevatedButton("👤 Ir a Proveedores", icon=ft.Icons.PEOPLE, style=button_style, on_click=lambda _: page.go("/proveedor")),
                                    ft.ElevatedButton("📦 Ir a Productos", icon=ft.Icons.INVENTORY, style=button_style, on_click=lambda _: page.go("/producto")),
                                    ft.ElevatedButton("🧑‍💼 Ir a Vendedores", icon=ft.Icons.BADGE, style=button_style, on_click=lambda _: page.go("/vendedor")),
                                    ft.ElevatedButton("🧾 Ir a Facturas", icon=ft.Icons.RECEIPT, style=button_style, on_click=lambda _: page.go("/factura")),
                                    ft.ElevatedButton("📋 Ir a Detalles de Factura", icon=ft.Icons.LIST_ALT, style=button_style, on_click=lambda _: page.go("/detalle_factura")),
                                    ft.ElevatedButton("📑 Ir a Órdenes de Compra", icon=ft.Icons.SHOPPING_CART, style=button_style, on_click=lambda _: page.go("/orden_compra")),
                                    ft.ElevatedButton("📦 Ir a Detalles de Compra", icon=ft.Icons.LIST, style=button_style, on_click=lambda _: page.go("/detalle_compra")),
                                    ft.ElevatedButton("🏢 Ir a Abastecimiento", icon=ft.Icons.WAREHOUSE, style=button_style, on_click=lambda _: page.go("/abastecimiento")),
                                    ft.ElevatedButton("🏙️ Ir a Distritos", icon=ft.Icons.LOCATION_CITY, style=button_style, on_click=lambda _: page.go("/distrito")),
                                    ft.ElevatedButton("👥 Ir a Clientes", icon=ft.Icons.PERSON, style=button_style, on_click=lambda _: page.go("/cliente")),
                                    ft.ElevatedButton("❌ Salir", icon=ft.Icons.EXIT_TO_APP, style=button_style, on_click=lambda _: sys.exit()),
                                    #no funciona esta funcion de arriba 
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
            )
        elif page.route == "/proveedor":
            page.views.append(vista_proveedor(page))
        elif page.route == "/producto":
            page.views.append(vista_producto(page))
        elif page.route == "/vendedor":
            page.views.append(vista_vendedor(page))
        elif page.route == "/factura":
            page.views.append(vista_factura(page))
        elif page.route == "/detalle_factura":
            page.views.append(vista_detalle_factura(page))
        elif page.route == "/orden_compra":
            page.views.append(vista_orden_compra(page))
        elif page.route == "/detalle_compra":
            page.views.append(vista_detalle_compra(page))
        elif page.route == "/abastecimiento":
            page.views.append(vista_abastecimiento(page))
        elif page.route == "/distrito":
            page.views.append(vista_distrito(page))
        elif page.route == "/cliente":
            page.views.append(vista_cliente(page))

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        page.update()

    # Estilo base para botones
    global button_style
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=20,
        bgcolor=ft.Colors.INDIGO,
        color=ft.Colors.WHITE,
        overlay_color=ft.Colors.INDIGO
    )

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
