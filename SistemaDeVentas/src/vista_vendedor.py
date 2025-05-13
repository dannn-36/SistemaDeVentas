import flet as ft
import vendedor_crud
print(vendedor_crud.__file__)   # Confirmar ruta real
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

    # Campos agregar
    agregar_fields = {name: ft.TextField(label=label) for name, label in {
        'cod_ven': "Código del vendedor",
        'nom_ven': "Nombre",
        'ape_ven': "Apellido",
        'sue_ven': "Sueldo",
        'fin_ven': "Fecha de ingreso",
        'tip_ven': "Tipo de vendedor",
        'cod_dis': "Código del distrito"
    }.items()}

    def on_guardar_vendedor(e):
        data = {k: f.value for k, f in agregar_fields.items()}
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
    actualizar_fields = {name: ft.TextField(label=label) for name, label in {
        'cod_ven': "Código del vendedor a actualizar",
        'nom_ven': "Nuevo nombre",
        'ape_ven': "Nuevo apellido",
        'sue_ven': "Nuevo sueldo",
        'fin_ven': "Nueva fecha de ingreso",
        'tip_ven': "Nuevo tipo de vendedor",
        'cod_dis': "Nuevo código de distrito"
    }.items()}

    def actualizar_vendedor(e):
        data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}
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

    page.add(
        ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Vendedores", size=30, weight="bold", color="indigo"),
                    ft.Text("Interfaz para administrar la base de datos de vendedores", color="grey"),

                    ft.Row([
                        ft.TextButton("Agregar Vendedor", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Vendedores", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Vendedor", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Vendedor", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text(ref=mensaje),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        content=ft.Column([
                            ft.Text("Agregar Nuevo Vendedor", size=20, weight="semi-bold", color="indigo"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Vendedor", on_click=on_guardar_vendedor, bgcolor="indigo", color="white")
                        ])
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        content=ft.Column([
                            ft.Text("Lista de Vendedores", size=20, weight="semi-bold", color="indigo"),
                            ft.ElevatedButton("Cargar Vendedores", on_click=cargar_vendedores, bgcolor="indigo", color="white"),
                            datatable
                        ])
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        content=ft.Column([
                            ft.Text("Actualizar Vendedor", size=20, weight="semi-bold", color="indigo"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Vendedor", on_click=actualizar_vendedor, bgcolor="indigo", color="white")
                        ])
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        content=ft.Column([
                            ft.Text("Eliminar Vendedor", size=20, weight="semi-bold", color="indigo"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Vendedor", on_click=eliminar_vendedor, bgcolor="red", color="white")
                        ])
                    )
                ],
                spacing=25,
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        )
    )

ft.app(target=main)
