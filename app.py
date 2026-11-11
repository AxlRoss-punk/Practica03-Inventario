"""Ejecutar: python app.py [--db ruta/a/inventario.sqlite3]."""

import argparse
import sys
from pathlib import Path
from tkinter import messagebox

from inventario.dominio import ErrorNegocio
from inventario.entorno import crear_ventana
from inventario.interfaz import Aplicacion
from inventario.persistencia import BaseDatos
from inventario.servicios import Inventario


def main():
    parser = argparse.ArgumentParser(description="Inventario de la práctica 3")
    parser.add_argument("--db", type=Path, default=Path(__file__).parent / "datos" / "inventario.sqlite3")
    argumentos = parser.parse_args()
    ventana = crear_ventana()
    ventana.withdraw()
    try:
        servicio = Inventario(BaseDatos(argumentos.db))
    except (ErrorNegocio, OSError) as exc:
        messagebox.showerror("No se pudo abrir el inventario", str(exc), parent=ventana)
        ventana.destroy()
        return 1
    Aplicacion(ventana, servicio)
    ventana.deiconify()
    ventana.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
