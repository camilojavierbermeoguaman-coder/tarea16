import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario


class MainView:

    def __init__(
        self, root, restaurante_servicio,
        usuario_actual, cerrar_sesion
    ):
        self.root = root
        self.servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.cerrar_sesion = cerrar_sesion

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.cargar_imagenes()
        self.crear_componentes()

    # =========================
    # GENERAL
    # =========================

    def cargar_imagenes(self):
        carpeta = Path(__file__).resolve().parent.parent / "assets"

        self.img_producto = tk.PhotoImage(
            file=str(carpeta / "producto.png")
        ).subsample(12, 12)

        self.img_usuario = tk.PhotoImage(
            file=str(carpeta / "usuario.png")
        ).subsample(12, 12)

        self.img_venta = tk.PhotoImage(
            file=str(carpeta / "venta.png")
        ).subsample(12, 12)

    def crear_componentes(self):
        tk.Label(
            self.frame,
            text="PANEL PRINCIPAL DEL RESTAURANTE",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        tk.Label(
            self.frame,
            text=f"Bienvenido, {self.usuario_actual.nombre}"
        ).pack()

        self.resumen = tk.Label(self.frame)
        self.resumen.pack(pady=5)
        self.actualizar_resumen()

        menu = tk.Frame(self.frame)
        menu.pack(pady=10)

        opciones = [
            ("Productos", self.img_producto, self.mostrar_productos)
        ]

        if self.usuario_actual.rol == "Administrador":
            opciones.append(
                ("Usuarios", self.img_usuario, self.mostrar_usuarios)
            )

        opciones.append(
            ("Ventas", self.img_venta, self.mostrar_ventas)
        )

        for i, (texto, imagen, comando) in enumerate(opciones):
            tk.Button(
                menu,
                text=texto,
                image=imagen,
                compound="left",
                width=160,
                command=comando
            ).grid(row=0, column=i, padx=5)

        self.contenedor = tk.Frame(self.frame)
        self.contenedor.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        tk.Button(
            self.frame,
            text="Cerrar sesión",
            command=self.salir
        ).pack(pady=10)

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def actualizar_resumen(self):
        self.resumen.config(
            text=(
                f"Productos: {self.servicio.cantidad_productos()} | "
                f"Usuarios: {self.servicio.cantidad_usuarios()} | "
                f"Ventas: {self.servicio.cantidad_ventas()}"
            )
        )

    # =========================
    # PRODUCTOS
    # =========================

    def mostrar_productos(self):
        self.limpiar_contenedor()

        tk.Label(
            self.contenedor,
            text="Gestión de productos",
            font=("Arial", 13, "bold")
        ).pack(pady=5)

        form = ttk.LabelFrame(
            self.contenedor,
            text="Datos del producto"
        )
        form.pack(fill="x", padx=10, pady=10)

        nombres = (
            "Código", "Nombre", "Categoría",
            "Precio", "Stock"
        )

        self.campos_producto = []

        for i, nombre in enumerate(nombres):
            fila = i // 2
            columna = (i % 2) * 2

            tk.Label(
                form,
                text=f"{nombre}:"
            ).grid(row=fila, column=columna, padx=5, pady=5)

            entrada = tk.Entry(form, width=22)
            entrada.grid(
                row=fila, column=columna + 1,
                padx=5, pady=5
            )

            self.campos_producto.append(entrada)

        acciones = tk.Frame(self.contenedor)
        acciones.pack()

        botones = (
            ("Registrar", self.registrar_producto),
            ("Cargar", self.cargar_producto),
            ("Actualizar", self.actualizar_producto),
            ("Eliminar", self.eliminar_producto),
            ("Limpiar", self.limpiar_producto)
        )

        for i, (texto, comando) in enumerate(botones):
            tk.Button(
                acciones,
                text=texto,
                command=comando
            ).grid(row=0, column=i, padx=4)

        columnas = (
            "codigo", "nombre", "categoria",
            "precio", "stock"
        )

        self.tabla_productos = ttk.Treeview(
            self.contenedor,
            columns=columnas,
            show="headings"
        )

        for columna, titulo in zip(columnas, nombres):
            self.tabla_productos.heading(
                columna,
                text=titulo
            )

        self.tabla_productos.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.actualizar_productos()

    def datos_producto(self):
        return [
            campo.get().strip()
            for campo in self.campos_producto
        ]

    def registrar_producto(self):
        try:
            codigo, nombre, categoria, precio, stock = (
                self.datos_producto()
            )

            producto = Producto(
                codigo, nombre, categoria,
                float(precio), int(stock)
            )

            if not self.servicio.registrar_producto(producto):
                raise ValueError(
                    "El código ya está registrado."
                )

            messagebox.showinfo(
                "Producto",
                "Producto registrado."
            )

            self.actualizar_productos()
            self.actualizar_resumen()
            self.limpiar_producto()

        except ValueError as error:
            messagebox.showerror("Producto", str(error))

    def cargar_producto(self):
        codigo = self.campos_producto[0].get().strip()
        producto = self.servicio.buscar_producto(codigo)

        if not producto:
            messagebox.showwarning(
                "Producto",
                "Producto no encontrado."
            )
            return

        datos = (
            producto.codigo,
            producto.nombre,
            producto.categoria,
            producto.precio,
            producto.stock
        )

        self.limpiar_producto()

        for campo, valor in zip(
            self.campos_producto, datos
        ):
            campo.insert(0, str(valor))

    def actualizar_producto(self):
        try:
            codigo, nombre, categoria, precio, stock = (
                self.datos_producto()
            )

            resultado = self.servicio.actualizar_producto(
                codigo,
                nombre,
                categoria,
                float(precio),
                int(stock)
            )

            if not resultado:
                raise ValueError(
                    "Producto no encontrado."
                )

            messagebox.showinfo(
                "Producto",
                "Producto actualizado."
            )

            self.actualizar_productos()
            self.limpiar_producto()

        except ValueError as error:
            messagebox.showerror("Producto", str(error))

    def eliminar_producto(self):
        codigo = self.campos_producto[0].get().strip()
        producto = self.servicio.buscar_producto(codigo)

        if not producto:
            messagebox.showwarning(
                "Producto",
                "Producto no encontrado."
            )
            return

        if messagebox.askyesno(
            "Eliminar",
            f"¿Eliminar {producto.nombre}?"
        ):
            self.servicio.eliminar_producto(codigo)
            self.actualizar_productos()
            self.actualizar_resumen()
            self.limpiar_producto()

    def limpiar_producto(self):
        for campo in self.campos_producto:
            campo.delete(0, tk.END)

    def actualizar_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for p in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    p.codigo,
                    p.nombre,
                    p.categoria,
                    f"${p.precio:.2f}",
                    p.stock
                )
            )

    # =========================
    # USUARIOS
    # =========================

    def mostrar_usuarios(self):
        self.limpiar_contenedor()

        tk.Label(
            self.contenedor,
            text="Gestión de usuarios",
            font=("Arial", 13, "bold")
        ).pack(pady=5)

        form = ttk.LabelFrame(
            self.contenedor,
            text="Datos del usuario"
        )
        form.pack(fill="x", padx=10, pady=10)

        nombres = (
            "Identificación",
            "Nombre",
            "Usuario",
            "Contraseña"
        )

        self.campos_usuario = []

        for i, nombre in enumerate(nombres):
            fila = i // 2
            columna = (i % 2) * 2

            tk.Label(
                form,
                text=f"{nombre}:"
            ).grid(row=fila, column=columna, padx=5, pady=5)

            campo = tk.Entry(
                form,
                width=22,
                show="*" if nombre == "Contraseña" else ""
            )

            campo.grid(
                row=fila,
                column=columna + 1,
                padx=5,
                pady=5
            )

            self.campos_usuario.append(campo)

        tk.Label(
            form,
            text="Rol:"
        ).grid(row=2, column=0)

        self.combo_rol = ttk.Combobox(
            form,
            values=("Empleado", "Cliente"),
            state="readonly",
            width=19
        )
        self.combo_rol.grid(row=2, column=1, pady=5)
        self.combo_rol.set("Cliente")

        self.label_rol = tk.Label(
            form,
            text="Rol: Cliente"
        )
        self.label_rol.grid(
            row=2,
            column=2,
            columnspan=2
        )

        acciones = tk.Frame(self.contenedor)
        acciones.pack()

        botones = (
            ("Registrar", self.registrar_usuario),
            ("Actualizar", self.actualizar_usuario),
            ("Eliminar", self.eliminar_usuario),
            ("Limpiar", self.limpiar_usuario)
        )

        for i, (texto, comando) in enumerate(botones):
            tk.Button(
                acciones,
                text=texto,
                command=comando
            ).grid(row=0, column=i, padx=5)

        columnas = (
            "identificacion",
            "nombre",
            "usuario",
            "rol"
        )

        self.tabla_usuarios = ttk.Treeview(
            self.contenedor,
            columns=columnas,
            show="headings"
        )

        for columna, titulo in zip(
            columnas,
            ("Identificación", "Nombre", "Usuario", "Rol")
        ):
            self.tabla_usuarios.heading(
                columna,
                text=titulo
            )

        self.tabla_usuarios.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Eventos de Semana 16
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_usuario
        )

        self.combo_rol.bind(
            "<<ComboboxSelected>>",
            self.cambiar_rol
        )

        for campo in (
            *self.campos_usuario,
            self.combo_rol
        ):
            campo.bind(
                "<Return>",
                self.evento_registrar
            )
            campo.bind(
                "<Escape>",
                self.evento_limpiar
            )

        self.actualizar_usuarios()

    def datos_usuario(self):
        datos = [
            campo.get().strip()
            for campo in self.campos_usuario
        ]
        return datos + [self.combo_rol.get()]

    def registrar_usuario(self):
        try:
            identificacion, nombre, login, clave, rol = (
                self.datos_usuario()
            )

            usuario = Usuario(
                identificacion,
                nombre,
                login,
                clave,
                rol
            )

            if not self.servicio.registrar_usuario(usuario):
                raise ValueError(
                    "Identificación o usuario repetido."
                )

            messagebox.showinfo(
                "Usuario",
                "Usuario registrado."
            )

            self.actualizar_usuarios()
            self.actualizar_resumen()
            self.limpiar_usuario()

        except ValueError as error:
            messagebox.showerror("Usuario", str(error))

    def actualizar_usuario(self):
        try:
            identificacion, nombre, login, clave, rol = (
                self.datos_usuario()
            )

            usuario = self.servicio.buscar_usuario(
                identificacion
            )

            if not usuario:
                raise ValueError(
                    "Usuario no encontrado."
                )

            if identificacion == self.usuario_actual.identificacion:
                rol = "Administrador"

            resultado = self.servicio.actualizar_usuario(
                identificacion,
                nombre,
                login,
                clave,
                rol
            )

            if not resultado:
                raise ValueError(
                    "No se pudo actualizar."
                )

            messagebox.showinfo(
                "Usuario",
                "Usuario actualizado."
            )

            self.actualizar_usuarios()
            self.limpiar_usuario()

        except ValueError as error:
            messagebox.showerror("Usuario", str(error))

    def eliminar_usuario(self):
        identificacion = (
            self.campos_usuario[0]
            .get()
            .strip()
        )

        usuario = self.servicio.buscar_usuario(
            identificacion
        )

        if not usuario:
            messagebox.showwarning(
                "Usuario",
                "Usuario no encontrado."
            )
            return

        if identificacion == self.usuario_actual.identificacion:
            messagebox.showwarning(
                "Usuario",
                "No puede eliminar su propia cuenta."
            )
            return

        if messagebox.askyesno(
            "Eliminar",
            f"¿Eliminar a {usuario.nombre}?"
        ):
            self.servicio.eliminar_usuario(
                identificacion,
                self.usuario_actual.identificacion
            )

            self.actualizar_usuarios()
            self.actualizar_resumen()
            self.limpiar_usuario()

    def seleccionar_usuario(self, event=None):
        seleccion = self.tabla_usuarios.selection()

        if not seleccion:
            return

        valores = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )

        usuario = self.servicio.buscar_usuario(
            str(valores[0])
        )

        if not usuario:
            return

        self.limpiar_usuario(False)

        datos = (
            usuario.identificacion,
            usuario.nombre,
            usuario.usuario,
            usuario.contrasena
        )

        for campo, valor in zip(
            self.campos_usuario,
            datos
        ):
            campo.insert(0, valor)

        self.combo_rol.set(usuario.rol)
        self.cambiar_rol()

    def cambiar_rol(self, event=None):
        self.label_rol.config(
            text=f"Rol: {self.combo_rol.get()}"
        )

    def evento_registrar(self, event=None):
        self.registrar_usuario()

    def evento_limpiar(self, event=None):
        self.limpiar_usuario()

    def limpiar_usuario(self, seleccion=True):
        for campo in self.campos_usuario:
            campo.delete(0, tk.END)

        self.combo_rol.set("Cliente")
        self.cambiar_rol()

        if seleccion:
            for item in self.tabla_usuarios.selection():
                self.tabla_usuarios.selection_remove(item)

    def actualizar_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for u in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                "end",
                values=(
                    u.identificacion,
                    u.nombre,
                    u.usuario,
                    u.rol
                )
            )

    # =========================
    # VENTAS
    # =========================

    def mostrar_ventas(self):
        self.limpiar_contenedor()

        tk.Label(
            self.contenedor,
            text="Gestión de ventas",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        form = ttk.LabelFrame(
            self.contenedor,
            text="Registrar venta"
        )
        form.pack(fill="x", padx=10, pady=10)

        self.usuarios_venta = {
            f"{u.identificacion} - {u.nombre}":
            u.identificacion
            for u in self.servicio.listar_usuarios()
        }

        self.productos_venta = {
            f"{p.codigo} - {p.nombre}":
            p.codigo
            for p in self.servicio.listar_productos()
        }

        tk.Label(form, text="Usuario:").grid(
            row=0, column=0, padx=5
        )

        self.combo_usuario = ttk.Combobox(
            form,
            values=list(self.usuarios_venta),
            state="readonly",
            width=25
        )
        self.combo_usuario.grid(
            row=0, column=1, padx=5
        )

        tk.Label(form, text="Producto:").grid(
            row=0, column=2, padx=5
        )

        self.combo_producto = ttk.Combobox(
            form,
            values=list(self.productos_venta),
            state="readonly",
            width=25
        )
        self.combo_producto.grid(
            row=0, column=3, padx=5
        )

        tk.Label(form, text="Cantidad:").grid(
            row=1, column=0, pady=10
        )

        self.cantidad = tk.Entry(form, width=15)
        self.cantidad.grid(row=1, column=1)

        tk.Button(
            form,
            text="Registrar venta",
            command=self.registrar_venta
        ).grid(
            row=1,
            column=2,
            columnspan=2
        )

        columnas = (
            "usuario",
            "producto",
            "cantidad",
            "fecha"
        )

        self.tabla_ventas = ttk.Treeview(
            self.contenedor,
            columns=columnas,
            show="headings"
        )

        for columna, titulo in zip(
            columnas,
            ("Usuario", "Producto", "Cantidad", "Fecha")
        ):
            self.tabla_ventas.heading(
                columna,
                text=titulo
            )

        self.tabla_ventas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.actualizar_ventas()

    def registrar_venta(self):
        try:
            usuario = self.combo_usuario.get()
            producto = self.combo_producto.get()

            if not usuario or not producto:
                raise ValueError(
                    "Seleccione usuario y producto."
                )

            self.servicio.registrar_venta(
                self.usuarios_venta[usuario],
                self.productos_venta[producto],
                int(self.cantidad.get())
            )

            messagebox.showinfo(
                "Venta",
                "Venta registrada."
            )

            self.actualizar_ventas()
            self.actualizar_resumen()

        except ValueError as error:
            messagebox.showerror("Venta", str(error))

    def actualizar_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for v in self.servicio.listar_ventas():
            usuario = self.servicio.buscar_usuario(
                v.usuario_id
            )
            producto = self.servicio.buscar_producto(
                v.producto_codigo
            )

            self.tabla_ventas.insert(
                "",
                "end",
                values=(
                    usuario.nombre if usuario else v.usuario_id,
                    producto.nombre if producto
                    else v.producto_codigo,
                    v.cantidad,
                    v.fecha
                )
            )

    # =========================
    # SALIR
    # =========================

    def salir(self):
        self.frame.destroy()
        self.cerrar_sesion()