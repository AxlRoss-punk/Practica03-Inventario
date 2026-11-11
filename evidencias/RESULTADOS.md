# Resultados de ejecución — práctica 3

Fecha: 2026-11-11T17:24:34-04:00 (America/Caracas). Python 3.14.7; SQLite 3.50.4.

**52/52 pruebas cumplen**; 0 fallidas, 0 errores y 0 omitidas.

La aceptación es **simulada**, mediante campos, botones, mensajes y tablas reales de Tkinter. No participó un usuario independiente. Cada caso utiliza una base SQLite temporal distinta.

| Ejercicio | Descripción | Cumplen | Ejecutadas |
| --- | --- | ---: | ---: |
| E01 | Validación de cantidades | 9 | 9 |
| E02 | Cálculo del valor del stock | 5 | 5 |
| E03 | Restricción de descuentos | 8 | 8 |
| E04 | Formulario y base de datos | 5 | 5 |
| E05 | Ventas e inventario | 5 | 5 |
| E06 | Lógica de negocio y SQLite | 3 | 3 |
| E07 | Aceptación del registro | 4 | 4 |
| E08 | Aceptación del proceso completo | 2 | 2 |
| E09 | Aceptación de excepciones | 4 | 4 |
| E10 | Validación final simulada | 7 | 7 |

## E01. Validación de cantidades

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E01-01 | Cantidad válida<br>Entrada: 10 | 10 | 10 | CUMPLE |
| E01-02 | Cantidad vacía<br>Entrada: cadena vacía | La cantidad es obligatoria. | La cantidad es obligatoria. | CUMPLE |
| E01-03 | Cantidad negativa<br>Entrada: -1 | La cantidad no puede ser negativa. | La cantidad no puede ser negativa. | CUMPLE |
| E01-04 | Cantidad fuera de rango<br>Entrada: 1000000 | La cantidad no puede superar 999999. | La cantidad no puede superar 999999. | CUMPLE |
| E01-05 | Formato incorrecto<br>Entrada: abc | La cantidad debe ser un número entero. | La cantidad debe ser un número entero. | CUMPLE |
| E01-06 | Límite inferior permitido<br>Entrada: 0 | 0 | 0 | CUMPLE |
| E01-07 | Límite superior permitido<br>Entrada: 999999 | 999999 | 999999 | CUMPLE |
| E01-08 | Una cantidad fraccionaria no es stock entero<br>Entrada: 1.5 | La cantidad debe ser un número entero. | La cantidad debe ser un número entero. | CUMPLE |
| E01-09 | Ausencia de dato<br>Entrada: None | La cantidad es obligatoria. | La cantidad es obligatoria. | CUMPLE |

## E02. Cálculo del valor del stock

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E02-01 | Valor normal<br>Entrada: 10 × 2.50 = 25.00 | "25.00" | "25.00" | CUMPLE |
| E02-02 | Stock cero<br>Entrada: 0 × 2.50 = 0.00 | "0.00" | "0.00" | CUMPLE |
| E02-03 | Precio cero<br>Entrada: 7 × 0.00 = 0.00 | "0.00" | "0.00" | CUMPLE |
| E02-04 | Importes con centavos<br>Entrada: 3 × 19.99 = 59.97 | "59.97" | "59.97" | CUMPLE |
| E02-05 | Límite de cantidad y precio<br>Entrada: 999999 × 999999.99 = 999998990000.01 | "999998990000.01" | "999998990000.01" | CUMPLE |

## E03. Restricción de descuentos

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E03-01 | Sin descuento<br>Entrada: 0 % | "0" | "0" | CUMPLE |
| E03-02 | Descuento normal<br>Entrada: 10 % | "10" | "10" | CUMPLE |
| E03-03 | Límite superior inclusivo<br>Entrada: 20 % | "20" | "20" | CUMPLE |
| E03-04 | Descuento negativo<br>Entrada: -0.01 % | El descuento no puede ser negativo. | El descuento no puede ser negativo. | CUMPLE |
| E03-05 | Supera el descuento permitido<br>Entrada: 20.01 % | El descuento no puede superar 20. | El descuento no puede superar 20. | CUMPLE |
| E03-06 | Descuento no numérico<br>Entrada: diez | El descuento debe ser un número con hasta 2 decimales. | El descuento debe ser un número con hasta 2 decimales. | CUMPLE |
| E03-07 | Precisión no permitida<br>Entrada: 1.001 % | El descuento admite hasta 2 decimales. | El descuento admite hasta 2 decimales. | CUMPLE |
| E03-08 | Redondeo comercial de una venta<br>Entrada: 1 × 0.05 × (1 − 10/100) = 0.045 → 0.05 | "0.05" | "0.05" | CUMPLE |

## E04. Formulario y base de datos

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E04-01 | Formulario válido persiste los datos exactos<br>Entrada: LAP-01, Lápiz HB, 10, 2.50 | ["LAP-01", "Lápiz HB", 10, 250] | ["LAP-01", "Lápiz HB", 10, 250] | CUMPLE |
| E04-02 | Campo obligatorio ausente no inserta<br>Entrada: nombre vacío | ["El nombre es obligatorio y debe tener entre 2 y 80 caracteres.", []] | ["El nombre es obligatorio y debe tener entre 2 y 80 caracteres.", []] | CUMPLE |
| E04-03 | Código duplicado no sobrescribe el registro<br>Entrada: LAP-01 y lap-01 | ["Ya existe un producto con ese código.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | ["Ya existe un producto con ese código.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | CUMPLE |
| E04-04 | Validación de cantidad se ejecuta desde el formulario<br>Entrada: cantidad -1 | ["La cantidad no puede ser negativa.", []] | ["La cantidad no puede ser negativa.", []] | CUMPLE |
| E04-05 | Persistencia al abrir otra conexión<br>Entrada: guardar y crear otra instancia del servicio | [["LAP-01", 10, 250]] | [["LAP-01", 10, 250]] | CUMPLE |

## E05. Ventas e inventario

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E05-01 | Una venta actualiza stock y genera historial<br>Entrada: stock 10; venta 3; precio 2.50; descuento 10 % | [7, 1, 675] | [7, 1, 675] | CUMPLE |
| E05-02 | Falta de stock no modifica ninguno de los módulos<br>Entrada: stock 10; venta 11 | No hay existencias suficientes para realizar la venta. | No hay existencias suficientes para realizar la venta. | CUMPLE |
| E05-03 | Venta exacta del stock deja cero<br>Entrada: stock 10; venta 10 | [0, 1] | [0, 1] | CUMPLE |
| E05-04 | Un fallo al insertar la venta revierte la reducción de stock<br>Entrada: trigger de prueba RAISE(ABORT) en ventas | No se pudo acceder a la base de datos. Intenta de nuevo. | No se pudo acceder a la base de datos. Intenta de nuevo. | CUMPLE |
| E05-05 | Ventas simultáneas no producen sobreventa<br>Entrada: stock 10; dos ventas concurrentes de 7 | [["rechazada", "registrada"], 3, 1] | [["rechazada", "registrada"], 3, 1] | CUMPLE |

## E06. Lógica de negocio y SQLite

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E06-01 | Integración correcta de lógica y SQLite<br>Entrada: registrar y consultar LAP-01 | LAP-01 | LAP-01 | CUMPLE |
| E06-02 | Base de datos bloqueada devuelve un error controlado<br>Entrada: BEGIN EXCLUSIVE en otra conexión; timeout 0.15 s | No se pudo acceder a la base de datos. Intenta de nuevo. | No se pudo acceder a la base de datos. Intenta de nuevo. | CUMPLE |
| E06-03 | El servicio se recupera después del bloqueo<br>Entrada: fallo con bloqueo; liberar conexión; repetir venta | [8, 1] | [8, 1] | CUMPLE |

## E07. Aceptación del registro

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E07-01 | El usuario encuentra los campos y acciones de registro<br>Entrada: abrir aplicación | [["codigo", "nombre", "cantidad", "precio"], "Guardar producto"] | [["codigo", "nombre", "cantidad", "precio"], "Guardar producto"] | CUMPLE |
| E07-02 | El usuario registra y consulta el producto<br>Entrada: LAP-01, Lápiz HB, 10, 2.50 | ["Producto LAP-01 registrado correctamente.", [["LAP-01", "Lápiz HB", "10", "2.50", "25.00"]]] | ["Producto LAP-01 registrado correctamente.", [["LAP-01", "Lápiz HB", "10", "2.50", "25.00"]]] | CUMPLE |
| E07-03 | Mensaje comprensible y posibilidad de corregir un dato obligatorio<br>Entrada: nombre vacío; corregir a Lápiz HB | [1, "Producto LAP-01 registrado correctamente."] | [1, "Producto LAP-01 registrado correctamente."] | CUMPLE |
| E07-04 | La interfaz impide registrar un precio negativo<br>Entrada: precio -2.50 | ["El precio no puede ser negativo.", []] | ["El precio no puede ser negativo.", []] | CUMPLE |

## E08. Aceptación del proceso completo

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E08-01 | Registrar producto, vender, consultar stock e historial<br>Entrada: 10 unidades a 2.50; vender 3 con 10 % | ["Venta 1 registrada correctamente. Total: 6.75.", [["LAP-01", "Lápiz HB", "7", "2.50", "17.50"]], [["1", "LAP-01", "3", "10", "6.75"]]] | ["Venta 1 registrada correctamente. Total: 6.75.", [["LAP-01", "Lápiz HB", "7", "2.50", "17.50"]], [["1", "LAP-01", "3", "10", "6.75"]]] | CUMPLE |
| E08-02 | Agotar existencias y comprobar rechazo de una segunda venta<br>Entrada: stock 2; vender 2; intentar vender 1 | ["No hay existencias suficientes para realizar la venta.", "0", 1] | ["No hay existencias suficientes para realizar la venta.", "0", 1] | CUMPLE |

## E09. Aceptación de excepciones

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E09-01 | Duplicado: se explica el error y se conserva el original<br>Entrada: registrar LAP-01 dos veces | ["Ya existe un producto con ese código.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | ["Ya existe un producto con ese código.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | CUMPLE |
| E09-02 | Información incompleta: no se guarda<br>Entrada: cantidad de producto vacía | ["La cantidad es obligatoria.", {"productos": [], "ventas": []}] | ["La cantidad es obligatoria.", {"productos": [], "ventas": []}] | CUMPLE |
| E09-03 | Existencias insuficientes: no se genera una venta<br>Entrada: stock 10; solicitar 11 | ["No hay existencias suficientes para realizar la venta.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | ["No hay existencias suficientes para realizar la venta.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | CUMPLE |
| E09-04 | Producto inexistente: mensaje comprensible<br>Entrada: vender XXX-01 sin registrarlo | ["No existe un producto con ese código.", {"productos": [], "ventas": []}] | ["No existe un producto con ese código.", {"productos": [], "ventas": []}] | CUMPLE |

## E10. Validación final simulada

| Caso | Descripción y entrada | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- | --- |
| E10-01 | CA-01: campos y acciones necesarios están disponibles<br>Entrada: abrir formulario de venta | [["codigo", "cantidad", "descuento"], "Registrar venta"] | [["codigo", "cantidad", "descuento"], "Registrar venta"] | CUMPLE |
| E10-02 | CA-02: venta sin cantidad se rechaza y mantiene la información<br>Entrada: cantidad vacía | ["La cantidad es obligatoria.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}, "LAP-01"] | ["La cantidad es obligatoria.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}, "LAP-01"] | CUMPLE |
| E10-03 | CA-03: el descuento máximo se aplica correctamente<br>Entrada: venta 2 × 2.50; descuento 20 % | ["Venta 1 registrada correctamente. Total: 4.00.", 400] | ["Venta 1 registrada correctamente. Total: 4.00.", 400] | CUMPLE |
| E10-04 | CA-04: descuento excesivo se rechaza sin cambios<br>Entrada: descuento 20.01 % | ["El descuento no puede superar 20.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | ["El descuento no puede superar 20.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | CUMPLE |
| E10-05 | CA-05: stock e historial reflejan la venta y pueden consultarse<br>Entrada: stock 10; venta de 3; actualizar consultas | ["7", "6.75", 7, 675] | ["7", "6.75", 7, 675] | CUMPLE |
| E10-06 | CA-06: una venta sin existencias se rechaza sin cambios<br>Entrada: stock 10; venta de 11 | ["No hay existencias suficientes para realizar la venta.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | ["No hay existencias suficientes para realizar la venta.", {"productos": [{"codigo": "LAP-01", "nombre": "Lápiz HB", "cantidad": 10, "precio_centavos": 250}], "ventas": []}] | CUMPLE |
| E10-07 | CA-07: error de base de datos comprensible y recuperación<br>Entrada: bloquear SQLite, intentar venta, desbloquear y reintentar | ["No se pudo acceder a la base de datos. Intenta de nuevo.", "Venta 1 registrada correctamente. Total: 6.75.", 7, 1] | ["No se pudo acceder a la base de datos. Intenta de nuevo.", "Venta 1 registrada correctamente. Total: 6.75.", 7, 1] | CUMPLE |

## Evidencia de formularios y persistencia

El archivo [resultados.json](resultados.json) conserva, por cada interacción capturada, los datos enviados al formulario, el mensaje visible, las filas de ambas tablas y los registros consultados en SQLite. [ejecucion.txt](ejecucion.txt) contiene la salida íntegra de unittest.
