# Acta de aceptación — ejercicio 10

**Sistema:** inventario de productos y ventas.

**Funcionalidad prioritaria:** registrar ventas y mantener la consistencia de las existencias y del historial.

**Fecha:** 2026-11-11T17:24:34-04:00 (America/Caracas).

**Modalidad y evaluador:** evaluación SIMULADA por automatización de la interfaz de escritorio. No equivale a la firma de un cliente ni a una evaluación realizada por una persona independiente.

**Entorno:** base de datos SQLite temporal por caso; producto LAP-01, nombre Lápiz HB, stock 10 y precio 2.50. El descuento de ejemplo es 10 %.

**Guion reproducible:** [GUION_ACEPTACION.md](../docs/GUION_ACEPTACION.md).

| Criterio | Evaluación | Estado |
| --- | --- | --- |
| CA-01 | campos y acciones necesarios están disponibles | CUMPLE |
| CA-02 | venta sin cantidad se rechaza y mantiene la información | CUMPLE |
| CA-03 | el descuento máximo se aplica correctamente | CUMPLE |
| CA-04 | descuento excesivo se rechaza sin cambios | CUMPLE |
| CA-05 | stock e historial reflejan la venta y pueden consultarse | CUMPLE |
| CA-06 | una venta sin existencias se rechaza sin cambios | CUMPLE |
| CA-07 | error de base de datos comprensible y recuperación | CUMPLE |

**Criterios cumplidos:** 7 de 7.

**Decisión:** ACEPTADA CON OBSERVACIONES (evaluación simulada).

**Justificación:** Los siete criterios se comprobaron y todas las pruebas de la práctica cumplen. La observación pendiente es realizar el guion con un usuario independiente para recoger su valoración de claridad y usabilidad.

**Observaciones:** no se evaluaron accesibilidad, rendimiento a gran escala ni compatibilidad en otros sistemas operativos. La recuperación ante indisponibilidad se comprobó con un bloqueo real y controlado de SQLite.

**Defectos pendientes en el alcance probado:** ninguno detectado por la suite actual.

**Firma de usuario real:** no aplica; evaluación simulada.

**Responsables del equipo:** completar antes de la entrega académica.
