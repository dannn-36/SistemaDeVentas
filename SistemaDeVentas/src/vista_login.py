import flet as ft
from database_connection import DatabaseConnection

def main(page: ft.Page) -> ft.View:
    # Inputs
    usuario_input = ft.TextField(label="Usuario", autofocus=True, width=300)
    contrasena_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    mensaje = ft.Text(value="", color="red")

    def on_login(e):
        usuario = usuario_input.value.strip()
        contrasena = contrasena_input.value.strip()

        if not usuario or not contrasena:
            mensaje.value = "⚠️ Usuario y contraseña son obligatorios."
            page.update()
            return

        DatabaseConnection.set_credentials(usuario, contrasena)

        conexion = DatabaseConnection.conexionBaseDeDatos()
        if conexion:
            page.go("/menu")
        else:
            mensaje.value = "❌ Credenciales incorrectas o error en la conexión."
            page.update()

    login_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Iniciar Sesión", size=30, weight="bold"),
                usuario_input,
                contrasena_input,
                ft.ElevatedButton("Ingresar", icon=ft.Icons.LOGIN, on_click=on_login),
                mensaje
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=400,
        padding=30,
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=ft.Colors.GREY_400,
            offset=ft.Offset(0, 4)
        ),
        alignment=ft.alignment.center
    )

    # Crear y retornar la vista completa
    return ft.View(
        "/",
        controls=[
            login_card
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#f2f2f7",
        padding=40
    )
