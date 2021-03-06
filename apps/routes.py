from flask import Blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound
from apps.controllers import galery_controller
import apps.substitution
import apps.vigenere
import apps.permutation
import apps.shift
import apps.afin
import apps.hill
import apps.RSA
import apps.Rabin
import apps.Elgamal
import apps.NEAR
import random
import os
from apps.controllers import *

bp = Blueprint("routes", __name__)


@bp.route('/')
def route_default():
    return render_template('routes/index.html', segment='index')


@bp.route('/galery')
def galery():
		res = galery_controller.get_list()
		return ((res))
		#galery.get_list= classmethod(galery.get_list)
		#galery.get_list()
    
		#return render_template('pages/galery.html')


@bp.route('/shift_code', methods=["POST", "GET"])
def shift_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.shift.clean_input(
            request.form['texto_claro_cifrar']).lower()
        texto_cifrado, clave_cifrar_clean = apps.shift.code(
            request.form['texto_claro_cifrar'], request.form['clave_cifrar'])

        return render_template('routes/shift.html', texto_claro_cifrar=texto_claro_cifrar_clean,
                               clave_cifrar=clave_cifrar_clean, texto_cifrado_cifrar=texto_cifrado, segment='shift', scroll="cifrar")
    else:
        texto_claro_cifrar_clean = apps.shift.clean_input(
            request.form['texto_claro_cifrar']).lower()
        clave = apps.shift.generate_key()
        return render_template('routes/shift.html', texto_claro_cifrar=texto_claro_cifrar_clean,
                               clave_cifrar=clave, texto_cifrado_cifrar="", segment='shift', scroll="cifrar")


@bp.route('/shift_decode', methods=["POST", "GET"])
def shift_decode():
    if request.form['action'] == 'descifrar':
        if len(request.form['clave_descifrar']) == 0:
            texto_cifrado_descifrar_clean = apps.shift.clean_input(
                request.form['texto_cifrado_descifrar'])
            solucion = apps.shift.criptoanalisis(texto_cifrado_descifrar_clean)
            return render_template('routes/shift.html', texto_cifrado_criptoanalisis=texto_cifrado_descifrar_clean, posibles_textos_claros=solucion,
                                   segment="shift", scroll="criptoanalisis")
        else:
            texto_claro, clave = apps.shift.decode(
                request.form['texto_cifrado_descifrar'], request.form['clave_descifrar'])
            return render_template('routes/shift.html', texto_claro_descifrar=texto_claro,
                                   clave_descifrar=clave, texto_cifrado_descifrar=apps.shift.clean_input(
                                       request.form['texto_cifrado_descifrar']),
                                   segment='shift', scroll="descifrar")
    else:
        texto_cifrado_descifrar_clean = apps.shift.clean_input(
            request.form['texto_cifrado_descifrar'])
        solucion = apps.shift.criptoanalisis(texto_cifrado_descifrar_clean)
        return render_template('routes/shift.html', texto_cifrado_criptoanalisis=texto_cifrado_descifrar_clean, posibles_textos_claros=solucion,
                               segment="shift", scroll="criptoanalisis")


@bp.route('/shift_attack', methods=["POST", "GET"])
def shift_attack():
    if len(apps.shift.clean_input(request.form['texto_claro_atacar'])) != len(apps.shift.clean_input(request.form['texto_cifrado_atacar'])):
        clave_atacar = "El texto claro y el texto cifrado no tienen la misma longitud"
        return render_template('routes/shift.html', texto_cifrado_atacar=apps.shift.clean_input(request.form['texto_cifrado_atacar']),
                               texto_claro_atacar=apps.shift.clean_input(request.form['texto_claro_atacar']), clave_atacar=clave_atacar, segment="shift", scroll="atacar")

    else:
        clave = apps.shift.attack(
            request.form['texto_claro_atacar'], request.form['texto_cifrado_atacar'])

    return render_template('routes/shift.html', texto_cifrado_atacar=apps.shift.clean_input(request.form['texto_cifrado_atacar']),
                           texto_claro_atacar=apps.shift.clean_input(request.form['texto_claro_atacar']).lower(), clave_atacar=clave, segment="shift", scroll="atacar")


@bp.route('/substitution_code', methods=["POST", "GET"])
def substitution_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.substitution.clean_input(
            request.form['texto_claro_cifrar']).lower()
        clave_cifrar_clean = apps.substitution.clean_input(
            request.form['clave_cifrar'])
        if len(clave_cifrar_clean) != 26 and len(clave_cifrar_clean) != 0:
            return render_template('routes/substitution.html', texto_claro_cifrar=texto_claro_cifrar_clean,
                                   clave_cifrar="La clave tiene una longitud diferente a 26", texto_cifrado_cifrar="", segment='substitution', scroll="cifrar")

        texto_cifrado, clave = apps.substitution.code(
            request.form['texto_claro_cifrar'], request.form['clave_cifrar'])

        return render_template('routes/substitution.html', texto_claro_cifrar=texto_claro_cifrar_clean,
                               clave_cifrar=clave, texto_cifrado_cifrar=texto_cifrado, segment='substitution', scroll="cifrar")
    else:
        texto_claro_cifrar_clean = apps.substitution.clean_input(
            request.form['texto_claro_cifrar']).lower()
        clave = apps.substitution.generate_key()
        return render_template('routes/substitution.html', texto_claro_cifrar=texto_claro_cifrar_clean,
                               clave_cifrar=clave, texto_cifrado_cifrar="", segment='substitution', scroll="cifrar")


@bp.route('/substitution_decode', methods=["POST", "GET"])
def substitution_decode():
    if request.form['action'] == 'descifrar':
        if len(apps.substitution.clean_input(request.form['clave_descifrar'])) == 0:
            letters, digrams, trigrams = apps.substitution.criptoanalisis(
                request.form['texto_cifrado_descifrar'])

            return render_template('routes/substitution.html', texto_cifrado_criptoanalisis=request.form['texto_cifrado_descifrar'].replace(" ", ""),
                                   frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="substitution", scroll="criptoanalisis")
        else:
            texto_claro = apps.substitution.decode(
                request.form['texto_cifrado_descifrar'], request.form['clave_descifrar'])

            return render_template('routes/substitution.html', texto_claro_descifrar=texto_claro.lower(),
                                   clave_descifrar=request.form['clave_descifrar'], texto_cifrado_descifrar=apps.substituion.clean_input(
                                       request.form['texto_cifrado_descifrar']),
                                   segment='index', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.substitution.criptoanalisis(
            request.form['texto_cifrado_descifrar'])

        return render_template('routes/substitution.html', texto_cifrado_criptoanalisis=request.form['texto_cifrado_descifrar'].replace(" ", ""),
                               frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="substitution", scroll="criptoanalisis")


@bp.route('/substitution_attack', methods=["POST", "GET"])
def substitution_attack():
    if len(apps.substitution.clean_input(request.form['texto_claro_atacar'])) != len(apps.substitution.clean_input(request.form['texto_cifrado_atacar'])):
        clave_atacar = "El texto claro y el texto cifrado no tienen la misma longitud"
        return render_template('routes/substitution.html', texto_cifrado_atacar=apps.substitution.clean_input(request.form['texto_cifrado_atacar']),
                               texto_claro_atacar=apps.substitution.clean_input(request.form['texto_claro_atacar']).lower(), clave_atacar=clave_atacar, segment="substitution", scroll="atacar")

    clave = apps.substitution.attack(
        request.form['texto_claro_atacar'], request.form['texto_cifrado_atacar'])

    return render_template('routes/substitution.html', texto_cifrado_atacar=request.form['texto_cifrado_atacar'].replace(" ", ""),
                           texto_claro_atacar=request.form['texto_claro_atacar'].replace(" ", ""), clave_atacar=clave, segment="substitution", scroll="atacar")


@bp.route('/vigenere_code', methods=["POST", "GET"])
def vigenere_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.vigenere.clean_input(
            request.form['texto_claro_cifrar']).lower()
        clave_cifrar_clean = apps.vigenere.clean_input(
            request.form['clave_cifrar'])

        size = len(clave_cifrar_clean)
        texto_cifrado = apps.vigenere.code(
            request.form['texto_claro_cifrar'], request.form['clave_cifrar'])

        return render_template('routes/vigenere.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_size=size,
                               clave_cifrar=clave_cifrar_clean, texto_cifrado_cifrar=texto_cifrado, segment='vigenere', scroll="cifrar")
    else:
        texto_claro_cifrar_clean = apps.vigenere.clean_input(
            request.form['texto_claro_cifrar']).lower()
        clave, size = apps.vigenere.generate_key(request.form['clave_size'])
        return render_template('routes/vigenere.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_size=size,
                               clave_cifrar=clave, texto_cifrado_cifrar="", segment='vigenere', scroll="cifrar")


@bp.route('/vigenere_decode', methods=["POST", "GET"])
def vigenere_decode():
    if request.form['action'] == 'descifrar':
        texto_claro = apps.vigenere.decode(
            request.form['texto_cifrado_descifrar'], request.form['clave_descifrar'])

        return render_template('routes/vigenere.html', texto_claro_descifrar=texto_claro.lower(),
                               clave_descifrar=apps.vigenere.clean_input(request.form['clave_descifrar']), texto_cifrado_descifrar=request.form['texto_cifrado_descifrar'],
                               segment='index', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.vigenere.criptoanalisis(
            request.form['texto_cifrado_descifrar'])

        return render_template('routes/vigenere.html', texto_cifrado_criptoanalisis=apps.vigenere.clean_input(request.form['texto_cifrado_descifrar']),
                               frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="vigenere", scroll="criptoanalisis")


@bp.route('/permutation_code', methods=["POST", "GET"])
def permutation_code():
    if request.form['action'] == 'cifrar':
        texto_claro_cifrar_clean = apps.permutation.clean_input(
            request.form['texto_claro_cifrar']).lower()

        texto_cifrado, clave_cifrar_clean, size, texto_claro, clave_numeros = apps.permutation.code(
            request.form['texto_claro_cifrar'], request.form['clave_cifrar'])

        return render_template('routes/permutation.html', texto_claro_cifrar=texto_claro.lower(), clave_size=size, numeros=clave_numeros,
                               clave_cifrar=clave_cifrar_clean, texto_cifrado_cifrar=texto_cifrado, segment='permutation', scroll="cifrar")
    else:
        texto_claro_cifrar_clean = apps.permutation.clean_input(
            request.form['texto_claro_cifrar']).lower()
        clave, size, clave_numeros = apps.permutation.generate_key(
            request.form['clave_size'])

        return render_template('routes/permutation.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_size=size, numeros=clave_numeros,
                               clave_cifrar=clave, texto_cifrado_cifrar="", segment='permutation', scroll="cifrar")


@bp.route('/permutation_decode', methods=["POST", "GET"])
def permutation_decode():
    if request.form['action'] == 'descifrar':
        if len(request.form['clave_descifrar']) == 0:
            letters, digrams, trigrams = apps.permutation.criptoanalisis(
                request.form['texto_cifrado_descifrar'])
            return render_template('routes/permutation.html', texto_cifrado_criptoanalisis=apps.permutation.clean_input(request.form['texto_cifrado_descifrar']),
                                   frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="permutation", scroll="criptoanalisis")

        else:
            texto_claro, clave_descifrar_clean, size, texto_cifrado, clave_numeros = apps.permutation.decode(
                request.form['texto_cifrado_descifrar'], request.form['clave_descifrar'])

            return render_template('routes/permutation.html', texto_claro_descifrar=texto_claro, clave_size=size, numeros=clave_numeros,
                                   clave_descifrar=clave_descifrar_clean, texto_cifrado_descifrar=texto_cifrado, segment='permutation', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.permutation.criptoanalisis(
            request.form['texto_cifrado_descifrar'])

        return render_template('routes/permutation.html', texto_cifrado_criptoanalisis=apps.permutation.clean_input(request.form['texto_cifrado_descifrar']),
                               frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="permutation", scroll="criptoanalisis")


@bp.route('/afin_code', methods=["POST", "GET"])
def afin_code():
    if request.form['action'] == 'cifrar':
        clave_a = apps.afin.clean_key(request.form['clave_cifrar_a'])
        clave_b = apps.afin.clean_key(request.form['clave_cifrar_b'])
        texto_claro_cifrar_clean = apps.afin.clean_input(
            request.form['texto_claro_cifrar']).lower()

        if clave_a > 26:
            return render_template('routes/afin.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                                   texto_cifrado_cifrar="La clave 'a' es mayor a 26", segment='afin', scroll="cifrar")

        if clave_b > 26:
            return render_template('routes/afin.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                                   texto_cifrado_cifrar="La clave 'b' es mayor a 26", segment='afin', scroll="cifrar")

        if apps.afin.maximo_comun_divisor(clave_a, 26) != 1:
            return render_template('routes/afin.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                                   texto_cifrado_cifrar="La clave 'a' no es primo relativo de 26", segment='afin', scroll="cifrar")

        texto_cifrado = apps.afin.code(
            texto_claro_cifrar_clean, clave_a, clave_b)

        return render_template('routes/afin.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                               texto_cifrado_cifrar=texto_cifrado, segment='afin', scroll="cifrar")
    else:
        texto_claro_cifrar_clean = apps.afin.clean_input(
            request.form['texto_claro_cifrar']).lower()
        clave_a, clave_b = apps.afin.generate_key()

        return render_template('routes/afin.html', texto_claro_cifrar=texto_claro_cifrar_clean, clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                               texto_cifrado_cifrar="", segment='afin', scroll="cifrar")


@bp.route('/afin_decode', methods=["POST", "GET"])
def afin_decode():
    if request.form['action'] == 'descifrar':
        if len(request.form['clave_descifrar']) == 0:
            letters, digrams, trigrams = apps.afin.criptoanalisis(
                request.form['texto_cifrado_descifrar'])
            return render_template('routes/afin.html', texto_cifrado_criptoanalisis=apps.afin.clean_input(request.form['texto_cifrado_descifrar']),
                                   frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="afin", scroll="criptoanalisis")
        clave_a = apps.afin.clean_key(request.form['clave_descifrar_a'])
        clave_b = apps.afin.clean_key(request.form['clave_descifrar_b'])
        texto_cifrado_descifrar_clean = apps.afin.clean_input(
            request.form['texto_cifrado_descifrar'])

        if clave_a > 26:
            return render_template('routes/afin.html', texto_cifrado_descifrar=texto_cifrado_descifrar_clean, clave_descifrar_a=clave_a, clave_descifrar_b=clave_b,
                                   texto_claro_descifrar="La clave 'a' es mayor a 26", segment='afin', scroll="descifrar")

        if clave_b > 26:
            return render_template('routes/afin.html', texto_cifrado_descifrar=texto_cifrado_descifrar_clean, clave_descifrar_a=clave_a, clave_descifrar_b=clave_b,
                                   texto_claro_descifrar="La clave 'b' es mayor a 26", segment='afin', scroll="descifrar")

        if apps.afin.maximo_comun_divisor(clave_a, 26) != 1:
            return render_template('routes/afin.html', texto_cifrado_descifrar=texto_cifrado_descifrar_clean, clave_descifrar_a=clave_a, clave_descifrar_b=clave_b,
                                   texto_claro_descifrar="La clave 'a' no es primo relativo de 26", segment='afin', scroll="descifrar")

        texto_claro = apps.afin.decode(
            texto_cifrado_descifrar_clean, clave_a, clave_b)

        return render_template('routes/afin.html', texto_claro_descifrar=texto_claro, clave_descifrar_a=clave_a, clave_descifrar_b=clave_b,
                               texto_cifrado_descifrar=texto_cifrado_descifrar_clean, segment='afin', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.afin.criptoanalisis(
            request.form['texto_cifrado_descifrar'])

        return render_template('routes/afin.html', texto_cifrado_criptoanalisis=apps.afin.clean_input(request.form['texto_cifrado_descifrar']),
                               frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="afin", scroll="criptoanalisis")


@bp.route('/hill_code', methods=["POST", "GET"])
def hill_code():
    texto_claro_cifrar_clean = apps.hill.clean_input(
        request.form['texto_claro_cifrar']).lower()

    if request.form['action'] == 'cifrar':
        tamanio = apps.hill.clean_key(request.form['clave_size'])
        clave_limpia, size = apps.hill.generate_matrix(tamanio)

        matriz_clave = []

        if tamanio is None or tamanio == "":
            lenght = random.randint(2, 10)
        else:
            largo = ""
            for i in tamanio:
                if i.isdigit():
                    largo = largo+str(i)
            lenght = int(largo)
            if lenght > 10:
                lenght = 10
            if lenght < 2:
                lenght = 2

        for i in range(lenght):
            row = []
            for j in range(lenght):
                nombre_celda = "celda_"+str(i)+str(j)
                row.append(request.form[nombre_celda])
            matriz_clave.append(row)

        texto_cifrado, texto_claro, clave, largo = apps.hill.code(
            request.form['texto_claro_cifrar'], matriz_clave, lenght)

        return render_template('routes/hill.html', texto_claro_cifrar=texto_claro.lower(), matriz_clave=clave, clave_size=largo,
                               texto_cifrado_cifrar=texto_cifrado, segment='hill', scroll="cifrar", test=matriz_clave)
    elif request.form['action'] == 'matriz':

        clave, size = apps.hill.generate_matrix(
            apps.hill.clean_key(request.form['clave_size']))
        return render_template('routes/hill.html', texto_claro_cifrar=texto_claro_cifrar_clean, matriz_clave=clave, clave_size=size,
                               texto_cifrado_cifrar="", segment='hill', scroll="cifrar")
    else:
        clave, size = apps.hill.generate_key(
            apps.hill.clean_key(request.form['clave_size']))

        return render_template('routes/hill.html', texto_claro_cifrar=texto_claro_cifrar_clean, matriz_clave=clave, clave_size=size,
                               texto_cifrado_cifrar="", segment='hill', scroll="cifrar")


@bp.route('/hill_decode', methods=["POST", "GET"])
def hill_decode():
    texto_cifrado_descifrar_clean = apps.hill.clean_input(
        request.form['texto_cifrado_descifrar'])

    if request.form['action'] == 'descifrar':
        tamanio = apps.hill.clean_key(request.form['clave_size'])
        clave_limpia, size = apps.hill.generate_matrix(tamanio)

        matriz_clave = []

        if tamanio is None or tamanio == "":
            lenght = random.randint(2, 10)
        else:
            largo = ""
            for i in tamanio:
                if i.isdigit():
                    largo = largo+str(i)
            lenght = int(largo)
            if lenght > 10:
                lenght = 10
            if lenght < 2:
                lenght = 2

        for i in range(lenght):
            row = []
            for j in range(lenght):
                nombre_celda = "celda_"+str(i)+str(j)
                row.append(request.form[nombre_celda])
            matriz_clave.append(row)

        texto_claro, texto_cifrado, clave, largo = apps.hill.decode(
            request.form['texto_cifrado_descifrar'], matriz_clave, lenght)

        if len(request.form['clave_size']) == 0:
            letters, digrams, trigrams = apps.hill.criptoanalisis(
                request.form['texto_cifrado_descifrar'])
            return render_template('routes/hill.html', texto_cifrado_criptoanalisis=apps.hill.clean_input(request.form['texto_cifrado_descifrar']),
                                   frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="hill", scroll="criptoanalisis")

        return render_template('routes/hill.html', texto_claro_descifrar=texto_claro, matriz_clave=clave, clave_size=largo,
                               texto_cifrado_descifrar=texto_cifrado, segment='hill', scroll="descifrar")

    elif request.form['action'] == 'matriz':
        clave, size = apps.hill.generate_matrix(
            apps.hill.clean_key(request.form['clave_size']))
        return render_template('routes/hill.html', texto_claro_descifrar="", matriz_clave=clave, clave_size=size,
                               texto_cifrado_descifrar=texto_cifrado_descifrar_clean, segment='hill', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.afin.criptoanalisis(
            request.form['texto_cifrado_descifrar'])

        return render_template('routes/hill.html', texto_cifrado_criptoanalisis=apps.afin.clean_input(request.form['texto_cifrado_descifrar']),
                               frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="hill", scroll="criptoanalisis")

@bp.route('/rsa_code', methods=["POST", "GET"])
def rsa_code():
    texto_claro_cifrar_clean = apps.hill.clean_input(request.form['texto_claro_cifrar']).lower()
    clave_a = apps.afin.clean_key(request.form['clave_cifrar_a'])
    clave_b = apps.afin.clean_key(request.form['clave_cifrar_b'])
    clave_p = apps.afin.clean_key(request.form['clave_cifrar_p'])
    clave_q = apps.afin.clean_key(request.form['clave_cifrar_q'])

    if request.form['action'] == 'cifrar':
        texto_claro_cifrar,texto_cifrado_cifrar = apps.RSA.code(request.form['texto_claro_cifrar'],clave_p,clave_q,clave_a,clave_b)
        phi = (clave_p-1)*(clave_q-1)
        phi_n = "\u03A6 (n) = "+str(phi)
        return render_template('routes/RSA.html', texto_claro_cifrar=texto_claro_cifrar, texto_cifrado_cifrar=texto_cifrado_cifrar, phi_n = phi_n, 
                                clave_cifrar_p=clave_p, clave_cifrar_q=clave_q,clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                                clave_descifrar_p=clave_p, clave_descifrar_q=clave_q,clave_descifrar_a=clave_a, clave_descifrar_b=clave_b,
                                segment='rsa', scroll="cifrar")
    else:
        p,q,a,b = apps.RSA.generate_key()
        phi = (p-1)*(q-1)
        phi_n = "\u03A6 (n) = "+str(phi)
        return render_template('routes/RSA.html', texto_claro_cifrar=texto_claro_cifrar_clean, texto_cifrado_cifrar="", phi_n = phi_n,
                                clave_cifrar_p=p, clave_cifrar_q=q, clave_cifrar_a=a, clave_cifrar_b=b,
                                clave_descifrar_p=p, clave_descifrar_q=q, clave_descifrar_a=a, clave_descifrar_b=b,
                                segment='rsa', scroll="cifrar")

@bp.route('/rsa_decode', methods=["POST", "GET"])
def rsa_decode():
    print("entra1")
    texto_cifrado_descifrar_clean = apps.hill.clean_input(request.form['texto_cifrado_descifrar']).lower()
    clave_a = apps.afin.clean_key(request.form['clave_descifrar_a'])
    clave_b = apps.afin.clean_key(request.form['clave_descifrar_b'])
    clave_p = apps.afin.clean_key(request.form['clave_descifrar_p'])
    clave_q = apps.afin.clean_key(request.form['clave_descifrar_q'])
    print("entra2")
    if request.form['action'] == 'descifrar':
        print("entra3")
        texto_cifrado_descifrar, texto_claro_descifrar = apps.RSA.decode(request.form['texto_cifrado_descifrar'],clave_p,clave_q,clave_a,clave_b)
        phi = (clave_p-1)*(clave_q-1)
        phi_n = "\u03A6 (n) = "+str(phi)
        return render_template('routes/RSA.html', texto_claro_descifrar=texto_claro_descifrar, texto_cifrado_descifrar=texto_cifrado_descifrar, phi_n = phi_n, 
                                clave_cifrar_p=clave_p, clave_cifrar_q=clave_q,clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                                clave_descifrar_p=clave_p, clave_descifrar_q=clave_q,clave_descifrar_a=clave_a, clave_descifrar_b=clave_b,
                                segment='rsa', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.afin.criptoanalisis(request.form['texto_cifrado_descifrar'])

        return render_template('routes/RSA.html', texto_cifrado_descifrar = apps.afin.clean_input(request.form['texto_cifrado_descifrar']), texto_cifrado_criptoanalisis=apps.afin.clean_input(request.form['texto_cifrado_descifrar']),
                               clave_cifrar_p=clave_p, clave_cifrar_q=clave_q,clave_cifrar_a=clave_a, clave_cifrar_b=clave_b,
                               clave_descifrar_p=clave_p, clave_descifrar_q=clave_q,clave_descifrar_a=clave_a, clave_descifrar_b=clave_b,
                               frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="rsa", scroll="criptoanalisis")


@bp.route('/rabin_code', methods=["POST", "GET"])
def rabin_code():
    texto_claro_cifrar_clean = apps.hill.clean_input(request.form['texto_claro_cifrar']).lower()
    clave_p = apps.afin.clean_key(request.form['clave_cifrar_p'])
    clave_q = apps.afin.clean_key(request.form['clave_cifrar_q'])
    clave_b = apps.afin.clean_key(request.form['clave_cifrar_b'])

    if request.form['action'] == 'cifrar':
        texto_claro_cifrar,texto_cifrado_cifrar = apps.Rabin.code(request.form['texto_claro_cifrar'],clave_p,clave_q,clave_b)
        return render_template('routes/rabin.html', texto_claro_cifrar=texto_claro_cifrar, texto_cifrado_cifrar=texto_cifrado_cifrar, 
                                clave_cifrar_p=clave_p, clave_cifrar_q=clave_q, clave_cifrar_b=clave_b,
                                clave_descifrar_p=clave_p, clave_descifrar_q=clave_q, clave_descifrar_b=clave_b,
                                segment='rabin', scroll="cifrar")
    else:
        p,q,b = apps.Rabin.generate_key()
        return render_template('routes/rabin.html', texto_claro_cifrar=texto_claro_cifrar_clean, texto_cifrado_cifrar="",
                                clave_cifrar_p=p, clave_cifrar_q=q, clave_cifrar_b=b,
                                clave_descifrar_p=p, clave_descifrar_q=q, clave_descifrar_b=b,
                                segment='rabin', scroll="cifrar")

@bp.route('/rabin_decode', methods=["POST", "GET"])
def rabin_decode():    
    clave_p = apps.afin.clean_key(request.form['clave_descifrar_p'])
    clave_q = apps.afin.clean_key(request.form['clave_descifrar_q'])
    clave_b = apps.afin.clean_key(request.form['clave_descifrar_b'])

    if request.form['action'] == 'descifrar':
        texto_cifrado_descifrar, texto_claro_descifrar = apps.Rabin.decode(request.form['texto_cifrado_descifrar'],clave_p,clave_q,clave_b)

        return render_template('routes/rabin.html', texto_claro_descifrar=texto_claro_descifrar, texto_cifrado_descifrar=texto_cifrado_descifrar, 
                                clave_cifrar_p=clave_p, clave_cifrar_q=clave_q, clave_cifrar_b=clave_b,
                                clave_descifrar_p=clave_p, clave_descifrar_q=clave_q,clave_descifrar_b=clave_b,
                                segment='rabin', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.afin.criptoanalisis(request.form['texto_cifrado_descifrar'])

        return render_template('routes/rabin.html', texto_cifrado_descifrar = apps.afin.clean_input(request.form['texto_cifrado_descifrar']), texto_cifrado_criptoanalisis=apps.afin.clean_input(request.form['texto_cifrado_descifrar']),
                               clave_cifrar_p=clave_p, clave_cifrar_q=clave_q, clave_cifrar_b=clave_b,
                               clave_descifrar_p=clave_p, clave_descifrar_q=clave_q, clave_descifrar_b=clave_b,
                               frecuencias_letras=letters, frecuencias_digramas=digrams, frecuencias_trigramas=trigrams, segment="rabin", scroll="criptoanalisis")


@bp.route('/elgamal_code', methods=["POST", "GET"])
def elgamal_code():
    texto_claro_cifrar_clean = apps.hill.clean_input(request.form['texto_claro_cifrar']).lower()
    clave_p = apps.afin.clean_key(request.form['clave_cifrar_p'])
    clave_alpha = apps.afin.clean_key(request.form['clave_cifrar_alpha'])
    clave_a = apps.afin.clean_key(request.form['clave_cifrar_a'])
    clave_m = apps.afin.clean_key(request.form['clave_cifrar_m'])

    if request.form['action'] == 'cifrar':
        texto_claro_cifrar,texto_cifrado_cifrar = apps.Elgamal.code(request.form['texto_claro_cifrar'],clave_p,clave_alpha,clave_a,clave_m)
        return render_template('routes/elgamal.html', texto_claro_cifrar=texto_claro_cifrar, texto_cifrado_cifrar=texto_cifrado_cifrar, 
                                clave_cifrar_p=clave_p, clave_cifrar_alpha=clave_alpha, clave_cifrar_a=clave_a, clave_cifrar_m=clave_m,
                                clave_descifrar_p=clave_p, clave_descifrar_alpha=clave_alpha, clave_descifrar_a=clave_a, clave_descifrar_m=clave_m,
                                segment='elgamal', scroll="cifrar")
    else:
        p,alpha,a,m = apps.Elgamal.generate_key()
        return render_template('routes/elgamal.html', texto_claro_cifrar=texto_claro_cifrar_clean, texto_cifrado_cifrar="",
                                clave_cifrar_p=p, clave_cifrar_alpha=alpha, clave_cifrar_a=a, clave_cifrar_m=m,
                                clave_descifrar_p=p, clave_descifrar_alpha=alpha, clave_descifrar_a=a, clave_descifrar_m=m,
                                segment='elgamal', scroll="cifrar")

@bp.route('/elgamal_decode', methods=["POST", "GET"])
def elgamal_decode():    
    clave_p = apps.afin.clean_key(request.form['clave_descifrar_p'])
    clave_alpha = apps.afin.clean_key(request.form['clave_descifrar_alpha'])
    clave_a = apps.afin.clean_key(request.form['clave_descifrar_a'])
    clave_m = apps.afin.clean_key(request.form['clave_descifrar_m'])

    if request.form['action'] == 'descifrar':
        texto_cifrado_descifrar, texto_claro_descifrar = apps.Elgamal.decode(request.form['texto_cifrado_descifrar'],clave_p,clave_alpha,clave_a)

        return render_template('routes/elgamal.html', texto_claro_descifrar=texto_claro_descifrar, texto_cifrado_descifrar=texto_cifrado_descifrar, 
                                clave_cifrar_p=clave_p, clave_cifrar_alpha=clave_alpha, clave_cifrar_a=clave_a, clave_cifrar_m=clave_m,
                                clave_descifrar_p=clave_p, clave_descifrar_alpha=clave_alpha, clave_descifrar_a=clave_a, clave_descifrar_m=clave_m,
                                segment='elgamal', scroll="descifrar")
    else:
        letters, digrams, trigrams = apps.afin.criptoanalisis(request.form['texto_cifrado_descifrar'])

        return render_template('routes/elgamal.html', segment="elgamal", scroll="criptoanalisis")




@bp.route('/mint_nft', methods=["POST", "GET"])
def mint_nft():
    student_first_name = request.form['student_first_name']
    student_last_name = request.form['student_last_name']
    student_nin = request.form['student_nin']
    course_name = request.form['course_name']
    professor_name = request.form['professor_name']
    graduation_date = request.form['graduation_date']
    minted, answer = apps.NEAR.mintCertificate(
        student_first_name, student_last_name, student_nin, course_name, professor_name, graduation_date)
    # minted=""
    # answer=""
    minted_info = minted.split("\n")
    link_transaction = minted_info[4]
    link_media = minted_info[11]

    return render_template('routes/academic_certificate.html', student_first_name=student_first_name, student_last_name=student_last_name, student_nin=student_nin,
                           course_name=course_name, professor_name=professor_name, graduation_date=graduation_date,
                           answer=answer, minted=minted, segment="certificate", linkTransaction=link_transaction, linkMedia=link_media[12:-2], scroll="create")


@bp.route('/nft_list', methods=["POST", "GET"])
def nft_list():
    answer = apps.NEAR.nft_list()
    return render_template('routes/academic_certificate.html', answer=answer, segment="certificate", scroll="list_nft")


@bp.route('/nft_list_by_account', methods=["POST", "GET"])
def nft_list_by_account():
    answer=apps.NEAR.nft_list_by_account(request.form['account'])
    return render_template('routes/academic_certificate.html',answer_account=answer,segment="certificate", scroll="list_nft")

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


@bp.route('/exampleRouting', methods=["GET"])
def exampleRouting():
    try:
        print("Example routing")
    except TemplateNotFound:
        return render_template('routes/page-404.html'), 404

    except:
        return render_template('routes/page-500.html'), 500
