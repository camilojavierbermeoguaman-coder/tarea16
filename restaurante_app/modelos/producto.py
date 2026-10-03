class Producto:

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        valor = valor.strip()

        if not valor:
            raise ValueError(
                "El código no puede estar vacío."
            )

        self._codigo = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = valor.strip()

        if not valor:
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        self._nombre = valor

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        valor = valor.strip()

        if not valor:
            raise ValueError(
                "La categoría no puede estar vacía."
            )

        self._categoria = valor.capitalize()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError(
                "El precio debe ser mayor que cero."
            )

        self._precio = valor

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise ValueError(
                "El stock debe ser un número entero."
            )

        if valor < 0:
            raise ValueError(
                "El stock no puede ser negativo."
            )

        self._stock = valor

    def vender(
        self,
        cantidad: int
    ) -> None:
        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        if cantidad > self.stock:
            raise ValueError(
                "No existe suficiente stock disponible."
            )

        self.stock -= cantidad

    def to_dict(
        self
    ) -> dict[str, object]:

        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def from_dict(
        cls,
        datos: dict[str, object]
    ) -> "Producto":

        return cls(
            codigo=str(
                datos["codigo"]
            ),
            nombre=str(
                datos["nombre"]
            ),
            categoria=str(
                datos["categoria"]
            ),
            precio=float(
                datos["precio"]
            ),
            stock=int(
                datos["stock"]
            )
        )

    def __str__(
        self
    ) -> str:

        return (
            f"Código: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock}"
        )