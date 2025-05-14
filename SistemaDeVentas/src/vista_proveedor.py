import flet as ft
from datetime import datetime
from proveedor_crud import ProveedorCRUD


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Proveedores"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona un proveedor", options=[])

    def cargar_proveedores_para_eliminar():
        proveedores = ProveedorCRUD.mostrar_proveedores()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{p[0]} - {p[1]}") for p in proveedores
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_proveedores_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    def validar_campos(data, es_actualizar=False):
        if not es_actualizar or data.get("cod_prv"):
            if not data["cod_prv"] or not data["cod_prv"].startswith("PR") or not data["cod_prv"][2:].isdigit():
                return False, "Código de proveedor inválido. Debe comenzar con 'PR' seguido de números (ej: PR01)."
            # Verificar si el proveedor ya existe
            if not es_actualizar:
                success, msg = ProveedorCRUD.agregar_proveedor(data["cod_prv"], None, None, None, None, None)
                if not success and "ya existe" in msg:
                    return False, msg

        if not es_actualizar or data.get("rso_prv"):
            if not data["rso_prv"]:
                return False, "La razón social no puede estar vacía."

        if not es_actualizar or data.get("dir_prv"):
            if not data["dir_prv"]:
                return False, "La dirección no puede estar vacía."

        if not es_actualizar or data.get("tel_prv"):
            if not data["tel_prv"].isdigit():
                return False, "El teléfono debe contener solo números."

        if not es_actualizar or data.get("cod_dis"):
            if not data["cod_dis"].startswith("D") or not data["cod_dis"][1:].isdigit():
                return False, "Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01)."

        if not es_actualizar or data.get("rep_pro"):
            if not data["rep_pro"]:
                return False, "El representante no puede estar vacío."

        return True, ""

    # Campos agregar
    agregar_fields = {
        'cod_prv': ft.TextField(label="Código del proveedor (ej: PR01)"),
        'rso_prv': ft.TextField(label="Razón Social"),
        'dir_prv': ft.TextField(label="Dirección"),
        'tel_prv': ft.TextField(label="Teléfono"),
        'cod_dis': ft.TextField(label="Código del distrito (ej: D01)"),
        'rep_pro': ft.TextField(label="Representante")
    }

    def on_guardar_proveedor(e):
        data = {k: f.value for k, f in agregar_fields.items()}

        valid, msg = validar_campos(data)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = ProveedorCRUD.agregar_proveedor(**data)
        mostrar_mensaje(msg, success)
        if success:
            for f in agregar_fields.values():
                f.value = ""

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Código")),
            ft.DataColumn(label=ft.Text("Razón Social")),
            ft.DataColumn(label=ft.Text("Dirección")),
            ft.DataColumn(label=ft.Text("Teléfono")),
            ft.DataColumn(label=ft.Text("Distrito")),
            ft.DataColumn(label=ft.Text("Representante")),
        ],
        rows=[]
    )

    def cargar_proveedores(e):
        proveedores = ProveedorCRUD.mostrar_proveedores()
        datatable.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in p])
            for p in proveedores
        ]
        mostrar_mensaje("Proveedores cargados correctamente")

    # Actualizar
    actualizar_fields = {
        'cod_prv': ft.TextField(label="Código del proveedor a actualizar (ej: PR01)"),
        'rso_prv': ft.TextField(label="Nueva razón social (dejar vacío para omitir)"),
        'dir_prv': ft.TextField(label="Nueva dirección (dejar vacío para omitir)"),
        'tel_prv': ft.TextField(label="Nuevo teléfono (dejar vacío para omitir)"),
        'cod_dis': ft.TextField(label="Nuevo código de distrito (ej: D01, dejar vacío para omitir)"),
        'rep_pro': ft.TextField(label="Nuevo representante (dejar vacío para omitir)")
    }

    def actualizar_proveedor(e):
        data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}

        valid, msg = validar_campos(data, es_actualizar=True)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = ProveedorCRUD.actualizar_proveedor(**data)
        mostrar_mensaje(msg, success)

    # Eliminar
    def eliminar_proveedor(e):
        if eliminar_dropdown.value:
            cod_prv = eliminar_dropdown.value.split(" - ")[0]
            success, msg = ProveedorCRUD.eliminar_proveedor(cod_prv)
            mostrar_mensaje(msg, success)
            cargar_proveedores_para_eliminar()
        else:
            mostrar_mensaje("Selecciona un proveedor para eliminar.", success=False)

    # UI
    page.add(
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Proveedores", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar la base de datos de proveedores", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Proveedor", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Proveedores", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Proveedor", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Proveedor", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text(ref=mensaje, text_align="center"),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Agregar Nuevo Proveedor", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Proveedor", on_click=on_guardar_proveedor, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Proveedores", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Proveedores", on_click=cargar_proveedores, bgcolor="indigo", color="white"),
                            datatable
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Proveedor", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Proveedor", on_click=actualizar_proveedor, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Proveedor", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Proveedor", on_click=eliminar_proveedor, bgcolor="red", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ],
                spacing=25,
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        )
    )


ft.app(target=main)
