from DetalleReceta import DetalleReceta


class Producto:
    def __init__(self, idProducto: int, nombre: str, precio: float, descripcion: str, receta: list[DetalleReceta] = None):
        self.idProducto = idProducto
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.__receta = receta if receta is not None else []

    def agregarIngrediente(self, detalleReceta: DetalleReceta):
        self.__receta.append(detalleReceta)

    def obtenerReceta(self) -> list[DetalleReceta]:
        return self.__receta

    def calcularCostoProduccion(self):
        pass