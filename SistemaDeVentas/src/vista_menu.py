import flet as ft
from vista_proveedor import main as vista_proveedor  # Importa la vista del proveedor
from vista_producto import main as vista_producto  # Importa la vista del producto
from vista_vendedor import main as vista_vendedor  # Importa la vista del vendedor
from vista_detalle_factura import main as vista_detalle_factura  # Importa la vista del detalle de factura
from vista_factura import main as vista_factura  # Importa la vista de la factura   

def main(page: ft.Page):
    page.title = "Sistema de Gestión"
    page.theme_mode = "light"
    page.scroll = "auto"

    def route_change(e: ft.RouteChangeEvent):
        #page.views.clear()

        if page.route == "/":
            # Vista del menú principal
            page.views.append(
                ft.View(
                    "/menu",
                    controls=[
                        ft.Text("Menú Principal", size=30, weight="bold", text_align="center"),
                        ft.ElevatedButton("Ir a Proveedores", on_click=lambda _: page.go("/proveedor")),
                        ft.ElevatedButton("Ir a Productos", on_click=lambda _: page.go("/producto")),
                        ft.ElevatedButton("Ir a Vendedores", on_click=lambda _: page.go("/vendedor")),
                        ft.ElevatedButton("Ir a Facturas", on_click=lambda _: page.go("/factura")),
                        ft.ElevatedButton("Ir a Detalles de Factura", on_click=lambda _: page.go("/detalle_factura"))
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        elif page.route == "/proveedor":
            # Cargar la vista del proveedor desde otro archivo
            page.views.append(vista_proveedor(page))
        elif page.route == "/producto":
            # Cargar la vista del producto desde otro archivo
            page.views.append(vista_producto(page))  
        elif page.route == "/vendedor":
            # Cargar la vista del vendedor desde otro archivo
            page.views.append(vista_vendedor(page)) 
        elif page.route == "/factura":
            # Cargar la vista de la factura desde otro archivo
            page.views.append(vista_factura(page))
        elif page.route == "/detalle_factura":
            # Cargar la vista del detalle de factura desde otro archivo
            page.views.append(vista_detalle_factura(page))

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
