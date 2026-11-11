# Requisitos de la práctica 3

Fuente: [enunciado original](ENUNCIADO.md), copiado de `../PRÁCTICA 3.md`. Este documento organiza los entregables de los diez ejercicios; se desarrollaron sobre el inventario en Python y SQLite elegido para la práctica.

| Ejercicio | Tipo de prueba | Cobertura mínima | Entregables |
| --- | --- | --- | --- |
| 1. Validación de entrada | Unitaria | Dato válido, vacío, negativo, fuera de rango y formato incorrecto | Función, código de pruebas y tabla de resultados esperados y obtenidos |
| 2. Cálculo del sistema | Unitaria | Cuatro casos: valores normales, cero y un límite aplicable | Fórmula, reglas, cálculos manuales, función y evidencia de ejecución |
| 3. Restricciones | Unitaria | Cinco casos válidos e inválidos de una regla de negocio | Pruebas, explicación de resultados y registro de defectos y correcciones |
| 4. Formulario y persistencia | Integración | Registro válido, campos obligatorios e identificador duplicado cuando corresponda | Diagrama de módulos, casos y evidencias del formulario y la base de datos |
| 5. Dos módulos funcionales | Integración | Operación correcta y operación rechazada sin inconsistencias | Relación entre módulos, casos, resultados y explicación de la consistencia |
| 6. Componente integrado | Integración | Respuesta correcta y error controlado; recuperación sin datos inconsistentes | Descripción, casos y evidencias de respuestas y tratamiento de errores |
| 7. Registro de información | Aceptación | Campos, validaciones, mensajes comprensibles, guardado, consulta y restricciones | Caso de aceptación, criterios, datos, evidencias y resultado |
| 8. Proceso completo | Aceptación | Flujo central de principio a fin, precondiciones y estado final | Flujo, criterios y evidencias de todos los pasos |
| 9. Escenarios excepcionales | Aceptación | Al menos tres situaciones excepcionales del sistema | Matriz de escenarios, comportamiento esperado, resultados y defectos |
| 10. Validación final | Aceptación | Entre cinco y ocho criterios verificables y guion para otro usuario | Acta con observaciones, criterios cumplidos e incumplidos, pendientes y decisión justificada |

## Condiciones de la entrega

- Las pruebas unitarias deben ejecutar las funciones de forma aislada y con entradas controladas.
- Las pruebas de integración deben comprobar el intercambio real entre los módulos incluidos en cada escenario.
- Las pruebas de aceptación deben ejecutar operaciones desde la interfaz disponible al usuario.
- Los resultados se registrarán después de ejecutar las pruebas. Un caso diseñado no constituye evidencia de ejecución.
- Si el sistema no tiene servicios externos, el ejercicio 6 permite utilizar la API interna o la integración entre lógica de negocio y base de datos.
- La evaluación del ejercicio 10 debe identificarse como **simulada** cuando no participe un usuario real.
- El acta final debe expresar una de estas decisiones: **aceptada**, **aceptada con observaciones** o **rechazada**, según los criterios comprobados.
