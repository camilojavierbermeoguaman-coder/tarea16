import tkinter as tk
from pathlib import Path

from servicios.restaurante_servicio import RestauranteServicio


class LoginView:

    def __init__(
        self,
        root: tk.Tk,
        restaurante_servicio: RestauranteServicio,
        mostrar_main
    ) -> None:

        self.root = root
        self.restaurante_servicio = restaurante_servicio
        self.mostrar_main = mostrar_main

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.crear_componentes()

    def crear_componentes(self) -> None:

        # Logo desde la carpeta assets
        ruta_logo = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "logo.png"
        )

        self.logo = tk.PhotoImage(
            file=str(ruta_logo)
        )

        self.logo = self.logo.subsample(5, 5)

        tk.Label(
            self.frame,
            image=self.logo
        ).pack(pady=(20, 5))

        tk.Label(
            self.frame,
            text="SISTEMA DE RESTAURANTE",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        tk.Label(
            self.frame,
            text="Inicio de sesión",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            self.frame,
            text="Usuario:"
        ).pack()

        self.entrada_usuario = tk.Entry(
            self.frame,
            width=30
        )
        self.entrada_usuario.pack(pady=5)

        tk.Label(
            self.frame,
            text="Contraseña:"
        ).pack(pady=5)

        self.entrada_contrasena = tk.Entry(
            self.frame,
            width=30,
            show="*"
        )
        self.entrada_contrasena.pack(pady=5)

        self.mensaje = tk.Label(
            self.frame,
            text=""
        )
        self.mensaje.pack(pady=5)

        tk.Button(
            self.frame,
            text="Ingresar",
            width=20,
            command=self.ingresar
        ).pack(pady=15)

    def ingresar(self) -> None:

        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not usuario or not contrasena:
            self.mensaje.config(
                text="Ingrese usuario y contraseña."
            )
            return

        usuario_validado = (
            self.restaurante_servicio.validar_login(
                usuario,
                contrasena
            )
        )

        if usuario_validado is None:
            self.mensaje.config(
                text="Usuario o contraseña incorrectos."
            )
            return

        self.frame.destroy()
        self.mostrar_main(usuario_validado)