from Inventario import Inventario

class InventarioProducto(Inventario):
    def __init__(self, idInventario, stockActual, stockMinimo):
        super().__init__(idInventario, stockActual, stockMinimo)
    
    
    def actualizarStock(cantidad:float):
        pass

    def validarStockSuficente(cantidadNecesaria:float)->bool:
        pass
      
    def validarAlerta()->bool:
        pass