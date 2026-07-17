import sqlite3
from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import SucursalRepository
from el_chambre.domain.entities.Sucursal import Sucursal


class SqliteSucursalRepository(SucursalRepository):
    """Repositorio SQLite para la entidad Sucursal."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(self, sucursal: Sucursal) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Sucursal (nombre, direccion, telefono)
            VALUES (?, ?, ?)
            """,
            (sucursal._nombre, sucursal._direccion, sucursal._telefono),
        )
        return cursor.lastrowid

    def get_by_id(self, id_sucursal: int) -> Sucursal | None:
        cursor = self._connection.execute(
            """
            SELECT id_sucursal, nombre, direccion, telefono
            FROM Sucursal
            WHERE id_sucursal = ?
            """,
            (id_sucursal,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Sucursal(
            row["id_sucursal"],
            row["nombre"],
            row["direccion"],
            row["telefono"],
        )

    def list_all(self) -> list[Sucursal]:
        cursor = self._connection.execute(
            """
            SELECT id_sucursal, nombre, direccion, telefono
            FROM Sucursal
            ORDER BY id_sucursal
            """
        )
        return [
            Sucursal(
                row["id_sucursal"],
                row["nombre"],
                row["direccion"],
                row["telefono"],
            )
            for row in cursor.fetchall()
        ]

    def update(self, sucursal: Sucursal) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Sucursal
            SET nombre = ?, direccion = ?, telefono = ?
            WHERE id_sucursal = ?
            """,
            (
                sucursal._nombre,
                sucursal._direccion,
                sucursal._telefono,
                sucursal._idSucursal,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"La sucursal {sucursal._idSucursal} no existe")
