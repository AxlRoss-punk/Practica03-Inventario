# Defectos y correcciones

Se distinguen los problemas observados durante la ejecución de las mejoras preventivas identificadas al revisar el código.

| ID | Origen y evidencia | Comportamiento observado o riesgo identificado | Corrección | Estado |
| --- | --- | --- | --- | --- |
| D-01 | Entorno; primera ejecución de la suite | Las 22 pruebas que abrían formularios devolvían `Cannot find a usable init.tcl`. Las 30 restantes pasaron. Python tenía las DLL de Tcl/Tk, pero faltaban sus scripts de inicialización. | Añadir scripts oficiales Tcl/Tk 9.0.4 al directorio local `.runtime/`, conservar sus licencias y recurrir a esa copia solamente si falla la inicialización normal. | Resuelto en este entorno; los formularios se abren y la suite final cumple. |
| D-02 | Código de pruebas; [diagnostico_conexion.txt](../evidencias/diagnostico_conexion.txt) | E04-01 verificaba correctamente la fila, pero su conexión de consulta quedaba abierta. Windows impedía eliminar el archivo temporal: `PermissionError: [WinError 32]`. Resultado de esa ejecución: 51 pruebas correctas y 1 con error. | Utilizar `contextlib.closing` para cerrar explícitamente la conexión de consulta. | Corregido y verificado en la suite final: 52/52. |
| MP-01 | Mejora preventiva durante revisión del código | Una excepción SQLite no prevista, como un fallo al insertar una venta, podía llegar a la interfaz como error técnico. No se presentó como un defecto observado por un usuario real. | Traducir los errores SQLite no interpretados por el servicio a `ErrorPersistencia`, con mensaje comprensible. El duplicado se interpreta específicamente en el servicio. | Verificado mediante E05-04 y los casos de bloqueo/recuperación. |

## Pruebas que comprueban la corrección

- **D-01:** los 22 casos con formularios de los ejercicios 4, 7, 8, 9 y 10 y las cinco capturas muestran que la interfaz se ejecuta.
- **D-02:** E04-01 consulta SQLite con una conexión independiente y el entorno temporal puede eliminarse al finalizar.
- **MP-01:** E05-04 utiliza un trigger real que falla después de descontar stock, durante la inserción de la venta. La transacción se revierte, el stock permanece igual y no se registra ninguna venta parcial. E06-02 y E10-07 comprueban un mensaje comprensible ante el bloqueo real de SQLite.

## Estado de cierre

La [ejecución final](../evidencias/ejecucion.txt) no detecta defectos pendientes dentro de los escenarios probados. Queda pendiente realizar el guion con un usuario independiente; la aceptación actual está expresamente identificada como simulada. El resultado de una suite no demuestra ausencia de defectos fuera de su cobertura.

Las fuentes de la copia local de Tcl/Tk son los repositorios oficiales [Tcl](https://github.com/tcltk/tcl/tree/core-9-0-4) y [Tk](https://github.com/tcltk/tk/tree/core-9-0-4). El archivo `.runtime/FUENTES.json` registra las URLs y las huellas SHA-256 de los archivos descargados.

