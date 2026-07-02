from abc import ABC, abstractmethod

class Inventario(ABC):
    def __init__(self, idInventario:int, stockActual:int, stockMinimo:int):
        self.idInventario = idInventario
        self.stockActual = stockActual
        self.stockMinimo = stockMinimo
    
    @abstractmethod
    def actualizarStock(cantidad:float):
        pass
    @abstractmethod
    def validarStockSuficente(cantidadNecesaria:float)->bool:
        pass    
    @abstractmethod
    def validarAlerta()->bool:
        pass