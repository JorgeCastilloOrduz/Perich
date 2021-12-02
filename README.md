# Perich

Aplicación web para la asignatura Criptografía y Teoria de la Información. Hecho por Jorge Luis Castillo Orduz y Juan Pablo Gutiérrez Restrepo.

## Cómo usarlo de forma local

```bash
$ # Get the code
$ git clone https://github.com/JorgeCastilloOrduz/perich.git
$ cd perich
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
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

## Code-base structure

The project is coded using blueprints, app factory pattern, dual configuration profile (development and production) and an intuitive structure presented bellow:

```bash
**********************************************************************************************************

< ROOT >
   |
   |-- apps/
   |    |
   |    |-- static/
   |    |    |   
   |    |    |-- <css, JS, images>          # CSS files, Javascripts files
   |    |
   |    |-- templates/                      # Templates used to render pages
   |    |    |
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |
   |    |    |    |-- sidebar.html          # Sidebar component
   |    |    |    |-- scripts.html          # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |
   |    |    |    |-- base-fullscreen.html  # Used by common pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- routes/                    # UI Kit Pages
   |    |         |
   |    |         |-- *.html                # All pages
   |    |
   |    |-- __init__.py                     # Initialize the app
   |    |-- config.py                       # Set up the app
   |    |-- routes.py                       # Define app routes
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway

**********************************************************************************************************
```