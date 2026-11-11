import sqlite3

from pruebas.soporte import CasoFormulario, caso
from pruebas.test_integracion import MENSAJE_DB


class RegistroUsuario(CasoFormulario):
    @caso("E07-01", "El usuario encuentra los campos y acciones de registro", "abrir aplicación")
    def test_campos(self):
        self.verificar((["codigo", "nombre", "cantidad", "precio"], "Guardar producto"),
                       (list(self.app.campos_producto), self.app.boton_producto.cget("text")))

    @caso("E07-02", "El usuario registra y consulta el producto", "LAP-01, Lápiz HB, 10, 2.50")
    def test_registrar_consultar(self):
        self.registrar()
        self.verificar(("Producto LAP-01 registrado correctamente.", [["LAP-01", "Lápiz HB", "10", "2.50", "25.00"]]),
                       (self.app.mensaje.get(), self.filas(self.app.tabla_productos)))

    @caso("E07-03", "Mensaje comprensible y posibilidad de corregir un dato obligatorio", "nombre vacío; corregir a Lápiz HB")
    def test_corregir(self):
        self.registrar(nombre="")
        self.assertIn("nombre es obligatorio", self.app.mensaje.get())
        self.assertEqual("LAP-01", self.app.campos_producto["codigo"].get())
        self.registrar()
        self.verificar((1, "Producto LAP-01 registrado correctamente."), (len(self.servicio.productos()), self.app.mensaje.get()))

    @caso("E07-04", "La interfaz impide registrar un precio negativo", "precio -2.50")
    def test_regla_negativo(self):
        self.registrar(precio="-2.50")
        self.verificar(("El precio no puede ser negativo.", []), (self.app.mensaje.get(), self.filas(self.app.tabla_productos)))


class ProcesoCompleto(CasoFormulario):
    @caso("E08-01", "Registrar producto, vender, consultar stock e historial", "10 unidades a 2.50; vender 3 con 10 %")
    def test_flujo_completo(self):
        self.registrar()
        self.vender()
        self.app.boton_actualizar.invoke()
        self.verificar(("Venta 1 registrada correctamente. Total: 6.75.",
                        [["LAP-01", "Lápiz HB", "7", "2.50", "17.50"]], [["1", "LAP-01", "3", "10", "6.75"]]),
                       (self.app.mensaje.get(), self.filas(self.app.tabla_productos), self.filas(self.app.tabla_ventas)))

    @caso("E08-02", "Agotar existencias y comprobar rechazo de una segunda venta", "stock 2; vender 2; intentar vender 1")
    def test_agotar(self):
        self.registrar(cantidad="2")
        self.vender(cantidad="2", descuento="0")
        self.vender(cantidad="1", descuento="0")
        self.verificar(("No hay existencias suficientes para realizar la venta.", "0", 1),
                       (self.app.mensaje.get(), self.filas(self.app.tabla_productos)[0][2], len(self.filas(self.app.tabla_ventas))))


class ExcepcionesUsuario(CasoFormulario):
    @caso("E09-01", "Duplicado: se explica el error y se conserva el original", "registrar LAP-01 dos veces")
    def test_duplicado(self):
        self.registrar()
        antes = self.estado_db()
        self.registrar(nombre="Producto repetido")
        self.verificar(("Ya existe un producto con ese código.", antes), (self.app.mensaje.get(), self.estado_db()))

    @caso("E09-02", "Información incompleta: no se guarda", "cantidad de producto vacía")
    def test_incompleto(self):
        self.registrar(cantidad="")
        self.verificar(("La cantidad es obligatoria.", {"productos": [], "ventas": []}), (self.app.mensaje.get(), self.estado_db()))

    @caso("E09-03", "Existencias insuficientes: no se genera una venta", "stock 10; solicitar 11")
    def test_no_disponible(self):
        self.registrar()
        antes = self.estado_db()
        self.vender(cantidad="11")
        self.verificar(("No hay existencias suficientes para realizar la venta.", antes), (self.app.mensaje.get(), self.estado_db()))

    @caso("E09-04", "Producto inexistente: mensaje comprensible", "vender XXX-01 sin registrarlo")
    def test_inexistente(self):
        self.vender(codigo="XXX-01")
        self.verificar(("No existe un producto con ese código.", {"productos": [], "ventas": []}), (self.app.mensaje.get(), self.estado_db()))


class ValidacionFinalSimulada(CasoFormulario):
    @caso("E10-01", "CA-01: campos y acciones necesarios están disponibles", "abrir formulario de venta")
    def test_ca01_campos(self):
        self.verificar((["codigo", "cantidad", "descuento"], "Registrar venta"),
                       (list(self.app.campos_venta), self.app.boton_venta.cget("text")))

    @caso("E10-02", "CA-02: venta sin cantidad se rechaza y mantiene la información", "cantidad vacía")
    def test_ca02_obligatorios(self):
        self.registrar()
        antes = self.estado_db()
        self.vender(cantidad="")
        self.verificar(("La cantidad es obligatoria.", antes, "LAP-01"),
                       (self.app.mensaje.get(), self.estado_db(), self.app.campos_venta["codigo"].get()))

    @caso("E10-03", "CA-03: el descuento máximo se aplica correctamente", "venta 2 × 2.50; descuento 20 %")
    def test_ca03_descuento_maximo(self):
        self.registrar()
        self.vender(cantidad="2", descuento="20")
        self.verificar(("Venta 1 registrada correctamente. Total: 4.00.", 400),
                       (self.app.mensaje.get(), self.servicio.ventas()[0]["total_centavos"]))

    @caso("E10-04", "CA-04: descuento excesivo se rechaza sin cambios", "descuento 20.01 %")
    def test_ca04_descuento_invalido(self):
        self.registrar()
        antes = self.estado_db()
        self.vender(descuento="20.01")
        self.verificar(("El descuento no puede superar 20.", antes), (self.app.mensaje.get(), self.estado_db()))

    @caso("E10-05", "CA-05: stock e historial reflejan la venta y pueden consultarse", "stock 10; venta de 3; actualizar consultas")
    def test_ca05_consistencia(self):
        self.registrar()
        self.vender()
        self.app.boton_actualizar.invoke()
        self.verificar(("7", "6.75", 7, 675),
                       (self.filas(self.app.tabla_productos)[0][2], self.filas(self.app.tabla_ventas)[0][4],
                        self.servicio.productos()[0]["cantidad"], self.servicio.ventas()[0]["total_centavos"]))

    @caso("E10-06", "CA-06: una venta sin existencias se rechaza sin cambios", "stock 10; venta de 11")
    def test_ca06_stock(self):
        self.registrar()
        antes = self.estado_db()
        self.vender(cantidad="11")
        self.verificar(("No hay existencias suficientes para realizar la venta.", antes), (self.app.mensaje.get(), self.estado_db()))

    @caso("E10-07", "CA-07: error de base de datos comprensible y recuperación", "bloquear SQLite, intentar venta, desbloquear y reintentar")
    def test_ca07_recuperacion(self):
        self.registrar()
        antes = self.estado_db()
        bloqueo = sqlite3.connect(self.ruta)
        try:
            bloqueo.execute("BEGIN EXCLUSIVE")
            self.app.campos_venta["codigo"].set("LAP-01")
            self.app.campos_venta["cantidad"].set("3")
            self.app.campos_venta["descuento"].set("10")
            self.app.boton_venta.invoke()
            mensaje_error = self.app.mensaje.get()
            self.assertEqual(MENSAJE_DB, mensaje_error)
        finally:
            bloqueo.rollback()
            bloqueo.close()
        self.assertEqual(antes, self.estado_db())
        self.evidencia("Venta rechazada por bloqueo; estado verificado después de liberar SQLite", {"codigo": "LAP-01", "cantidad": "3", "descuento": "10"})
        self.vender()
        self.verificar((MENSAJE_DB, "Venta 1 registrada correctamente. Total: 6.75.", 7, 1),
                       (mensaje_error, self.app.mensaje.get(), self.servicio.productos()[0]["cantidad"], len(self.servicio.ventas())))
