import flet as ft
from abastecimiento_crud import AbastecimientoCRUD


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

    # Campos agregar
    agregar_fields = {
        'cod_prv': ft.TextField(label="Código del proveedor (ej: PR01)"),
        'cod_pro': ft.TextField(label="Código del producto (ej: P001)"),
        'pre_aba': ft.TextField(label="Precio de abastecimiento")
    }

    def on_guardar_abastecimiento(e):
        try:
            data = {k: f.value for k, f in agregar_fields.items()}
            try:
                data["pre_aba"] = float(data["pre_aba"])
            except ValueError:
                mostrar_mensaje("El precio debe ser un número sin puntos ni comas.", success=False)
                return

            success, msg = AbastecimientoCRUD.insertar_abastecimiento(**data)
            mostrar_mensaje(msg, success)
            if success:
                for f in agregar_fields.values():
                    f.value = ""
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar abastecimiento: {ex}", success=False)

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Proveedor")),
            ft.DataColumn(label=ft.Text("Producto")),
            ft.DataColumn(label=ft.Text("Precio")),
        ],
        rows=[]
    )

    def cargar_abastecimientos(e):
        try:
            abastecimientos = AbastecimientoCRUD.listar_abastecimientos()
            datatable.rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in a])
                for a in abastecimientos
            ]
            mostrar_mensaje("Abastecimientos cargados correctamente")
        except Exception as ex:
            mostrar_mensaje(f"Error al cargar abastecimientos: {ex}", success=False)

    # Actualizar
    actualizar_fields = {
        'cod_prv': ft.TextField(label="Código del proveedor (ej: PR01)"),
        'cod_pro': ft.TextField(label="Código del producto (ej: P001)"),
        'nuevo_precio': ft.TextField(label="Nuevo precio de abastecimiento")
    }

    def actualizar_abastecimiento(e):
        try:
            data = {k: v.value for k, v in actualizar_fields.items()}
            try:
                data["nuevo_precio"] = float(data["nuevo_precio"])
            except ValueError:
                mostrar_mensaje("El precio debe ser un número.", success=False)
                return

            success, msg = AbastecimientoCRUD.actualizar_abastecimiento(**data)
            mostrar_mensaje(msg, success)
        except Exception as ex:
            mostrar_mensaje(f"Error al actualizar abastecimiento: {ex}", success=False)

    # Eliminar
    def eliminar_abastecimiento(e):
        try:
            if eliminar_dropdown.value:
                cod_prv, cod_pro = eliminar_dropdown.value.split(" - ")
                success, msg = AbastecimientoCRUD.eliminar_abastecimiento(cod_prv, cod_pro)
                mostrar_mensaje(msg, success)
                cargar_abastecimientos_para_eliminar()
            else:
                mostrar_mensaje("Selecciona un abastecimiento para eliminar.", success=False)
        except Exception as ex:
            mostrar_mensaje(f"Error al eliminar abastecimiento: {ex}", success=False)

    # UI
    return ft.View(
        route="/abastecimiento",
        controls=[
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
        ]
    )



