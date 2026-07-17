from datetime import date
from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import VentaRepository
from el_chambre.domain.entities.DetalleVenta import DetalleVenta
from el_chambre.domain.entities.Venta import Venta


class SqliteVentaRepository(VentaRepository):
    """Repositorio SQLite para ventas y sus detalles."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(
        self,
        venta: Venta,
    ) -> int:
        total = sum(detalle.obtenerSubtotal() for detalle in venta._detalleVenta)
        cursor = self._connection.execute(
            """
            INSERT INTO Venta (fecha, total, metodo_pago, id_sucursal)
            VALUES (?, ?, ?, ?)
            """,
            (
                venta.fechaVenta.isoformat()
                if isinstance(venta.fechaVenta, date)
                else venta.fechaVenta,
                total,
                venta.metodoPago,
                venta.idSucursal,
            ),
        )
        id_venta = cursor.lastrowid
        for detalle in venta._detalleVenta:
            self._connection.execute(
                """
                INSERT INTO Detalle_venta (cantidad, subtotal, id_venta, id_producto)
                VALUES (?, ?, ?, ?)
                """,
                (
                    detalle.obtenerCantidad(),
                    detalle.obtenerSubtotal(),
                    id_venta,
                    detalle.idProducto,
                ),
            )
        return id_venta

    def get_by_id(
        self,
        id_venta: int,
    ) -> Venta | None:
        cursor = self._connection.execute(
            """
            SELECT id_venta, fecha, total, metodo_pago, id_sucursal
            FROM Venta
            WHERE id_venta = ?
            """,
            (id_venta,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        venta = Venta(
            row["id_venta"],
            date.fromisoformat(row["fecha"]),
            row["metodo_pago"],
            row["id_sucursal"],
        )
        venta._total = row["total"]

        detalles = self._get_detalles(id_venta)
        for detalle in detalles:
            venta.agregarDetalleVenta(detalle)

        return venta

    def list_all(
        self,
        id_sucursal: int | None = None,
    ) -> list[Venta]:
        query = """
            SELECT id_venta, fecha, total, metodo_pago, id_sucursal
            FROM Venta
        """
        params = ()
        if id_sucursal is not None:
            query += "WHERE id_sucursal = ?\n"
            params = (id_sucursal,)
        query += "ORDER BY id_venta"

        cursor = self._connection.execute(query, params)
        ventas = []
        for row in cursor.fetchall():
            venta = Venta(
                row["id_venta"],
                date.fromisoformat(row["fecha"]),
                row["metodo_pago"],
                row["id_sucursal"],
            )
            venta._total = row["total"]
            for detalle in self._get_detalles(row["id_venta"]):
                venta.agregarDetalleVenta(detalle)
            ventas.append(venta)
        return ventas

    def _get_detalles(self, id_venta: int) -> list[DetalleVenta]:
        cursor = self._connection.execute(
            """
            SELECT id_det_venta, cantidad, subtotal, id_producto
            FROM Detalle_venta
            WHERE id_venta = ?
            ORDER BY id_det_venta
            """,
            (id_venta,),
        )
        return [
            DetalleVenta(
                row["id_det_venta"],
                row["id_producto"],
                row["cantidad"],
            )
            for row in cursor.fetchall()
        ]
