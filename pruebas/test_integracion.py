import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from threading import Barrier

from inventario.dominio import ErrorNegocio, ErrorPersistencia
from inventario.persistencia import BaseDatos
from inventario.servicios import Inventario
from pruebas.soporte import CasoBaseDatos, CasoFormulario, caso

MENSAJE_DB = "No se pudo acceder a la base de datos. Intenta de nuevo."


class FormularioPersistencia(CasoFormulario):
    @caso("E04-01", "Formulario válido persiste los datos exactos", "LAP-01, Lápiz HB, 10, 2.50")
    def test_registro_valido(self):
        self.registrar()
        with closing(sqlite3.connect(self.ruta)) as conexion:
            obtenido = conexion.execute("SELECT codigo, nombre, cantidad, precio_centavos FROM productos").fetchone()
        self.verificar(("LAP-01", "Lápiz HB", 10, 250), obtenido)

    @caso("E04-02", "Campo obligatorio ausente no inserta", "nombre vacío")
    def test_obligatorio(self):
        self.registrar(nombre="")
        self.verificar(("El nombre es obligatorio y debe tener entre 2 y 80 caracteres.", []),
                       (self.app.mensaje.get(), self.servicio.productos()))

    @caso("E04-03", "Código duplicado no sobrescribe el registro", "LAP-01 y lap-01")
    def test_duplicado(self):
        self.registrar()
        antes = self.estado_db()
        self.registrar(codigo="lap-01", nombre="Otro nombre", cantidad="5")
        self.verificar(("Ya existe un producto con ese código.", antes), (self.app.mensaje.get(), self.estado_db()))

    @caso("E04-04", "Validación de cantidad se ejecuta desde el formulario", "cantidad -1")
    def test_cantidad_invalida(self):
        self.registrar(cantidad="-1")
        self.verificar(("La cantidad no puede ser negativa.", []), (self.app.mensaje.get(), self.servicio.productos()))

    @caso("E04-05", "Persistencia al abrir otra conexión", "guardar y crear otra instancia del servicio")
    def test_reabrir(self):
        self.registrar()
        nuevo = Inventario(BaseDatos(self.ruta))
        self.verificar([("LAP-01", 10, 250)], [(p["codigo"], p["cantidad"], p["precio_centavos"]) for p in nuevo.productos()])


class VentasInventario(CasoBaseDatos):
    @caso("E05-01", "Una venta actualiza stock y genera historial", "stock 10; venta 3; precio 2.50; descuento 10 %")
    def test_venta_actualiza(self):
        self.producto()
        self.servicio.registrar_venta("LAP-01", "3", "10")
        self.verificar((7, 1, 675), (self.servicio.productos()[0]["cantidad"], len(self.servicio.ventas()), self.servicio.ventas()[0]["total_centavos"]))

    @caso("E05-02", "Falta de stock no modifica ninguno de los módulos", "stock 10; venta 11")
    def test_sin_stock(self):
        self.producto()
        antes = self.estado_db()
        self.rechazar(lambda: self.servicio.registrar_venta("LAP-01", "11"), "No hay existencias suficientes para realizar la venta.")
        self.assertEqual(antes, self.estado_db())

    @caso("E05-03", "Venta exacta del stock deja cero", "stock 10; venta 10")
    def test_stock_exacto(self):
        self.producto()
        self.servicio.registrar_venta("LAP-01", 10)
        self.verificar((0, 1), (self.servicio.productos()[0]["cantidad"], len(self.servicio.ventas())))

    @caso("E05-04", "Un fallo al insertar la venta revierte la reducción de stock", "trigger de prueba RAISE(ABORT) en ventas")
    def test_rollback_real(self):
        self.producto()
        antes = self.estado_db()
        with self.base.conexion() as conexion:
            conexion.execute("CREATE TRIGGER fallo_venta BEFORE INSERT ON ventas BEGIN SELECT RAISE(ABORT, 'fallo controlado'); END")
        self.rechazar(lambda: self.servicio.registrar_venta("LAP-01", 3), MENSAJE_DB, ErrorPersistencia)
        self.assertEqual(antes, self.estado_db())

    @caso("E05-05", "Ventas simultáneas no producen sobreventa", "stock 10; dos ventas concurrentes de 7")
    def test_concurrencia(self):
        self.producto()
        inicio = Barrier(2)

        def vender():
            inicio.wait(timeout=5)
            try:
                self.servicio.registrar_venta("LAP-01", 7)
                return "registrada"
            except ErrorNegocio:
                return "rechazada"

        with ThreadPoolExecutor(max_workers=2) as ejecutor:
            resultados = list(ejecutor.map(lambda _: vender(), range(2)))
        self.verificar((["rechazada", "registrada"], 3, 1),
                       (sorted(resultados), self.servicio.productos()[0]["cantidad"], len(self.servicio.ventas())))


class ServicioBaseDatos(CasoBaseDatos):
    @caso("E06-01", "Integración correcta de lógica y SQLite", "registrar y consultar LAP-01")
    def test_respuesta_correcta(self):
        self.producto()
        self.verificar("LAP-01", self.servicio.productos()[0]["codigo"])

    @caso("E06-02", "Base de datos bloqueada devuelve un error controlado", "BEGIN EXCLUSIVE en otra conexión; timeout 0.15 s")
    def test_bloqueo(self):
        self.producto()
        antes = self.estado_db()
        bloqueo = sqlite3.connect(self.ruta)
        try:
            bloqueo.execute("BEGIN EXCLUSIVE")
            self.rechazar(lambda: self.servicio.registrar_venta("LAP-01", 2), MENSAJE_DB, ErrorPersistencia)
        finally:
            bloqueo.rollback()
            bloqueo.close()
        self.assertEqual(antes, self.estado_db())

    @caso("E06-03", "El servicio se recupera después del bloqueo", "fallo con bloqueo; liberar conexión; repetir venta")
    def test_recuperacion(self):
        self.producto()
        bloqueo = sqlite3.connect(self.ruta)
        try:
            bloqueo.execute("BEGIN EXCLUSIVE")
            with self.assertRaises(ErrorPersistencia):
                self.servicio.registrar_venta("LAP-01", 2)
        finally:
            bloqueo.rollback()
            bloqueo.close()
        self.servicio.registrar_venta("LAP-01", 2)
        self.verificar((8, 1), (self.servicio.productos()[0]["cantidad"], len(self.servicio.ventas())))

