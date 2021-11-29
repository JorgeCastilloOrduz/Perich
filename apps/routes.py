from flask import Blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound
from bs4 import BeautifulSoup
import random

bp = Blueprint("routes", __name__)

@bp.route('/')
def route_default():
    return render_template('routes/index.html', segment='index')


@bp.route('/substitution_code', methods=["POST", "GET"])
def substitution_code():
    if request.form['action'] == 'cifrar':
        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        texto_claro = request.form['texto_claro_cifrar'].replace(" ", "")
        clave = request.form['clave_desplazamiento_cifrar'].upper()
        texto_cifrado = ""
        dict_key = dict(zip(list(abc),list(clave)))

        for i in texto_claro.upper():
            texto_cifrado = texto_cifrado+str(dict_key[i])

        return render_template('routes/substitution.html', texto_claro_cifrar = request.form['texto_claro_cifrar'],
                                clave_cifrar = clave, texto_cifrado_cifrar = texto_cifrado, segment='substitution', scroll = "cifrar")
    else:
        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        texto_claro = request.form['texto_claro_cifrar']
        clave = ''.join(random.sample(abc,len(abc)))
        texto_cifrado = ""
        return render_template('routes/substitution.html', texto_claro_cifrar = request.form['texto_claro_cifrar'],
                                clave_cifrar = clave, texto_cifrado_cifrar = texto_cifrado, segment='substitution', scroll = "cifrar")

@bp.route('/substitution_decode', methods=["POST", "GET"])
def substitution_decode():
    if request.form['action'] == 'descifrar':
        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        texto_cifrado = request.form['texto_cifrado_descifrar'].replace(" ", "")
        clave = request.form['clave_desplazamiento_descifrar'].upper()
        texto_claro = ""
        dict_key = dict(zip(list(clave),list(abc)))

        for i in texto_cifrado.upper():
            texto_claro = texto_claro+str(dict_key[i])

        return render_template('routes/substitution.html', texto_claro_descifrar = texto_claro.lower(),
                                clave_descifrar = clave, texto_cifrado_descifrar = texto_cifrado, segment = 'index', scroll = "descifrar")
    else:
        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        texto_cifrado = request.form['texto_cifrado_descifrar'].replace(" ", "")
        return render_template('routes/substitution.html', texto_cifrado_criptoanalisis = texto_cifrado, segment="substitution", scroll = "criptoanalisis")





@bp.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = request.path.split('/')[-1]

        # Serve the file (if exists) from app/templates/routes/*.html
        return render_template("routes/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('routes/page-404.html'), 404

    except:
        return render_template('routes/page-500.html'), 500