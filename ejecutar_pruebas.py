"""Ejecuta la suite y genera evidencia verificable; devuelve 1 si algo falla."""

import io
import json
import platform
import sqlite3
import sys
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
EJERCICIOS = {
    "E01": "Validación de cantidades",
    "E02": "Cálculo del valor del stock",
    "E03": "Restricción de descuentos",
    "E04": "Formulario y base de datos",
    "E05": "Ventas e inventario",
    "E06": "Lógica de negocio y SQLite",
    "E07": "Aceptación del registro",
    "E08": "Aceptación del proceso completo",
    "E09": "Aceptación de excepciones",
    "E10": "Validación final simulada",
}


class ResultadoDocumentado(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.casos = []

    def startTest(self, test):
        self.inicio_caso = time.perf_counter()
        super().startTest(test)

    def registrar(self, test, estado, detalle=""):
        metodo = getattr(test, test._testMethodName)
        self.casos.append({
            "id": getattr(metodo, "caso_id", test.id()),
            "descripcion": getattr(metodo, "descripcion", test.id()),
            "entrada": getattr(metodo, "entrada", ""),
            "esperado": getattr(test, "esperado", "Ver detalle de la prueba"),
            "obtenido": getattr(test, "obtenido", detalle or "Sin resultado"),
            "estado": estado,
            "duracion_segundos": round(time.perf_counter() - self.inicio_caso, 4),
            "prueba": test.id(),
            "detalle_error": detalle,
            "evidencias": getattr(test, "evidencias", []),
        })

    def addSuccess(self, test):
        super().addSuccess(test)
        self.registrar(test, "CUMPLE")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.registrar(test, "NO CUMPLE", self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self.registrar(test, "ERROR", self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.registrar(test, "OMITIDA", reason)


def celda(valor):
    if not isinstance(valor, str):
        valor = json.dumps(valor, ensure_ascii=False, default=str)
    return valor.replace("|", "\\|").replace("\n", "<br>").replace("\r", "")


def guardar_informes(resultado, consola):
    carpeta = RAIZ / "evidencias"
    carpeta.mkdir(exist_ok=True)
    casos = sorted(resultado.casos, key=lambda caso: caso["id"])
    fecha = datetime.now(timezone(timedelta(hours=-4))).isoformat(timespec="seconds")
    documento = {
        "fecha": fecha, "zona_horaria": "America/Caracas",
        "python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
        "sistema": platform.platform(), "ejecutable": sys.executable,
        "aceptacion": "SIMULADA: automatización de los formularios Tkinter; sin usuario independiente",
        "total": resultado.testsRun,
        "aprobadas": sum(caso["estado"] == "CUMPLE" for caso in casos),
        "fallidas": len(resultado.failures), "errores": len(resultado.errors),
        "omitidas": len(resultado.skipped), "casos": casos,
    }
    (carpeta / "resultados.json").write_text(json.dumps(documento, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    (carpeta / "ejecucion.txt").write_text(consola, encoding="utf-8")
    lineas = [
        "# Resultados de ejecución — práctica 3", "",
        f"Fecha: {fecha} (America/Caracas). Python {documento['python']}; SQLite {documento['sqlite']}.", "",
        f"**{documento['aprobadas']}/{documento['total']} pruebas cumplen**; {documento['fallidas']} fallidas, {documento['errores']} errores y {documento['omitidas']} omitidas.", "",
        "La aceptación es **simulada**, mediante campos, botones, mensajes y tablas reales de Tkinter. No participó un usuario independiente. Cada caso utiliza una base SQLite temporal distinta.", "",
        "| Ejercicio | Descripción | Cumplen | Ejecutadas |", "| --- | --- | ---: | ---: |",
    ]
    for identificador, titulo in EJERCICIOS.items():
        grupo = [caso for caso in casos if caso["id"].startswith(identificador + "-")]
        lineas.append(f"| {identificador} | {titulo} | {sum(c['estado'] == 'CUMPLE' for c in grupo)} | {len(grupo)} |")
    for identificador, titulo in EJERCICIOS.items():
        lineas += ["", f"## {identificador}. {titulo}", "",
                   "| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |",
                   "| --- | --- | --- | --- | --- |"]
        for caso in casos:
            if caso["id"].startswith(identificador + "-"):
                lineas.append(f"| {caso['id']} | {celda(caso['descripcion'])}<br>Entrada: {celda(caso['entrada'])} | {celda(caso['esperado'])} | {celda(caso['obtenido'])} | {caso['estado']} |")
    lineas += ["", "## Evidencia de formularios y persistencia", "",
               "El archivo [resultados.json](resultados.json) conserva, por cada interacción capturada, los datos enviados al formulario, el mensaje visible, las filas de ambas tablas y los registros consultados en SQLite. [ejecucion.txt](ejecucion.txt) contiene la salida íntegra de unittest.", ""]
    (carpeta / "RESULTADOS.md").write_text("\n".join(lineas), encoding="utf-8")

    criterios = [caso for caso in casos if caso["id"].startswith("E10-")]
    completo = {caso["id"] for caso in criterios} == {f"E10-{numero:02}" for numero in range(1, 8)}
    aceptada = completo and all(caso["estado"] == "CUMPLE" for caso in casos) and not resultado.skipped
    decision = "ACEPTADA CON OBSERVACIONES (evaluación simulada)" if aceptada else "RECHAZADA (evaluación simulada)"
    acta = [
        "# Acta de aceptación — ejercicio 10", "",
        "**Sistema:** inventario de productos y ventas.", "",
        "**Funcionalidad prioritaria:** registrar ventas y mantener la consistencia de las existencias y del historial.", "",
        f"**Fecha:** {fecha} (America/Caracas).", "",
        "**Modalidad y evaluador:** evaluación SIMULADA por automatización de la interfaz de escritorio. No equivale a la firma de un cliente ni a una evaluación realizada por una persona independiente.", "",
        "**Entorno:** base de datos SQLite temporal por caso; producto LAP-01, nombre Lápiz HB, stock 10 y precio 2.50. El descuento de ejemplo es 10 %.", "",
        "**Guion reproducible:** [GUION_ACEPTACION.md](../docs/GUION_ACEPTACION.md).", "",
        "| Criterio | Evaluación | Estado |", "| --- | --- | --- |",
    ]
    for caso in criterios:
        acta.append(f"| {caso['id'].replace('E10-', 'CA-')} | {caso['descripcion'].split(': ', 1)[-1]} | {caso['estado']} |")
    acta += ["", f"**Criterios cumplidos:** {sum(c['estado'] == 'CUMPLE' for c in criterios)} de 7.", "",
             f"**Decisión:** {decision}.", "",
             "**Justificación:** " + ("Los siete criterios se comprobaron y todas las pruebas de la práctica cumplen. La observación pendiente es realizar el guion con un usuario independiente para recoger su valoración de claridad y usabilidad." if aceptada else "Existen pruebas fallidas, con errores, omitidas o criterios sin ejecutar; revisar los resultados antes de aceptar la funcionalidad."), "",
             "**Observaciones:** no se evaluaron accesibilidad, rendimiento a gran escala ni compatibilidad en otros sistemas operativos. La recuperación ante indisponibilidad se comprobó con un bloqueo real y controlado de SQLite.", "",
             "**Defectos pendientes en el alcance probado:** " + ("ninguno detectado por la suite actual." if aceptada else "consultar los casos que no cumplen en RESULTADOS.md."), "",
             "**Firma de usuario real:** no aplica; evaluación simulada.", "",
             "**Responsables del equipo:** completar antes de la entrega académica.", ""]
    (carpeta / "ACTA_ACEPTACION.md").write_text("\n".join(acta), encoding="utf-8")
    return documento


def main():
    consola = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(RAIZ / "pruebas"), top_level_dir=str(RAIZ))
    resultado = unittest.TextTestRunner(stream=consola, verbosity=2, resultclass=ResultadoDocumentado).run(suite)
    informe = guardar_informes(resultado, consola.getvalue())
    print(consola.getvalue())
    print(f"Evidencias: {RAIZ / 'evidencias'}")
    return 0 if resultado.wasSuccessful() and informe["omitidas"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
