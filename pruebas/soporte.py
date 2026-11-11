import tempfile
import unittest
from pathlib import Path

from inventario.dominio import ErrorValidacion
from inventario.entorno import crear_ventana
from inventario.interfaz import Aplicacion
from inventario.persistencia import BaseDatos
from inventario.servicios import Inventario


def caso(identificador, descripcion, entrada):
    def decorar(funcion):
        funcion.caso_id = identificador
        funcion.descripcion = descripcion
        funcion.entrada = entrada
        return funcion
    return decorar


class Caso(unittest.TestCase):
    def verificar(self, esperado, obtenido):
        self.esperado = esperado
        self.obtenido = obtenido
        self.assertEqual(esperado, obtenido)

    def rechazar(self, operacion, mensaje, tipo=ErrorValidacion):
        self.esperado = mensaje
        with self.assertRaises(tipo) as resultado:
            operacion()
        self.obtenido = str(resultado.exception)
        self.assertEqual(mensaje, self.obtenido)


class CasoBaseDatos(Caso):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory(prefix="practica3_")
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "pruebas.sqlite3"
        self.base = BaseDatos(self.ruta)
        self.servicio = Inventario(self.base)

    def producto(self, codigo="LAP-01", cantidad="10", precio="2.50"):
        return self.servicio.registrar_producto(codigo, "Lápiz HB", cantidad, precio)

    def estado_db(self):
        return {"productos": self.servicio.productos(), "ventas": self.servicio.ventas()}


class CasoFormulario(CasoBaseDatos):
    def setUp(self):
        super().setUp()
        self.ventana = crear_ventana()
        self.ventana.withdraw()
        self.addCleanup(self.ventana.destroy)
        self.app = Aplicacion(self.ventana, self.servicio)
        self.evidencias = []

    def registrar(self, codigo="LAP-01", nombre="Lápiz HB", cantidad="10", precio="2.50"):
        datos = dict(codigo=codigo, nombre=nombre, cantidad=cantidad, precio=precio)
        for clave, valor in datos.items():
            self.app.campos_producto[clave].set(valor)
        self.app.boton_producto.invoke()
        self.evidencia("Registro de producto", datos)

    def vender(self, codigo="LAP-01", cantidad="3", descuento="10"):
        datos = dict(codigo=codigo, cantidad=cantidad, descuento=descuento)
        for clave, valor in datos.items():
            self.app.campos_venta[clave].set(valor)
        self.app.boton_venta.invoke()
        self.evidencia("Registro de venta", datos)

    def filas(self, tabla):
        return [list(tabla.item(item, "values")) for item in tabla.get_children()]

    def evidencia(self, accion, datos):
        self.evidencias.append({
            "accion": accion,
            "entrada_formulario": datos,
            "mensaje_visible": self.app.mensaje.get(),
            "tabla_productos": self.filas(self.app.tabla_productos),
            "tabla_ventas": self.filas(self.app.tabla_ventas),
            "base_datos": self.estado_db(),
        })

