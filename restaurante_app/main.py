import tkinter as tk
from pathlib import Path

from modelos.usuario import Usuario

from servicios.archivo_servicio import (
    ArchivoServicio
)

from servicios.restaurante_servicio import (
    RestauranteServicio
)

from ui.login_view import LoginView
from ui.main_view import MainView


# =========================
# RUTAS
# =========================

CARPETA_DATOS = (
    Path(__file__).resolve().parent
    / "datos"
)

RUTA_PRODUCTOS = str(
    CARPETA_DATOS
    / "productos.json"
)

RUTA_USUARIOS = str(
    CARPETA_DATOS
    / "usuarios.json"
)

RUTA_VENTAS = str(
    CARPETA_DATOS
    / "ventas.json"
)


# =========================
# APLICACIÓN
# =========================

class Aplicacion:

    def __init__(
        self
    ) -> None:

        self.root = tk.Tk()

        self.root.title(
            "Restaurante App"
        )

        self.root.geometry(
            "1000x700"
        )

        archivo_servicio = ArchivoServicio(
            RUTA_PRODUCTOS,
            RUTA_USUARIOS,
            RUTA_VENTAS
        )

        productos = (
            archivo_servicio
            .cargar_productos()
        )

        usuarios = (
            archivo_servicio
            .cargar_usuarios()
        )

        ventas = (
            archivo_servicio
            .cargar_ventas()
        )

        self.restaurante_servicio = (
            RestauranteServicio(
                productos,
                usuarios,
                ventas,
                archivo_servicio
            )
        )

        self.mostrar_login()

    def mostrar_login(
        self
    ) -> None:

        LoginView(
            self.root,
            self.restaurante_servicio,
            self.mostrar_main
        )

    def mostrar_main(
        self,
        usuario_actual: Usuario
    ) -> None:

        MainView(
            self.root,
            self.restaurante_servicio,
            usuario_actual,
            self.mostrar_login
        )

    def ejecutar(
        self
    ) -> None:

        self.root.mainloop()


if __name__ == "__main__":

    aplicacion = Aplicacion()

    aplicacion.ejecutar()