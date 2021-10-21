# Ejercicio 5: IKEA CRAWLER

1. Mediante el ChromeWebDriver de selenium, obtengo la pagina web con el JavaScript renderizado.
2. Consulto cual es el total de sofas listados, y sabiendo que se muestran 24 por pagina, solicito la misma url con el valor `?page=(N_sofas/24 + 1)`. De este modo, obtengo la web con el listado de sofás completo.
3. Una vez cuento con la lista completa, la recorro entera obteniendo la información de cada sofa y guardo si cada uno de ellos tiene variantes o no (sin consultar sus variantes en si mismas).
4. Para todos los sofás que tienen variantes, accedo a su pagina principal y extraigo las urls a cada una de las variantes.
5. Entro a cada url de cada variante y obtengo la información. He necesitado acceder a cada url por separado para obtener el link de la imagen en resolución alta.
6. Algunos sofás (sobretodo aquellos que son sofá cama y cuentan con diferentes opciones de colchón), no cuentan con las variantes en su pagina principal, sino que requieren del desplegado de un menú (con una llamada JS). Para estos se aplica otra estrategia, que consiste en extraer los links directamente de producto listado en la página principal. (Esta estrategia no se ha seguido con los otros, porque hay sofás que cuentan con más variantes de las que se muestran, y faltaría información).
7. Tras contar con toda la información, que se ha ido guardando en diccionarios de python, esta se exporta al fichero []`./data/ikea_sofas.json`
