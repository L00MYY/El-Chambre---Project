from datetime import date

from el_chambre.application.exceptions.exceptions import (
    ValidationError,
    NotFoundError,
    ConflictError,
    InsufficientStockError,
)
from el_chambre.domain.entities.Produccion import Produccion
from el_chambre.domain.entities.DetalleProduccion import DetalleProduccion


class ProduccionService:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def registrar_produccion(self, id_sucursal, id_producto, cantidad, observacion=""):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidationError(
                "La cantidad a producir debe ser un número entero mayor que 0"
            )

        with self._uow_factory() as uow:
            sucursal = uow.sucursales.get_by_id(id_sucursal)
            if sucursal is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")

            producto = uow.productos.get_by_id(id_producto)
            if producto is None:
                raise NotFoundError(f"El producto {id_producto} no existe")

            receta = uow.recetas.get_by_producto(id_producto)
            if not receta:
                raise ConflictError(
                    f"El producto {id_producto} no tiene una receta registrada; no se puede producir"
                )

            necesidades = {
                detalle.obtenerIdMateriaPrima(): detalle.obtenerCantidadUsada() * cantidad
                for detalle in receta
            }

            inventarios_mp = {}
            for id_materia, cantidad_necesaria in necesidades.items():
                inventario_mp = uow.inventarios.get_materia_prima(id_sucursal, id_materia)
                if inventario_mp is None:
                    raise NotFoundError(
                        f"No existe inventario de la materia prima {id_materia} en la sucursal {id_sucursal}"
                    )
                if not inventario_mp.validarStockSuficente(cantidad_necesaria):
                    raise InsufficientStockError(
                        f"Stock insuficiente de la materia prima {id_materia} para completar la producción"
                    )
                inventarios_mp[id_materia] = inventario_mp

            inventario_producto = uow.inventarios.get_producto(id_sucursal, id_producto)
            if inventario_producto is None:
                raise ConflictError(
                    f"El producto {id_producto} no tiene inventario configurado en la sucursal {id_sucursal}"
                )

            produccion = Produccion(
                idProduccion=0,
                fechaProduccion=date.today(),
                observacion=observacion,
                idSucursal=id_sucursal,
            )
            detalle_produccion = DetalleProduccion(
                idDetProduccion=0,
                idProducto=id_producto,
                cantidadProducida=cantidad,
            )
            produccion.agregarDetalleProduccion(detalle_produccion)

            for id_materia, cantidad_necesaria in necesidades.items():
                inventarios_mp[id_materia].actualizarStock(-cantidad_necesaria)

            inventario_producto.actualizarStock(cantidad)

            id_produccion = uow.producciones.add(produccion)
            produccion.idProduccion = id_produccion

            for inventario_mp in inventarios_mp.values():
                uow.inventarios.update_materia_prima(inventario_mp)
            uow.inventarios.update_producto(inventario_producto)

            uow.commit()

            return {
                "produccion": produccion,
                "alertas_materias_primas": uow.inventarios.list_alertas_materias_primas(id_sucursal),
            }

    def obtener_produccion(self, id_produccion):
        with self._uow_factory() as uow:
            produccion = uow.producciones.get_by_id(id_produccion)
            if produccion is None:
                raise NotFoundError(f"La producción {id_produccion} no existe")
            return produccion

    def listar_producciones(self, id_sucursal=None):
        with self._uow_factory() as uow:
            return uow.producciones.list_all(id_sucursal)