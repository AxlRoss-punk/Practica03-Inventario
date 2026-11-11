PRÁCTICA 3

Ejercicios de pruebas unitarias

En cada ejercicio se debe probar una función o método de forma aislada, utilizando entradas
controladas y verificando el resultado esperado.

Ejercicio 1. Validación de datos de entrada

Objetivo: verificar que una función valide correctamente los datos ingresados por el usuario.

Cada equipo debe seleccionar un dato relevante de su sistema, por ejemplo:

•  Hospital: edad de un paciente.

•  Biblioteca: código de un libro.

•

Inventario: cantidad de productos.

•  Unidad educativa: nota de un estudiante.

Actividades:

1.

Implementar o identificar una función de validación.

2.  Diseñar al menos cinco casos de prueba: dato válido, dato vacío, dato negativo cuando

no corresponda, dato fuera de rango y dato con formato incorrecto.

3.  Ejecutar las pruebas de manera aislada.

4.  Comparar los resultados obtenidos con los esperados.

Entregable: código de las pruebas y tabla de resultados.

Ejercicio 2. Cálculo de valores del sistema

Objetivo: verificar que una función matemática o de negocio produzca resultados correctos.

Seleccionar un cálculo propio del sistema. Por ejemplo:

•  Hospital: cálculo del importe de una consulta.

•  Biblioteca: cálculo de una multa por retraso.

•

Inventario: cálculo del valor total del stock.

•  Unidad educativa: cálculo del promedio de calificaciones.

Actividades:

1.

Identificar la fórmula y las reglas de negocio.

2.  Diseñar cuatro casos de prueba como mínimo, incluyendo valores normales, cero y un

caso límite aplicable.

3.  Calcular manualmente los resultados esperados.

4.  Comparar los resultados de la función con los valores esperados.

Entregable: función probada, casos de prueba y evidencia de ejecución.

Ejercicio 3. Reglas de validación y restricciones

Objetivo: comprobar que una función respete las reglas particulares del sistema.

Ejemplos: impedir registrar cantidades negativas, rechazar una fecha de nacimiento futura o
verificar que un descuento no supere el límite permitido.

Actividades:

1.  Seleccionar una regla de negocio del proyecto.

2.  Diseñar al menos cinco casos de prueba, incluyendo situaciones válidas e inválidas.

3.  Verificar que la función acepte los casos válidos y rechace los inválidos.

4.  Registrar los defectos detectados y corregirlos si corresponde.

Entregable: pruebas implementadas y explicación de los resultados.

Ejercicios de pruebas de integración

En estos ejercicios se debe comprobar que los módulos intercambien información
correctamente y trabajen de manera coordinada.

Ejercicio 4. Integración entre formulario y base de datos

Objetivo: verificar que los datos ingresados en un formulario se almacenen correctamente.

Escenario: registrar una entidad principal del sistema, como un paciente, libro, producto o
estudiante.

Actividades:

1.

2.

Identificar el formulario, la lógica de registro y el módulo de persistencia.

Ingresar datos válidos desde el formulario.

3.  Comprobar que se ejecuten las validaciones correspondientes.

4.  Verificar que el registro quede almacenado correctamente en la base de datos.

5.  Probar qué sucede cuando faltan datos obligatorios o se introduce un identificador

duplicado, si la regla del sistema lo prohíbe.

Entregable: diagrama sencillo de los módulos involucrados, casos de prueba y evidencias del
formulario y la base de datos.

Ejercicio 5. Integración entre dos módulos funcionales

Objetivo: comprobar que una operación realizada en un módulo actualice correctamente la
información utilizada por otro.

Cada equipo seleccionará dos módulos relacionados. Algunos ejemplos son:

Sistema

Módulo 1

Módulo 2

Hospital

Registro de pacientes  Gestión de consultas

Biblioteca

Préstamos

Disponibilidad de libros

Inventario

Registro de ventas

Control de existencias

Unidad educativa  Inscripción

Registro de estudiantes

Actividades:

1.  Describir la relación entre ambos módulos.

2.  Ejecutar una operación en el primer módulo.

3.  Comprobar que el segundo módulo reciba o refleje la información correspondiente.

4.  Probar un escenario en el que la operación no deba completarse, por ejemplo, un

préstamo de un libro no disponible.

5.  Verificar que no se generen inconsistencias entre módulos.

Entregable: casos de prueba, resultados y explicación de cómo se mantiene la consistencia de
los datos.

Ejercicio 6. Integración entre la aplicación y un servicio externo

Objetivo: verificar la comunicación entre el sistema y otro componente, como una API, un
servicio de correo, un mecanismo de autenticación o un servicio de generación de
documentos.

Actividades:

1.

Identificar el componente externo o servicio integrado.

2.  Ejecutar una operación válida y verificar la respuesta recibida.

3.  Simular un error controlado, como un tiempo de espera agotado, una respuesta

inválida o un servicio no disponible.

4.  Comprobar que el sistema gestione el error sin bloquearse ni guardar información

inconsistente.

5.  Si el proyecto no utiliza servicios externos, realizar la prueba entre la aplicación y su

API interna o entre la lógica de negocio y la base de datos.

Entregable: descripción de la integración, casos de prueba, evidencias de respuestas correctas
e incorrectas y tratamiento de errores.

Ejercicios de pruebas de aceptación

Las pruebas de aceptación deben comprobar si el sistema satisface los requisitos y criterios
acordados con sus usuarios. Deben realizarse desde la perspectiva del usuario, sin limitarse a
comprobar funciones aisladas.

Ejercicio 7. Aceptación del registro de información

Objetivo: verificar que el usuario pueda completar correctamente el registro de una entidad
principal.

Escenario: un usuario registra un paciente, estudiante, libro, producto u otra entidad de su
sistema.

Criterios de aceptación:

•  El formulario presenta los campos requeridos.

•

Los campos obligatorios se validan correctamente.

•  El sistema informa los errores de forma comprensible.

•  El registro válido se guarda y puede consultarse posteriormente.

•  El sistema impide las operaciones no permitidas por las reglas de negocio.

Actividades:

1.  Redactar los criterios de aceptación a partir de los requisitos del proyecto.

2.  Preparar los datos necesarios.

3.  Ejecutar el escenario como usuario final.

4.  Registrar qué criterios se cumplen y cuáles no.

Entregable: caso de aceptación documentado, evidencias y resultado final.

Ejercicio 8. Aceptación de un proceso completo

Objetivo: verificar que un usuario pueda completar un proceso de principio a fin.

Seleccionar un proceso central del sistema. Por ejemplo:

•  Hospital: registrar paciente, programar consulta y consultar la cita.

•  Biblioteca: buscar libro, solicitar préstamo y verificar la disponibilidad actualizada.

•

Inventario: registrar venta y comprobar la actualización del stock.

•  Unidad educativa: registrar estudiante, completar inscripción y consultar el registro.

Actividades:

1.  Describir el proceso desde la perspectiva del usuario.

2.  Establecer las precondiciones y los datos iniciales.

3.  Ejecutar todos los pasos en orden.

4.  Verificar el resultado final y los cambios producidos en el sistema.

5.  Determinar si el proceso cumple los criterios de aceptación.

Entregable: flujo del proceso, criterios de aceptación y evidencias de ejecución completa.

Ejercicio 9. Aceptación de escenarios excepcionales

Objetivo: verificar que el sistema responda adecuadamente ante situaciones que impiden
completar una operación.

Seleccionar al menos tres escenarios excepcionales propios del proyecto, por ejemplo:

•

•

•

•

Intentar registrar un dato duplicado.

Intentar realizar una operación sin los permisos necesarios.

Intentar ejecutar una operación con información incompleta.

Intentar reservar un recurso que ya no está disponible.

Actividades:

1.

Identificar las situaciones que el usuario puede encontrar.

2.  Definir el comportamiento esperado para cada escenario.

3.  Ejecutar las pruebas con la aplicación.

4.  Comprobar que el sistema muestre mensajes comprensibles y preserve la integridad

de los datos.

5.  Registrar cualquier comportamiento que impida aceptar la funcionalidad.

Entregable: matriz de escenarios excepcionales, resultados y defectos encontrados.

Ejercicio 10. Validación final con el usuario

Objetivo: determinar si una funcionalidad importante del sistema está preparada para ser
aceptada por su usuario o cliente.

Actividades:

1.  Seleccionar una funcionalidad prioritaria del proyecto.

2.  Elaborar entre cinco y ocho criterios de aceptación verificables.

3.  Preparar un guion de prueba que pueda ejecutar un usuario que no sea el

desarrollador de esa funcionalidad.

4.  Ejecutar el guion en un entorno de prueba.

5.  Registrar observaciones, criterios cumplidos, criterios incumplidos y defectos

pendientes.

6.  Emitir una conclusión: aceptada, aceptada con observaciones o rechazada, justificando

la decisión según los criterios definidos.

Entregable: acta de aceptación con la funcionalidad evaluada, resultados, observaciones y
decisión final. Si no se dispone de un usuario real, la evaluación debe identificarse como
simulada.

