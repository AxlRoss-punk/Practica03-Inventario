"""Persistencia real en SQLite; cada operación usa una conexión independiente."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from inventario.dominio import ErrorPersistencia

ESQUEMA = """
CREATE TABLE IF NOT EXISTS productos (
    codigo TEXT PRIMARY KEY COLLATE NOCASE,
    nombre TEXT NOT NULL CHECK(length(trim(nombre)) BETWEEN 2 AND 80),
    cantidad INTEGER NOT NULL CHECK(typeof(cantidad) = 'integer' AND cantidad BETWEEN 0 AND 999999),
    precio_centavos INTEGER NOT NULL CHECK(typeof(precio_centavos) = 'integer' AND precio_centavos BETWEEN 0 AND 99999999)
);
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL REFERENCES productos(codigo),
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    descuento TEXT NOT NULL,
    total_centavos INTEGER NOT NULL CHECK(total_centavos >= 0),
    fecha TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
"""


class BaseDatos:
    def __init__(self, ruta):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.conexion() as conexion:
            conexion.executescript(ESQUEMA)

    @contextmanager
    def conexion(self):
        conexion = None
        try:
            conexion = sqlite3.connect(self.ruta, timeout=0.15)
            conexion.row_factory = sqlite3.Row
            conexion.execute("PRAGMA foreign_keys = ON")
            with conexion:
                yield conexion
        except sqlite3.Error as exc:
            raise ErrorPersistencia("No se pudo acceder a la base de datos. Intenta de nuevo.") from exc
        finally:
            if conexion is not None:
                conexion.close()

