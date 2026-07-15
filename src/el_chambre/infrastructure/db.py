"""Conexión y manejo de transacciones para la base de datos SQLite."""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "el_chambre.db"


def get_db_path() -> Path:
    """Obtiene la ruta configurada para la base de datos local."""
    configured_path = os.getenv("EL_CHAMBRE_DB_PATH")
    return Path(configured_path) if configured_path else DEFAULT_DB_PATH


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Crea una conexión SQLite lista para ser usada por los repositorios."""
    path = Path(db_path) if db_path else get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 5000")
    return connection


@contextmanager
def transaction(
    db_path: str | Path | None = None,
) -> Iterator[sqlite3.Connection]:
    """Confirma la operación completa o revierte todos sus cambios si falla."""
    connection = get_connection(db_path)

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
