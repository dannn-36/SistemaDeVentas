import flet as ft
from detalle_factura_crud import DetalleFacturaCRUD


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Detalles de Factura"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona un detalle de factura", options=[])

    def cargar_detalles_para_eliminar():
        detalles = DetalleFacturaCRUD.listar_detalles_factura()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{d[0]} - {d[1]}") for d in detalles
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_detalles_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    # Campos agregar
    agregar_fields = {
        'num_fac': ft.TextField(label="Número de factura (ej: FA001)"),
        'cod_pro': ft.TextField(label="Código del producto (ej: P001)"),
        'can_ven': ft.TextField(label="Cantidad vendida"),
        'pre_ven': ft.TextField(label="Precio de venta")
    }

    def on_guardar_detalle(e):
        try:
            data = {k: f.value for k, f in agregar_fields.items()}
            data["can_ven"] = int(data["can_ven"])
            data["pre_ven"] = float(data["pre_ven"])
            success, msg = DetalleFacturaCRUD.insertar_detalle_factura(**data)
            mostrar_mensaje(msg, success)
            if success:
                for f in agregar_fields.values():
                    f.value = ""
        except ValueError:
            mostrar_mensaje("Cantidad y precio deben ser números válidos.", success=False)
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar detalle: {ex}", success=False)

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Número de Factura")),
            ft.DataColumn(label=ft.Text("Código de Producto")),
            ft.DataColumn(label=ft.Text("Cantidad Vendida")),
            ft.DataColumn(label=ft.Text("Precio de Venta")),
        ],
        rows=[]
    )

    def cargar_detalles(e):
        try:
            detalles = DetalleFacturaCRUD.listar_detalles_factura()
            datatable.rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in d])
                for d in detalles
            ]
            mostrar_mensaje("Detalles de factura cargados correctamente")
        except Exception as ex:
            mostrar_mensaje(f"Error al cargar detalles: {ex}", success=False)

    # Actualizar
    actualizar_fields = {
        'num_fac': ft.TextField(label="Número de factura (ej: FA001)"),
        'cod_pro': ft.TextField(label="Código del producto (ej: P001)"),
        'can_ven': ft.TextField(label="Nueva cantidad vendida"),
        'pre_ven': ft.TextField(label="Nuevo precio de venta")
    }

    def actualizar_detalle(e):
        try:
            data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}
            if data["can_ven"]:
                data["can_ven"] = int(data["can_ven"])
            if data["pre_ven"]:
                data["pre_ven"] = float(data["pre_ven"])
            success, msg = DetalleFacturaCRUD.actualizar_detalle_factura(**data)
            mostrar_mensaje(msg, success)
        except ValueError:
            mostrar_mensaje("Cantidad y precio deben ser números válidos.", success=False)
        except Exception as ex:
            mostrar_mensaje(f"Error al actualizar detalle: {ex}", success=False)

    # Eliminar
    def eliminar_detalle(e):
        try:
            if eliminar_dropdown.value:
                num_fac, cod_pro = eliminar_dropdown.value.split(" - ")
                success, msg = DetalleFacturaCRUD.eliminar_detalle_factura(num_fac, cod_pro)
                mostrar_mensaje(msg, success)
                cargar_detalles_para_eliminar()
            else:
                mostrar_mensaje("Selecciona un detalle para eliminar.", success=False)
        except Exception as ex:
            mostrar_mensaje(f"Error al eliminar detalle: {ex}", success=False)

    # UI
    return ft.View(
        route="/detalle_factura",
        controls=[
            
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Detalles de Factura", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar los detalles de factura", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Detalle", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Detalles", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Detalle", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Detalle", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                     # Botón para volver al menú principal
                    ft.ElevatedButton(
                        "Volver al Menú Principal",
                        on_click=lambda e: page.go("/"),
                        bgcolor="indigo",
                        color="white"
                    ),

                    ft.Text(ref=mensaje, text_align="center"),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Agregar Nuevo Detalle de Factura", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Detalle", on_click=on_guardar_detalle, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Detalles de Factura", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Detalles", on_click=cargar_detalles, bgcolor="indigo", color="white"),
                            datatable
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Detalle de Factura", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Detalle", on_click=actualizar_detalle, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Detalle de Factura", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Detalle", on_click=eliminar_detalle, bgcolor="red", color="white")
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


