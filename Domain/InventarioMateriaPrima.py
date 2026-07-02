from Inventario import Inventario
class InventarioMateriaPrima(Inventario):
    def __init__(self, idInventario, stockActual, stockMinimo):
        super().__init__(idInventario, stockActual, stockMinimo)
    
        
    def actualizarStock(cantidad:float):
        pass

    def validarStockSuficente(cantidadNecesaria:float)->bool:
        pass
      
    def validarAlerta()->bool:
        pass