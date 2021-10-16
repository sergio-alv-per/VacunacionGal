# VacunacionGal
Programa en Python que procesa los datos proporcionados por el Ministerio de Sanidad sobre la vacunación en España y publica tweets con dichos datos actualizados, específicamente sobre la vacunación en Galicia.

Este programa se utiliza para la publicación de los datos en [@VacunacionGal](https://twitter.com/VacunacionGal), en Twitter.

## Ejecución del programa
Para ejecutar el programa se requiere de una base de datos PostgreSQL con la estructura apropiada y las claves de la API de la cuenta de Twitter donde se publicarán los tweets. La URL de la base de datos y las cuatro claves de la API deben ser variables del entorno en donde se ejecute el programa, específicamente con los nombres `BDD_URL`, `CONSUMER_KEY`, `CONSUMER_SECRET`, `KEY` y `SECRET`.

En cada ejecución, el programa accede a la página web del Ministerio de Sanidad y intenta descargar el archivo que contiene la información necesaria. Si se produce algún error en este proceso (habitualmente que el archivo aún no esté subido), el programa aborta su ejecución. Si el programa detecta que ya ha leído el informe de hoy y publicado la información, no hace nada. El programa está diseñado para ser ejecutado periódicamente.
