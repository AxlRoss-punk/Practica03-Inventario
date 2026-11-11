# Guion de aceptación para un usuario independiente

## Propósito y preparación

Evaluar el registro de ventas y la actualización del inventario desde la perspectiva del usuario. El ejecutor no necesita conocer el código.

**Evaluador:** ____________________. **Fecha:** ____________________. **Equipo:** ____________________.

La ejecución documentada en el acta incluida es **simulada**. Este guion permite repetirla con una persona independiente y registrar una nueva evaluación.

1. Abrir PowerShell en la carpeta `Practica03`.
2. Utilizar una base de prueba nueva. Si ya existe `datos/aceptacion_01.sqlite3`, elegir otro nombre, por ejemplo `aceptacion_02.sqlite3`, y usarlo también al probar el bloqueo.
3. Abrir la aplicación con:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\iniciar.ps1 -Db datos/aceptacion_01.sqlite3
   ```

4. Comprobar que no aparecen productos ni ventas. Registrar el producto **LAP-01**, nombre **Lápiz HB**, cantidad **10**, precio **2.50**, y pulsar **Guardar producto**. Debe aparecer una confirmación y el producto en la tabla, con valor de stock **25.00**.

El guion siguiente es secuencial. Los tests automatizados verifican los mismos criterios con una base independiente para cada caso, por lo que su stock inicial vuelve a ser 10 en cada test.

## Criterios verificables

| Criterio | Condición para cumplir |
| --- | --- |
| CA-01 | El usuario encuentra los campos código, cantidad y descuento y el botón Registrar venta. |
| CA-02 | La cantidad de venta vacía se rechaza con un mensaje comprensible, conservando los datos para corregirlos y sin modificar el inventario. |
| CA-03 | El descuento máximo permitido, 20 %, se acepta y calcula correctamente. |
| CA-04 | Un descuento superior a 20 % se rechaza sin modificar stock ni historial. |
| CA-05 | Una venta correcta se confirma, reduce el stock y aparece con su total correcto en el historial y al actualizar consultas. |
| CA-06 | Una venta mayor que el stock disponible se rechaza, manteniendo ambos módulos sin cambios. |
| CA-07 | Una base de datos bloqueada produce un mensaje comprensible, no registra cambios y permite reintentar después de liberar el bloqueo. |

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado | Criterio |
| --- | --- | --- | --- |
| 1 | Localizar Código del producto, Cantidad a vender, Descuento y Registrar venta. | Todos los campos y la acción están disponibles; los obligatorios están señalados con *. | CA-01 |
| 2 | Ingresar LAP-01, dejar cantidad vacía, descuento 10; pulsar Registrar venta. | Mensaje «La cantidad es obligatoria.». LAP-01 permanece en el formulario; stock 10 e historial vacío. | CA-02 |
| 3 | Ingresar cantidad 3, descuento 20.01 y pulsar Registrar venta. | «El descuento no puede superar 20.». Stock 10 e historial vacío. | CA-04 |
| 4 | Cambiar cantidad a 2, descuento a 20; registrar la venta. | Confirmación de venta 1, total 4.00; stock 8 e historial con una venta. Cálculo: 2 × 2.50 × 0.80 = 4.00. | CA-03 |
| 5 | Ingresar cantidad 3, descuento 10; registrar. Pulsar Actualizar consultas. | Confirmación de venta 2, total 6.75; stock 5, valor del stock 12.50 e historial con dos ventas. | CA-05 |
| 6 | Ingresar cantidad 6, descuento 10; registrar. | «No hay existencias suficientes para realizar la venta.». Stock 5 e historial con dos ventas. | CA-06 |
| 7 | Seguir el procedimiento de bloqueo siguiente. Intentar vender 1 unidad con descuento 0 mientras la base está bloqueada. | «No se pudo acceder a la base de datos. Intenta de nuevo.». La ventana sigue operativa y conserva los datos introducidos. | CA-07 |
| 8 | Liberar el bloqueo y pulsar Actualizar consultas antes de reintentar. | Stock 5 e historial con dos ventas: el intento fallido no se almacenó. | CA-07 |
| 9 | Reintentar la venta de 1 unidad, descuento 0. | Confirmación de venta 3, total 2.50; stock 4 e historial con tres ventas. | CA-07 |

## Cómo simular la indisponibilidad para CA-07

Con la aplicación abierta, abrir **otra terminal** en `Practica03` y ejecutar:

```powershell
powershell -ExecutionPolicy Bypass -File .\iniciar.ps1 -Modo bloqueo -Db datos/aceptacion_01.sqlite3
```

Esperar el texto **Bloqueo de prueba activo**. Volver al formulario e intentar la venta del paso 7. Para liberar la base, volver a la segunda terminal y pulsar **Enter**. Continuar con los pasos 8 y 9.

La herramienta no inserta ni modifica registros; mantiene una transacción exclusiva y la revierte al terminar. Utilizar exactamente la misma base de prueba que se abrió en la aplicación.

## Registro del evaluador

| Criterio | Cumple / No cumple | Observaciones o referencia de evidencia |
| --- | --- | --- |
| CA-01 | | |
| CA-02 | | |
| CA-03 | | |
| CA-04 | | |
| CA-05 | | |
| CA-06 | | |
| CA-07 | | |

**Defectos encontrados:** ____________________________________________________________.

**Criterios incumplidos:** ____________________________________________________________.

**Decisión:** aceptada / aceptada con observaciones / rechazada.

**Justificación:** __________________________________________________________________.

**Firma del evaluador:** ____________________________________________________________.

La decisión será **rechazada** si un criterio de integridad, cálculo, validación o recuperación no se cumple. Puede ser **aceptada con observaciones** cuando los siete criterios se cumplan y existan observaciones que no impidan el proceso. Puede ser **aceptada** cuando se cumplan los siete criterios sin observaciones pendientes.

