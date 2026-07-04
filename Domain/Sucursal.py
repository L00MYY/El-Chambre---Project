from InventarioMateriaPrima import InventarioMateriaPrima
from InventarioProducto import InventarioProducto


class Sucursal:
    def __init__(self, idSucursal: int, nombre: str, direccion: str, telefono: str):
        self._idSucursal = idSucursal
        self._nombre = nombre
        self._direccion = direccion
        self._telefono = telefono
        # si se elimina la sucursal, estos registros se eliminan, pero la
        # MateriaPrima/Producto siguen existiendo en el sistema
        self._inventarioProductos: list[InventarioProducto] = []
        self._inventarioMateriaPrima: list[InventarioMateriaPrima] = []

    def agregarInventarioMateriaPrima(self, inventario: InventarioMateriaPrima):
        pass

    def agregarInventarioProducto(self, inventario: InventarioProducto):
        self._inventarioProductos.append(inventario)

    def buscarInventarioMateriaPrima(self, idMateriaPrima: int) -> InventarioMateriaPrima | None:
        pass

    def buscarInventarioProducto(self, idProducto: int) -> InventarioProducto | None:
        for inventario in self._inventarioProductos:
            if inventario.idProducto == idProducto:
                return inventario
        return None

    def obtenerInventario(self):
        pass
