from el_chambre.application.services.catalogo_service import CatalogoService
from el_chambre.application.services.inventario_service import InventarioService
from el_chambre.application.services.produccion_service import ProduccionService
from el_chambre.application.services.receta_service import RecetaService
from el_chambre.application.services.venta_service import VentaService
from el_chambre.infrastructure.unit_of_work import SqliteUnitOfWork


def get_catalogo_service():
    return CatalogoService(SqliteUnitOfWork)


def get_inventario_service():
    return InventarioService(SqliteUnitOfWork)


def get_receta_service():
    return RecetaService(SqliteUnitOfWork)


def get_venta_service():
    return VentaService(SqliteUnitOfWork)


def get_produccion_service():
    return ProduccionService(SqliteUnitOfWork)
