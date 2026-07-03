from Inventario import Inventario
 
 
class InventarioProducto(Inventario):
    def __init__(self, idInventario: int, idProducto: int, stockActual: float, stockMinimo: float):
        super().__init__(idInventario, stockActual, stockMinimo)
        self.idProducto = idProducto

    def actualizarStock(self, cantidad:float):
        pass

    def validarStockSuficente(self,cantidadNecesaria:float)->bool:
        pass
      
    def validarAlerta(self)->bool:
        pass