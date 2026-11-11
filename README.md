# Práctica 3 — pruebas de un inventario

Sistema de escritorio en **Python + Tkinter + SQLite** con registro de productos, consulta de existencias, registro de ventas y descuentos. Incluye el desarrollo de los diez ejercicios del enunciado, las pruebas, sus resultados y el acta de aceptación simulada.

Repositorio público: [AxlRoss-punk/Practica03-Inventario](https://github.com/AxlRoss-punk/Practica03-Inventario).

**Verificación realizada el 11 de noviembre de 2026:** 52 pruebas aprobadas: 22 unitarias, 13 de integración y 17 de aceptación simulada. Los resultados se regeneran al ejecutar la suite.

## Comenzar en Windows

Desde esta carpeta, abrir PowerShell y ejecutar:

```powershell
powershell -ExecutionPolicy Bypass -File .\iniciar.ps1
```

El lanzador detecta la instalación de Python y abre la aplicación. La base de trabajo se crea en `datos/inventario.sqlite3`; comienza vacía y se conserva entre ejecuciones.

Para ejecutar las pruebas y generar nuevamente sus tablas y acta:

```powershell
powershell -ExecutionPolicy Bypass -File .\iniciar.ps1 -Modo pruebas
```

Para reproducir también las cinco capturas y la base de demostración:

```powershell
powershell -ExecutionPolicy Bypass -File .\iniciar.ps1 -Modo todo
```

Las pruebas utilizan bases temporales. La generación de evidencias sustituye únicamente los archivos de demostración de `evidencias/`.

## Entregables

| Documento o archivo | Contenido |
| --- | --- |
| [Informe de la práctica](docs/INFORME_PRACTICA3.md) | Desarrollo de los diez ejercicios, reglas, cálculos y explicación de los resultados |
| [Resultados](evidencias/RESULTADOS.md) | Tablas con entrada, resultado esperado, resultado obtenido y estado de cada prueba |
| [Guion de aceptación](docs/GUION_ACEPTACION.md) | Pasos para que otra persona compruebe la funcionalidad |
| [Acta de aceptación](evidencias/ACTA_ACEPTACION.md) | Siete criterios, observaciones y decisión de la evaluación simulada |
| [Registro de defectos](docs/DEFECTOS.md) | Problemas encontrados, correcciones y evidencia de comprobación |
| [Evidencias](evidencias/README.md) | Capturas, base SQLite, consultas SQL, trazas y resultados estructurados |
| [Requisitos](docs/REQUISITOS_PRACTICA.md) | Correspondencia entre el enunciado y los entregables |

La aceptación fue **simulada por automatización de los formularios reales**, sin evaluador humano independiente. El acta indica **aceptada con observaciones** por esa limitación. Completar los nombres del equipo antes de la entrega académica.

## Requisitos técnicos

- Python 3.11 o posterior, con Tkinter y SQLite. La ejecución se comprobó con Python 3.14.7 y SQLite 3.50.4 en Windows.
- Sin paquetes de `pip` ni servicios remotos.
- Para ejecutar los formularios y sus pruebas se necesita una sesión de escritorio.
- En esta instalación faltaban los scripts de Tcl/Tk 9.0.4. La carpeta `.runtime/` contiene una copia local de los scripts oficiales y sus licencias. La aplicación utiliza esa copia únicamente si falla la inicialización normal con `init.tcl`; no cambia la instalación de Python.

Con una instalación de Python accesible desde la terminal también se puede ejecutar:

```text
python app.py
python ejecutar_pruebas.py
python generar_evidencias.py
python -m unittest discover -s pruebas -v
```

Para elegir otra base: `python app.py --db datos/otra_base.sqlite3`, o pasar `-Db datos/otra_base.sqlite3` al lanzador. Para elegir otro intérprete, usar `-Python 'C:\ruta\python.exe'`.

Si se necesita reconstruir la copia local de Tcl/Tk 9.0.4, `python -m herramientas.preparar_tk` descarga las fuentes oficiales. Esa copia corresponde al motor Tcl/Tk 9.0.4 utilizado aquí; en otras versiones de Python conviene utilizar su instalación completa de Tkinter.

## Organización del código

```text
app.py                       Entrada de la aplicación
iniciar.ps1                  Lanzador para Windows
inventario/dominio.py        Validaciones y cálculos puros
inventario/persistencia.py   Esquema, conexiones y transacciones SQLite
inventario/servicios.py      Registro, inventario y ventas
inventario/interfaz.py       Formularios y tablas Tkinter
inventario/entorno.py        Compatibilidad local de Tcl/Tk
pruebas/test_unitarias.py    Ejercicios 1, 2 y 3
pruebas/test_integracion.py  Ejercicios 4, 5 y 6
pruebas/test_aceptacion.py   Ejercicios 7, 8, 9 y 10
ejecutar_pruebas.py          Generación de resultados y acta
generar_evidencias.py        Capturas y base de demostración
docs/                       Informe y guiones
evidencias/                 Archivos de evidencia conservados
```

El alcance es académico: productos, ventas y consistencia de los datos. No incluye autenticación, facturación fiscal ni conexión con servicios externos.

