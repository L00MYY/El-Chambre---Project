from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType

from el_chambre.domain.entities.DetalleReceta import DetalleReceta
from el_chambre.domain.entities.InventarioMateriaPrima import (
    InventarioMateriaPrima,
)
from el_chambre.domain.entities.InventarioProducto import InventarioProducto
from el_chambre.domain.entities.MateriaPrima import MateriaPrima
from el_chambre.domain.entities.Produccion import Produccion
from el_chambre.domain.entities.Producto import Producto
from el_chambre.domain.entities.Sucursal import Sucursal
from el_chambre.domain.entities.Venta import Venta


# ==========================================================
# Repositorios  
# ==========================================================


class SucursalRepository(ABC):
    """Contrato de persistencia para sucursales."""

    @abstractmethod
    def add(self, sucursal: Sucursal) -> int:
        """Guarda una sucursal y devuelve su identificador."""
        ...

    @abstractmethod
    def get_by_id(self, id_sucursal: int) -> Sucursal | None:
        """Busca una sucursal por su identificador."""
        ...

    @abstractmethod
    def list_all(self) -> list[Sucursal]:
        """Devuelve todas las sucursales."""
        ...

    @abstractmethod
    def update(self, sucursal: Sucursal) -> None:
        """Actualiza una sucursal existente."""
        ...


class ProductoRepository(ABC):
    """Contrato de persistencia para productos."""

    @abstractmethod
    def add(self, producto: Producto) -> int:
        """Guarda un producto y devuelve su identificador."""
        ...

    @abstractmethod
    def get_by_id(self, id_producto: int) -> Producto | None:
        """Busca un producto por su identificador."""
        ...

    @abstractmethod
    def list_all(self) -> list[Producto]:
        """Devuelve todos los productos."""
        ...

    @abstractmethod
    def update(self, producto: Producto) -> None:
        """Actualiza un producto existente."""
        ...


class MateriaPrimaRepository(ABC):
    """Contrato de persistencia para materias primas."""

    @abstractmethod
    def add(self, materia_prima: MateriaPrima) -> int:
        """Guarda una materia prima y devuelve su identificador."""
        ...

    @abstractmethod
    def get_by_id(self, id_materia: int) -> MateriaPrima | None:
        """Busca una materia prima por su identificador."""
        ...

    @abstractmethod
    def list_all(self) -> list[MateriaPrima]:
        """Devuelve todas las materias primas."""
        ...

    @abstractmethod
    def update(self, materia_prima: MateriaPrima) -> None:
        """Actualiza una materia prima existente."""
        ...


class InventarioRepository(ABC):
    """
    Contrato para administrar inventarios de productos
    y materias primas por sucursal.
    """

    @abstractmethod
    def add_producto(
        self,
        id_sucursal: int,
        inventario_producto: InventarioProducto,
    ) -> int:
        """
        Guarda un inventario de producto y devuelve
        su identificador.
        """
        ...

    @abstractmethod
    def add_materia_prima(
        self,
        id_sucursal: int,
        inventario_materia_prima: InventarioMateriaPrima,
    ) -> int:
        """
        Guarda un inventario de materia prima y devuelve
        su identificador.
        """
        ...

    @abstractmethod
    def get_producto(
        self,
        id_sucursal: int,
        id_producto: int,
    ) -> InventarioProducto | None:
        """
        Busca el inventario de un producto dentro
        de una sucursal.
        """
        ...

    @abstractmethod
    def get_materia_prima(
        self,
        id_sucursal: int,
        id_materia: int,
    ) -> InventarioMateriaPrima | None:
        """
        Busca el inventario de una materia prima dentro
        de una sucursal.
        """
        ...

    @abstractmethod
    def list_productos(
        self,
        id_sucursal: int,
    ) -> list[InventarioProducto]:
        """Lista los inventarios de productos de una sucursal."""
        ...

    @abstractmethod
    def list_materias_primas(
        self,
        id_sucursal: int,
    ) -> list[InventarioMateriaPrima]:
        """
        Lista los inventarios de materias primas
        de una sucursal.
        """
        ...

    @abstractmethod
    def update_producto(
        self,
        inventario_producto: InventarioProducto,
    ) -> None:
        """Actualiza un inventario de producto."""
        ...

    @abstractmethod
    def update_materia_prima(
        self,
        inventario_materia_prima: InventarioMateriaPrima,
    ) -> None:
        """Actualiza un inventario de materia prima."""
        ...

    @abstractmethod
    def list_alertas_productos(
        self,
        id_sucursal: int,
    ) -> list[InventarioProducto]:
        """
        Lista los inventarios de productos cuyo stock
        se encuentra en alerta.
        """
        ...

    @abstractmethod
    def list_alertas_materias_primas(
        self,
        id_sucursal: int,
    ) -> list[InventarioMateriaPrima]:
        """
        Lista los inventarios de materias primas cuyo stock
        se encuentra en alerta.
        """
        ...


class RecetaRepository(ABC):
    """Contrato de persistencia para recetas de productos."""

    @abstractmethod
    def get_by_producto(
        self,
        id_producto: int,
    ) -> list[DetalleReceta]:
        """Devuelve los detalles de la receta de un producto."""
        ...

    @abstractmethod
    def replace(
        self,
        id_producto: int,
        detalles: list[DetalleReceta],
    ) -> None:
        """
        Reemplaza completamente la receta de un producto.

        La implementación concreta debe eliminar la receta
        anterior y guardar la nueva dentro de la misma transacción.
        """
        ...

    @abstractmethod
    def delete_by_producto(
        self,
        id_producto: int,
    ) -> None:
        """Elimina todos los detalles de receta de un producto."""
        ...


class VentaRepository(ABC):
    """Contrato de persistencia para ventas y sus detalles."""

    @abstractmethod
    def add(
        self,
        venta: Venta,
    ) -> int:
        """
        Guarda una venta completa, incluyendo sus detalles,
        y devuelve su identificador.
        """
        ...

    @abstractmethod
    def get_by_id(
        self,
        id_venta: int,
    ) -> Venta | None:
        """Busca una venta por su identificador."""
        ...

    @abstractmethod
    def list_all(
        self,
        id_sucursal: int | None = None,
    ) -> list[Venta]:
        """
        Lista todas las ventas o las filtra por sucursal
        cuando se proporciona un identificador.
        """
        ...


class ProduccionRepository(ABC):
    """Contrato de persistencia para producciones y sus detalles."""

    @abstractmethod
    def add(
        self,
        produccion: Produccion,
    ) -> int:
        """
        Guarda una producción completa, incluyendo sus detalles,
        y devuelve su identificador.
        """
        ...

    @abstractmethod
    def get_by_id(
        self,
        id_produccion: int,
    ) -> Produccion | None:
        """Busca una producción por su identificador."""
        ...

    @abstractmethod
    def list_all(
        self,
        id_sucursal: int | None = None,
    ) -> list[Produccion]:
        """
        Lista todas las producciones o las filtra por sucursal
        cuando se proporciona un identificador.
        """
        ...


# ==========================================================
# Unidad de trabajo abstracta
# ==========================================================


class AbstractUnitOfWork(ABC):
    """
    Contrato para coordinar repositorios dentro de una transacción.

    La implementación concreta será responsabilidad de infraestructura,
    por ejemplo, mediante una clase SqliteUnitOfWork.
    """

    sucursales: SucursalRepository
    productos: ProductoRepository
    materias_primas: MateriaPrimaRepository
    inventarios: InventarioRepository
    recetas: RecetaRepository
    ventas: VentaRepository
    producciones: ProduccionRepository

    @abstractmethod
    def __enter__(self) -> AbstractUnitOfWork:
        """Inicia el alcance de la unidad de trabajo."""
        ...

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Finaliza el alcance de la unidad de trabajo.

        La implementación concreta debe ejecutar rollback cuando
        la operación termine con una excepción.
        """
        ...

    @abstractmethod
    def commit(self) -> None:
        """Confirma todos los cambios de la transacción actual."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """Revierte todos los cambios de la transacción actual."""
        ...