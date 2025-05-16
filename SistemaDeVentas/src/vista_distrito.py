import flet as ft
from distrito_crud import DistritoCRUD

def main(page: ft.Page):
    page.title = "Sistema de Gestión de Distritos"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona un Distrito", options=[])

    def cargar_distritos_para_eliminar():
        distritos = DistritoCRUD.listar_distritos()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{d[0]} - {d[1]}") for d in distritos
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_distritos_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    def validar_campos(data, es_actualizar=False):
        if not es_actualizar or data.get("cod_dis"):
            if not data["cod_dis"] or not data["cod_dis"].startswith("D") or not data["cod_dis"][1:].isdigit():
                return False, "Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01)."

        if not es_actualizar or data.get("nom_dis"):
            if not data["nom_dis"]:
                return False, "El nombre del distrito no puede estar vacío."
            if any(char.isdigit() for char in data["nom_dis"]):
                return False, "El nombre del distrito no debe contener números."

        return True, "Campos válidos."  # <--- Este return faltaba


    # Campos agregar
    agregar_fields = {
        'cod_dis': ft.TextField(label="Código del distrito (ej: D01)"),
        'nom_dis': ft.TextField(label="Nombre del distrito")
    }

    def on_guardar_distrito(e):
        data = {k: f.value for k, f in agregar_fields.items()}

        valid, msg = validar_campos(data)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = DistritoCRUD.insertar_distrito(**data)
        mostrar_mensaje(msg, success)
        if success:
            for f in agregar_fields.values():
                f.value = ""

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Código")),
            ft.DataColumn(label=ft.Text("Nombre"))
        ],
        rows=[]
    )

    def cargar_distritos(e):
        distritos = DistritoCRUD.listar_distritos()
        datatable.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in d])
            for d in distritos
        ]
        mostrar_mensaje("Distritos cargados correctamente")

    # Actualizar
    actualizar_fields = {
        'cod_dis': ft.TextField(label="Código del distrito a actualizar (ej: D01)"),
        'nom_dis': ft.TextField(label="Nuevo nombre del distrito (dejar vacío para omitir)")
    }

    def actualizar_distrito(e):
        data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}

        valid, msg = validar_campos(data, es_actualizar=True)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return

        success, msg = DistritoCRUD.actualizar_distrito(**data)
        mostrar_mensaje(msg, success)

    # Eliminar
    def eliminar_distrito(e):
        if eliminar_dropdown.value:
            cod_dis = eliminar_dropdown.value.split(" - ")[0]
            success, msg = DistritoCRUD.eliminar_distrito(cod_dis)
            mostrar_mensaje(msg, success)
            cargar_distritos_para_eliminar()
        else:
            mostrar_mensaje("Selecciona un distrito para eliminar.", success=False)

    # UI
    return ft.View(
        route="/distrito",
        controls=[

        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Distritos", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar la base de datos de distritos", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Distrito", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Distritos", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Distrito", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Distrito", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                     # Botón para volver al menú principal
                    ft.ElevatedButton(
                        "Volver al Menú Principal",
                        on_click=lambda e: page.go("/menu"),
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
                            ft.Text("Agregar Nuevo Distrito", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Distrito", on_click=on_guardar_distrito, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Distritos", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Distritos", on_click=cargar_distritos, bgcolor="indigo", color="white"),
                            ft.Container(
                                ft.Column(
                                    [datatable],
                                    scroll="auto",
                                    expand=True,
                                ),
                                height=400,
                                expand=True,
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Distrito", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Distrito", on_click=actualizar_distrito, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Distrito", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Distrito", on_click=eliminar_distrito, bgcolor="red", color="white")
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
