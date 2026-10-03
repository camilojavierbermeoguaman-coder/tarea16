# restaurante_app

## Autor

Camilo Javier Bermeo Guaman

Aplicación desarrollada en Python para la gestión de un restaurante.

El proyecto permite administrar productos, usuarios y ventas mediante una interfaz gráfica creada con Tkinter.

## Funcionalidades

### Productos
- Registrar productos.
- Buscar productos.
- Actualizar productos.
- Eliminar productos.
- Controlar el stock.
- Guardar los cambios en JSON.

### Usuarios
- Registrar usuarios.
- Consultar usuarios.
- Actualizar usuarios.
- Eliminar usuarios.
- Manejar roles:
  - Administrador
  - Empleado
  - Cliente
- El administrador tiene acceso a la gestión de usuarios.
- Se evita eliminar la cuenta del administrador que tiene la sesión iniciada.

### Ventas
- Seleccionar un usuario.
- Seleccionar un producto.
- Registrar la cantidad vendida.
- Actualizar el stock.
- Guardar las ventas en JSON.

## Manejo de eventos

En la gestión de usuarios se implementaron eventos con `bind()`:

- `<<TreeviewSelect>>`: permite seleccionar un usuario de la tabla y cargar sus datos.
- `<<ComboboxSelected>>`: detecta el cambio del rol seleccionado.
- `<Return>`: permite registrar un usuario al presionar Enter.
- `<Escape>`: limpia los campos del formulario.

Los botones utilizan `command=` para ejecutar acciones como registrar, actualizar, eliminar y limpiar.

## Estructura del proyecto

restaurante_app/

- assets/
  - logo.png
  - producto.png
  - usuario.png
  - venta.png
- datos/
  - productos.json
  - usuarios.json
  - venta.json
- modelos/
  - producto.py
  - usuario.py
  - venta.py
- servicios/
  - archivo_servicio.py
  - restaurante_servicio.py
- ui/
  - login_view.py
  - main_view.py
- main.py
- README.md

## Persistencia

La información se almacena en archivos JSON.

Los cambios realizados en productos, usuarios y ventas se guardan mediante `ArchivoServicio`.

## Interfaz gráfica

La aplicación utiliza Tkinter para mostrar:

- Inicio de sesión.
- Gestión de productos.
- Gestión de usuarios.
- Gestión de ventas.

La carpeta `assets` contiene las imágenes utilizadas en la interfaz.

## Ejecución

Para iniciar la aplicación se debe ejecutar:

python main.py