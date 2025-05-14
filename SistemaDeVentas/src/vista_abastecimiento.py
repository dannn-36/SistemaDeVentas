import flet as ft
from abastecimiento_crud import AbastecimientoCRUD
from proveedor_crud import ProveedorCRUD
from producto_crud import ProductoCRUD

def main(page: ft.Page):
    page.title = "Sistema de Gestión de Abastecimientos"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona un abastecimiento", options=[])

    def cargar_abastecimientos_para_eliminar():
        abastecimientos = AbastecimientoCRUD.listar_abastecimientos()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{a[0]} - {a[1]}") for a in abastecimientos
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_abastecimientos_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    def validar_campos(data, es_actualizar=False):
        if not es_actualizar or data.get("cod_prv") and data.get("cod_pro") and data.get("precio"):
            if not data["cod_prv"]:
                return False, "El proveedor no puede estar vacío."
            if not data["cod_pro"]:
                return False, "El producto no puede estar vacío."
            if not data["precio"].replace(".", "").isdigit():
                return False, "El precio debe ser un número válido."

        return True, ""

    # Campos agregar
    agregar_fields = {
        'cod_prv': ft.Dropdown(label="Proveedor", options=[]),
        'cod_pro': ft.Dropdown(label="Producto", options=[]),
        'precio': ft.TextField(label="Precio")
    }

    def cargar_proveedores_y_productos():
        proveedores = ProveedorCRUD.mostrar_proveedores()
        productos = ProductoCRUD.mostrar_productos()

        agregar_fields['cod_prv'].options = [
            ft.dropdown.Option(f"{p[0]} - {p[1]}") for p in proveedores
        ]
        agregar_fields['cod_pro'].options = [
            ft.dropdown.Option(f"{p[0]} - {p[1]}") for p in productos
        ]
        page.update()

    def on_guardar_abastecimiento(e):
        data = {k: f.value for k, f in agregar_fields.items()}

        valid, msg = validar_campos(data)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = AbastecimientoCRUD.insertar_abastecimiento(data["cod_prv"], data["cod_pro"], data["precio"])
        mostrar_mensaje(msg, success)
        if success:
            for f in agregar_fields.values():
                f.value = ""  # Limpiar los campos

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[ft.DataColumn(label=ft.Text("Proveedor")), ft.DataColumn(label=ft.Text("Producto")), ft.DataColumn(label=ft.Text("Precio"))],
        rows=[]
    )

    def cargar_abastecimientos(e):
        abastecimientos = AbastecimientoCRUD.listar_abastecimientos()
        datatable.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in a])
            for a in abastecimientos
        ]
        mostrar_mensaje("Abastecimientos cargados correctamente")

    # Actualizar
    actualizar_fields = {
        'cod_prv': ft.TextField(label="Código de proveedor a actualizar (ej: PR01)"),
        'cod_pro': ft.TextField(label="Código de producto a actualizar (ej: P001)"),
        'nuevo_precio': ft.TextField(label="Nuevo precio (dejar vacío para omitir)")
    }

    def actualizar_abastecimiento(e):
        data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}

        valid, msg = validar_campos(data, es_actualizar=True)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = AbastecimientoCRUD.actualizar_abastecimiento(**data)
        mostrar_mensaje(msg, success)

    # Eliminar
    def eliminar_abastecimiento(e):
        if eliminar_dropdown.value:
            cod_abs = eliminar_dropdown.value.split(" - ")[0]
            success, msg = AbastecimientoCRUD.eliminar_abastecimiento(cod_abs)
            mostrar_mensaje(msg, success)
            cargar_abastecimientos_para_eliminar()
        else:
            mostrar_mensaje("Selecciona un abastecimiento para eliminar.", success=False)

    # UI
    page.add(
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Abastecimientos", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar la base de datos de abastecimientos", color="grey", text_align="center"),

                    ft.Row([ 
                        ft.TextButton("Agregar Abastecimiento", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Abastecimientos", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Abastecimiento", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Abastecimiento", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text(ref=mensaje, text_align="center"),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Agregar Nuevo Abastecimiento", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Abastecimiento", on_click=on_guardar_abastecimiento, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Abastecimientos", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Abastecimientos", on_click=cargar_abastecimientos, bgcolor="indigo", color="white"),
                            datatable
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Abastecimiento", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Abastecimiento", on_click=actualizar_abastecimiento, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Abastecimiento", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Abastecimiento", on_click=eliminar_abastecimiento, bgcolor="red", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ],
                spacing=25,
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        )
    )

    cargar_proveedores_y_productos()

ft.app(target=main)
