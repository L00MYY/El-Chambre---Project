

class DetalleVenta:
    def __init__(self, idDetVenta: int, idProducto: int, cantidad: float):
        if cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a 0")

        self.idDetVenta = idDetVenta
        self.idProducto = idProducto
        self._cantidad = cantidad
        self._subtotal = 0.0

    def obtenerCantidad(self) -> float:
        return self._cantidad

    def calcularSubTotal(self, precioUnitario: float) -> float:
        self._subtotal = self._cantidad * precioUnitario
        return self._subtotal

    def obtenerSubtotal(self) -> float:
        return self._subtotal
