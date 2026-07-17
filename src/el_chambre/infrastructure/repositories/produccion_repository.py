from datetime import date
from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import ProduccionRepository
from el_chambre.domain.entities.DetalleProduccion import DetalleProduccion
from el_chambre.domain.entities.Produccion import Produccion


class SqliteProduccionRepository(ProduccionRepository):
    """Repositorio SQLite para producciones y sus detalles."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(
        self,
        produccion: Produccion,
    ) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Produccion (fecha, observacion, id_sucursal)
            VALUES (?, ?, ?)
            """,
            (
                produccion._fechaProduccion.isoformat()
                if isinstance(produccion._fechaProduccion, date)
                else produccion._fechaProduccion,
                produccion.observacion,
                produccion.idSucursal,
            ),
        )
        id_produccion = cursor.lastrowid

        for detalle in produccion._detallesDeProduccion:
            self._connection.execute(
                """
                INSERT INTO Detalle_produccion (cantidad_producida, id_produccion, id_producto)
                VALUES (?, ?, ?)
                """,
                (
                    detalle.obtenerCantidadProducida(),
                    id_produccion,
                    detalle.idProducto,
                ),
            )

        return id_produccion

    def get_by_id(
        self,
        id_produccion: int,
    ) -> Produccion | None:
        cursor = self._connection.execute(
            """
            SELECT id_produccion, fecha, observacion, id_sucursal
            FROM Produccion
            WHERE id_produccion = ?
            """,
            (id_produccion,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        produccion = Produccion(
            row["id_produccion"],
            date.fromisoformat(row["fecha"]),
            row["observacion"],
            row["id_sucursal"],
        )

        for detalle in self._get_detalles(id_produccion):
            produccion._detallesDeProduccion.append(detalle)

        return produccion

    def list_all(
        self,
        id_sucursal: int | None = None,
    ) -> list[Produccion]:
        query = """
            SELECT id_produccion, fecha, observacion, id_sucursal
            FROM Produccion
        """
        params = ()
        if id_sucursal is not None:
            query += "WHERE id_sucursal = ?\n"
            params = (id_sucursal,)
        query += "ORDER BY id_produccion"

        cursor = self._connection.execute(query, params)
        producciones = []
        for row in cursor.fetchall():
            produccion = Produccion(
                row["id_produccion"],
                date.fromisoformat(row["fecha"]),
                row["observacion"],
                row["id_sucursal"],
            )
            for detalle in self._get_detalles(row["id_produccion"]):
                produccion._detallesDeProduccion.append(detalle)
            producciones.append(produccion)

        return producciones

    def _get_detalles(self, id_produccion: int) -> list[DetalleProduccion]:
        cursor = self._connection.execute(
            """
            SELECT id_det_produccion, cantidad_producida, id_producto
            FROM Detalle_produccion
            WHERE id_produccion = ?
            ORDER BY id_det_produccion
            """,
            (id_produccion,),
        )
        return [
            DetalleProduccion(
                row["id_det_produccion"],
                row["id_producto"],
                row["cantidad_producida"],
            )
            for row in cursor.fetchall()
        ]
