import flet as ft
from client_crud import ClienteCRUD  # ajusta el import según tu estructura real

def main(page: ft.Page):
    page.title = "CRUD de Clientes"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS

    inputs = {
        "cod_cli": ft.TextField(label="Código Cliente"),
        "rso_cli": ft.TextField(label="Razón Social"),
        "dir_cli": ft.TextField(label="Dirección"),
        "tlf_cli": ft.TextField(label="Teléfono"),
        "ruc_cli": ft.TextField(label="RUC"),
        "cod_dis": ft.TextField(label="Código Distrito"),
        "fec_reg": ft.TextField(label="Fecha Registro (YYYY-MM-DD)"),
        "tip_cli": ft.TextField(label="Tipo Cliente"),
        "con_cli": ft.TextField(label="Condición Cliente"),
    }

    output = ft.Text()

    def crear_cliente(e):
        try:
            ClienteCRUD.crear_cliente(
                inputs["cod_cli"].value,
                inputs["rso_cli"].value,
                inputs["dir_cli"].value,
                inputs["tlf_cli"].value,
                inputs["ruc_cli"].value,
                inputs["cod_dis"].value,
                inputs["fec_reg"].value,
                inputs["tip_cli"].value,
                inputs["con_cli"].value
            )
            output.value = "Cliente creado exitosamente."
        except Exception as ex:
            output.value = f"Error: {ex}"
        page.update()

    def leer_clientes(e):
        try:
            clientes = ClienteCRUD.leer_clientes()
            output.value = "\n".join(str(cliente) for cliente in clientes) if clientes else "No hay clientes registrados."
        except Exception as ex:
            output.value = f"Error: {ex}"
        page.update()

    def actualizar_cliente(e):
        try:
            ClienteCRUD.actualizar_cliente(
                inputs["cod_cli"].value,
                rso_cli=inputs["rso_cli"].value,
                dir_cli=inputs["dir_cli"].value,
                tlf_cli=inputs["tlf_cli"].value,
                ruc_cli=inputs["ruc_cli"].value,
                cod_dis=inputs["cod_dis"].value,
                fec_reg=inputs["fec_reg"].value,
                tip_cli=inputs["tip_cli"].value,
                con_cli=inputs["con_cli"].value
            )
            output.value = "Cliente actualizado exitosamente."
        except Exception as ex:
            output.value = f"Error: {ex}"
        page.update()

    def eliminar_cliente(e):
        try:
            ClienteCRUD.eliminar_cliente(inputs["cod_cli"].value)
            output.value = f"Cliente con código {inputs['cod_cli'].value} eliminado."
        except Exception as ex:
            output.value = f"Error: {ex}"
        page.update()

    botones = ft.Row([
        ft.ElevatedButton("Crear", on_click=crear_cliente),
        ft.ElevatedButton("Leer", on_click=leer_clientes),
        ft.ElevatedButton("Actualizar", on_click=actualizar_cliente),
        ft.ElevatedButton("Eliminar", on_click=eliminar_cliente),
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    page.add(
        ft.Column(
            [inputs[k] for k in inputs] + [botones, output],
            expand=True,
        )
    )

ft.app(target=main)
