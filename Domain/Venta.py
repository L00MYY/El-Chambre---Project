from datetime import date
from DetalleVenta import DetalleVenta
from Producto import Producto
from Sucursal import Sucursal

class Venta:
    
    def __init__(self, idVenta: int, fecha: date, metodoPago: str, idSucursal: int):
        self.idVenta = idVenta
        self._total = 0.0
        self.fechaVenta = fecha
        self.metodoPago = metodoPago
        self.idSucursal = idSucursal  # SUC-02
        self._detalleVenta: list[DetalleVenta] = []

    
    def calcularTotalVenta():
        pass
    def validarStockProductos():
        pass