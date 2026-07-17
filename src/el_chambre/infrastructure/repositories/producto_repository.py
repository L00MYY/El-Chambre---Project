import sqlite3
from sqlite3 import Connection
from datetime import date

from el_chambre.application.interfaces.repositories import ProductoRepository
from el_chambre.domain.entities.DetalleReceta import DetalleReceta
from el_chambre.domain.entities.Producto import Producto


class SqliteProductoRepository(ProductoRepository):
    """Repositorio SQLite para la entidad Producto."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(self, producto: Producto) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Producto (nombre, precio, descripcion)
            VALUES (?, ?, ?)
            """,
            (producto.nombre, producto.precio, producto.descripcion),
        )
        return cursor.lastrowid

    def get_by_id(self, id_producto: int) -> Producto | None:
        cursor = self._connection.execute(
            """
            SELECT id_producto, nombre, precio, descripcion
            FROM Producto
            WHERE id_producto = ?
            """,
            (id_producto,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        detalles = self._get_receta(id_producto)
        return Producto(
            row["id_producto"],
            row["nombre"],
            row["precio"],
            row["descripcion"],
            detalles,
        )

    def list_all(self) -> list[Producto]:
        cursor = self._connection.execute(
            """
            SELECT id_producto, nombre, precio, descripcion
            FROM Producto
            ORDER BY id_producto
            """
        )
        productos = []
        for row in cursor.fetchall():
            detalles = self._get_receta(row["id_producto"])
            productos.append(
                Producto(
                    row["id_producto"],
                    row["nombre"],
                    row["precio"],
                    row["descripcion"],
                    detalles,
                )
            )
        return productos

    def update(self, producto: Producto) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Producto
            SET nombre = ?, precio = ?, descripcion = ?
            WHERE id_producto = ?
            """,
            (
                producto.nombre,
                producto.precio,
                producto.descripcion,
                producto.idProducto,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"El producto {producto.idProducto} no existe")

    def _get_receta(self, id_producto: int) -> list[DetalleReceta]:
        cursor = self._connection.execute(
            """
            SELECT id_detalle_receta, id_materia, cantidad_usada
            FROM Detalle_receta
            WHERE id_producto = ?
            ORDER BY id_detalle_receta
            """,
            (id_producto,),
        )
        return [
            DetalleReceta(
                row["id_detalle_receta"],
                row["id_materia"],
                row["cantidad_usada"],
            )
            for row in cursor.fetchall()
        ]
