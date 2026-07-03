class DetalleProduccion:
    def __init__(self, idDetProduccion: int, idProducto: int, cantidadProducida: float):
        self.idDetProduccion = idDetProduccion
        self.idProducto = idProducto
        self._cantidadProducida = cantidadProducida

    def obtenerCantidadProducida(self) -> float:
        pass