from Inventario import Inventario
 
 
class InventarioProducto(Inventario):
    def __init__(self, idInventario: int, idProducto: int, stockActual: float, stockMinimo: float):
        super().__init__(idInventario, stockActual, stockMinimo)
        self.idProducto = idProducto

    def actualizarStock(self, cantidad: float):
        nuevoStock = self.stockActual + cantidad
        if nuevoStock < 0:
            raise ValueError("No hay suficiente stock")
        self.stockActual = nuevoStock

    def validarStockSuficente(self, cantidadNecesaria: float) -> bool:
        return cantidadNecesaria > 0 and self.stockActual >= cantidadNecesaria
      
    def validarAlerta(self) -> bool:
        return self.stockActual <= self.stockMinimo
