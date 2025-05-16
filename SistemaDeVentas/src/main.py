import flet as ft
from vista_login import main as vista_login
from vista_menu import vista_menu
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
from vista_menu_reportes import vista_menu_reportes
from vista_reporte_auditoria import vista_reporte_auditoria
from vista_reporte_empleados import vista_reporte_empleados

def main(page: ft.Page):
    page.title = "Sistema de Ventas"
    page.theme_mode = "light"
    page.scroll = "auto"
    page.padding = 30
    page.bgcolor = "#f2f2f7"

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        if page.route == "/":
            page.views.append(vista_login(page))
        elif page.route == "/menu":
            page.views.append(vista_menu(page))
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
        elif page.route == "/reportes":
            page.views.append(vista_menu_reportes(page))
        elif page.route == "/reporte_auditoria":
            page.views.append(vista_reporte_auditoria(page))
        elif page.route == "/reporte_empleados":
            page.views.append(vista_reporte_empleados(page))
        page.update()


    def view_pop(e: ft.ViewPopEvent):
        #page.views.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)


#Proyecto final de la materia de Bases de Datos II
# Integrantes:
# - Daniel Villamil
# - Sebastian Pineda
# - Gianfranco Peniche