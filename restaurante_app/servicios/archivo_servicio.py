import json
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:

    def __init__(
        self,
        ruta_productos: str,
        ruta_usuarios: str,
        ruta_ventas: str
    ) -> None:

        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios
        self.ruta_ventas = ruta_ventas

    def cargar(
        self,
        ruta: str,
        clase
    ) -> list:

        try:
            ruta_archivo = Path(ruta)

            if not ruta_archivo.exists():
                return []

            with open(
                ruta_archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, list):
                print(
                    "Error: el archivo debe contener una lista."
                )
                return []

            return [
                clase.from_dict(dato)
                for dato in datos
            ]

        except json.JSONDecodeError:
            print(
                f"Error: {ruta} no contiene un JSON válido."
            )
            return []

        except (KeyError, ValueError) as error:
            print(
                f"Error en los datos: {error}"
            )
            return []

        except OSError as error:
            print(
                f"Error al cargar: {error}"
            )
            return []

    def guardar(
        self,
        datos: list,
        ruta: str
    ) -> bool:

        try:
            ruta_archivo = Path(ruta)

            ruta_archivo.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            datos_json = [
                objeto.to_dict()
                for objeto in datos
            ]

            with open(
                ruta_archivo,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    datos_json,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except (OSError, TypeError) as error:
            print(
                f"Error al guardar: {error}"
            )
            return False

    def cargar_productos(
        self
    ) -> list[Producto]:

        return self.cargar(
            self.ruta_productos,
            Producto
        )

    def cargar_usuarios(
        self
    ) -> list[Usuario]:

        return self.cargar(
            self.ruta_usuarios,
            Usuario
        )

    def cargar_ventas(
        self
    ) -> list[Venta]:

        return self.cargar(
            self.ruta_ventas,
            Venta
        )

    def guardar_productos(
        self,
        productos: list[Producto]
    ) -> bool:

        return self.guardar(
            productos,
            self.ruta_productos
        )

    def guardar_usuarios(
        self,
        usuarios: list[Usuario]
    ) -> bool:

        return self.guardar(
            usuarios,
            self.ruta_usuarios
        )

    def guardar_ventas(
        self,
        ventas: list[Venta]
    ) -> bool:

        return self.guardar(
            ventas,
            self.ruta_ventas
        )