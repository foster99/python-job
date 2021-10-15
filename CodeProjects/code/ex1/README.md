# README
Se incluye el directorio `ex1-env`, el cual contiene el interprete de python con las librerias necesarias para ejecutar el programa.

Basta con ejecutar a traves de terminal el script `main.py` para que se conecte a la base de datos del contenedor, y lleve a cabo las 3 tareas:
* Importar los datos de los ficheros `.json` a la BD.
* Lanzar consultas a la base de datos sobre restaurantes dado un conjunto de parámetros (tal y como se mostraba en el enunciado de la prueba).
* Extraer todos los datos de la BD y convertirlos en un único objeto `.json` denominado `exported_data.json` que contiene todos los segmentos y restaurantes sin repeticiones.

También se incluye el fichero `dump.sql` con el contenido de la base de datos MySQL tras importar los datos.