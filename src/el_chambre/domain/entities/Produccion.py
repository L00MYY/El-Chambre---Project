from datetime import date
from .DetalleProduccion import DetalleProduccion
from .Producto import Producto
from .Sucursal import Sucursal

class Produccion:
    def __init__(self, idProduccion: int, fechaProduccion: date, observacion: str, idSucursal: int):
        self.idProduccion = idProduccion
        self._fechaProduccion = fechaProduccion
        self.observacion = observacion
        self.idSucursal = idSucursal  #Toda producción pertenece a UNA sucursal
        #Una cabecera Produccion compone VARIOS DetalleProduccion
        self._detallesDeProduccion: list[DetalleProduccion] = []


    def validarMateriaPrima(self, producto: Producto, sucursal: Sucursal) -> bool:
        cantidadProducida = self._detallesDeProduccion.obtenerCantidadProducida()
        for ingrediente in producto.obtenerReceta():
            necesidadTotal = cantidadProducida * ingrediente.obtenerCantidadUsada()
            inventarioMP = sucursal.buscarInventarioMateriaPrima(ingrediente.obtenerIdMateriaPrima())
            if inventarioMP is None:
                return False
            if not inventarioMP.validarStockSuficente(necesidadTotal):
                return False
        return True
    
    def calcularTotalProducido(self) -> float:
        return sum(d.obtenerCantidadProducida() for d in self._detallesDeProduccion)
    
    def registrarProduccion(self, productos: list[Producto], sucursal: Sucursal):
        """Transacción inversa a la venta: se consume  la materia prima y acredita el producto terminado"""
        #  1: validar  antes de tocar nada
        for detalle in self._detallesDeProduccion:
            producto = next((p for p in productos if p.idProducto == detalle.idProducto), None)
            if producto is None:
                raise ValueError("Producto no encontrado")
            if not self.validarMateriaPrima(producto, detalle.obtenerCantidadProducida(), sucursal):
                raise ValueError(f"No hay suficiente materia prima para producir {producto.nombre}")

        #  2: solo si pasó la validación, se aplican los movimientos
        for detalle in self._detallesDeProduccion:
            producto = next(p for p in productos if p.idProducto == detalle.idProducto)
            cantidadProducida = detalle.obtenerCantidadProducida()

            for ingrediente in producto.obtenerReceta():
                necesidadTotal = cantidadProducida * ingrediente.obtenerCantidadUsada()
                inventarioMP = sucursal.buscarInventarioMateriaPrima(ingrediente.obtenerIdMateriaPrima())
                inventarioMP.actualizarStock(-necesidadTotal)

            inventarioProd = sucursal.buscarInventarioProducto(detalle.idProducto)
            if inventarioProd is None:
                raise ValueError("No existe inventario de producto en esta sucursal")
            inventarioProd.actualizarStock(cantidadProducida)
