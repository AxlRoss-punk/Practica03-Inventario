from decimal import Decimal

from inventario.dominio import (
    calcular_total_venta, calcular_valor_stock, validar_cantidad, validar_descuento,
)
from pruebas.soporte import Caso, caso


class ValidacionCantidad(Caso):
    @caso("E01-01", "Cantidad válida", "10")
    def test_valida(self):
        self.verificar(10, validar_cantidad("10"))

    @caso("E01-02", "Cantidad vacía", "cadena vacía")
    def test_vacia(self):
        self.rechazar(lambda: validar_cantidad(""), "La cantidad es obligatoria.")

    @caso("E01-03", "Cantidad negativa", "-1")
    def test_negativa(self):
        self.rechazar(lambda: validar_cantidad("-1"), "La cantidad no puede ser negativa.")

    @caso("E01-04", "Cantidad fuera de rango", "1000000")
    def test_fuera_rango(self):
        self.rechazar(lambda: validar_cantidad("1000000"), "La cantidad no puede superar 999999.")

    @caso("E01-05", "Formato incorrecto", "abc")
    def test_formato(self):
        self.rechazar(lambda: validar_cantidad("abc"), "La cantidad debe ser un número entero.")

    @caso("E01-06", "Límite inferior permitido", "0")
    def test_cero(self):
        self.verificar(0, validar_cantidad("0"))

    @caso("E01-07", "Límite superior permitido", "999999")
    def test_maximo(self):
        self.verificar(999999, validar_cantidad("999999"))

    @caso("E01-08", "Una cantidad fraccionaria no es stock entero", "1.5")
    def test_fraccion(self):
        self.rechazar(lambda: validar_cantidad("1.5"), "La cantidad debe ser un número entero.")

    @caso("E01-09", "Ausencia de dato", "None")
    def test_ausente(self):
        self.rechazar(lambda: validar_cantidad(None), "La cantidad es obligatoria.")


class ValorStock(Caso):
    @caso("E02-01", "Valor normal", "10 × 2.50 = 25.00")
    def test_normal(self):
        self.verificar(Decimal("25.00"), calcular_valor_stock(10, "2.50"))

    @caso("E02-02", "Stock cero", "0 × 2.50 = 0.00")
    def test_cero(self):
        self.verificar(Decimal("0.00"), calcular_valor_stock(0, "2.50"))

    @caso("E02-03", "Precio cero", "7 × 0.00 = 0.00")
    def test_precio_cero(self):
        self.verificar(Decimal("0.00"), calcular_valor_stock(7, "0"))

    @caso("E02-04", "Importes con centavos", "3 × 19.99 = 59.97")
    def test_centavos(self):
        self.verificar(Decimal("59.97"), calcular_valor_stock(3, "19.99"))

    @caso("E02-05", "Límite de cantidad y precio", "999999 × 999999.99 = 999998990000.01")
    def test_limite(self):
        self.verificar(Decimal("999998990000.01"), calcular_valor_stock(999999, "999999.99"))


class RestriccionDescuento(Caso):
    @caso("E03-01", "Sin descuento", "0 %")
    def test_cero(self):
        self.verificar(Decimal("0"), validar_descuento("0"))

    @caso("E03-02", "Descuento normal", "10 %")
    def test_normal(self):
        self.verificar(Decimal("10"), validar_descuento("10"))

    @caso("E03-03", "Límite superior inclusivo", "20 %")
    def test_limite(self):
        self.verificar(Decimal("20"), validar_descuento("20"))

    @caso("E03-04", "Descuento negativo", "-0.01 %")
    def test_negativo(self):
        self.rechazar(lambda: validar_descuento("-0.01"), "El descuento no puede ser negativo.")

    @caso("E03-05", "Supera el descuento permitido", "20.01 %")
    def test_excesivo(self):
        self.rechazar(lambda: validar_descuento("20.01"), "El descuento no puede superar 20.")

    @caso("E03-06", "Descuento no numérico", "diez")
    def test_formato(self):
        self.rechazar(lambda: validar_descuento("diez"), "El descuento debe ser un número con hasta 2 decimales.")

    @caso("E03-07", "Precisión no permitida", "1.001 %")
    def test_precision(self):
        self.rechazar(lambda: validar_descuento("1.001"), "El descuento admite hasta 2 decimales.")

    @caso("E03-08", "Redondeo comercial de una venta", "1 × 0.05 × (1 − 10/100) = 0.045 → 0.05")
    def test_redondeo(self):
        self.verificar(Decimal("0.05"), calcular_total_venta(1, "0.05", "10"))

