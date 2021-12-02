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

def code(texto_claro_cifrar, clave_a, clave_b):
    texto_cifrado = []
    texto_claro_cifrar_clean = clean_input(texto_claro_cifrar)
    texto_claro_as_list_of_numbers = input_to_numbers(texto_claro_cifrar_clean)
    for i in texto_claro_as_list_of_numbers:
        texto_cifrado.append((i*int(clave_a)%26+int(clave_b))%26)

    return input_to_letters(texto_cifrado)


def decode(texto_claro_cifrar, clave_a, clave_b):
    texto_claro = []
    k=pow(clave_a, -1, 26)
    texto_claro_cifrar_clean = clean_input(texto_claro_cifrar)
    texto_claro_as_list_of_numbers = input_to_numbers(texto_claro_cifrar_clean)
    for i in texto_claro_as_list_of_numbers:
        texto_claro.append(((i-int(clave_b))*k)%26)

    return input_to_letters(texto_claro).lower()



def generate_key():
    possible_a_keys=[]
    for i in range(27):
        if maximo_comun_divisor(i,26)==1:
            possible_a_keys.append(i)

    clave_a = random.sample(possible_a_keys,1)[0]
    clave_b = random.randint(1, 26)

    return clave_a, clave_b



def criptoanalisis(texto_cifrado):
    alphanumeric = clean_input(texto_cifrado)
    frequencies = {} 
    frequencies_digrams = {}
    frequencies_trigrams = {}

    #Contando letras
    for i in abc:
        frequencies[i] = 0
  
    for char in alphanumeric.upper(): 
        if char in frequencies:             
            frequencies[char] += 1

    table_letters = []
    for key in frequencies:   
        temp = []
        temp.extend([key,frequencies[key]]) 
        table_letters.append(temp)

    
    #Contando digramas
    for i in range(len(alphanumeric)-1):
        if i == len(alphanumeric)-1:
            pass
        if alphanumeric[i:i+2] in frequencies_digrams:
            frequencies_digrams[alphanumeric[i:i+2]] +=1
        else:
            frequencies_digrams[alphanumeric[i:i+2]] = 1

    table_digrams = []
    for key in frequencies_digrams:   
        temp = []
        temp.extend([key,frequencies_digrams[key]]) 
        table_digrams.append(temp)

    #Contando trigramas
    for i in range(len(alphanumeric)-2):
        if i == len(alphanumeric)-2:
            pass
        if alphanumeric[i:i+3] in frequencies_trigrams:
            frequencies_trigrams[alphanumeric[i:i+3]] +=1
        else:
            frequencies_trigrams[alphanumeric[i:i+3]] = 1

    table_trigrams = []
    for key in frequencies_trigrams:   
        temp = []
        temp.extend([key,frequencies_trigrams[key]]) 
        table_trigrams.append(temp)

    return table_letters, table_digrams, table_trigrams

def indices_coincidencia(texto_cifrado):
    alphanumeric = clean_input(texto_cifrado)
    

def attack(texto_claro, texto_cifrado):
    alphanumeric_claro = clean_input(texto_claro)
    alphanumeric_cifrado = clean_input(texto_cifrado)

    dict_key = {} 
    key=[]
    for i in abc:
        dict_key[i] = "-"

    for i in range(len(alphanumeric_claro)):
        dict_key[alphanumeric_claro[i]]=alphanumeric_cifrado[i]
    
    for i in abc:
        key.append(dict_key[i])

    string_key = "".join(key)

    return string_key 

def clean_input(input):
    alphanumeric_claro = ""
    for character in input.replace(" ", ""):
        if character == 'Ñ' or character == 'ñ':
            continue
        if not character.isdigit() and character.isalpha():
            alphanumeric_claro += character

    return alphanumeric_claro.upper()

def clean_key(key):
    key_numbers = ""
    for character in key:
        if character.isdigit():
            key_numbers += character
    if key_numbers=="":
        clave = 1
    else:
        clave = int(key_numbers)
    return clave

def maximo_comun_divisor(a, b):
    temporal = 0
    while b != 0:
        temporal = b
        b = a % b
        a = temporal
    return a
