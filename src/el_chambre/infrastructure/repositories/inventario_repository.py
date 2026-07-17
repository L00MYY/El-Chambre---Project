from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import InventarioRepository
from el_chambre.domain.entities.InventarioMateriaPrima import InventarioMateriaPrima
from el_chambre.domain.entities.InventarioProducto import InventarioProducto


class SqliteInventarioRepository(InventarioRepository):
    """Repositorio SQLite para los inventarios de productos y materias primas."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add_producto(
        self,
        id_sucursal: int,
        inventario_producto: InventarioProducto,
    ) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Inventario_producto (stock_actual, stock_minimo, id_sucursal, id_producto)
            VALUES (?, ?, ?, ?)
            """,
            (
                inventario_producto.stockActual,
                inventario_producto.stockMinimo,
                id_sucursal,
                inventario_producto.idProducto,
            ),
        )
        return cursor.lastrowid

    def add_materia_prima(
        self,
        id_sucursal: int,
        inventario_materia_prima: InventarioMateriaPrima,
    ) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Inventario_materia_prima (stock_actual, stock_minimo, id_sucursal, id_materia)
            VALUES (?, ?, ?, ?)
            """,
            (
                inventario_materia_prima.stockActual,
                inventario_materia_prima.stockMinimo,
                id_sucursal,
                inventario_materia_prima.idMateriaPrima,
            ),
        )
        return cursor.lastrowid

    def get_producto(
        self,
        id_sucursal: int,
        id_producto: int,
    ) -> InventarioProducto | None:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_producto, stock_actual, stock_minimo, id_producto
            FROM Inventario_producto
            WHERE id_sucursal = ? AND id_producto = ?
            """,
            (id_sucursal, id_producto),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return InventarioProducto(
            row["id_inventario_producto"],
            row["id_producto"],
            row["stock_actual"],
            row["stock_minimo"],
        )

    def get_materia_prima(
        self,
        id_sucursal: int,
        id_materia: int,
    ) -> InventarioMateriaPrima | None:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_mp, stock_actual, stock_minimo, id_materia
            FROM Inventario_materia_prima
            WHERE id_sucursal = ? AND id_materia = ?
            """,
            (id_sucursal, id_materia),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return InventarioMateriaPrima(
            row["id_inventario_mp"],
            row["id_materia"],
            row["stock_actual"],
            row["stock_minimo"],
        )

    def list_productos(
        self,
        id_sucursal: int,
    ) -> list[InventarioProducto]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_producto, stock_actual, stock_minimo, id_producto
            FROM Inventario_producto
            WHERE id_sucursal = ?
            ORDER BY id_inventario_producto
            """,
            (id_sucursal,),
        )
        return [
            InventarioProducto(
                row["id_inventario_producto"],
                row["id_producto"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]

    def list_materias_primas(
        self,
        id_sucursal: int,
    ) -> list[InventarioMateriaPrima]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_mp, stock_actual, stock_minimo, id_materia
            FROM Inventario_materia_prima
            WHERE id_sucursal = ?
            ORDER BY id_inventario_mp
            """,
            (id_sucursal,),
        )
        return [
            InventarioMateriaPrima(
                row["id_inventario_mp"],
                row["id_materia"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]

    def update_producto(
        self,
        inventario_producto: InventarioProducto,
    ) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Inventario_producto
            SET stock_actual = ?, stock_minimo = ?
            WHERE id_inventario_producto = ?
            """,
            (
                inventario_producto.stockActual,
                inventario_producto.stockMinimo,
                inventario_producto.idInventario,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"El inventario de producto {inventario_producto.idInventario} no existe")

    def update_materia_prima(
        self,
        inventario_materia_prima: InventarioMateriaPrima,
    ) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Inventario_materia_prima
            SET stock_actual = ?, stock_minimo = ?
            WHERE id_inventario_mp = ?
            """,
            (
                inventario_materia_prima.stockActual,
                inventario_materia_prima.stockMinimo,
                inventario_materia_prima.idInventario,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"El inventario de materia prima {inventario_materia_prima.idInventario} no existe")

    def list_alertas_productos(
        self,
        id_sucursal: int,
    ) -> list[InventarioProducto]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_producto, stock_actual, stock_minimo, id_producto
            FROM Inventario_producto
            WHERE id_sucursal = ? AND stock_actual <= stock_minimo
            ORDER BY id_inventario_producto
            """,
            (id_sucursal,),
        )
        return [
            InventarioProducto(
                row["id_inventario_producto"],
                row["id_producto"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]

    def list_alertas_materias_primas(
        self,
        id_sucursal: int,
    ) -> list[InventarioMateriaPrima]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_mp, stock_actual, stock_minimo, id_materia
            FROM Inventario_materia_prima
            WHERE id_sucursal = ? AND stock_actual <= stock_minimo
            ORDER BY id_inventario_mp
            """,
            (id_sucursal,),
        )
        return [
            InventarioMateriaPrima(
                row["id_inventario_mp"],
                row["id_materia"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]
