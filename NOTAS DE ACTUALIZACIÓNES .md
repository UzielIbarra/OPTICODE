Cambios, Agregados y Correcciones OPTICODE 1.1

Migración de Lógica: Se movió el núcleo del programa de una estructura dispersa a una Programación Orientada a Objetos (POO) mediante la clase Tarea. 
Esto facilita el manejo de los datos (nombre, tiempo, valor) en un solo objeto.

Cambio de Interfaz: Se priorizó la ejecución mediante consola/terminal para asegurar que la lógica del algoritmo voraz sea el centro del funcionamiento,
eliminando distracciones de diseño visual previo.Flujo de Ejecución: Se implementó un método main() organizado que separa la entrada de datos,el procesamiento (algoritmo) y la salida de resultados.

Lo que se Agregó (Lógica Voraz)Cálculo de Rentabilidad: Se agregó una métrica de decisión basada en la fórmula $Rentabilidad = \frac{Valor}{Tiempo}$. 
Este es el "cerebro" del programa, ya que permite identificar qué tareas ofrecen más beneficio por cada minuto invertido.

Mecanismo de Ordenamiento (Sorting): Se integró una función de ordenamiento descendente que organiza las tareas de mayor a menor rentabilidad antes de iniciar la selección.

Algoritmo de Selección: Se añadió la lógica de "Mochila 0/1" mediante un enfoque voraz, donde el programa decide en milisegundos qué tareas entran en el tiempo disponible y
cuáles se descartan por falta de espacio.

Resumen de Eficiencia: Al final del proceso, se agregó un bloque de resultados que calcula automáticamente el tiempo utilizado, el tiempo restante y el puntaje total obtenido. 3. 

Lo que se Corrigió (Bugs y Estabilidad)Error de División por Cero: 

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
