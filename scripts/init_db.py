"""Crea las tablas necesarias para ejecutar El Chambre localmente."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from el_chambre.infrastructure.db import get_db_path, transaction


SCHEMA = """
BEGIN;

CREATE TABLE IF NOT EXISTS Sucursal (
    id_sucursal INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    direccion TEXT NOT NULL CHECK (length(trim(direccion)) > 0),
    telefono TEXT
);

CREATE TABLE IF NOT EXISTS Producto (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    precio NUMERIC NOT NULL CHECK (precio >= 0),
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS Materia_prima (
    id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    unidad_medida TEXT NOT NULL CHECK (length(trim(unidad_medida)) > 0),
    costo_unitario NUMERIC,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS Inventario_producto (
    id_inventario_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_actual INTEGER NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo INTEGER NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),
    id_sucursal INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    UNIQUE (id_sucursal, id_producto),
    FOREIGN KEY (id_sucursal)
        REFERENCES Sucursal(id_sucursal)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_producto)
        REFERENCES Producto(id_producto)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Inventario_materia_prima (
    id_inventario_mp INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_actual NUMERIC NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo NUMERIC NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),
    id_sucursal INTEGER NOT NULL,
    id_materia INTEGER NOT NULL,
    UNIQUE (id_sucursal, id_materia),
    FOREIGN KEY (id_sucursal)
        REFERENCES Sucursal(id_sucursal)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_materia)
        REFERENCES Materia_prima(id_materia)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Produccion (
    id_produccion INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    observacion TEXT,
    id_sucursal INTEGER NOT NULL,
    FOREIGN KEY (id_sucursal)
        REFERENCES Sucursal(id_sucursal)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Detalle_produccion (
    id_det_produccion INTEGER PRIMARY KEY AUTOINCREMENT,
    cantidad_producida INTEGER NOT NULL CHECK (cantidad_producida > 0),
    id_produccion INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    UNIQUE (id_produccion, id_producto),
    FOREIGN KEY (id_produccion)
        REFERENCES Produccion(id_produccion)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_producto)
        REFERENCES Producto(id_producto)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Detalle_receta (
    id_detalle_receta INTEGER PRIMARY KEY AUTOINCREMENT,
    cantidad_usada NUMERIC NOT NULL CHECK (cantidad_usada > 0),
    id_producto INTEGER NOT NULL,
    id_materia INTEGER NOT NULL,
    UNIQUE (id_producto, id_materia),
    FOREIGN KEY (id_producto)
        REFERENCES Producto(id_producto)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_materia)
        REFERENCES Materia_prima(id_materia)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Venta (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    total NUMERIC NOT NULL CHECK (total >= 0),
    metodo_pago TEXT NOT NULL CHECK (length(trim(metodo_pago)) > 0),
    id_sucursal INTEGER NOT NULL,
    FOREIGN KEY (id_sucursal)
        REFERENCES Sucursal(id_sucursal)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Detalle_venta (
    id_det_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    subtotal NUMERIC NOT NULL CHECK (subtotal >= 0),
    id_venta INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    UNIQUE (id_venta, id_producto),
    FOREIGN KEY (id_venta)
        REFERENCES Venta(id_venta)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_producto)
        REFERENCES Producto(id_producto)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_venta_sucursal
    ON Venta(id_sucursal);
CREATE INDEX IF NOT EXISTS idx_produccion_sucursal
    ON Produccion(id_sucursal);
CREATE INDEX IF NOT EXISTS idx_inventario_producto_stock
    ON Inventario_producto(id_sucursal, stock_actual, stock_minimo);
CREATE INDEX IF NOT EXISTS idx_inventario_mp_stock
    ON Inventario_materia_prima(id_sucursal, stock_actual, stock_minimo);

COMMIT;
"""


def init_database() -> Path:
    """Ejecuta el esquema de forma segura y devuelve la ruta creada."""
    db_path = get_db_path()

    with transaction(db_path) as connection:
        connection.executescript(SCHEMA)

    return db_path


if __name__ == "__main__":
    database_path = init_database()
    print(f"Base de datos preparada en: {database_path}")
