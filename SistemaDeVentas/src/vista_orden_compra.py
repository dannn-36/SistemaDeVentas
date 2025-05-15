import flet as ft
from orden_compra_crud import OrdenCompraCRUD


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Órdenes de Compra"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona una orden de compra", options=[])

    def cargar_ordenes_para_eliminar():
        ordenes = OrdenCompraCRUD.listar_ordenes_compra()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{o[0]}") for o in ordenes
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_ordenes_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    # Campos agregar
    agregar_fields = {
        'num_oco': ft.TextField(label="Número de orden de compra (ej: OC001)"),
        'fec_oco': ft.TextField(label="Fecha de orden de compra (YYYY-MM-DD)"),
        'cod_prv': ft.TextField(label="Código del proveedor (ej: PR01)"),
        'fat_oco': ft.TextField(label="Fecha de facturación (YYYY-MM-DD)"),
        'est_oco': ft.TextField(label="Estado de la orden de compra (1, 2 o 3)")
    }

    def on_guardar_orden(e):
        try:
            data = {k: f.value for k, f in agregar_fields.items()}
            success, msg = OrdenCompraCRUD.insertar_orden_compra(**data)
            mostrar_mensaje(msg, success)
            if success:
                for f in agregar_fields.values():
                    f.value = ""
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar orden: {ex}", success=False)

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Número")),
            ft.DataColumn(label=ft.Text("Fecha de Orden")),
            ft.DataColumn(label=ft.Text("Proveedor")),
            ft.DataColumn(label=ft.Text("Fecha de Facturación")),
            ft.DataColumn(label=ft.Text("Estado")),
        ],
        rows=[]
    )

    def cargar_ordenes(e):
        try:
            ordenes = OrdenCompraCRUD.listar_ordenes_compra()
            datatable.rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in o])
                for o in ordenes
            ]
            mostrar_mensaje("Órdenes de compra cargadas correctamente")
        except Exception as ex:
            mostrar_mensaje(f"Error al cargar órdenes: {ex}", success=False)

    # Actualizar
    actualizar_fields = {
        'num_oco': ft.TextField(label="Número de orden de compra a actualizar (ej: OC001)"),
        'fec_oco': ft.TextField(label="Nueva fecha de orden de compra (YYYY-MM-DD)"),
        'cod_prv': ft.TextField(label="Nuevo código del proveedor (ej: PR01)"),
        'fat_oco': ft.TextField(label="Nueva fecha de facturación (YYYY-MM-DD)"),
        'est_oco': ft.TextField(label="Nuevo estado de la orden de compra (1, 2 o 3)")
    }

    def actualizar_orden(e):
        try:
            data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}
            success, msg = OrdenCompraCRUD.actualizar_orden_compra(**data)
            mostrar_mensaje(msg, success)
        except Exception as ex:
            mostrar_mensaje(f"Error al actualizar orden: {ex}", success=False)

    # Eliminar
    def eliminar_orden(e):
        try:
            if eliminar_dropdown.value:
                num_oco = eliminar_dropdown.value
                success, msg = OrdenCompraCRUD.eliminar_orden_compra(num_oco)
                mostrar_mensaje(msg, success)
                cargar_ordenes_para_eliminar()
            else:
                mostrar_mensaje("Selecciona una orden para eliminar.", success=False)
        except Exception as ex:
            mostrar_mensaje(f"Error al eliminar orden: {ex}", success=False)

    # UI
    return ft.View(
        route="/orden_compra",
        controls=[
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Órdenes de Compra", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar la base de datos de órdenes de compra", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Orden", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Órdenes", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Orden", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Orden", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text(ref=mensaje, text_align="center"),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Agregar Nueva Orden de Compra", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Orden", on_click=on_guardar_orden, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Órdenes de Compra", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Órdenes", on_click=cargar_ordenes, bgcolor="indigo", color="white"),
                            datatable
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Orden de Compra", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Orden", on_click=actualizar_orden, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Orden de Compra", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Orden", on_click=eliminar_orden, bgcolor="red", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ],
                spacing=25,
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        )
        ]
    )


