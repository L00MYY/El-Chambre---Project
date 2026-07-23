from flask import jsonify, request

from el_chambre.api.dependencies import (
    get_catalogo_service,
    get_inventario_service,
    get_produccion_service,
    get_receta_service,
    get_venta_service,
)
from el_chambre.api.serializers import (
    serialize_inventario_materia_prima,
    serialize_inventario_producto,
    serialize_materia_prima,
    serialize_produccion,
    serialize_producto,
    serialize_receta,
    serialize_sucursal,
    serialize_venta,
)
from el_chambre.application.exceptions.exceptions import ValidationError


def _get_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("El cuerpo de la solicitud debe ser un objeto JSON")
    return data


def _require_fields(data, *fields):
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValidationError(
            f"Faltan campos obligatorios: {', '.join(missing)}"
        )


def _optional_query_int(name):
    value = request.args.get(name)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError as error:
        raise ValidationError(f"El parámetro {name} debe ser un entero") from error


def register_routes(app):
    @app.get("/")
    def home():
        return jsonify(
            {
                "aplicacion": "El Chambre",
                "mensaje": "API de inventario funcionando",
            }
        )

    # Sucursales

    @app.post("/sucursales")
    def crear_sucursal():
        data = _get_json()
        _require_fields(data, "nombre", "direccion")
        sucursal = get_catalogo_service().crear_sucursal(
            data["nombre"],
            data["direccion"],
            data.get("telefono"),
        )
        return jsonify({"data": serialize_sucursal(sucursal)}), 201

    @app.get("/sucursales")
    def listar_sucursales():
        sucursales = get_catalogo_service().listar_sucursales()
        return jsonify({"data": [serialize_sucursal(item) for item in sucursales]})

    @app.get("/sucursales/<int:id_sucursal>")
    def obtener_sucursal(id_sucursal):
        sucursal = get_catalogo_service().obtener_sucursal(id_sucursal)
        return jsonify({"data": serialize_sucursal(sucursal)})

    @app.put("/sucursales/<int:id_sucursal>")
    def actualizar_sucursal(id_sucursal):
        data = _get_json()
        _require_fields(data, "nombre", "direccion")
        sucursal = get_catalogo_service().actualizar_sucursal(
            id_sucursal,
            data["nombre"],
            data["direccion"],
            data.get("telefono"),
        )
        return jsonify({"data": serialize_sucursal(sucursal)})

    # Productos

    @app.post("/productos")
    def crear_producto():
        data = _get_json()
        _require_fields(data, "nombre", "precio")
        producto = get_catalogo_service().crear_producto(
            data["nombre"],
            data["precio"],
            data.get("descripcion", ""),
        )
        return jsonify({"data": serialize_producto(producto)}), 201

    @app.get("/productos")
    def listar_productos():
        productos = get_catalogo_service().listar_productos()
        return jsonify({"data": [serialize_producto(item) for item in productos]})

    @app.get("/productos/<int:id_producto>")
    def obtener_producto(id_producto):
        producto = get_catalogo_service().obtener_producto(id_producto)
        return jsonify({"data": serialize_producto(producto)})

    @app.put("/productos/<int:id_producto>")
    def actualizar_producto(id_producto):
        data = _get_json()
        _require_fields(data, "nombre", "precio")
        producto = get_catalogo_service().actualizar_producto(
            id_producto,
            data["nombre"],
            data["precio"],
            data.get("descripcion", ""),
        )
        return jsonify({"data": serialize_producto(producto)})

    # Materias primas

    @app.post("/materias-primas")
    def crear_materia_prima():
        data = _get_json()
        _require_fields(data, "nombre", "unidad_medida")
        materia_prima = get_catalogo_service().crear_materia_prima(
            data["nombre"],
            data["unidad_medida"],
            data.get("costo_unitario", 0),
            data.get("descripcion", ""),
        )
        return jsonify({"data": serialize_materia_prima(materia_prima)}), 201

    @app.get("/materias-primas")
    def listar_materias_primas():
        materias = get_catalogo_service().listar_materias_primas()
        return jsonify(
            {"data": [serialize_materia_prima(item) for item in materias]}
        )

    @app.get("/materias-primas/<int:id_materia>")
    def obtener_materia_prima(id_materia):
        materia = get_catalogo_service().obtener_materia_prima(id_materia)
        return jsonify({"data": serialize_materia_prima(materia)})

    @app.put("/materias-primas/<int:id_materia>")
    def actualizar_materia_prima(id_materia):
        data = _get_json()
        _require_fields(data, "nombre", "unidad_medida")
        materia = get_catalogo_service().actualizar_materia_prima(
            id_materia,
            data["nombre"],
            data["unidad_medida"],
            data.get("costo_unitario", 0),
            data.get("descripcion", ""),
        )
        return jsonify({"data": serialize_materia_prima(materia)})

    # Inventarios

    @app.post("/inventarios/productos")
    def crear_inventario_producto():
        data = _get_json()
        _require_fields(data, "id_sucursal", "id_producto")
        inventario = get_inventario_service().crear_inventario_producto(
            data["id_sucursal"],
            data["id_producto"],
            data.get("stock_inicial", 0),
            data.get("stock_minimo", 0),
        )
        return jsonify({"data": serialize_inventario_producto(inventario)}), 201

    @app.post("/inventarios/materias-primas")
    def crear_inventario_materia_prima():
        data = _get_json()
        _require_fields(data, "id_sucursal", "id_materia")
        inventario = get_inventario_service().crear_inventario_materia_prima(
            data["id_sucursal"],
            data["id_materia"],
            data.get("stock_inicial", 0),
            data.get("stock_minimo", 0),
        )
        return (
            jsonify({"data": serialize_inventario_materia_prima(inventario)}),
            201,
        )

    @app.patch("/inventarios/productos/stock")
    def ajustar_stock_producto():
        data = _get_json()
        _require_fields(
            data,
            "id_sucursal",
            "id_producto",
            "tipo",
            "cantidad",
        )
        resultado = get_inventario_service().ajustar_stock_producto(
            data["id_sucursal"],
            data["id_producto"],
            data["tipo"],
            data["cantidad"],
        )
        return jsonify({"data": resultado})

    @app.patch("/inventarios/materias-primas/stock")
    def ajustar_stock_materia_prima():
        data = _get_json()
        _require_fields(
            data,
            "id_sucursal",
            "id_materia",
            "tipo",
            "cantidad",
        )
        resultado = get_inventario_service().ajustar_stock_materia_prima(
            data["id_sucursal"],
            data["id_materia"],
            data["tipo"],
            data["cantidad"],
        )
        return jsonify({"data": resultado})

    @app.patch("/inventarios/productos/minimo")
    def actualizar_minimo_producto():
        data = _get_json()
        _require_fields(data, "id_sucursal", "id_producto", "stock_minimo")
        inventario = get_inventario_service().actualizar_minimo_producto(
            data["id_sucursal"],
            data["id_producto"],
            data["stock_minimo"],
        )
        return jsonify({"data": serialize_inventario_producto(inventario)})

    @app.patch("/inventarios/materias-primas/minimo")
    def actualizar_minimo_materia_prima():
        data = _get_json()
        _require_fields(data, "id_sucursal", "id_materia", "stock_minimo")
        inventario = get_inventario_service().actualizar_minimo_materia_prima(
            data["id_sucursal"],
            data["id_materia"],
            data["stock_minimo"],
        )
        return jsonify({"data": serialize_inventario_materia_prima(inventario)})

    @app.get("/sucursales/<int:id_sucursal>/inventarios/productos")
    def listar_inventario_productos(id_sucursal):
        inventarios = get_inventario_service().listar_productos(id_sucursal)
        return jsonify(
            {"data": [serialize_inventario_producto(item) for item in inventarios]}
        )

    @app.get("/sucursales/<int:id_sucursal>/inventarios/materias-primas")
    def listar_inventario_materias_primas(id_sucursal):
        inventarios = get_inventario_service().listar_materias_primas(id_sucursal)
        return jsonify(
            {
                "data": [
                    serialize_inventario_materia_prima(item)
                    for item in inventarios
                ]
            }
        )

    @app.get("/sucursales/<int:id_sucursal>/alertas")
    def obtener_alertas(id_sucursal):
        alertas = get_inventario_service().obtener_alertas(id_sucursal)
        return jsonify(
            {
                "data": {
                    "productos": [
                        serialize_inventario_producto(item)
                        for item in alertas["productos"]
                    ],
                    "materias_primas": [
                        serialize_inventario_materia_prima(item)
                        for item in alertas["materias_primas"]
                    ],
                }
            }
        )

    # Recetas

    @app.put("/productos/<int:id_producto>/receta")
    def guardar_receta(id_producto):
        data = _get_json()
        _require_fields(data, "ingredientes")
        receta = get_receta_service().guardar_receta(
            id_producto,
            data["ingredientes"],
        )
        return jsonify({"data": serialize_receta(receta)})

    @app.get("/productos/<int:id_producto>/receta")
    def obtener_receta(id_producto):
        receta = get_receta_service().obtener_receta(id_producto)
        return jsonify({"data": serialize_receta(receta)})

    @app.delete("/productos/<int:id_producto>/receta")
    def eliminar_receta(id_producto):
        get_receta_service().eliminar_receta(id_producto)
        return "", 204

    # Ventas

    @app.post("/ventas")
    def registrar_venta():
        data = _get_json()
        _require_fields(data, "id_sucursal", "metodo_pago", "detalles")
        resultado = get_venta_service().registrar_venta(
            data["id_sucursal"],
            data["metodo_pago"],
            data["detalles"],
        )
        return (
            jsonify(
                {
                    "data": {
                        "venta": serialize_venta(resultado["venta"]),
                        "alertas_productos": [
                            serialize_inventario_producto(item)
                            for item in resultado["alertas_productos"]
                        ],
                    }
                }
            ),
            201,
        )

    @app.get("/ventas")
    def listar_ventas():
        id_sucursal = _optional_query_int("id_sucursal")
        ventas = get_venta_service().listar_ventas(id_sucursal)
        return jsonify({"data": [serialize_venta(item) for item in ventas]})

    @app.get("/ventas/<int:id_venta>")
    def obtener_venta(id_venta):
        venta = get_venta_service().obtener_venta(id_venta)
        return jsonify({"data": serialize_venta(venta)})

    # Producciones

    @app.post("/producciones")
    def registrar_produccion():
        data = _get_json()
        _require_fields(data, "id_sucursal", "id_producto", "cantidad")
        resultado = get_produccion_service().registrar_produccion(
            data["id_sucursal"],
            data["id_producto"],
            data["cantidad"],
            data.get("observacion", ""),
        )
        return (
            jsonify(
                {
                    "data": {
                        "produccion": serialize_produccion(
                            resultado["produccion"]
                        ),
                        "alertas_materias_primas": [
                            serialize_inventario_materia_prima(item)
                            for item in resultado["alertas_materias_primas"]
                        ],
                    }
                }
            ),
            201,
        )

    @app.get("/producciones")
    def listar_producciones():
        id_sucursal = _optional_query_int("id_sucursal")
        producciones = get_produccion_service().listar_producciones(id_sucursal)
        return jsonify(
            {"data": [serialize_produccion(item) for item in producciones]}
        )

    @app.get("/producciones/<int:id_produccion>")
    def obtener_produccion(id_produccion):
        produccion = get_produccion_service().obtener_produccion(id_produccion)
        return jsonify({"data": serialize_produccion(produccion)})
