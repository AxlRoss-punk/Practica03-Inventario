"""Induce un bloqueo real de la base de pruebas hasta pulsar Enter."""

import argparse
import sqlite3
from contextlib import closing
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Bloqueo controlado para CA-07; utilizar una base de prueba")
    parser.add_argument("--db", type=Path, required=True)
    argumentos = parser.parse_args()
    if not argumentos.db.is_file():
        parser.error("La base indicada no existe; abre primero la aplicación con esa misma ruta.")
    with closing(sqlite3.connect(argumentos.db, timeout=1)) as conexion:
        try:
            conexion.execute("BEGIN EXCLUSIVE")
            print(f"Bloqueo de prueba activo: {argumentos.db.resolve()}")
            input("Prueba ahora una venta en la aplicación. Pulsa Enter aquí para liberar la base: ")
        except (KeyboardInterrupt, EOFError):
            print("\nLiberando bloqueo.")
        finally:
            conexion.rollback()
    print("Base liberada. Puedes repetir la venta.")


if __name__ == "__main__":
    main()
