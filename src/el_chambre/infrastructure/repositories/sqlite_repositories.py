"""Implementaciones SQLite de los repositorios de la aplicación."""

from datetime import date
from sqlite3 import Connection

from el_chambre.application.interfaces.repositories import (
    InventarioRepository,
    MateriaPrimaRepository,
    ProduccionRepository,
    ProductoRepository,
    RecetaRepository,
    SucursalRepository,
    VentaRepository,
)
from el_chambre.domain.entities.DetalleProduccion import DetalleProduccion
from el_chambre.domain.entities.DetalleReceta import DetalleReceta
from el_chambre.domain.entities.DetalleVenta import DetalleVenta
from el_chambre.domain.entities.InventarioMateriaPrima import InventarioMateriaPrima
from el_chambre.domain.entities.InventarioProducto import InventarioProducto
from el_chambre.domain.entities.MateriaPrima import MateriaPrima
from el_chambre.domain.entities.Produccion import Produccion
from el_chambre.domain.entities.Producto import Producto
from el_chambre.domain.entities.Sucursal import Sucursal
from el_chambre.domain.entities.Venta import Venta


class SqliteSucursalRepository(SucursalRepository):
    """Repositorio SQLite para sucursales."""

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


class SqliteProductoRepository(ProductoRepository):
    """Repositorio SQLite para productos."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(self, producto: Producto) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Producto (nombre, precio, descripcion)
            VALUES (?, ?, ?)
            """,
            (producto.nombre, producto.precio, producto.descripcion),
        )
        return cursor.lastrowid

    def get_by_id(self, id_producto: int) -> Producto | None:
        cursor = self._connection.execute(
            """
            SELECT id_producto, nombre, precio, descripcion
            FROM Producto
            WHERE id_producto = ?
            """,
            (id_producto,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Producto(
            row["id_producto"],
            row["nombre"],
            row["precio"],
            row["descripcion"],
            self._get_receta(id_producto),
        )

    def list_all(self) -> list[Producto]:
        cursor = self._connection.execute(
            """
            SELECT id_producto, nombre, precio, descripcion
            FROM Producto
            ORDER BY id_producto
            """
        )
        return [
            Producto(
                row["id_producto"],
                row["nombre"],
                row["precio"],
                row["descripcion"],
                self._get_receta(row["id_producto"]),
            )
            for row in cursor.fetchall()
        ]

    def update(self, producto: Producto) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Producto
            SET nombre = ?, precio = ?, descripcion = ?
            WHERE id_producto = ?
            """,
            (
                producto.nombre,
                producto.precio,
                producto.descripcion,
                producto.idProducto,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"El producto {producto.idProducto} no existe")

    def _get_receta(self, id_producto: int) -> list[DetalleReceta]:
        cursor = self._connection.execute(
            """
            SELECT id_detalle_receta, id_materia, cantidad_usada
            FROM Detalle_receta
            WHERE id_producto = ?
            ORDER BY id_detalle_receta
            """,
            (id_producto,),
        )
        return [
            DetalleReceta(
                row["id_detalle_receta"],
                row["id_materia"],
                row["cantidad_usada"],
            )
            for row in cursor.fetchall()
        ]


class SqliteMateriaPrimaRepository(MateriaPrimaRepository):
    """Repositorio SQLite para materias primas."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(self, materia_prima: MateriaPrima) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Materia_prima
                (nombre, unidad_medida, costo_unitario, descripcion)
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
            raise ValueError(
                f"La materia prima {materia_prima.idMateriaPrima} no existe"
            )


class SqliteInventarioRepository(InventarioRepository):
    """Repositorio SQLite para inventarios de productos y materias primas."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add_producto(
        self,
        id_sucursal: int,
        inventario_producto: InventarioProducto,
    ) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Inventario_producto
                (stock_actual, stock_minimo, id_sucursal, id_producto)
            VALUES (?, ?, ?, ?)
            """,
            (
                inventario_producto.stockActual,
                inventario_producto.stockMinimo,
                id_sucursal,
                inventario_producto.idProducto,
            ),
        )
        return cursor.lastrowid

    def add_materia_prima(
        self,
        id_sucursal: int,
        inventario_materia_prima: InventarioMateriaPrima,
    ) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO Inventario_materia_prima
                (stock_actual, stock_minimo, id_sucursal, id_materia)
            VALUES (?, ?, ?, ?)
            """,
            (
                inventario_materia_prima.stockActual,
                inventario_materia_prima.stockMinimo,
                id_sucursal,
                inventario_materia_prima.idMateriaPrima,
            ),
        )
        return cursor.lastrowid

    def get_producto(
        self,
        id_sucursal: int,
        id_producto: int,
    ) -> InventarioProducto | None:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_producto, stock_actual, stock_minimo, id_producto
            FROM Inventario_producto
            WHERE id_sucursal = ? AND id_producto = ?
            """,
            (id_sucursal, id_producto),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return InventarioProducto(
            row["id_inventario_producto"],
            row["id_producto"],
            row["stock_actual"],
            row["stock_minimo"],
        )

    def get_materia_prima(
        self,
        id_sucursal: int,
        id_materia: int,
    ) -> InventarioMateriaPrima | None:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_mp, stock_actual, stock_minimo, id_materia
            FROM Inventario_materia_prima
            WHERE id_sucursal = ? AND id_materia = ?
            """,
            (id_sucursal, id_materia),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return InventarioMateriaPrima(
            row["id_inventario_mp"],
            row["id_materia"],
            row["stock_actual"],
            row["stock_minimo"],
        )

    def list_productos(self, id_sucursal: int) -> list[InventarioProducto]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_producto, stock_actual, stock_minimo, id_producto
            FROM Inventario_producto
            WHERE id_sucursal = ?
            ORDER BY id_inventario_producto
            """,
            (id_sucursal,),
        )
        return [
            InventarioProducto(
                row["id_inventario_producto"],
                row["id_producto"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]

    def list_materias_primas(
        self,
        id_sucursal: int,
    ) -> list[InventarioMateriaPrima]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_mp, stock_actual, stock_minimo, id_materia
            FROM Inventario_materia_prima
            WHERE id_sucursal = ?
            ORDER BY id_inventario_mp
            """,
            (id_sucursal,),
        )
        return [
            InventarioMateriaPrima(
                row["id_inventario_mp"],
                row["id_materia"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]

    def update_producto(self, inventario_producto: InventarioProducto) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Inventario_producto
            SET stock_actual = ?, stock_minimo = ?
            WHERE id_inventario_producto = ?
            """,
            (
                inventario_producto.stockActual,
                inventario_producto.stockMinimo,
                inventario_producto.idInventario,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(
                f"El inventario de producto {inventario_producto.idInventario} no existe"
            )

    def update_materia_prima(
        self,
        inventario_materia_prima: InventarioMateriaPrima,
    ) -> None:
        cursor = self._connection.execute(
            """
            UPDATE Inventario_materia_prima
            SET stock_actual = ?, stock_minimo = ?
            WHERE id_inventario_mp = ?
            """,
            (
                inventario_materia_prima.stockActual,
                inventario_materia_prima.stockMinimo,
                inventario_materia_prima.idInventario,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError(
                "El inventario de materia prima "
                f"{inventario_materia_prima.idInventario} no existe"
            )

    def list_alertas_productos(
        self,
        id_sucursal: int,
    ) -> list[InventarioProducto]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_producto, stock_actual, stock_minimo, id_producto
            FROM Inventario_producto
            WHERE id_sucursal = ? AND stock_actual <= stock_minimo
            ORDER BY id_inventario_producto
            """,
            (id_sucursal,),
        )
        return [
            InventarioProducto(
                row["id_inventario_producto"],
                row["id_producto"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]

    def list_alertas_materias_primas(
        self,
        id_sucursal: int,
    ) -> list[InventarioMateriaPrima]:
        cursor = self._connection.execute(
            """
            SELECT id_inventario_mp, stock_actual, stock_minimo, id_materia
            FROM Inventario_materia_prima
            WHERE id_sucursal = ? AND stock_actual <= stock_minimo
            ORDER BY id_inventario_mp
            """,
            (id_sucursal,),
        )
        return [
            InventarioMateriaPrima(
                row["id_inventario_mp"],
                row["id_materia"],
                row["stock_actual"],
                row["stock_minimo"],
            )
            for row in cursor.fetchall()
        ]


class SqliteRecetaRepository(RecetaRepository):
    """Repositorio SQLite para detalles de recetas."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def get_by_producto(self, id_producto: int) -> list[DetalleReceta]:
        cursor = self._connection.execute(
            """
            SELECT id_detalle_receta, id_materia, cantidad_usada
            FROM Detalle_receta
            WHERE id_producto = ?
            ORDER BY id_detalle_receta
            """,
            (id_producto,),
        )
        return [
            DetalleReceta(
                row["id_detalle_receta"],
                row["id_materia"],
                row["cantidad_usada"],
            )
            for row in cursor.fetchall()
        ]

    def replace(
        self,
        id_producto: int,
        detalles: list[DetalleReceta],
    ) -> None:
        self._connection.execute(
            """
            DELETE FROM Detalle_receta
            WHERE id_producto = ?
            """,
            (id_producto,),
        )
        for detalle in detalles:
            self._connection.execute(
                """
                INSERT INTO Detalle_receta
                    (cantidad_usada, id_producto, id_materia)
                VALUES (?, ?, ?)
                """,
                (
                    detalle.obtenerCantidadUsada(),
                    id_producto,
                    detalle.obtenerIdMateriaPrima(),
                ),
            )

    def delete_by_producto(self, id_producto: int) -> None:
        self._connection.execute(
            """
            DELETE FROM Detalle_receta
            WHERE id_producto = ?
            """,
            (id_producto,),
        )


class SqliteVentaRepository(VentaRepository):
    """Repositorio SQLite para ventas y sus detalles."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(self, venta: Venta) -> int:
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
                INSERT INTO Detalle_venta
                    (cantidad, subtotal, id_venta, id_producto)
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

    def get_by_id(self, id_venta: int) -> Venta | None:
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
        for detalle in self._get_detalles(id_venta):
            venta.agregarDetalleVenta(detalle)
        return venta

    def list_all(self, id_sucursal: int | None = None) -> list[Venta]:
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
        detalles = []
        for row in cursor.fetchall():
            detalle = DetalleVenta(
                row["id_det_venta"],
                row["id_producto"],
                row["cantidad"],
            )
            detalle._subtotal = row["subtotal"]
            detalles.append(detalle)
        return detalles


class SqliteProduccionRepository(ProduccionRepository):
    """Repositorio SQLite para producciones y sus detalles."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def add(self, produccion: Produccion) -> int:
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
                INSERT INTO Detalle_produccion
                    (cantidad_producida, id_produccion, id_producto)
                VALUES (?, ?, ?)
                """,
                (
                    detalle.obtenerCantidadProducida(),
                    id_produccion,
                    detalle.idProducto,
                ),
            )
        return id_produccion

    def get_by_id(self, id_produccion: int) -> Produccion | None:
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
