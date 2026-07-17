"""
InventarioService — Integrante 1, Tarea 2.

Gestiona inventarios iniciales, entradas/salidas manuales, stocks mínimos,
consultas de existencias y alertas.

No escribe SQL, no abre conexiones directamente: todo pasa por una
Unidad de Trabajo obtenida de `uow_factory`.

Recordatorio de la regla transaccional del documento: este servicio es
SOLO para ajustes manuales. VentaService y ProduccionService no deben
llamarlo — ellos modifican inventarios dentro de su propia unidad de
trabajo para no partir la transacción en dos.
"""

from el_chambre.application.exceptions.exceptions import (
    ValidationError,
    NotFoundError,
    ConflictError,
    InsufficientStockError,
)
from el_chambre.domain.entities.InventarioProducto import InventarioProducto
from el_chambre.domain.entities.InventarioMateriaPrima import InventarioMateriaPrima


class InventarioService:
    def __init__(self, uow_factory):
        """uow_factory: callable sin argumentos que devuelve una nueva
        instancia de AbstractUnitOfWork (por ejemplo, la clase
        SqliteUnitOfWork que construya infraestructura)."""
        self._uow_factory = uow_factory

    # ------------
    # Crear inventarios
    # ------------

    def crear_inventario_producto(self, id_sucursal, id_producto, stock_inicial=0, stock_minimo=0):
        with self._uow_factory() as uow:
            sucursal = uow.sucursales.get_by_id(id_sucursal)
            if sucursal is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")

            producto = uow.productos.get_by_id(id_producto)
            if producto is None:
                raise NotFoundError(f"El producto {id_producto} no existe")

            if stock_inicial < 0:
                raise ValidationError("El stock inicial no puede ser negativo")
            if stock_minimo < 0:
                raise ValidationError("El stock mínimo no puede ser negativo")

            if uow.inventarios.get_producto(id_sucursal, id_producto) is not None:
                raise ConflictError(
                    f"Ya existe inventario del producto {id_producto} en la sucursal {id_sucursal}"
                )

            inventario = InventarioProducto(
                idInventario=0,
                idProducto=id_producto,
                stockActual=stock_inicial,
                stockMinimo=stock_minimo,
            )
            nuevo_id = uow.inventarios.add_producto(id_sucursal, inventario)
            inventario.idInventario = nuevo_id
            uow.commit()
            return inventario

    def crear_inventario_materia_prima(self, id_sucursal, id_materia, stock_inicial=0, stock_minimo=0):
        with self._uow_factory() as uow:
            sucursal = uow.sucursales.get_by_id(id_sucursal)
            if sucursal is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")

            materia_prima = uow.materias_primas.get_by_id(id_materia)
            if materia_prima is None:
                raise NotFoundError(f"La materia prima {id_materia} no existe")

            if stock_inicial < 0:
                raise ValidationError("El stock inicial no puede ser negativo")
            if stock_minimo < 0:
                raise ValidationError("El stock mínimo no puede ser negativo")

            if uow.inventarios.get_materia_prima(id_sucursal, id_materia) is not None:
                raise ConflictError(
                    f"Ya existe inventario de la materia prima {id_materia} en la sucursal {id_sucursal}"
                )

            inventario = InventarioMateriaPrima(
                idInventario=0,
                idMateriaPrima=id_materia,
                stockActual=stock_inicial,
                stockMinimo=stock_minimo,
            )
            nuevo_id = uow.inventarios.add_materia_prima(id_sucursal, inventario)
            inventario.idInventario = nuevo_id
            uow.commit()
            return inventario

    # ------------
    # Ajustes manuales de stock (entrada / salida)
    # ------------

    def ajustar_stock_producto(self, id_sucursal, id_producto, tipo, cantidad):
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que 0")
        if tipo not in ("entrada", "salida"):
            raise ValidationError("El tipo debe ser 'entrada' o 'salida'")

        with self._uow_factory() as uow:
            inventario = uow.inventarios.get_producto(id_sucursal, id_producto)
            if inventario is None:
                raise NotFoundError(
                    f"No existe inventario del producto {id_producto} en la sucursal {id_sucursal}"
                )

            if tipo == "salida":
                if not inventario.validarStockSuficente(cantidad):
                    raise InsufficientStockError(
                        f"Stock insuficiente del producto {id_producto} para la salida solicitada"
                    )
                movimiento = -cantidad
            else:
                movimiento = cantidad

            inventario.actualizarStock(movimiento)
            uow.inventarios.update_producto(inventario)
            uow.commit()

            return {
                "stock_actual": inventario.stockActual,
                "en_alerta": inventario.validarAlerta(),
            }

    def ajustar_stock_materia_prima(self, id_sucursal, id_materia, tipo, cantidad):
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que 0")
        if tipo not in ("entrada", "salida"):
            raise ValidationError("El tipo debe ser 'entrada' o 'salida'")

        with self._uow_factory() as uow:
            inventario = uow.inventarios.get_materia_prima(id_sucursal, id_materia)
            if inventario is None:
                raise NotFoundError(
                    f"No existe inventario de la materia prima {id_materia} en la sucursal {id_sucursal}"
                )

            if tipo == "salida":
                if not inventario.validarStockSuficente(cantidad):
                    raise InsufficientStockError(
                        f"Stock insuficiente de la materia prima {id_materia} para la salida solicitada"
                    )
                movimiento = -cantidad
            else:
                movimiento = cantidad

            inventario.actualizarStock(movimiento)
            uow.inventarios.update_materia_prima(inventario)
            uow.commit()

            return {
                "stock_actual": inventario.stockActual,
                "en_alerta": inventario.validarAlerta(),
            }
    # ------------
    # Stocks mínimos
    # ------------
    def actualizar_minimo_producto(self, id_sucursal, id_producto, stock_minimo):
        if stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo")

        with self._uow_factory() as uow:
            inventario = uow.inventarios.get_producto(id_sucursal, id_producto)
            if inventario is None:
                raise NotFoundError(
                    f"No existe inventario del producto {id_producto} en la sucursal {id_sucursal}"
                )
            inventario.stockMinimo = stock_minimo
            uow.inventarios.update_producto(inventario)
            uow.commit()
            return inventario

    def actualizar_minimo_materia_prima(self, id_sucursal, id_materia, stock_minimo):
        if stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo")

        with self._uow_factory() as uow:
            inventario = uow.inventarios.get_materia_prima(id_sucursal, id_materia)
            if inventario is None:
                raise NotFoundError(
                    f"No existe inventario de la materia prima {id_materia} en la sucursal {id_sucursal}"
                )
            inventario.stockMinimo = stock_minimo
            uow.inventarios.update_materia_prima(inventario)
            uow.commit()
            return inventario

    # ------------
    # Consultas (nunca hacen commit)
    # ------------

    def listar_productos(self, id_sucursal):
        with self._uow_factory() as uow:
            if uow.sucursales.get_by_id(id_sucursal) is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")
            return uow.inventarios.list_productos(id_sucursal)

    def listar_materias_primas(self, id_sucursal):
        with self._uow_factory() as uow:
            if uow.sucursales.get_by_id(id_sucursal) is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")
            return uow.inventarios.list_materias_primas(id_sucursal)

    def obtener_alertas(self, id_sucursal):
        with self._uow_factory() as uow:
            if uow.sucursales.get_by_id(id_sucursal) is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")
            return {
                "productos": uow.inventarios.list_alertas_productos(id_sucursal),
                "materias_primas": uow.inventarios.list_alertas_materias_primas(id_sucursal),
            }