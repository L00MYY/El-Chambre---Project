from __future__ import annotations

from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import AbstractUnitOfWork
from el_chambre.infrastructure.db import get_connection
from el_chambre.infrastructure.repositories import (
    SqliteSucursalRepository,
    SqliteProductoRepository,
    SqliteMateriaPrimaRepository,
    SqliteInventarioRepository,
    SqliteRecetaRepository,
    SqliteVentaRepository,
    SqliteProduccionRepository,
)


class SqliteUnitOfWork(AbstractUnitOfWork):
    """Unidad de trabajo SQLite que agrupa repositorios y controla transacción."""

    def __init__(self, db_path: str | None = None):
        self._db_path = db_path
        self._connection: Connection | None = None
        self.sucursales = None
        self.productos = None
        self.materias_primas = None
        self.inventarios = None
        self.recetas = None
        self.ventas = None
        self.producciones = None

    def __enter__(self) -> SqliteUnitOfWork:
        self._connection = get_connection(self._db_path)
        self.sucursales = SqliteSucursalRepository(self._connection)
        self.productos = SqliteProductoRepository(self._connection)
        self.materias_primas = SqliteMateriaPrimaRepository(self._connection)
        self.inventarios = SqliteInventarioRepository(self._connection)
        self.recetas = SqliteRecetaRepository(self._connection)
        self.ventas = SqliteVentaRepository(self._connection)
        self.producciones = SqliteProduccionRepository(self._connection)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: type[BaseException] | None,
    ) -> None:
        if self._connection is None:
            return

        if exc_type:
            self._connection.rollback()
        else:
            self._connection.commit()

        self._connection.close()
        self._connection = None

    def commit(self) -> None:
        if self._connection is None:
            raise RuntimeError("La conexión no está abierta")
        self._connection.commit()

    def rollback(self) -> None:
        if self._connection is None:
            raise RuntimeError("La conexión no está abierta")
        self._connection.rollback()
