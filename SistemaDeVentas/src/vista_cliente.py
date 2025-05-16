import flet as ft
from datetime import datetime
from cliente_crud import ClienteCRUD
from distrito_crud import DistritoCRUD  # Import DistritoCRUD for district validation


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Clientes"
    page.theme_mode = "light"
    page.scroll = "auto"

    selected_tab = ft.Ref[ft.TextButton]()
    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona un cliente", options=[])

    def cargar_clientes_para_eliminar():
        clientes = ClienteCRUD.mostrar_clientes()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{c[0]} - {c[1]}") for c in clientes
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_clientes_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    def validar_campos(data, es_actualizar=False):
        if not es_actualizar or data.get("fec_reg"):
            try:
                fecha_registro = datetime.strptime(data["fec_reg"], "%Y-%m-%d")
                if fecha_registro > datetime.now():
                    return False, "La fecha de registro no puede ser mayor que la fecha actual."
            except ValueError:
                return False, "Fecha inválida. Debe tener el formato YYYY-MM-DD (ej: 2023-12-31)."

        if not es_actualizar or data.get("tip_cli"):
            if not data["tip_cli"].isdigit():
                return False, "El tipo de cliente debe contener solo números."

        if not es_actualizar or data.get("con_cli"):
            if not data["con_cli"].strip():
                return False, "El nombre del contacto es obligatorio."
            if not all(char.isalpha() or char.isspace() for char in data["con_cli"]):
                return False, "El nombre del contacto debe contener solo letras y espacios."

        if not es_actualizar or data.get("cod_cli"):
            if not data["cod_cli"] or not data["cod_cli"].startswith("C") or not data["cod_cli"][1:].isdigit():
                return False, "Código de cliente inválido. Debe comenzar con 'C' seguido de números (ej: C001)."
            if len(data["cod_cli"][1:]) < 3:
                return False, "El código de cliente debe tener al menos 3 caracteres numéricos después de 'C' (ej: C001)."
            # Verificar si el código de cliente ya existe
            codigos_existentes = [c[0] for c in ClienteCRUD.mostrar_clientes()]
            if data["cod_cli"] in codigos_existentes:
                return False, "El código de cliente ya existe. Por favor, utiliza un código único."

        if not es_actualizar or data.get("rso_cli"):
            if not data["rso_cli"]:
                return False, "La razón social no puede estar vacía."

        if not es_actualizar or data.get("dir_cli"):
            if not data["dir_cli"]:
                return False, "La dirección no puede estar vacía."

        if data.get("ruc_cli"):
            if not data["ruc_cli"].isdigit():
                return False, "El RUC debe contener solo números si se proporciona."

        if not es_actualizar or data.get("tlf_cli"):
            if not data["tlf_cli"].isdigit():
                return False, "El teléfono debe contener solo números."

        if not es_actualizar or data.get("cod_dis"):
            if not data["cod_dis"].startswith("D") or not data["cod_dis"][1:].isdigit():
                return False, "Código de distrito inválido. Debe comenzar con 'D' seguido de números (ej: D01)."
            # Validar si el distrito existe
            distritos_existentes = [d[0] for d in DistritoCRUD.listar_distritos()]
            if data["cod_dis"] not in distritos_existentes:
                return False, "El código de distrito no existe. Por favor, verifica el código."

        return True, ""

    # Campos agregar
    agregar_fields = {
        'cod_cli': ft.TextField(label="Código del cliente (ej: C001)"),
        'rso_cli': ft.TextField(label="Razón Social"),
        'dir_cli': ft.TextField(label="Dirección"),
        'tlf_cli': ft.TextField(label="Teléfono"),
        'ruc_cli': ft.TextField(label="RUC (opcional)"),
        'cod_dis': ft.TextField(label="Código del distrito (ej: D01)"),
        'fec_reg': ft.TextField(label="Fecha de registro (YYYY-MM-DD)"),
        'tip_cli': ft.TextField(label="Tipo de cliente"),
        'con_cli': ft.TextField(label="Nombre del contacto (obligatorio)")
    }

    def on_guardar_cliente(e):
        try:
            data = {k: f.value for k, f in agregar_fields.items()}
            data["ruc_cli"] = data["ruc_cli"] or None  # Make RUC optional

            valid, msg = validar_campos(data)
            if not valid:
                mostrar_mensaje(msg, success=False)
                return

            success, msg = ClienteCRUD.agregar_cliente(**data)
            mostrar_mensaje(msg, success)
            if success:
                for f in agregar_fields.values():
                    f.value = ""
        except Exception as ex:
            mostrar_mensaje(f"Error al guardar cliente: {ex}", success=False)

    # Mostrar tabla
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Código")),
            ft.DataColumn(label=ft.Text("Razón Social")),
            ft.DataColumn(label=ft.Text("Dirección")),
            ft.DataColumn(label=ft.Text("Teléfono")),
            ft.DataColumn(label=ft.Text("RUC")),
            ft.DataColumn(label=ft.Text("Distrito")),
            ft.DataColumn(label=ft.Text("Fecha Registro")),
            ft.DataColumn(label=ft.Text("Tipo")),
            ft.DataColumn(label=ft.Text("Contacto")),
        ],
        rows=[]
    )

    def cargar_clientes(e):
        try:
            clientes = ClienteCRUD.mostrar_clientes()
            datatable.rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in c])
                for c in clientes
            ]
            mostrar_mensaje("Clientes cargados correctamente")
        except Exception as ex:
            mostrar_mensaje(f"Error al cargar clientes: {ex}", success=False)

    # Actualizar
    actualizar_fields = {
        'cod_cli': ft.TextField(label="Código del cliente a actualizar (ej: C001)"),
        'rso_cli': ft.TextField(label="Nueva razón social (dejar vacío para omitir)"),
        'dir_cli': ft.TextField(label="Nueva dirección (dejar vacío para omitir)"),
        'tlf_cli': ft.TextField(label="Nuevo teléfono (dejar vacío para omitir)"),
        'ruc_cli': ft.TextField(label="Nuevo RUC (opcional, dejar vacío para omitir)"),
        'cod_dis': ft.TextField(label="Nuevo código de distrito (ej: D01, dejar vacío para omitir)"),
        'fec_reg': ft.TextField(label="Nueva fecha de registro (YYYY-MM-DD, dejar vacío para omitir)"),
        'tip_cli': ft.TextField(label="Nuevo tipo de cliente (dejar vacío para omitir)"),
        'con_cli': ft.TextField(label="Nuevo nombre del contacto (obligatorio, dejar vacío para omitir)")
    }

    def actualizar_cliente(e):
        try:
            data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}

            valid, msg = validar_campos(data, es_actualizar=True)
            if not valid:
                mostrar_mensaje(msg, success=False)
                return

            success, msg = ClienteCRUD.actualizar_cliente(**data)
            mostrar_mensaje(msg, success)
        except Exception as ex:
            mostrar_mensaje(f"Error al actualizar cliente: {ex}", success=False)

    # Eliminar
    def eliminar_cliente(e):
        try:
            if eliminar_dropdown.value:
                cod_cli = eliminar_dropdown.value.split(" - ")[0]
                success, msg = ClienteCRUD.eliminar_cliente(cod_cli)
                mostrar_mensaje(msg, success)
                cargar_clientes_para_eliminar()
            else:
                mostrar_mensaje("Selecciona un cliente para eliminar.", success=False)
        except Exception as ex:
            mostrar_mensaje(f"Error al eliminar cliente: {ex}", success=False)

    # UI
    return ft.View(
        route="/cliente",
        controls=[
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Clientes", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar la base de datos de clientes", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Cliente", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Clientes", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Cliente", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Cliente", on_click=lambda e: cambiar_formulario(form_eliminar)),
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
                            ft.Text("Agregar Nuevo Cliente", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Cliente", on_click=on_guardar_cliente, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Clientes", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Clientes", on_click=cargar_clientes, bgcolor="indigo", color="white"),
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
                            ft.Text("Actualizar Cliente", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Cliente", on_click=actualizar_cliente, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Cliente", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Cliente", on_click=eliminar_cliente, bgcolor="red", color="white")
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



