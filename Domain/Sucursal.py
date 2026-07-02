from InventarioMateriaPrima import InventarioMateriaPrima
from InventarioProducto import InventarioProducto


class Sucursal:
    def __init__(self, idSucursal:int, nombre:str, dirreccion:str, telefono:str, inventarioProductos:InventarioProducto,inventarioMateriaPrima:InventarioMateriaPrima):
        self.idSucursal= idSucursal
        self._nombre = nombre
        self._direccion = dirreccion
        self._telefono = telefono
        self._inventarioProductos = list[inventarioProductos]
        self._inventarioMateriaPrima= list[inventarioMateriaPrima]

    
    def obtenerInventario():
        pass