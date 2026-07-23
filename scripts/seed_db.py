"""Carga datos de demostración en la base SQLite local."""

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from el_chambre.application.services.catalogo_service import CatalogoService
from el_chambre.application.services.inventario_service import InventarioService
from el_chambre.application.services.produccion_service import ProduccionService
from el_chambre.application.services.receta_service import RecetaService
from el_chambre.application.services.venta_service import VentaService
from el_chambre.infrastructure.db import get_db_path
from el_chambre.infrastructure.unit_of_work import SqliteUnitOfWork
from init_db import init_database
from reset_db import reset_database


def _database_has_data() -> bool:
    with SqliteUnitOfWork() as uow:
        return bool(
            uow.sucursales.list_all()
            or uow.productos.list_all()
            or uow.materias_primas.list_all()
        )


def seed_database(reset: bool = False) -> dict | None:
    """Crea un escenario demo completo sin duplicar datos existentes."""
    if reset:
        reset_database(skip_confirmation=True)
    else:
        init_database()

    if _database_has_data():
        print(
            "La base ya contiene datos. "
            "Usa --reset si deseas reemplazarlos por la demo."
        )
        return None

    catalogo = CatalogoService(SqliteUnitOfWork)
    inventario = InventarioService(SqliteUnitOfWork)
    recetas = RecetaService(SqliteUnitOfWork)
    producciones = ProduccionService(SqliteUnitOfWork)
    ventas = VentaService(SqliteUnitOfWork)

    # Catálogo
    centro = catalogo.crear_sucursal(
        "Sucursal Centro",
        "Calle principal, San Salvador",
        "2222-1000",
    )
    santa_tecla = catalogo.crear_sucursal(
        "Sucursal Santa Tecla",
        "Avenida Central, Santa Tecla",
        "2222-2000",
    )

    pan_frances = catalogo.crear_producto(
        "Pan francés",
        0.25,
        "Pan tradicional para consumo diario",
    )
    concha = catalogo.crear_producto(
        "Concha",
        0.75,
        "Pan dulce con cubierta de azúcar",
    )
    croissant = catalogo.crear_producto(
        "Croissant",
        1.25,
        "Pan hojaldrado con mantequilla",
    )

    harina = catalogo.crear_materia_prima(
        "Harina de trigo",
        "kg",
        1.20,
        "Harina para panificación",
    )
    azucar = catalogo.crear_materia_prima(
        "Azúcar",
        "kg",
        1.10,
        "Azúcar blanca",
    )
    mantequilla = catalogo.crear_materia_prima(
        "Mantequilla",
        "kg",
        4.50,
        "Mantequilla sin sal",
    )
    levadura = catalogo.crear_materia_prima(
        "Levadura",
        "kg",
        3.80,
        "Levadura para pan",
    )

    # Inventarios de productos terminados
    inventarios_productos = [
        (centro, pan_frances, 40, 10),
        (centro, concha, 20, 8),
        (centro, croissant, 15, 5),
        (santa_tecla, pan_frances, 25, 8),
        (santa_tecla, concha, 12, 5),
        (santa_tecla, croissant, 4, 4),
    ]
    for sucursal, producto, stock, minimo in inventarios_productos:
        inventario.crear_inventario_producto(
            sucursal._idSucursal,
            producto.idProducto,
            stock,
            minimo,
        )

    # Inventarios de materias primas
    inventarios_materias = [
        (centro, harina, 60, 15),
        (centro, azucar, 4, 5),
        (centro, mantequilla, 12, 4),
        (centro, levadura, 3, 1),
        (santa_tecla, harina, 35, 10),
        (santa_tecla, azucar, 10, 3),
        (santa_tecla, mantequilla, 6, 2),
        (santa_tecla, levadura, 1.5, 0.5),
    ]
    for sucursal, materia, stock, minimo in inventarios_materias:
        inventario.crear_inventario_materia_prima(
            sucursal._idSucursal,
            materia.idMateriaPrima,
            stock,
            minimo,
        )

    # Recetas
    recetas.guardar_receta(
        pan_frances.idProducto,
        [
            {"id_materia": harina.idMateriaPrima, "cantidad_usada": 0.10},
            {"id_materia": levadura.idMateriaPrima, "cantidad_usada": 0.005},
        ],
    )
    recetas.guardar_receta(
        concha.idProducto,
        [
            {"id_materia": harina.idMateriaPrima, "cantidad_usada": 0.12},
            {"id_materia": azucar.idMateriaPrima, "cantidad_usada": 0.03},
            {"id_materia": mantequilla.idMateriaPrima, "cantidad_usada": 0.02},
            {"id_materia": levadura.idMateriaPrima, "cantidad_usada": 0.005},
        ],
    )
    recetas.guardar_receta(
        croissant.idProducto,
        [
            {"id_materia": harina.idMateriaPrima, "cantidad_usada": 0.15},
            {"id_materia": mantequilla.idMateriaPrima, "cantidad_usada": 0.08},
            {"id_materia": levadura.idMateriaPrima, "cantidad_usada": 0.006},
        ],
    )

    # Movimientos demo
    producciones.registrar_produccion(
        centro._idSucursal,
        concha.idProducto,
        10,
        "Producción de apertura",
    )
    ventas.registrar_venta(
        centro._idSucursal,
        "efectivo",
        [
            {"id_producto": pan_frances.idProducto, "cantidad": 6},
            {"id_producto": concha.idProducto, "cantidad": 4},
        ],
    )
    ventas.registrar_venta(
        santa_tecla._idSucursal,
        "tarjeta",
        [
            {"id_producto": pan_frances.idProducto, "cantidad": 3},
            {"id_producto": croissant.idProducto, "cantidad": 1},
        ],
    )

    summary = {
        "sucursales": 2,
        "productos": 3,
        "materias_primas": 4,
        "recetas": 3,
        "producciones": 1,
        "ventas": 2,
    }
    print(f"Datos demo cargados en: {get_db_path()}")
    print(
        "Resumen: "
        + ", ".join(f"{name}={amount}" for name, amount in summary.items())
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Carga un escenario de demostración para El Chambre.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="reconstruye la base antes de cargar los datos demo",
    )
    args = parser.parse_args()
    seed_database(reset=args.reset)


if __name__ == "__main__":
    main()
