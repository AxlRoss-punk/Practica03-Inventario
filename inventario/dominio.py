"""Reglas puras: no dependen de la interfaz ni de SQLite."""

import re
from decimal import Decimal, InvalidOperation

MAX_CANTIDAD = 999_999
MAX_PRECIO = Decimal("999999.99")
MAX_DESCUENTO = Decimal("20")
CENTAVO = Decimal("0.01")


class ErrorNegocio(Exception):
    """Error que puede mostrarse al usuario sin detalles técnicos."""


class ErrorValidacion(ErrorNegocio):
    pass


class ErrorPersistencia(ErrorNegocio):
    pass


def validar_cantidad(valor, *, permitir_cero=True):
    texto = str(valor).strip() if valor is not None else ""
    if not texto:
        raise ErrorValidacion("La cantidad es obligatoria.")
    if not re.fullmatch(r"-?[0-9]+", texto):
        raise ErrorValidacion("La cantidad debe ser un número entero.")
    # Limitar la longitud antes de convertir evita entradas arbitrariamente grandes.
    if texto.startswith("-") and any(c != "0" for c in texto[1:]):
        raise ErrorValidacion("La cantidad no puede ser negativa.")
    digitos = texto.lstrip("-").lstrip("0") or "0"
    if len(digitos) > 6:
        raise ErrorValidacion("La cantidad no puede superar 999999.")
    cantidad = int(digitos)
    if cantidad > MAX_CANTIDAD:
        raise ErrorValidacion("La cantidad no puede superar 999999.")
    if not permitir_cero and cantidad == 0:
        raise ErrorValidacion("La cantidad de venta debe ser mayor que cero.")
    return cantidad


def validar_decimal(valor, campo, maximo, decimales=2):
    texto = str(valor).strip() if valor is not None else ""
    if not texto:
        raise ErrorValidacion(f"{campo} es obligatorio.")
    if len(texto) > 32 or not re.fullmatch(r"-?[0-9]+(?:[.,][0-9]+)?", texto):
        raise ErrorValidacion(f"{campo} debe ser un número con hasta {decimales} decimales.")
    try:
        numero = Decimal(texto.replace(",", "."))
    except InvalidOperation as exc:
        raise ErrorValidacion(f"{campo} tiene un formato incorrecto.") from exc
    if numero < 0:
        raise ErrorValidacion(f"{campo} no puede ser negativo.")
    if numero > maximo:
        raise ErrorValidacion(f"{campo} no puede superar {maximo}.")
    if numero.as_tuple().exponent < -decimales:
        raise ErrorValidacion(f"{campo} admite hasta {decimales} decimales.")
    return numero


def validar_precio(valor):
    return validar_decimal(valor, "El precio", MAX_PRECIO).quantize(CENTAVO)


def validar_descuento(valor):
    return validar_decimal(valor, "El descuento", MAX_DESCUENTO)


def validar_codigo(valor):
    codigo = str(valor).strip().upper() if valor is not None else ""
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9-]{1,19}", codigo):
        raise ErrorValidacion("El código debe tener de 2 a 20 letras, números o guiones y comenzar con letra o número.")
    return codigo


def validar_nombre(valor):
    nombre = str(valor).strip() if valor is not None else ""
    if not 2 <= len(nombre) <= 80:
        raise ErrorValidacion("El nombre es obligatorio y debe tener entre 2 y 80 caracteres.")
    return nombre


def calcular_valor_stock(cantidad, precio):
    return (validar_cantidad(cantidad) * validar_precio(precio)).quantize(CENTAVO)


def calcular_total_venta(cantidad, precio, descuento):
    unidades = validar_cantidad(cantidad, permitir_cero=False)
    importe = unidades * validar_precio(precio)
    porcentaje = validar_descuento(descuento)
    # Redondeo comercial explícito, independiente del contexto global de Decimal.
    from decimal import ROUND_HALF_UP

    return (importe * (1 - porcentaje / 100)).quantize(CENTAVO, rounding=ROUND_HALF_UP)

