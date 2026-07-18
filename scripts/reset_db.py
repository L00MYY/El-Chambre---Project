"""Elimina y reconstruye la base de datos SQLite local."""

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from el_chambre.infrastructure.db import get_db_path
from init_db import init_database


SQLITE_EXTENSIONS = {".db", ".sqlite", ".sqlite3"}


def _confirm_reset(db_path: Path) -> bool:
    answer = input(
        f"Se eliminarán todos los datos de {db_path}. ¿Continuar? [s/N]: "
    )
    return answer.strip().lower() in {"s", "si", "sí", "y", "yes"}


def reset_database(skip_confirmation: bool = False) -> Path | None:
    """Elimina la base actual y crea nuevamente el esquema vacío."""
    db_path = get_db_path().resolve()

    if db_path.suffix.lower() not in SQLITE_EXTENSIONS:
        raise ValueError(
            "La ruta configurada no parece corresponder a una base SQLite: "
            f"{db_path}"
        )

    if db_path.exists():
        if not db_path.is_file():
            raise ValueError(f"La ruta de la base no es un archivo: {db_path}")
        if not skip_confirmation and not _confirm_reset(db_path):
            print("Reinicio cancelado. La base de datos no fue modificada.")
            return None
        db_path.unlink()

    initialized_path = init_database()
    print(f"Base de datos reiniciada en: {initialized_path}")
    return initialized_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Elimina los datos locales y reconstruye la base SQLite.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="omite la confirmación interactiva",
    )
    args = parser.parse_args()
    reset_database(skip_confirmation=args.yes)


if __name__ == "__main__":
    main()
