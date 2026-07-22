def serialize_sucursal(sucursal):
    return {
        "id_sucursal": sucursal._idSucursal,
        "nombre": sucursal._nombre,
        "direccion": sucursal._direccion,
        "telefono": sucursal._telefono,
    }


def serialize_producto(producto):
    return {
        "id_producto": producto.idProducto,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "descripcion": producto.descripcion,
        "receta": serialize_receta(producto.obtenerReceta()),
    }


def serialize_materia_prima(materia_prima):
    return {
        "id_materia": materia_prima.idMateriaPrima,
        "nombre": materia_prima.nombre,
        "unidad_medida": materia_prima.unidadMedida,
        "costo_unitario": materia_prima.costoUnitario,
        "descripcion": materia_prima.descripcion,
    }


def serialize_inventario_producto(inventario):
    return {
        "id_inventario": inventario.idInventario,
        "id_producto": inventario.idProducto,
        "stock_actual": inventario.stockActual,
        "stock_minimo": inventario.stockMinimo,
        "en_alerta": inventario.validarAlerta(),
    }


def serialize_inventario_materia_prima(inventario):
    return {
        "id_inventario": inventario.idInventario,
        "id_materia": inventario.idMateriaPrima,
        "stock_actual": inventario.stockActual,
        "stock_minimo": inventario.stockMinimo,
        "en_alerta": inventario.validarAlerta(),
    }


def serialize_receta(detalles):
    return [
        {
            "id_detalle_receta": detalle.idDetReceta,
            "id_materia": detalle.obtenerIdMateriaPrima(),
            "cantidad_usada": detalle.obtenerCantidadUsada(),
        }
        for detalle in detalles
    ]


def serialize_venta(venta):
    return {
        "id_venta": venta.idVenta,
        "fecha": venta.fechaVenta.isoformat(),
        "total": venta._total,
        "metodo_pago": venta.metodoPago,
        "id_sucursal": venta.idSucursal,
        "detalles": [
            {
                "id_detalle_venta": detalle.idDetVenta,
                "id_producto": detalle.idProducto,
                "cantidad": detalle.obtenerCantidad(),
                "subtotal": detalle.obtenerSubtotal(),
            }
            for detalle in venta._detalleVenta
        ],
    }


def serialize_produccion(produccion):
    return {
        "id_produccion": produccion.idProduccion,
        "fecha": produccion._fechaProduccion.isoformat(),
        "observacion": produccion.observacion,
        "id_sucursal": produccion.idSucursal,
        "detalles": [
            {
                "id_detalle_produccion": detalle.idDetProduccion,
                "id_producto": detalle.idProducto,
                "cantidad_producida": detalle.obtenerCantidadProducida(),
            }
            for detalle in produccion._detallesDeProduccion
        ],
    }
