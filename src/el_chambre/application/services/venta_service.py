from datetime import date

from el_chambre.application.exceptions.exceptions import (
    InsufficientStockError,
    NotFoundError,
    ValidationError,
)
from el_chambre.domain.entities.DetalleVenta import DetalleVenta
from el_chambre.domain.entities.Venta import Venta


class VentaService:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def registrar_venta(self, id_sucursal, metodo_pago, detalles):
        if not isinstance(metodo_pago, str) or not metodo_pago.strip():
            raise ValidationError("El método de pago es obligatorio")
        if not isinstance(detalles, list) or not detalles:
            raise ValidationError("La venta debe incluir al menos un producto")

        cantidades = self._agrupar_cantidades(detalles)

        with self._uow_factory() as uow:
            if uow.sucursales.get_by_id(id_sucursal) is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")

            productos = []
            inventarios = []

            for id_producto, cantidad in cantidades.items():
                producto = uow.productos.get_by_id(id_producto)
                if producto is None:
                    raise NotFoundError(f"El producto {id_producto} no existe")

                inventario = uow.inventarios.get_producto(id_sucursal, id_producto)
                if inventario is None:
                    raise NotFoundError(
                        f"No existe inventario del producto {id_producto} "
                        f"en la sucursal {id_sucursal}"
                    )
                if not inventario.validarStockSuficente(cantidad):
                    raise InsufficientStockError(
                        f"Stock insuficiente del producto {id_producto}"
                    )

                productos.append(producto)
                inventarios.append((inventario, cantidad))

            venta = Venta(0, date.today(), metodo_pago.strip(), id_sucursal)
            for id_producto, cantidad in cantidades.items():
                venta.agregarDetalleVenta(DetalleVenta(0, id_producto, cantidad))

            venta.calcularTotalVenta(productos)

            for inventario, cantidad in inventarios:
                inventario.actualizarStock(-cantidad)

            venta.idVenta = uow.ventas.add(venta)
            for inventario, _ in inventarios:
                uow.inventarios.update_producto(inventario)

            alertas = uow.inventarios.list_alertas_productos(id_sucursal)
            uow.commit()

            return {
                "venta": venta,
                "alertas_productos": alertas,
            }

    def obtener_venta(self, id_venta):
        with self._uow_factory() as uow:
            venta = uow.ventas.get_by_id(id_venta)
            if venta is None:
                raise NotFoundError(f"La venta {id_venta} no existe")
            return venta

    def listar_ventas(self, id_sucursal=None):
        with self._uow_factory() as uow:
            if (
                id_sucursal is not None
                and uow.sucursales.get_by_id(id_sucursal) is None
            ):
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")
            return uow.ventas.list_all(id_sucursal)

    @staticmethod
    def _agrupar_cantidades(detalles):
        cantidades = {}

        for detalle in detalles:
            if not isinstance(detalle, dict):
                raise ValidationError("Cada detalle de venta debe ser un objeto")

            id_producto = detalle.get("id_producto")
            cantidad = detalle.get("cantidad")

            if isinstance(id_producto, bool) or not isinstance(id_producto, int) or id_producto <= 0:
                raise ValidationError("El id del producto debe ser un entero mayor que 0")
            if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
                raise ValidationError("La cantidad debe ser un entero mayor que 0")

            cantidades[id_producto] = cantidades.get(id_producto, 0) + cantidad

        return cantidades
