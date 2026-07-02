from datetime import date
from DetalleVenta import DetalleVenta

class Venta:
    def __init__(self, idVenta:int, total:float, fecha:date, metodoPago:str, idDetVenta:int, cantidad:float, subtotal:float):
        self.idVenta = idVenta
        self._total = total
        self.fechaVenta=fecha
        self.metodoPago= metodoPago
        self._detalleVenta = DetalleVenta(idDetVenta, cantidad, subtotal)
    
    def calcularTotalVenta():
        pass
    def validarStockProductos():
        pass