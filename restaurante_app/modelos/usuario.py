class Usuario:

    ROLES = (
        "Administrador",
        "Empleado",
        "Cliente"
    )

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str
    ) -> None:

        self.identificacion = identificacion
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(
        self,
        valor: str
    ) -> None:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                "La identificación no puede estar vacía."
            )

        self._identificacion = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(
        self,
        valor: str
    ) -> None:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        self._nombre = valor

    @property
    def usuario(self) -> str:
        return self._usuario

    @usuario.setter
    def usuario(
        self,
        valor: str
    ) -> None:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                "El usuario no puede estar vacío."
            )

        self._usuario = valor

    @property
    def contrasena(self) -> str:
        return self._contrasena

    @contrasena.setter
    def contrasena(
        self,
        valor: str
    ) -> None:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

        self._contrasena = valor

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(
        self,
        valor: str
    ) -> None:

        valor = valor.strip().capitalize()

        if valor not in self.ROLES:
            raise ValueError(
                "El rol debe ser Administrador, "
                "Empleado o Cliente."
            )

        self._rol = valor

    def to_dict(self) -> dict:

        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @classmethod
    def from_dict(
        cls,
        datos: dict
    ):

        return cls(
            identificacion=str(
                datos["identificacion"]
            ),
            nombre=str(
                datos["nombre"]
            ),
            usuario=str(
                datos["usuario"]
            ),
            contrasena=str(
                datos["contrasena"]
            ),
            rol=str(
                datos.get(
                    "rol",
                    "Cliente"
                )
            )
        )

    def __str__(self) -> str:

        return (
            f"{self.identificacion} - "
            f"{self.nombre} - "
            f"{self.usuario} - "
            f"{self.rol}"
        )