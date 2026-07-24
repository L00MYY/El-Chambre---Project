# Postman

Colección ejecutable de los 31 endpoints de El Chambre.

## Preparación

Reiniciar la base de datos:

```powershell
python scripts\reset_db.py --yes
```

Iniciar la API:

```powershell
$env:PYTHONPATH="$PWD\src"
python -m flask --app el_chambre.api.app run
```

Ejecutar la colección desde otra terminal:

```powershell
postman collection run postman/collections/El-Chambre-API `
  -e postman/environments/Local.environment.yaml `
  --bail
```

La colección debe ejecutarse en orden sobre una base vacía. Las solicitudes de
creación guardan los identificadores utilizados por las solicitudes siguientes.

## Variables

| Variable | Uso |
| --- | --- |
| `base_url` | Dirección de la API. Por defecto: `http://localhost:5000`. |
| `id_sucursal` | Sucursal creada durante la ejecución. |
| `id_producto` | Producto creado durante la ejecución. |
| `id_materia` | Materia prima creada durante la ejecución. |
| `id_venta` | Venta registrada durante la ejecución. |
| `id_produccion` | Producción registrada durante la ejecución. |

## Endpoints

### General

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| GET | `/` | Comprueba que la API esté disponible. Incluye `Demo`. | 200 |

### Sucursales

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| POST | `/sucursales` | Crea una sucursal y guarda `id_sucursal`. Incluye `Demo`. | 201 |
| GET | `/sucursales` | Lista las sucursales. | 200 |
| GET | `/sucursales/{id_sucursal}` | Obtiene una sucursal. Incluye `Demo`. | 200 |
| PUT | `/sucursales/{id_sucursal}` | Actualiza una sucursal. | 200 |

### Productos

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| POST | `/productos` | Crea un producto y guarda `id_producto`. Incluye `Demo`. | 201 |
| GET | `/productos` | Lista los productos. | 200 |
| GET | `/productos/{id_producto}` | Obtiene un producto. | 200 |
| PUT | `/productos/{id_producto}` | Actualiza un producto. | 200 |

### Materias primas

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| POST | `/materias-primas` | Crea una materia prima y guarda `id_materia`. Incluye `Demo`. | 201 |
| GET | `/materias-primas` | Lista las materias primas. | 200 |
| GET | `/materias-primas/{id_materia}` | Obtiene una materia prima. | 200 |
| PUT | `/materias-primas/{id_materia}` | Actualiza una materia prima. | 200 |

### Inventarios

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| POST | `/inventarios/productos` | Crea el inventario de un producto en una sucursal. | 201 |
| POST | `/inventarios/materias-primas` | Crea el inventario de una materia prima en una sucursal. | 201 |
| PATCH | `/inventarios/productos/stock` | Registra una entrada o salida de producto. | 200 |
| PATCH | `/inventarios/materias-primas/stock` | Registra una entrada o salida de materia prima. | 200 |
| PATCH | `/inventarios/productos/minimo` | Cambia el stock mínimo de un producto. | 200 |
| PATCH | `/inventarios/materias-primas/minimo` | Cambia el stock mínimo de una materia prima. | 200 |
| GET | `/sucursales/{id_sucursal}/inventarios/productos` | Lista el inventario de productos de una sucursal. | 200 |
| GET | `/sucursales/{id_sucursal}/inventarios/materias-primas` | Lista el inventario de materias primas de una sucursal. | 200 |
| GET | `/sucursales/{id_sucursal}/alertas` | Lista existencias iguales o inferiores al mínimo. Incluye `Demo`. | 200 |

### Recetas

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| PUT | `/productos/{id_producto}/receta` | Guarda o reemplaza la receta de un producto. Incluye `Demo`. | 200 |
| GET | `/productos/{id_producto}/receta` | Obtiene la receta de un producto. | 200 |
| DELETE | `/productos/{id_producto}/receta` | Elimina la receta de un producto. | 204 |

### Producciones

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| POST | `/producciones` | Consume materias primas y aumenta el producto terminado. Guarda `id_produccion` e incluye `Demo`. | 201 |
| GET | `/producciones` | Lista las producciones. | 200 |
| GET | `/producciones/{id_produccion}` | Obtiene una producción. | 200 |

### Ventas

| Método | Ruta | Función | Estado |
| --- | --- | --- | --- |
| POST | `/ventas` | Valida stock, calcula el total y descuenta productos. Guarda `id_venta` e incluye `Demo`. | 201 |
| GET | `/ventas` | Lista las ventas. | 200 |
| GET | `/ventas/{id_venta}` | Obtiene una venta. | 200 |

## Cuerpos JSON

Los archivos `*.request.yaml` contienen los valores utilizados por las pruebas.

| Operación | Campos |
| --- | --- |
| Crear o actualizar sucursal | `nombre`, `direccion`, `telefono` opcional |
| Crear o actualizar producto | `nombre`, `precio`, `descripcion` opcional |
| Crear o actualizar materia prima | `nombre`, `unidad_medida`, `costo_unitario` y `descripcion` opcionales |
| Crear inventario de producto | `id_sucursal`, `id_producto`, `stock_inicial`, `stock_minimo` |
| Crear inventario de materia prima | `id_sucursal`, `id_materia`, `stock_inicial`, `stock_minimo` |
| Ajustar stock | Identificadores, `tipo` (`entrada` o `salida`) y `cantidad` |
| Actualizar mínimo | Identificadores y `stock_minimo` |
| Guardar receta | `ingredientes`: lista de `id_materia` y `cantidad_usada` |
| Registrar producción | `id_sucursal`, `id_producto`, `cantidad`, `observacion` opcional |
| Registrar venta | `id_sucursal`, `metodo_pago`, `detalles`: lista de `id_producto` y `cantidad` |

## Pruebas y ejemplos

Todas las solicitudes comprueban que la respuesta tenga un estado menor que 400.
Las creaciones principales también validan el estado 201 y guardan su identificador.

Los ejemplos `Demo` incluyen una solicitud y una respuesta precargadas. En Postman
se pueden abrir y ejecutar con `Try`. Sus identificadores y fechas son datos de
referencia; la respuesta real depende de la base local.

Las respuestas con contenido utilizan `{"data": ...}`. Los errores utilizan
`{"error": "..."}` y pueden devolver 400, 404, 409 o 500.
