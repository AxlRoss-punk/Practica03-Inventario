"""Reproduce el flujo visual y conserva capturas, entradas, consultas y SQLite."""

import json
import sqlite3
import sys
import tempfile
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path

from herramientas.captura import guardar_ventana_png
from inventario.entorno import crear_ventana
from inventario.interfaz import Aplicacion
from inventario.persistencia import BaseDatos
from inventario.servicios import Inventario

RAIZ = Path(__file__).resolve().parent


def main():
    carpeta = RAIZ / "evidencias"
    carpeta.mkdir(exist_ok=True)
    pasos = []
    with tempfile.TemporaryDirectory(prefix="practica3_evidencia_") as temporal:
        base = BaseDatos(Path(temporal) / "demostracion.sqlite3")
        servicio = Inventario(base)
        ventana = crear_ventana()
        ventana.withdraw()
        try:
            app = Aplicacion(ventana, servicio)
            ventana.deiconify()

            def capturar(nombre, entrada):
                ventana.update()
                if sys.platform == "win32":
                    guardar_ventana_png(ventana, carpeta / f"{nombre}.png")
                pasos.append({
                    "paso": nombre, "entrada": entrada, "mensaje": app.mensaje.get(),
                    "productos": servicio.productos(), "ventas": servicio.ventas(),
                })

            capturar("01_formulario", {})
            datos = {"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": "10", "precio": "2.50"}
            for clave, valor in datos.items():
                app.campos_producto[clave].set(valor)
            app.boton_producto.invoke()
            capturar("02_producto_guardado", datos)
            datos_venta = {"codigo": "LAP-01", "cantidad": "3", "descuento": "10"}
            for clave, valor in datos_venta.items():
                app.campos_venta[clave].set(valor)
            app.boton_venta.invoke()
            capturar("03_venta_realizada", datos_venta)
            app.campos_venta["cantidad"].set("8")
            app.boton_venta.invoke()
            capturar("04_stock_insuficiente", dict(datos_venta, cantidad="8"))
            app.campos_producto["codigo"].set("LAP-01")
            app.campos_producto["nombre"].set("Lápiz repetido")
            app.campos_producto["cantidad"].set("10")
            app.campos_producto["precio"].set("2.50")
            app.boton_producto.invoke()
            capturar("05_codigo_duplicado", {"codigo": "LAP-01"})
            with closing(sqlite3.connect(base.ruta)) as origen:
                with closing(sqlite3.connect(carpeta / "demostracion.sqlite3")) as copia:
                    # Backup sustituye el contenido de la evidencia; no modifica la base del usuario.
                    origen.backup(copia)
                consultas = [
                    "SELECT codigo, nombre, cantidad, precio_centavos FROM productos;",
                    "SELECT id, codigo, cantidad, descuento, total_centavos FROM ventas;",
                    "PRAGMA integrity_check;", "PRAGMA foreign_key_check;",
                ]
                lineas = []
                for consulta in consultas:
                    filas = origen.execute(consulta).fetchall()
                    lineas.extend([consulta, repr(filas), ""])
            (carpeta / "consultas_sql.txt").write_text("\n".join(lineas), encoding="utf-8")
        finally:
            ventana.destroy()
    datos = {"fecha": datetime.now(timezone(timedelta(hours=-4))).isoformat(timespec="seconds"), "modalidad": "SIMULADA", "pasos": pasos}
    (carpeta / "flujo_formularios.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Evidencias generadas en {carpeta}")


if __name__ == "__main__":
    main()
