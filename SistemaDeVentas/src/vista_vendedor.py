import flet as ft
from datetime import datetime
import vendedor_crud
from vendedor_crud import VendedorCRUD


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Vendedores"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona un vendedor", options=[])

    def cargar_vendedores_para_eliminar():
        vendedores = VendedorCRUD.mostrar_vendedores()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{v[0]} - {v[1]} {v[2]}") for v in vendedores
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_vendedores_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    def validar_campos(data, es_actualizar=False):
        # Validar fecha primero si está presente
        if 'fin_ven' in data and data['fin_ven']:
            try:
                datetime.strptime(data['fin_ven'], "%Y-%m-%d")
            except ValueError:
                return False, "Fecha inválida. Debe tener el formato YYYY-MM-DD (ej: 2023-12-31)."

        if not es_actualizar or data.get("cod_ven"):
            if not data["cod_ven"] or not data["cod_ven"].startswith("V") or not data["cod_ven"][1:].isdigit():
                return False, "Código de vendedor inválido. Debe comenzar con 'V' seguido de números (ej: V11)."

        if not es_actualizar or data.get("nom_ven"):
            if any(char.isdigit() for char in data.get("nom_ven", "")):
                return False, "El nombre no debe contener números."

        if not es_actualizar or data.get("ape_ven"):
            if any(char.isdigit() for char in data.get("ape_ven", "")):
                return False, "El apellido no debe contener números."

        if not es_actualizar or data.get("sue_ven"):
            if "." in data.get("sue_ven", "") or "," in data.get("sue_ven", ""):
                return False, "El sueldo no debe contener puntos ni comas."
                
        if not es_actualizar or data.get("tip_ven"):
            if not data["tip_ven"].isdigit():
               return False, "El tipo de vendedor debe contener solo números."

        if not es_actualizar or data.get("cod_dis"):
            if not data["cod_dis"].startswith("D") or not data["cod_dis"][1:].isdigit():
                return False, "Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01)."

        return True, ""

    # Campos agregar
    agregar_fields = {
        'cod_ven': ft.TextField(label="Código del vendedor (ej: V11)"),
        'nom_ven': ft.TextField(label="Nombre"),
        'ape_ven': ft.TextField(label="Apellido"),
        'sue_ven': ft.TextField(label="Sueldo (Sin puntos ni comas, ej: 1500)"),
        'fin_ven': ft.TextField(label="Fecha de ingreso, formato YYYY-MM-DD (ej: 2023-12-31)"),
        'tip_ven': ft.TextField(label="Tipo de vendedor (ej: 1 o 2)"),
        'cod_dis': ft.TextField(label="Código del distrito (ej: D01)")
    }

    def on_guardar_vendedor(e):
        data = {k: f.value for k, f in agregar_fields.items()}

        valid, msg = validar_campos(data)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = VendedorCRUD.agregar_vendedor(**data)
        mostrar_mensaje(msg, success)
        if success:
            for f in agregar_fields.values():
                f.value = ""

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Código")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Apellido")),
            ft.DataColumn(label=ft.Text("Sueldo")),
            ft.DataColumn(label=ft.Text("Fecha Ingreso")),
            ft.DataColumn(label=ft.Text("Tipo")),
            ft.DataColumn(label=ft.Text("Distrito")),
        ],
        rows=[]
    )

    def cargar_vendedores(e):
        vendedores = VendedorCRUD.mostrar_vendedores()
        datatable.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in v])
            for v in vendedores
        ]
        mostrar_mensaje("Vendedores cargados correctamente")

    # Actualizar
    actualizar_fields = {
        'cod_ven': ft.TextField(label="Código del vendedor a actualizar (ej: V03)"),
        'nom_ven': ft.TextField(label="Nuevo nombre (dejar vacío para omitir)"),
        'ape_ven': ft.TextField(label="Nuevo apellido (dejar vacío para omitir)"),
        'sue_ven': ft.TextField(label="Nuevo sueldo (Sin puntos ni comas, ej: 1500, dejar vacío para omitir)"),
        'fin_ven': ft.TextField( label="Nueva fecha de ingreso, formato YYYY-MM-DD (dejar vacío para omitir)"),
        'tip_ven': ft.TextField(label="Nuevo tipo de vendedor (ej: 1 o 2, dejar vacío para omitir)"),
        'cod_dis': ft.TextField(label="Nuevo código de distrito (ej: D05, dejar vacío para omitir)")
    }

    def actualizar_vendedor(e):
        data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}

        valid, msg = validar_campos(data, es_actualizar=True)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = VendedorCRUD.actualizar_vendedor(**data)
        mostrar_mensaje(msg, success)

    # Eliminar
    def eliminar_vendedor(e):
        if eliminar_dropdown.value:
            cod_ven = eliminar_dropdown.value.split(" - ")[0]
            success, msg = VendedorCRUD.eliminar_vendedor(cod_ven)
            mostrar_mensaje(msg, success)
            cargar_vendedores_para_eliminar()
        else:
            mostrar_mensaje("Selecciona un vendedor para eliminar.", success=False)

    # UI
    page.add(
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Vendedores", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar la base de datos de vendedores", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Vendedor", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Vendedores", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Vendedor", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Vendedor", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text(ref=mensaje, text_align="center"),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Agregar Nuevo Vendedor", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Vendedor", on_click=on_guardar_vendedor, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Vendedores", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Vendedores", on_click=cargar_vendedores, bgcolor="indigo", color="white"),
                            datatable
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Vendedor", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Vendedor", on_click=actualizar_vendedor, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Vendedor", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Vendedor", on_click=eliminar_vendedor, bgcolor="red", color="white")
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