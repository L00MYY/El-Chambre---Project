from datetime import date
from DetalleProduccion import DetalleProduccion
from Producto import Producto
from Sucursal import Sucursal

class Produccion:
    def __init__(self, idProduccion: int, fechaProduccion: date, observacion: str, idSucursal: int):
        self.idProduccion = idProduccion
        self._fechaProduccion = fechaProduccion
        self.observacion = observacion
        self.idSucursal = idSucursal  #Toda producción pertenece a UNA sucursal
        #Una cabecera Produccion compone VARIOS DetalleProduccion
        self._detallesDeProduccion: list[DetalleProduccion] = []


    def validarMateriaPrima(self, producto: Producto, sucursal: Sucursal) -> bool:
        cantidadProducida = self._detallesDeProduccion.obtenerCantidadProducid()
        for ingrediente in producto.obtenerReceta():
            necesidadTotal = cantidadProducida * ingrediente.obtenerCantidadUsada()
            inventarioMP = sucursal.buscarInventarioMateriaPrima(ingrediente.obtenerIdMateriaPrima())
            if inventarioMP is None:
                return False
            if not inventarioMP.validarStockSuficente(necesidadTotal):
                return False
        return True
    
    def calcularTotalProducido(self):
        pass