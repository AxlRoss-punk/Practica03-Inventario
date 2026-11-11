"""Formularios de escritorio. La interfaz llama a los mismos servicios probados."""

import tkinter as tk
from decimal import Decimal
from tkinter import ttk

from inventario.dominio import ErrorNegocio


class Aplicacion(ttk.Frame):
    def __init__(self, ventana, servicio):
        super().__init__(ventana, padding=20)
        self.servicio = servicio
        self.pack(fill="both", expand=True)
        ventana.title("Práctica 3 · Inventario y ventas")
        ventana.geometry("1040x720")
        ventana.minsize(850, 650)
        estilo = ttk.Style(ventana)
        estilo.theme_use("clam")
        estilo.configure("TButton", padding=(12, 7))
        estilo.configure("Treeview", rowheight=28)
        estilo.configure("Title.TLabel", font=("Segoe UI", 21, "bold"))
        ttk.Label(self, text="Inventario y ventas", style="Title.TLabel").pack(anchor="w")
        ttk.Label(self, text="Registra productos, controla existencias y consulta tus ventas.").pack(anchor="w", pady=(2, 16))

        formularios = ttk.Frame(self)
        formularios.pack(fill="x")
        formularios.columnconfigure((0, 1), weight=1)
        registro = ttk.LabelFrame(formularios, text="1. Registrar producto", padding=14)
        registro.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        venta = ttk.LabelFrame(formularios, text="2. Registrar venta", padding=14)
        venta.grid(row=0, column=1, sticky="nsew")
        self.campos_producto = self._campos(registro, (
            ("codigo", "Código *"), ("nombre", "Nombre *"),
            ("cantidad", "Cantidad inicial *"), ("precio", "Precio unitario *"),
        ))
        self.campos_venta = self._campos(venta, (
            ("codigo", "Código del producto *"), ("cantidad", "Cantidad a vender *"),
            ("descuento", "Descuento (%) * · de 0 a 20"),
        ))
        self.campos_venta["descuento"].set("0")
        self.boton_producto = ttk.Button(registro, text="Guardar producto", command=self.guardar_producto)
        self.boton_producto.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        self.boton_venta = ttk.Button(venta, text="Registrar venta", command=self.guardar_venta)
        self.boton_venta.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        self.mensaje = tk.StringVar(value="Los campos con * son obligatorios. Los importes se expresan en unidades monetarias.")
        self.estado = ttk.Label(self, textvariable=self.mensaje, wraplength=960)
        self.estado.pack(fill="x", pady=12)
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 6))
        ttk.Label(barra, text="Productos disponibles", font=("Segoe UI", 12, "bold")).pack(side="left")
        self.boton_actualizar = ttk.Button(barra, text="Actualizar consultas", command=self.actualizar)
        self.boton_actualizar.pack(side="right")
        self.tabla_productos = self._tabla(("Código", "Nombre", "Stock", "Precio", "Valor del stock"), 4)
        ttk.Label(self, text="Historial de ventas", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(12, 6))
        self.tabla_ventas = self._tabla(("Venta", "Código", "Cantidad", "Descuento (%)", "Total"), 3)
        self.actualizar()

    def _campos(self, contenedor, definiciones):
        contenedor.columnconfigure(1, weight=1)
        campos = {}
        for fila, (clave, etiqueta) in enumerate(definiciones):
            ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 10), pady=4)
            variable = tk.StringVar()
            ttk.Entry(contenedor, textvariable=variable, width=24).grid(row=fila, column=1, sticky="ew", pady=4)
            campos[clave] = variable
        return campos

    def _tabla(self, columnas, alto):
        bloque = ttk.Frame(self)
        bloque.pack(fill="both", expand=True)
        tabla = ttk.Treeview(bloque, columns=columnas, show="headings", height=alto)
        for columna in columnas:
            tabla.heading(columna, text=columna)
            tabla.column(columna, width=130, minwidth=80)
        barra = ttk.Scrollbar(bloque, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def _informar(self, texto, error=False):
        self.mensaje.set(texto)
        self.estado.configure(foreground="#a62020" if error else "#145c37")

    def guardar_producto(self):
        try:
            codigo = self.servicio.registrar_producto(**{k: v.get() for k, v in self.campos_producto.items()})
        except ErrorNegocio as exc:
            self._informar(str(exc), error=True)
            return
        self._informar(f"Producto {codigo} registrado correctamente.")
        for variable in self.campos_producto.values():
            variable.set("")
        self.actualizar()

    def guardar_venta(self):
        try:
            identificador, total = self.servicio.registrar_venta(**{k: v.get() for k, v in self.campos_venta.items()})
        except ErrorNegocio as exc:
            self._informar(str(exc), error=True)
            return
        self._informar(f"Venta {identificador} registrada correctamente. Total: {total:.2f}.")
        self.campos_venta["cantidad"].set("")
        self.actualizar()

    def actualizar(self):
        try:
            # Leer ambas consultas antes de sustituir los datos visibles.
            productos = self.servicio.productos()
            ventas = self.servicio.ventas()
        except ErrorNegocio as exc:
            self._informar(str(exc), error=True)
            return
        for tabla in (self.tabla_productos, self.tabla_ventas):
            for item in tabla.get_children():
                tabla.delete(item)
        for producto in productos:
            precio = Decimal(producto["precio_centavos"]) / 100
            self.tabla_productos.insert("", "end", values=(
                producto["codigo"], producto["nombre"], producto["cantidad"],
                f"{precio:.2f}", f"{precio * producto['cantidad']:.2f}",
            ))
        for venta in ventas:
            self.tabla_ventas.insert("", "end", values=(
                venta["id"], venta["codigo"], venta["cantidad"], venta["descuento"],
                f"{Decimal(venta['total_centavos']) / 100:.2f}",
            ))

