from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import RecetaRepository
from el_chambre.domain.entities.DetalleReceta import DetalleReceta


class SqliteRecetaRepository(RecetaRepository):
    """Repositorio SQLite para los detalles de receta."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def get_by_producto(
        self,
        id_producto: int,
    ) -> list[DetalleReceta]:
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

    def replace(
        self,
        id_producto: int,
        detalles: list[DetalleReceta],
    ) -> None:
        self._connection.execute(
            """
            DELETE FROM Detalle_receta
            WHERE id_producto = ?
            """,
            (id_producto,),
        )
        for detalle in detalles:
            self._connection.execute(
                """
                INSERT INTO Detalle_receta (cantidad_usada, id_producto, id_materia)
                VALUES (?, ?, ?)
                """,
                (
                    detalle.obtenerCantidadUsada(),
                    id_producto,
                    detalle.obtenerIdMateriaPrima(),
                ),
            )

    def delete_by_producto(
        self,
        id_producto: int,
    ) -> None:
        self._connection.execute(
            """
            DELETE FROM Detalle_receta
            WHERE id_producto = ?
            """,
            (id_producto,),
        )
