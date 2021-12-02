import random

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def input_to_numbers(input):
    dict_values = {}
    dict_letters = {}
    index=0
    for i in abc:
        dict_values[index] = i
        dict_letters[i] = index
        index += 1
    input_as_list = []
    for k in input:
        input_as_list.append(dict_letters[k])
    return input_as_list

def input_to_letters(input):
    dict_values = {}
    dict_letters = {}
    index=0
    for i in abc:
        dict_values[index] = i
        dict_letters[i] = index
        index += 1
    input_as_string = ""
    for i in input:
        input_as_string  = input_as_string+str(dict_values[i])
    return input_as_string

def code(texto_claro_cifrar,clave_cifrar):
    texto_claro_as_list = input_to_numbers(clean_input(texto_claro_cifrar))
    clave_clean = clean_input(clave_cifrar)
    texto_cifrado = []
    if len(clave_clean)==0:
        key = input_to_numbers(generate_key())[0]
    else:
        key = input_to_numbers(clave_clean[0])[0]

    for i in range(len(texto_claro_as_list)):
        texto_cifrado.append((texto_claro_as_list[i]+key)%26)
    return input_to_letters(texto_cifrado), input_to_letters([key])

def generate_key():
    clave = ''.join(random.sample(abc,1))
    return clave

def decode(texto_cifrado, clave):
    texto_cifrado_as_list = input_to_numbers(clean_input(texto_cifrado))
    clave_clean = clean_input(clave)
    texto_claro = []
    key = input_to_numbers(clave_clean[0])[0]

    for i in range(len(texto_cifrado_as_list)):
        texto_claro.append((texto_cifrado_as_list[i]-key)%26)
    return input_to_letters(texto_claro).lower(), input_to_letters([key])


def criptoanalisis(texto_cifrado):
    texto_cifrado_as_list = input_to_numbers(clean_input(texto_cifrado))
    claves = input_to_numbers(abc)
    solucion = ""
    for i in claves:
        texto_claro_as_list = []
        for j in range(len(texto_cifrado_as_list)):
            texto_claro_as_list.append((texto_cifrado_as_list[j]-i)%26)
        solucion = solucion + "Clave = "+abc[i]+" ("+str(i)+")  -  " + input_to_letters(texto_claro_as_list).lower()+"\n\n"

    return solucion

def attack(texto_claro, texto_cifrado):
    texto_claro_as_list = input_to_numbers(clean_input(texto_claro))
    texto_cifrado_as_list = input_to_numbers(clean_input(texto_cifrado))

    for i in range(len(texto_claro_as_list)):
        clave_aux = (texto_cifrado_as_list[0]-texto_claro_as_list[0])%26
        clave = (texto_cifrado_as_list[i]-texto_claro_as_list[i])%26
        if clave!=clave_aux:
            return "El texto está siendo cifrado con más de una clave"
    return input_to_letters([clave]) 

def clean_input(input):
    alphanumeric_claro = ""
    for character in input.replace(" ", ""):
        if character == 'Ñ' or character == 'ñ':
            continue
        if not character.isdigit() and character.isalpha():
            alphanumeric_claro += character

    return alphanumeric_claro.upper()