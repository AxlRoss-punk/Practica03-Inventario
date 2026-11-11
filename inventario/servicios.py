"""Coordinación de registro, inventario y ventas."""

import sqlite3
from decimal import Decimal

from inventario.dominio import (
    ErrorValidacion,
    calcular_total_venta,
    validar_cantidad,
    validar_codigo,
    validar_descuento,
    validar_nombre,
    validar_precio,
)


class Inventario:
    def __init__(self, base):
        self.base = base

    def registrar_producto(self, codigo, nombre, cantidad, precio):
        codigo = validar_codigo(codigo)
        nombre = validar_nombre(nombre)
        cantidad = validar_cantidad(cantidad)
        precio = validar_precio(precio)
        with self.base.conexion() as conexion:
            try:
                conexion.execute(
                    "INSERT INTO productos VALUES (?, ?, ?, ?)",
                    (codigo, nombre, cantidad, int(precio * 100)),
                )
            except sqlite3.IntegrityError as exc:
                if conexion.execute("SELECT 1 FROM productos WHERE codigo = ?", (codigo,)).fetchone():
                    raise ErrorValidacion("Ya existe un producto con ese código.") from exc
                raise
        return codigo

    def productos(self):
        with self.base.conexion() as conexion:
            return [dict(fila) for fila in conexion.execute("SELECT * FROM productos ORDER BY codigo")]

    def ventas(self):
        with self.base.conexion() as conexion:
            return [dict(fila) for fila in conexion.execute("SELECT * FROM ventas ORDER BY id")]

    def registrar_venta(self, codigo, cantidad, descuento="0"):
        codigo = validar_codigo(codigo)
        cantidad = validar_cantidad(cantidad, permitir_cero=False)
        descuento = validar_descuento(descuento)
        with self.base.conexion() as conexion:
            # Reserva la escritura antes de leer el stock: dos ventas concurrentes se serializan.
            conexion.execute("BEGIN IMMEDIATE")
            producto = conexion.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,)).fetchone()
            if producto is None:
                raise ErrorValidacion("No existe un producto con ese código.")
            if producto["cantidad"] < cantidad:
                raise ErrorValidacion("No hay existencias suficientes para realizar la venta.")
            total = calcular_total_venta(cantidad, Decimal(producto["precio_centavos"]) / 100, descuento)
            conexion.execute("UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?", (cantidad, codigo))
            cursor = conexion.execute(
                "INSERT INTO ventas (codigo, cantidad, descuento, total_centavos) VALUES (?, ?, ?, ?)",
                (codigo, cantidad, str(descuento), int(total * 100)),
            )
            identificador = cursor.lastrowid
        return identificador, total

