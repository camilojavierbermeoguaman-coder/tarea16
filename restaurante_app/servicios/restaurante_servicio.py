from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:

    def __init__(
        self,
        productos,
        usuarios,
        ventas,
        archivo_servicio
    ) -> None:

        self.productos = productos
        self.usuarios = usuarios
        self.ventas = ventas
        self.archivo_servicio = archivo_servicio

        self.productos_por_codigo = {}
        self.usuarios_por_identificacion = {}
        self.categorias = set()

        self.reconstruir_indices()

    # =========================
    # PRODUCTOS
    # =========================

    def registrar_producto(
        self,
        producto: Producto
    ) -> bool:

        if self.buscar_producto(
            producto.codigo
        ) is not None:
            return False

        self.productos.append(
            producto
        )

        self.reconstruir_indices()

        self.archivo_servicio.guardar_productos(
            self.productos
        )

        return True

    def buscar_producto(
        self,
        codigo: str
    ):

        return self.productos_por_codigo.get(
            codigo
        )

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> bool:

        producto = self.buscar_producto(
            codigo
        )

        if producto is None:
            return False

        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock

        self.reconstruir_indices()

        self.archivo_servicio.guardar_productos(
            self.productos
        )

        return True

    def eliminar_producto(
        self,
        codigo: str
    ) -> bool:

        producto = self.buscar_producto(
            codigo
        )

        if producto is None:
            return False

        self.productos.remove(
            producto
        )

        self.reconstruir_indices()

        self.archivo_servicio.guardar_productos(
            self.productos
        )

        return True

    def listar_productos(
        self
    ):

        return self.productos

    def cantidad_productos(
        self
    ) -> int:

        return len(
            self.productos
        )

    # =========================
    # USUARIOS
    # =========================

    def registrar_usuario(
        self,
        usuario: Usuario
    ) -> bool:

        if self.buscar_usuario(
            usuario.identificacion
        ) is not None:
            return False

        for usuario_existente in self.usuarios:

            if (
                usuario_existente.usuario
                == usuario.usuario
            ):
                return False

        self.usuarios.append(
            usuario
        )

        self.reconstruir_indices()

        self.archivo_servicio.guardar_usuarios(
            self.usuarios
        )

        return True

    def buscar_usuario(
        self,
        identificacion: str
    ):

        return (
            self.usuarios_por_identificacion
            .get(identificacion)
        )

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str
    ) -> bool:

        usuario_objeto = (
            self.buscar_usuario(
                identificacion
            )
        )

        if usuario_objeto is None:
            return False

        for otro_usuario in self.usuarios:

            if (
                otro_usuario.usuario == usuario
                and
                otro_usuario.identificacion
                != identificacion
            ):
                return False

        usuario_objeto.nombre = nombre
        usuario_objeto.usuario = usuario
        usuario_objeto.contrasena = contrasena
        usuario_objeto.rol = rol

        self.reconstruir_indices()

        self.archivo_servicio.guardar_usuarios(
            self.usuarios
        )

        return True

    def eliminar_usuario(
        self,
        identificacion: str,
        identificacion_actual: str
    ) -> bool:

        if (
            identificacion
            == identificacion_actual
        ):
            return False

        usuario = self.buscar_usuario(
            identificacion
        )

        if usuario is None:
            return False

        self.usuarios.remove(
            usuario
        )

        self.reconstruir_indices()

        self.archivo_servicio.guardar_usuarios(
            self.usuarios
        )

        return True

    def listar_usuarios(
        self
    ):

        return self.usuarios

    def cantidad_usuarios(
        self
    ) -> int:

        return len(
            self.usuarios
        )

    # =========================
    # VENTAS
    # =========================

    def registrar_venta(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int
    ):

        usuario = self.buscar_usuario(
            usuario_id
        )

        if usuario is None:
            raise ValueError(
                "Usuario no encontrado."
            )

        producto = self.buscar_producto(
            producto_codigo
        )

        if producto is None:
            raise ValueError(
                "Producto no encontrado."
            )

        producto.vender(
            cantidad
        )

        venta = Venta.crear(
            usuario_id,
            producto_codigo,
            cantidad
        )

        self.ventas.append(
            venta
        )

        self.archivo_servicio.guardar_productos(
            self.productos
        )

        self.archivo_servicio.guardar_ventas(
            self.ventas
        )

        return venta

    def listar_ventas(
        self
    ):

        return self.ventas

    def cantidad_ventas(
        self
    ) -> int:

        return len(
            self.ventas
        )

    # =========================
    # LOGIN
    # =========================

    def validar_login(
        self,
        usuario: str,
        contrasena: str
    ):

        for usuario_objeto in self.usuarios:

            if (
                usuario_objeto.usuario
                == usuario
                and
                usuario_objeto.contrasena
                == contrasena
            ):
                return usuario_objeto

        return None

    # =========================
    # CATEGORÍAS
    # =========================

    def obtener_categorias(
        self
    ):

        return sorted(
            self.categorias
        )

    # =========================
    # ÍNDICES
    # =========================

    def reconstruir_indices(
        self
    ) -> None:

        self.productos_por_codigo = {
            producto.codigo: producto
            for producto in self.productos
        }

        self.usuarios_por_identificacion = {
            usuario.identificacion: usuario
            for usuario in self.usuarios
        }

        self.categorias = {
            producto.categoria
            for producto in self.productos
        }