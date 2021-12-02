from flask import Blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound
import apps.substitution
import apps.vigenere
import apps.permutation
import apps.shift
import apps.afin
import apps.hill


bp = Blueprint("routes", __name__)

@bp.route('/')
def route_default():
    return render_template('routes/index.html', segment='index')

@bp.route('/shift_code', methods=["POST", "GET"])
def shift_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.shift.clean_input(request.form['texto_claro_cifrar']).lower() 
        texto_cifrado, clave_cifrar_clean = apps.shift.code(request.form['texto_claro_cifrar'],request.form['clave_cifrar'])
        
        return render_template('routes/shift.html', texto_claro_cifrar = texto_claro_cifrar_clean,
                                clave_cifrar = clave_cifrar_clean, texto_cifrado_cifrar = texto_cifrado, segment='shift', scroll = "cifrar")
    else:
        texto_claro_cifrar_clean = apps.shift.clean_input(request.form['texto_claro_cifrar']).lower()
        clave = apps.shift.generate_key()        
        return render_template('routes/shift.html', texto_claro_cifrar = texto_claro_cifrar_clean,
                                clave_cifrar = clave, texto_cifrado_cifrar = "", segment='shift', scroll = "cifrar")

@bp.route('/shift_decode', methods=["POST", "GET"])
def shift_decode():
    if request.form['action'] == 'descifrar':
        if len(request.form['clave_descifrar'])==0:
            texto_cifrado_descifrar_clean = apps.shift.clean_input(request.form['texto_cifrado_descifrar'])
            solucion = apps.shift.criptoanalisis(texto_cifrado_descifrar_clean)      
            return render_template('routes/shift.html', texto_cifrado_criptoanalisis = texto_cifrado_descifrar_clean, posibles_textos_claros=solucion,
                                segment="shift", scroll = "criptoanalisis")
        else:
            texto_claro, clave = apps.shift.decode(request.form['texto_cifrado_descifrar'], request.form['clave_descifrar'])      
            return render_template('routes/shift.html', texto_claro_descifrar = texto_claro,
                                clave_descifrar = clave, texto_cifrado_descifrar = apps.shift.clean_input(request.form['texto_cifrado_descifrar']), 
                                segment = 'shift', scroll = "descifrar")
    else:
        texto_cifrado_descifrar_clean = apps.shift.clean_input(request.form['texto_cifrado_descifrar'])
        solucion = apps.shift.criptoanalisis(texto_cifrado_descifrar_clean)      
        return render_template('routes/shift.html', texto_cifrado_criptoanalisis = texto_cifrado_descifrar_clean, posibles_textos_claros=solucion,
                                segment="shift", scroll = "criptoanalisis")

@bp.route('/shift_attack', methods=["POST", "GET"])
def shift_attack():
        if len(apps.shift.clean_input(request.form['texto_claro_atacar']))!=len(apps.shift.clean_input(request.form['texto_cifrado_atacar'])):
            clave_atacar="El texto claro y el texto cifrado no tienen la misma longitud"
            return render_template('routes/shift.html', texto_cifrado_atacar = apps.shift.clean_input(request.form['texto_cifrado_atacar']), 
                                texto_claro_atacar = apps.shift.clean_input(request.form['texto_claro_atacar']), clave_atacar=clave_atacar, segment="shift", scroll = "atacar")

        else:       
            clave = apps.shift.attack(request.form['texto_claro_atacar'], request.form['texto_cifrado_atacar'])

        return render_template('routes/shift.html', texto_cifrado_atacar = apps.shift.clean_input(request.form['texto_cifrado_atacar']), 
                                texto_claro_atacar = apps.shift.clean_input(request.form['texto_claro_atacar']).lower(), clave_atacar=clave, segment="shift", scroll = "atacar")



@bp.route('/substitution_code', methods=["POST", "GET"])
def substitution_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.substitution.clean_input(request.form['texto_claro_cifrar']).lower() 
        clave_cifrar_clean = apps.substitution.clean_input(request.form['clave_cifrar'])
        if len(clave_cifrar_clean)!=26 and len(clave_cifrar_clean)!=0:
            return render_template('routes/substitution.html', texto_claro_cifrar = texto_claro_cifrar_clean,
                                clave_cifrar = "La clave tiene una longitud diferente a 26", texto_cifrado_cifrar = "", segment='substitution', scroll = "cifrar")

        texto_cifrado,clave = apps.substitution.code(request.form['texto_claro_cifrar'],request.form['clave_cifrar'])
        
        return render_template('routes/substitution.html', texto_claro_cifrar = texto_claro_cifrar_clean,
                                clave_cifrar = clave, texto_cifrado_cifrar = texto_cifrado, segment='substitution', scroll = "cifrar")
    else:
        texto_claro_cifrar_clean = apps.substitution.clean_input(request.form['texto_claro_cifrar']).lower()
        clave = apps.substitution.generate_key()        
        return render_template('routes/substitution.html', texto_claro_cifrar = texto_claro_cifrar_clean,
                                clave_cifrar = clave, texto_cifrado_cifrar = "", segment='substitution', scroll = "cifrar")

@bp.route('/substitution_decode', methods=["POST", "GET"])
def substitution_decode():
    if request.form['action'] == 'descifrar':
        if len(apps.substitution.clean_input(request.form['clave_descifrar']))==0:
            letters,digrams,trigrams = apps.substitution.criptoanalisis(request.form['texto_cifrado_descifrar'])

            return render_template('routes/substitution.html', texto_cifrado_criptoanalisis = request.form['texto_cifrado_descifrar'].replace(" ", ""), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="substitution", scroll = "criptoanalisis")
        else:
            texto_claro = apps.substitution.decode(request.form['texto_cifrado_descifrar'], request.form['clave_descifrar'])      

            return render_template('routes/substitution.html', texto_claro_descifrar = texto_claro.lower(),
                                    clave_descifrar = request.form['clave_descifrar'], texto_cifrado_descifrar = apps.substituion.clean_input(request.form['texto_cifrado_descifrar']), 
                                    segment = 'index', scroll = "descifrar")
    else:
        letters,digrams,trigrams = apps.substitution.criptoanalisis(request.form['texto_cifrado_descifrar'])

        return render_template('routes/substitution.html', texto_cifrado_criptoanalisis = request.form['texto_cifrado_descifrar'].replace(" ", ""), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="substitution", scroll = "criptoanalisis")

@bp.route('/substitution_attack', methods=["POST", "GET"])
def substitution_attack():
        if len(apps.substitution.clean_input(request.form['texto_claro_atacar']))!=len(apps.substitution.clean_input(request.form['texto_cifrado_atacar'])):
            clave_atacar="El texto claro y el texto cifrado no tienen la misma longitud"
            return render_template('routes/substitution.html', texto_cifrado_atacar = apps.substitution.clean_input(request.form['texto_cifrado_atacar']), 
                                texto_claro_atacar = apps.substitution.clean_input(request.form['texto_claro_atacar']).lower(), clave_atacar=clave_atacar, segment="substitution", scroll = "atacar")



        clave = apps.substitution.attack(request.form['texto_claro_atacar'], request.form['texto_cifrado_atacar'])

        return render_template('routes/substitution.html', texto_cifrado_atacar = request.form['texto_cifrado_atacar'].replace(" ", ""), 
                                texto_claro_atacar = request.form['texto_claro_atacar'].replace(" ", ""), clave_atacar=clave, segment="substitution", scroll = "atacar")


@bp.route('/vigenere_code', methods=["POST", "GET"])
def vigenere_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.vigenere.clean_input(request.form['texto_claro_cifrar']).lower() 
        clave_cifrar_clean = apps.vigenere.clean_input(request.form['clave_cifrar'])
        
        size = len(clave_cifrar_clean)
        texto_cifrado = apps.vigenere.code(request.form['texto_claro_cifrar'],request.form['clave_cifrar'])
        
        return render_template('routes/vigenere.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_size = size,
                                clave_cifrar = clave_cifrar_clean, texto_cifrado_cifrar = texto_cifrado, segment='vigenere', scroll = "cifrar")
    else:
        texto_claro_cifrar_clean = apps.vigenere.clean_input(request.form['texto_claro_cifrar']).lower()
        clave, size = apps.vigenere.generate_key(request.form['clave_size'])        
        return render_template('routes/vigenere.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_size = size,
                                clave_cifrar = clave, texto_cifrado_cifrar = "", segment='vigenere', scroll = "cifrar")

@bp.route('/vigenere_decode', methods=["POST", "GET"])
def vigenere_decode():
    if request.form['action'] == 'descifrar':
        texto_claro = apps.vigenere.decode(request.form['texto_cifrado_descifrar'], request.form['clave_descifrar'])      

        return render_template('routes/vigenere.html', texto_claro_descifrar = texto_claro.lower(),
                                clave_descifrar = apps.vigenere.clean_input(request.form['clave_descifrar']), texto_cifrado_descifrar = request.form['texto_cifrado_descifrar'], 
                                segment = 'index', scroll = "descifrar")
    else:
        letters,digrams,trigrams = apps.vigenere.criptoanalisis(request.form['texto_cifrado_descifrar'])
        
        return render_template('routes/vigenere.html', texto_cifrado_criptoanalisis = apps.vigenere.clean_input(request.form['texto_cifrado_descifrar']), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="vigenere", scroll = "criptoanalisis")

@bp.route('/permutation_code', methods=["POST", "GET"])
def permutation_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.permutation.clean_input(request.form['texto_claro_cifrar']).lower()
        
        texto_cifrado,clave_cifrar_clean, size, texto_claro, clave_numeros = apps.permutation.code(request.form['texto_claro_cifrar'],request.form['clave_cifrar'])
        
        return render_template('routes/permutation.html', texto_claro_cifrar = texto_claro.lower(), clave_size = size, numeros = clave_numeros,
                                clave_cifrar = clave_cifrar_clean, texto_cifrado_cifrar = texto_cifrado, segment='permutation', scroll = "cifrar")
    else:        
        texto_claro_cifrar_clean = apps.permutation.clean_input(request.form['texto_claro_cifrar']).lower()
        clave, size, clave_numeros = apps.permutation.generate_key(request.form['clave_size'])
               
        return render_template('routes/permutation.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_size = size, numeros = clave_numeros,
                                clave_cifrar = clave, texto_cifrado_cifrar = "", segment='permutation', scroll = "cifrar")


@bp.route('/permutation_decode', methods=["POST", "GET"])
def permutation_decode():
    if request.form['action'] == 'descifrar':    
        if len(request.form['clave_descifrar'])==0:
            letters,digrams,trigrams = apps.permutation.criptoanalisis(request.form['texto_cifrado_descifrar'])        
            return render_template('routes/permutation.html', texto_cifrado_criptoanalisis = apps.permutation.clean_input(request.form['texto_cifrado_descifrar']), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="permutation", scroll = "criptoanalisis")        
        
        else:        
            texto_claro,clave_descifrar_clean, size, texto_cifrado, clave_numeros = apps.permutation.decode(request.form['texto_cifrado_descifrar'],request.form['clave_descifrar'])
            
            return render_template('routes/permutation.html', texto_claro_descifrar = texto_claro, clave_size = size, numeros=clave_numeros,
                                clave_descifrar = clave_descifrar_clean, texto_cifrado_descifrar = texto_cifrado, segment='permutation', scroll = "descifrar")
    else:
        letters,digrams,trigrams = apps.permutation.criptoanalisis(request.form['texto_cifrado_descifrar'])
        
        return render_template('routes/permutation.html', texto_cifrado_criptoanalisis = apps.permutation.clean_input(request.form['texto_cifrado_descifrar']), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="permutation", scroll = "criptoanalisis")

@bp.route('/afin_code', methods=["POST", "GET"])
def afin_code():
    if request.form['action'] == 'cifrar':
        clave_a = apps.afin.clean_key(request.form['clave_cifrar_a'])
        clave_b = apps.afin.clean_key(request.form['clave_cifrar_b'])
        texto_claro_cifrar_clean = apps.afin.clean_input(request.form['texto_claro_cifrar']).lower()

        if clave_a>26:
            return render_template('routes/afin.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_cifrar_a = clave_a, clave_cifrar_b = clave_b, 
                                    texto_cifrado_cifrar="La clave 'a' es mayor a 26",segment='afin', scroll = "cifrar")

        if clave_b>26:
            return render_template('routes/afin.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_cifrar_a = clave_a, clave_cifrar_b = clave_b, 
                                    texto_cifrado_cifrar="La clave 'b' es mayor a 26", segment='afin', scroll = "cifrar")

        if apps.afin.maximo_comun_divisor(clave_a,26)!=1:
            return render_template('routes/afin.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_cifrar_a = clave_a, clave_cifrar_b = clave_b, 
                                    texto_cifrado_cifrar="La clave 'a' no es primo relativo de 26",segment='afin', scroll = "cifrar")

        texto_cifrado = apps.afin.code(texto_claro_cifrar_clean,clave_a,clave_b)
        
        return render_template('routes/afin.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_cifrar_a = clave_a, clave_cifrar_b = clave_b, 
                                texto_cifrado_cifrar = texto_cifrado, segment='afin', scroll = "cifrar")
    else:        
        texto_claro_cifrar_clean = apps.afin.clean_input(request.form['texto_claro_cifrar']).lower()
        clave_a,clave_b = apps.afin.generate_key()
               
        return render_template('routes/afin.html', texto_claro_cifrar = texto_claro_cifrar_clean, clave_cifrar_a = clave_a, clave_cifrar_b = clave_b,
                                texto_cifrado_cifrar = "", segment='afin', scroll = "cifrar")

@bp.route('/afin_decode', methods=["POST", "GET"])
def afin_decode():
    if request.form['action'] == 'descifrar':
        if len(request.form['clave_descifrar'])==0:
            letters,digrams,trigrams = apps.afin.criptoanalisis(request.form['texto_cifrado_descifrar'])        
            return render_template('routes/afin.html', texto_cifrado_criptoanalisis = apps.afin.clean_input(request.form['texto_cifrado_descifrar']), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="afin", scroll = "criptoanalisis")        
        clave_a = apps.afin.clean_key(request.form['clave_descifrar_a'])
        clave_b = apps.afin.clean_key(request.form['clave_descifrar_b'])
        texto_cifrado_descifrar_clean = apps.afin.clean_input(request.form['texto_cifrado_descifrar'])

        if clave_a>26:
            return render_template('routes/afin.html', texto_cifrado_descifrar = texto_cifrado_descifrar_clean, clave_descifrar_a = clave_a, clave_descifrar_b = clave_b, 
                                    texto_claro_descifrar="La clave 'a' es mayor a 26",segment='afin', scroll = "descifrar")

        if clave_b>26:
            return render_template('routes/afin.html', texto_cifrado_descifrar = texto_cifrado_descifrar_clean, clave_descifrar_a = clave_a, clave_descifrar_b = clave_b, 
                                    texto_claro_descifrar="La clave 'b' es mayor a 26", segment='afin', scroll = "descifrar")

        if apps.afin.maximo_comun_divisor(clave_a,26)!=1:
            return render_template('routes/afin.html', texto_cifrado_descifrar = texto_cifrado_descifrar_clean, clave_descifrar_a = clave_a, clave_descifrar_b = clave_b, 
                                    texto_claro_descifrar="La clave 'a' no es primo relativo de 26",segment='afin', scroll = "descifrar")

        texto_claro = apps.afin.decode(texto_cifrado_descifrar_clean,clave_a,clave_b)
        
        return render_template('routes/afin.html', texto_claro_descifrar = texto_claro, clave_descifrar_a = clave_a, clave_descifrar_b = clave_b, 
                                texto_cifrado_descifrar = texto_cifrado_descifrar_clean, segment='afin', scroll = "descifrar")
    else:        
        letters,digrams,trigrams = apps.afin.criptoanalisis(request.form['texto_cifrado_descifrar'])
        
        return render_template('routes/afin.html', texto_cifrado_criptoanalisis = apps.afin.clean_input(request.form['texto_cifrado_descifrar']), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="afin", scroll = "criptoanalisis")

@bp.route('/hill_code', methods=["POST", "GET"])
def hill_code():
    texto_claro_cifrar_clean = apps.hill.clean_input(request.form['texto_claro_cifrar']).lower()

    if request.form['action'] == 'cifrar':
        clave, size = apps.hill.generate_matrix(apps.hill.clean_key(request.form['clave_size']))
        
        
        return render_template('routes/hill.html', texto_claro_cifrar = texto_claro_cifrar_clean, matriz_clave = clave, clave_size = size,
                                texto_cifrado_cifrar = "Este módulo aún está en construcción", segment='hill', scroll = "cifrar")
    elif request.form['action'] == 'matriz':
        
        clave, size = apps.hill.generate_matrix(apps.hill.clean_key(request.form['clave_size']))
        return render_template('routes/hill.html', texto_claro_cifrar = texto_claro_cifrar_clean, matriz_clave = clave, clave_size = size,
                                texto_cifrado_cifrar = "Este módulo aún está en construcción", segment='hill', scroll = "cifrar")
    else:       
        clave, size = apps.hill.generate_key(apps.hill.clean_key(request.form['clave_size']))

        return render_template('routes/hill.html', texto_claro_cifrar = texto_claro_cifrar_clean, matriz_clave = clave, clave_size = size,
                                texto_cifrado_cifrar = "Este módulo aún está en construcción", segment='hill', scroll = "cifrar")

@bp.route('/hill_decode', methods=["POST", "GET"])
def hill_decode():
    texto_cifrado_descifrar_clean = apps.hill.clean_input(request.form['texto_cifrado_descifrar'])

    if request.form['action'] == 'descifrar':
        if len(request.form['clave_size'])==0:
            letters,digrams,trigrams = apps.hill.criptoanalisis(request.form['texto_cifrado_descifrar'])        
            return render_template('routes/hill.html', texto_cifrado_criptoanalisis = apps.hill.clean_input(request.form['texto_cifrado_descifrar']), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="hill", scroll = "criptoanalisis")        

        clave, size = apps.hill.generate_matrix(apps.hill.clean_key(request.form['clave_size']))
        return render_template('routes/hill.html', texto_claro_descifrar = "Este módulo aún está en construcción", matriz_clave = clave, clave_size = size,
                                texto_cifrado_descifrar = texto_cifrado_descifrar_clean, segment='hill', scroll = "descifrar")
        

    elif request.form['action'] == 'matriz':
        clave, size = apps.hill.generate_matrix(apps.hill.clean_key(request.form['clave_size']))
        return render_template('routes/hill.html', texto_claro_descifrar = "", matriz_clave = clave, clave_size = size,
                                texto_cifrado_descifrar = texto_cifrado_descifrar_clean, segment='hill', scroll = "descifrar")
    else:
        letters,digrams,trigrams = apps.afin.criptoanalisis(request.form['texto_cifrado_descifrar'])
        
        return render_template('routes/hill.html', texto_cifrado_criptoanalisis = apps.afin.clean_input(request.form['texto_cifrado_descifrar']), 
                                frecuencias_letras = letters, frecuencias_digramas = digrams, frecuencias_trigramas = trigrams , segment="hill", scroll = "criptoanalisis")



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