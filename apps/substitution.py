import random

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def code(texto_claro_cifrar,clave_cifrar):
    alphanumeric = clean_input(texto_claro_cifrar)
    clave_clean = clean_input(clave_cifrar)
    if len(clave_clean)==0:
        clave_clean = generate_key()
    texto_cifrado = ""
    dict_key = dict(zip(list(abc),list(clave_clean)))
    for i in alphanumeric.upper():
        texto_cifrado = texto_cifrado+str(dict_key[i])

    return texto_cifrado,clave_clean

def generate_key():
    clave = ''.join(random.sample(abc,len(abc)))
    return clave

def decode(texto_cifrado, clave):
    alphanumeric = clean_input(texto_cifrado)
    clave_clean = clean_input(clave)
    
    texto_claro = ""
    dict_key = dict(zip(list(clave_clean),list(abc)))
    for i in alphanumeric.upper():
        texto_claro = texto_claro+str(dict_key[i])

    return texto_claro

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