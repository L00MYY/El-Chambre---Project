class DetalleReceta:
    def __init__(self, idDetReceta: int, idMateriaPrima: int, cantidadUsada: float):
        self.idDetReceta = idDetReceta
        self.idMateriaPrima = idMateriaPrima
        self._cantidadUsada = cantidadUsada

    def obtenerIdMateriaPrima(self) -> int:
        return self.idMateriaPrima

    def obtenerCantidadUsada(self) -> float:
        return self._cantidadUsada