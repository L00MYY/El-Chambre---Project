from .Inventario import Inventario

class InventarioMateriaPrima(Inventario):
    def __init__(self, idInventario: int, idMateriaPrima: int, stockActual: float, stockMinimo: float):
        super().__init__(idInventario, stockActual, stockMinimo)
        self.idMateriaPrima = idMateriaPrima

    def actualizarStock(self, cantidad: float):
        nuevoStock = self.stockActual + cantidad
        if nuevoStock < 0:
            raise ValueError("No hay suficiente stock de materia prima")
        self.stockActual = nuevoStock

    def validarStockSuficente(self, cantidadNecesaria: float) -> bool:
        return cantidadNecesaria > 0 and self.stockActual >= cantidadNecesaria

    def validarAlerta(self) -> bool:
        return self.stockActual <= self.stockMinimo