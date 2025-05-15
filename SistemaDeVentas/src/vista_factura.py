import flet as ft
from factura_crud import FacturaCRUD


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Facturas"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona una factura", options=[])

    def cargar_facturas_para_eliminar():
        facturas = FacturaCRUD.listar_facturas()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{f[0]}") for f in facturas
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_facturas_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    # Campos agregar
    agregar_fields = {
        'num_fac': ft.TextField(label="Número de factura"),
        'fec_fac': ft.TextField(label="Fecha de factura (YYYY-MM-DD)"),
        'cod_cli': ft.TextField(label="Código del cliente"),
        'fec_can': ft.TextField(label="Fecha de cancelación (YYYY-MM-DD)"),
        'est_fac': ft.TextField(label="Estado de la factura"),
        'cod_ven': ft.TextField(label="Código del vendedor"),
        'por_igv': ft.TextField(label="Porcentaje de IGV")
    }

    def on_guardar_factura(e):
        try:
            data = {k: f.value for k, f in agregar_fields.items()}
            success, msg = FacturaCRUD.insertar_factura(**data)
            mostrar_mensaje(msg, success)
            if success:
                for f in agregar_fields.values():
                    f.value = ""
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar factura: {ex}", success=False)

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Número")),
            ft.DataColumn(label=ft.Text("Fecha")),
            ft.DataColumn(label=ft.Text("Cliente")),
            ft.DataColumn(label=ft.Text("Cancelación")),
            ft.DataColumn(label=ft.Text("Estado")),
            ft.DataColumn(label=ft.Text("Vendedor")),
            ft.DataColumn(label=ft.Text("IGV")),
        ],
        rows=[]
    )

    def cargar_facturas(e):
        try:
            facturas = FacturaCRUD.listar_facturas()
            datatable.rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in f])
                for f in facturas
            ]
            mostrar_mensaje("Facturas cargadas correctamente")
        except Exception as ex:
            mostrar_mensaje(f"Error al cargar facturas: {ex}", success=False)

    # Actualizar
    actualizar_fields = {
        'num_fac': ft.TextField(label="Número de factura a actualizar"),
        'fec_fac': ft.TextField(label="Nueva fecha de factura (YYYY-MM-DD)"),
        'cod_cli': ft.TextField(label="Nuevo código del cliente"),
        'fec_can': ft.TextField(label="Nueva fecha de cancelación (YYYY-MM-DD)"),
        'est_fac': ft.TextField(label="Nuevo estado de la factura"),
        'cod_ven': ft.TextField(label="Nuevo código del vendedor"),
        'por_igv': ft.TextField(label="Nuevo porcentaje de IGV")
    }

    def actualizar_factura(e):
        try:
            data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}
            success, msg = FacturaCRUD.actualizar_factura(**data)
            mostrar_mensaje(msg, success)
        except Exception as ex:
            mostrar_mensaje(f"Error al actualizar factura: {ex}", success=False)

    # Eliminar
    def eliminar_factura(e):
        try:
            if eliminar_dropdown.value:
                num_fac = eliminar_dropdown.value
                success, msg = FacturaCRUD.eliminar_factura(num_fac)
                mostrar_mensaje(msg, success)
                cargar_facturas_para_eliminar()
            else:
                mostrar_mensaje("Selecciona una factura para eliminar.", success=False)
        except Exception as ex:
            mostrar_mensaje(f"Error al eliminar factura: {ex}", success=False)

    # UI
    return ft.View(
        route="/producto",
        controls=[
            
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Facturas", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar la base de datos de facturas", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Factura", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Facturas", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Factura", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Factura", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text(ref=mensaje, text_align="center"),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Agregar Nueva Factura", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Factura", on_click=on_guardar_factura, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Facturas", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Facturas", on_click=cargar_facturas, bgcolor="indigo", color="white"),
                            datatable
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Factura", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Factura", on_click=actualizar_factura, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Factura", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Factura", on_click=eliminar_factura, bgcolor="red", color="white")
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

