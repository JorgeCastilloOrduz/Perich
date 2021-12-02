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
    clave, clave_as_list = clean_key(clave_cifrar)
    texto_cifrado = ""
    texto_claro_cifrar_clean = clean_input(texto_claro_cifrar)
    if len(texto_claro_cifrar_clean)%len(clave_as_list)!=0:
        for i in range(len(clave_as_list)-(len(texto_claro_cifrar_clean)%len(clave_as_list))):
            texto_claro_cifrar_clean = texto_claro_cifrar_clean+"E"

    
    for i in range(0,len(texto_claro_cifrar_clean),len(clave_as_list)):        
        string_aux = texto_claro_cifrar_clean[i:i+len(clave_as_list)]
        for j in range(len(clave_as_list)):
            texto_cifrado=texto_cifrado+str(string_aux[clave_as_list[j]])
    
    clave_numeros = ''.join([str(int)+" " for int in range(len(clave_as_list))])
        
    return texto_cifrado, clave, len(clave_as_list), texto_claro_cifrar_clean.lower(),clave_numeros


def decode(texto_cifrado_descifrar,clave_descifrar):
    clave, clave_as_list = clean_key(clave_descifrar)
    texto_claro = ""
    texto_cifrado_descifrar_clean = clean_input(texto_cifrado_descifrar)
    if len(texto_cifrado_descifrar_clean)%len(clave_as_list)!=0:
        for i in range(len(clave_as_list)-(len(texto_cifrado_descifrar_clean)%len(clave_as_list))):
            texto_cifrado_descifrar_clean = texto_cifrado_descifrar_clean+"E"

    for i in range(0,len(texto_cifrado_descifrar_clean),len(clave_as_list)):        
        string_aux = texto_cifrado_descifrar_clean[i:i+len(clave_as_list)]        
        for j in range(len(clave_as_list)):
            texto_claro=texto_claro+str(string_aux[clave_as_list.index(j)])
        
    clave_numeros = ''.join([str(int)+" " for int in range(len(clave_as_list))])

    return texto_claro.lower(), clave, len(clave_as_list),texto_cifrado_descifrar_clean,clave_numeros

def generate_key(size):
    if size is None or size == "":
        lenght = random.randint(2, 26)
    else:
        largo=""
        for i in size:
            if i.isdigit():
                largo = largo+str(i)
        lenght = int(largo)
        if lenght>26:
            lenght = 26
        if lenght<2:
            lenght = 2
    clave = ''.join(random.sample([str(int)+" " for int in range(lenght)],int(lenght)))
    clave_numeros = ''.join([str(int)+" " for int in range(lenght)])



    return clave, lenght, clave_numeros



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
        if character.isdigit() or character ==' ':
            key_numbers += character
    key_as_list_of_numbers = list(map(int, key_numbers.split()))
    
    return key_numbers, key_as_list_of_numbers