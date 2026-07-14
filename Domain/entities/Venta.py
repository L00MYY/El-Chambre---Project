from datetime import date
from .DetalleVenta import DetalleVenta
from .Producto import Producto
from .Sucursal import Sucursal

class Venta:
    
    def __init__(self, idVenta: int, fecha: date, metodoPago: str, idSucursal: int):
        self.idVenta = idVenta
        self._total = 0.0
        self.fechaVenta = fecha
        self.metodoPago = metodoPago
        self.idSucursal = idSucursal  # SUC-02
        self._detalleVenta: list[DetalleVenta] = []

    def agregarDetalleVenta(self, detalleVenta: DetalleVenta):
        self._detalleVenta.append(detalleVenta)

    def calcularTotalVenta(self, productos: list[Producto]) -> float:
        self._total = 0.0

        for detalle in self._detalleVenta:
            productoEncontrado = None
            for producto in productos:
                if producto.idProducto == detalle.idProducto:
                    productoEncontrado = producto
                    break

            if productoEncontrado is None:
                raise ValueError("Producto no encontrado")

            self._total += detalle.calcularSubTotal(productoEncontrado.precio)

        return self._total

    def validarStockProductos(self, sucursal: Sucursal) -> bool:
        cantidadesVendidas = {}
        for detalle in self._detalleVenta:
            cantidadesVendidas[detalle.idProducto] = (
                cantidadesVendidas.get(detalle.idProducto, 0)
                + detalle.obtenerCantidad()
            )

        for idProducto, cantidad in cantidadesVendidas.items():
            inventario = sucursal.buscarInventarioProducto(idProducto)
            if inventario is None or not inventario.validarStockSuficente(cantidad):
                return False

        return True

    def registrarVenta(self, productos: list[Producto], sucursal: Sucursal) -> float:
        if not self.validarStockProductos(sucursal):
            raise ValueError("No hay suficiente stock para registrar la venta")

        total = self.calcularTotalVenta(productos)

        cantidadesVendidas = {}
        for detalle in self._detalleVenta:
            cantidadesVendidas[detalle.idProducto] = (
                cantidadesVendidas.get(detalle.idProducto, 0)
                + detalle.obtenerCantidad()
            )

        for idProducto, cantidad in cantidadesVendidas.items():
            inventario = sucursal.buscarInventarioProducto(idProducto)
            inventario.actualizarStock(-cantidad)

        return total
