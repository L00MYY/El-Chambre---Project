from Inventario import Inventario

class InventarioMateriaPrima(Inventario):
    def __init__(self, idInventario: int, idMateriaPrima: int, stockActual: float, stockMinimo: float):
        super().__init__(idInventario, stockActual, stockMinimo)
        self.idMateriaPrima = idMateriaPrima

    def actualizarStock(self, cantidad: float):
        pass

    def validarStockSuficente(self, cantidadNecesaria: float) -> bool:
        pass

    def validarAlerta(self) -> bool:
        pass