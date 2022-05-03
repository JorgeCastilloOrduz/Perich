# Perich

Aplicación web para la asignatura Criptografía y Teoria de la Información. Hecho por Jorge Luis Castillo Orduz.

## Cómo usarlo de forma local

```bash
$ # Get the code
$ git clone https://github.com/JorgeCastilloOrduz/perich.git
$ cd perich
$
$ # Install modules - SQLite Database
$ pip3 install -r requirements.txt
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ virtualenv env
$ .\env\Scripts\activate
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ (Unix/Mac) export FLASK_ENV=development
$ (Windows) set FLASK_ENV=development
$ (Powershell) $env:FLASK_ENV = "development"
$
$ flask run

