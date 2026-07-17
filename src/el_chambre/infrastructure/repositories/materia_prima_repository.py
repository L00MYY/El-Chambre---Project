from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import MateriaPrimaRepository
from el_chambre.domain.entities.MateriaPrima import MateriaPrima


class SqliteMateriaPrimaRepository(MateriaPrimaRepository):
    """Repositorio SQLite para la entidad MateriaPrima."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(self, materia_prima: MateriaPrima) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Materia_prima (nombre, unidad_medida, costo_unitario, descripcion)
            VALUES (?, ?, ?, ?)
            """,
            (
                materia_prima.nombre,
                materia_prima.unidadMedida,
                materia_prima.costoUnitario,
                materia_prima.descripcion,
            ),
        )
        return cursor.lastrowid

    def get_by_id(self, id_materia: int) -> MateriaPrima | None:
        cursor = self._connection.execute(
            """
            SELECT id_materia, nombre, unidad_medida, costo_unitario, descripcion
            FROM Materia_prima
            WHERE id_materia = ?
            """,
            (id_materia,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return MateriaPrima(
            row["id_materia"],
            row["nombre"],
            row["unidad_medida"],
            row["costo_unitario"],
            row["descripcion"],
        )

    def list_all(self) -> list[MateriaPrima]:
        cursor = self._connection.execute(
            """
            SELECT id_materia, nombre, unidad_medida, costo_unitario, descripcion
            FROM Materia_prima
            ORDER BY id_materia
            """
        )
        return [
            MateriaPrima(
                row["id_materia"],
                row["nombre"],
                row["unidad_medida"],
                row["costo_unitario"],
                row["descripcion"],
            )
            for row in cursor.fetchall()
        ]

    def update(self, materia_prima: MateriaPrima) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Materia_prima
            SET nombre = ?, unidad_medida = ?, costo_unitario = ?, descripcion = ?
            WHERE id_materia = ?
            """,
            (
                materia_prima.nombre,
                materia_prima.unidadMedida,
                materia_prima.costoUnitario,
                materia_prima.descripcion,
                materia_prima.idMateriaPrima,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"La materia prima {materia_prima.idMateriaPrima} no existe")
