"""Copia los scripts oficiales Tcl/Tk 9.0.4 al proyecto, sin instalar paquetes."""

import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main():
    runtime = RAIZ / ".runtime"
    runtime.mkdir(exist_ok=True)
    fuentes = []
    for componente in ("tcl", "tk"):
        url = f"https://github.com/tcltk/{componente}/archive/refs/tags/core-9-0-4.zip"
        archivo = runtime / f"{componente}.zip"
        if not archivo.is_file():
            urllib.request.urlretrieve(url, archivo)
        destino = runtime / f"{componente}9.0"
        with zipfile.ZipFile(archivo) as zip_origen:
            prefijo = f"{componente}-core-9-0-4/"
            for entrada in zip_origen.infolist():
                if entrada.is_dir():
                    continue
                if entrada.filename.startswith(prefijo + "library/"):
                    relativa = entrada.filename.removeprefix(prefijo + "library/")
                elif entrada.filename == prefijo + "license.terms":
                    relativa = "license.terms"
                else:
                    continue
                salida = (destino / relativa).resolve()
                if not salida.is_relative_to(destino.resolve()):
                    raise ValueError("Ruta inválida en archivo Tcl/Tk")
                salida.parent.mkdir(parents=True, exist_ok=True)
                salida.write_bytes(zip_origen.read(entrada))
        fuentes.append({"componente": componente, "version": "9.0.4", "url": url,
                        "sha256": hashlib.sha256(archivo.read_bytes()).hexdigest()})
        print(f"Preparado: {destino}")
    (runtime / "FUENTES.json").write_text(json.dumps(fuentes, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
