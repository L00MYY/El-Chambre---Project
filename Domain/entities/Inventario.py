from abc import ABC, abstractmethod


class Inventario(ABC):
    def __init__(self, idInventario: int, stockActual: float, stockMinimo: float):
        self.idInventario = idInventario
        self.stockActual = stockActual
        self.stockMinimo = stockMinimo

    @abstractmethod
    def actualizarStock(self, cantidad: float):
        pass

    @abstractmethod
    def validarStockSuficente(self, cantidadNecesaria: float) -> bool:
        pass

    @abstractmethod
    def validarAlerta(self) -> bool:
        pass