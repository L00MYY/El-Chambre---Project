from .DetalleReceta import DetalleReceta


class Producto:
    def __init__(self, idProducto: int, nombre: str, precio: float, descripcion: str, receta: list[DetalleReceta]):
        self.idProducto = idProducto
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.__receta = receta

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
    
    def calcularCostoProduccion(self, catalogoMateriaPrima: dict) -> float:
        costoTotal = 0.0
        for ingrediente in self.__receta:
            mp = catalogoMateriaPrima.get(ingrediente.obtenerIdMateriaPrima())
            if mp is None:
                raise ValueError("Materia prima no encontrada en el catálogo")
        costoTotal += ingrediente.obtenerCantidadUsada() * mp.costoUnitario
        return costoTotal
