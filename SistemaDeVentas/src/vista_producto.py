import flet as ft
from producto_crud import ProductoCRUD


def main(page: ft.Page):
    page.title = "Sistema de Gestión de Productos"
    page.theme_mode = "light"
    page.scroll = "auto"

    form_agregar = ft.Ref[ft.Container]()
    form_mostrar = ft.Ref[ft.Container]()
    form_actualizar = ft.Ref[ft.Container]()
    form_eliminar = ft.Ref[ft.Container]()
    mensaje = ft.Ref[ft.Text]()

    eliminar_dropdown = ft.Dropdown(label="Selecciona un producto", options=[])

    def cargar_productos_para_eliminar():
        productos = ProductoCRUD.mostrar_productos()
        eliminar_dropdown.options = [
            ft.dropdown.Option(f"{p[0]} - {p[1]}") for p in productos
        ]
        eliminar_dropdown.value = None
        page.update()

    def cambiar_formulario(tab_ref):
        for ref in [form_agregar, form_mostrar, form_actualizar, form_eliminar]:
            ref.current.visible = False
        tab_ref.current.visible = True
        mensaje.current.value = ""
        if tab_ref == form_eliminar:
            cargar_productos_para_eliminar()
        page.update()

    def mostrar_mensaje(msg, success=True):
        mensaje.current.value = msg
        mensaje.current.color = "green" if success else "red"
        page.update()

    def validar_campos(data, es_actualizar=False):
        if not es_actualizar or data.get("cod_pro"):
            if not data["cod_pro"] or not data["cod_pro"].startswith("P") or not data["cod_pro"][1:].isdigit():
                return False, "Código inválido. Debe comenzar con 'P' seguido de números (ej: P01)."

        if not es_actualizar or data.get("des_pro"):
            if not data["des_pro"]:
                return False, "La descripción no puede estar vacía."

        if not es_actualizar or data.get("pre_pro"):
            try:
                float(data["pre_pro"])
            except:
                return False, "Precio inválido. Debe ser un número."

        if not es_actualizar or data.get("sac_pro"):
            try:
                int(data["sac_pro"])
            except:
                return False, "Stock actual debe ser un número entero."

        if not es_actualizar or data.get("smi_pro"):
            try:
                int(data["smi_pro"])
            except:
                return False, "Stock mínimo debe ser un número entero."

        if not es_actualizar or data.get("uni_pro"):
            if not data["uni_pro"]:
                return False, "La unidad no puede estar vacía."

        if not es_actualizar or data.get("lin_pro"):
            if not data["lin_pro"]:
                return False, "La línea del producto no puede estar vacía."

        if not es_actualizar or data.get("imp_pro"):
            try:
                float(data["imp_pro"])
            except:
                return False, "Impuesto inválido. Debe ser un número."

        return True, ""

    # Campos agregar
    agregar_fields = {
        'cod_pro': ft.TextField(label="Código del producto (ej: P01)"),
        'des_pro': ft.TextField(label="Descripción"),
        'pre_pro': ft.TextField(label="Precio"),
        'sac_pro': ft.TextField(label="Stock actual"),
        'smi_pro': ft.TextField(label="Stock mínimo"),
        'uni_pro': ft.TextField(label="Unidad"),
        'lin_pro': ft.TextField(label="Línea"),
        'imp_pro': ft.TextField(label="Impuesto")
    }

    def on_guardar_producto(e):
        data = {k: f.value for k, f in agregar_fields.items()}
        valid, msg = validar_campos(data)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return
        success, msg = ProductoCRUD.agregar_producto(**data)
        mostrar_mensaje(msg, success)
        if success:
            for f in agregar_fields.values():
                f.value = ""

    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Código")),
            ft.DataColumn(label=ft.Text("Descripción")),
            ft.DataColumn(label=ft.Text("Precio")),
            ft.DataColumn(label=ft.Text("Stock Actual")),
            ft.DataColumn(label=ft.Text("Stock Mínimo")),
            ft.DataColumn(label=ft.Text("Unidad")),
            ft.DataColumn(label=ft.Text("Línea")),
            ft.DataColumn(label=ft.Text("Impuesto")),
        ],
        rows=[]
    )

    def cargar_productos(e):
        productos = ProductoCRUD.mostrar_productos()
        datatable.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in p])
            for p in productos
        ]
        mostrar_mensaje("Productos cargados correctamente")

    # Campos actualizar
    actualizar_fields = {
        'cod_pro': ft.TextField(label="Código del producto a actualizar (ej: P01)"),
        'des_pro': ft.TextField(label="Nueva descripción (dejar vacío para omitir)"),
        'pre_pro': ft.TextField(label="Nuevo precio"),
        'sac_pro': ft.TextField(label="Nuevo stock actual"),
        'smi_pro': ft.TextField(label="Nuevo stock mínimo"),
        'uni_pro': ft.TextField(label="Nueva unidad"),
        'lin_pro': ft.TextField(label="Nueva línea"),
        'imp_pro': ft.TextField(label="Nuevo impuesto")
    }

    def actualizar_producto(e):
        data = {k: v.value if v.value != "" else None for k, v in actualizar_fields.items()}
        valid, msg = validar_campos(data, es_actualizar=True)
        if not valid:
            mostrar_mensaje(msg, success=False)
            return
        success, msg = ProductoCRUD.actualizar_producto(**data)
        mostrar_mensaje(msg, success)

    def eliminar_producto(e):
        if eliminar_dropdown.value:
            cod_pro = eliminar_dropdown.value.split(" - ")[0]
            success, msg = ProductoCRUD.eliminar_producto(cod_pro)
            mostrar_mensaje(msg, success)
            cargar_productos_para_eliminar()
        else:
            mostrar_mensaje("Selecciona un producto para eliminar.", success=False)

    # UI general
    return ft.View(
        route="/producto",
        controls=[
            
        ft.Container(
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Sistema de Gestión de Productos", size=30, weight="bold", color="indigo", text_align="center"),
                    ft.Text("Interfaz para administrar productos", color="grey", text_align="center"),

                    ft.Row([
                        ft.TextButton("Agregar Producto", on_click=lambda e: cambiar_formulario(form_agregar)),
                        ft.TextButton("Mostrar Productos", on_click=lambda e: cambiar_formulario(form_mostrar)),
                        ft.TextButton("Actualizar Producto", on_click=lambda e: cambiar_formulario(form_actualizar)),
                        ft.TextButton("Eliminar Producto", on_click=lambda e: cambiar_formulario(form_eliminar)),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text(ref=mensaje, text_align="center"),

                    # Agregar
                    ft.Container(
                        ref=form_agregar,
                        visible=True,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Agregar Nuevo Producto", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *agregar_fields.values(),
                            ft.ElevatedButton("Guardar Producto", on_click=on_guardar_producto, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Mostrar
                    ft.Container(
                        ref=form_mostrar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Lista de Productos", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            ft.ElevatedButton("Cargar Productos", on_click=cargar_productos, bgcolor="indigo", color="white"),
                            datatable
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Actualizar
                    ft.Container(
                        ref=form_actualizar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Actualizar Producto", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            *actualizar_fields.values(),
                            ft.ElevatedButton("Actualizar Producto", on_click=actualizar_producto, bgcolor="indigo", color="white")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # Eliminar
                    ft.Container(
                        ref=form_eliminar,
                        visible=False,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text("Eliminar Producto", size=20, weight="semi-bold", color="indigo", text_align="center"),
                            eliminar_dropdown,
                            ft.ElevatedButton("Eliminar Producto", on_click=eliminar_producto, bgcolor="red", color="white")
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



