

class DetalleVenta:
    def __init__(self, idDetVenta: int, idProducto: int, cantidad: float):
        self.idDetVenta = idDetVenta
        self.idProducto = idProducto
        self._cantidad = cantidad
        self._subtotal = 0.0
    
    def calcularSubTotal():
        pass

    def obtenerCantidad(self) -> float:
        pass
    def calcularSubTotal(self, precioUnitario: float) -> float:
        pass
    def obtenerSubtotal(self) -> float:
        pass