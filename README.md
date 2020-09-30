<h1 align="center">exportdede</h1>
<p align="center"><img src="https://i.imgur.com/wTBblA4.png" title="Megadede Tweet" alt="Megadede Tweet"></p>

**Requisitos**
* Tener al menos uno de estos navegadores instalado:
    * [Google Chrome](https://www.google.com/chrome)
    * [Mozilla Firefox](https://www.mozilla.org/firefox)

## Archivo ejecutable
**IMPORTANTE** * Es probable que este proceso pueda llegar a tardar más de lo esperado, esto depende de la velocidad de conexión a internet de cada uno y/o de la cantidad de información que la herramienta tenga que procesar.
* Descargar herramienta según el navegador instalado:
    * [exportdede para Chrome](https://github.com/cecicifu/exportdede/releases/download/1.0/exportdede_chrome.zip)
    * [exportdede para Firefox](https://github.com/cecicifu/exportdede/releases/download/1.0/exportdede_firefox.zip)
* Extraer archivo comprimido.
* Ejecutar archivo `exportdede.exe`.
* Se abrirá el navegador donde deberás introducir tus credenciales.
* Introducidos correctamente la herramienta efectuará los siguientes pasos de manera automática y exportará las listas a un archivo llamado `lists.json` en el mismo directorio.
## Línea de comandos (Avanzado)
**IMPORTANTE** * Es probable que este proceso pueda llegar a tardar más de lo esperado, esto depende de la velocidad de conexión a internet de cada uno y/o de la cantidad de información que la herramienta tenga que procesar.

**IMPORTANTE** * Para este paso es necesario tener instalado previamente Python 3 junto a todas las dependencias indicadas en el archivo `requirements.txt`.
* [Descargar herramienta](https://github.com/cecicifu/exportdede/archive/master.zip)
* Dirígete al directorio de la herramienta a través de la terminal.
* Una vez allí, ejecutar el siguiente comando en la terminal dependiendo de tu navegador:
    * Google Chrome:
        ```shell
        $ py exportdede.py --chrome
        ```
    * Mozilla Firefox:
        ```shell
        $ py exportdede.py --firefox
        ```
* Se abrirá el navegador donde deberás introducir tus credenciales.
* Introducidos correctamente la herramienta efectuará los siguientes pasos de manera automática y exportará las listas a un archivo llamado `lists.json` en el mismo directorio.
