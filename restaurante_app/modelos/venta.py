from datetime import datetime


class Venta:

    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int,
        fecha: str
    ) -> None:

        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad
        self.fecha = fecha

    @property
    def usuario_id(self) -> str:
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(
        self,
        valor: str
    ) -> None:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                "El usuario no puede estar vacío."
            )

        self._usuario_id = valor

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(
        self,
        valor: str
    ) -> None:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                "El producto no puede estar vacío."
            )

        self._producto_codigo = valor

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(
        self,
        valor: int
    ) -> None:

        if not isinstance(valor, int):
            raise ValueError(
                "La cantidad debe ser un número entero."
            )

        if valor <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        self._cantidad = valor

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(
        self,
        valor: str
    ) -> None:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                "La fecha no puede estar vacía."
            )

        self._fecha = valor

    @classmethod
    def crear(
        cls,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int
    ) -> "Venta":

        fecha = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return cls(
            usuario_id,
            producto_codigo,
            cantidad,
            fecha
        )

    def to_dict(
        self
    ) -> dict[str, object]:

        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(
        cls,
        datos: dict[str, object]
    ) -> "Venta":

        return cls(
            usuario_id=str(
                datos["usuario_id"]
            ),
            producto_codigo=str(
                datos["producto_codigo"]
            ),
            cantidad=int(
                datos["cantidad"]
            ),
            fecha=str(
                datos["fecha"]
            )
        )