"""Crea una entrega que incluye fuentes, evidencias y los scripts locales de Tcl/Tk."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

RAIZ = Path(__file__).resolve().parent.parent


def main():
    destino = RAIZ / "Practica3_Inventario.zip"
    carpetas = {"inventario", "pruebas", "herramientas", "docs", "evidencias", ".runtime"}
    archivos_raiz = {".gitignore", "README.md", "app.py", "iniciar.ps1", "ejecutar_pruebas.py", "generar_evidencias.py"}
    contador = 0
    with ZipFile(destino, "w", compression=ZIP_DEFLATED) as entrega:
        for archivo in sorted(RAIZ.rglob("*")):
            if not archivo.is_file():
                continue
            relativa = archivo.relative_to(RAIZ)
            if relativa.parts[0] not in carpetas and str(relativa) not in archivos_raiz:
                continue
            if "__pycache__" in relativa.parts or archivo.suffix in {".pyc", ".zip"}:
                continue
            entrega.write(archivo, f"Practica3_Inventario/{relativa.as_posix()}")
            contador += 1
    with ZipFile(destino) as entrega:
        if entrega.testzip() is not None:
            raise RuntimeError("El archivo de entrega no superó su comprobación de integridad.")
    print(f"Entrega: {destino} ({contador} archivos, {destino.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
