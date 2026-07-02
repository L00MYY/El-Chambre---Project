from datetime import date
from DetalleProduccion import DetalleProduccion
class Produccion:
    def __init__(self, idProduccion:int, fechaProduccion:date, observacion:str,idDetProduccion:int, cantidadProducida:float):
        self.idProduccion = idProduccion
        self._fechaProduccion = fechaProduccion
        self.observacion = observacion
        self._detallesDeProduccion = DetalleProduccion(idDetProduccion,cantidadProducida)

    def validarMateriaPrima():
        pass
    def calcularTotalProducido():
        pass