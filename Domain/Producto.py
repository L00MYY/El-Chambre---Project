from DetalleReceta import DetalleReceta


class Producto:
    def __init__(self, idProducto: int, nombre: str, precio: float, descripcion: str, receta: list[DetalleReceta] = None):
        self.idProducto = idProducto
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.__receta = receta if receta is not None else []

    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("No se aceptan precios negativos")
        self.__precio = valor

    def agregarIngrediente(self, detalleReceta: DetalleReceta):
        if detalleReceta.obtenerCantidadUsada() <= 0:
            raise ValueError("La cantidad usada debe ser mayor a 0")
        
        for ingrediente in self.__receta:
            if ingrediente.obtenerIdMateriaPrima() == detalleReceta.obtenerIdMateriaPrima():
                raise ValueError("Ingrediente ya esta en la receta")

        self.__receta.append(detalleReceta)

    def obtenerReceta(self) -> list[DetalleReceta]:
        return self.__receta

    def esProducible(self) -> bool:
        return len(self.__receta) > 0

    def calcularCostoProduccion(self):
        pass