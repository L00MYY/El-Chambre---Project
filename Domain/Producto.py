from DetalleReceta import DetalleReceta

class Producto:
    def __init__(self, idProducto: int, nombre:str, precio:float, descripcion:str, idDetReceta:int, cantidadUsada:float):
        self.idProducto = idProducto
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.__detalleReceta = DetalleReceta(idDetReceta,cantidadUsada)
    
    def obtenerReceta():
        pass

    def calcularCostoProduccion():
        pass