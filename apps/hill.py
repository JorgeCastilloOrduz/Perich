import random
import numpy as np

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

def input_to_single_numbers(input):
    dict_values = {}
    dict_letters = {}
    index=0
    for i in abc:
        dict_values[index] = i
        dict_letters[i] = index
        index += 1
    input_as_list = []
    for k in input:
        input_as_list.append([dict_letters[k]])
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

def code(texto_claro_cifrar,clave_table,lenght):
    for i in range(lenght):        
        for j in range(lenght):
            clave_table[i][j] = clean_celda(clave_table[i][j])



    texto_claro_cifrar_clean = clean_input(texto_claro_cifrar)
    if len(texto_claro_cifrar_clean)%lenght!=0:
        for i in range(lenght-(len(texto_claro_cifrar_clean)%lenght)):
            texto_claro_cifrar_clean = texto_claro_cifrar_clean+"Z"

    matriz_cifrada = []
    for i in range(0,len(texto_claro_cifrar_clean),lenght):
        string_aux = texto_claro_cifrar_clean[i:i+lenght]
        matriz_aux = input_to_single_numbers(string_aux)
        A=np.array(np.array(matriz_aux)).reshape(1,lenght)
        B=np.array(clave_table).reshape(lenght,lenght)
        print("A")
        print(A)
        print("B")
        print(B)
        print(np.dot(A,B))
        for k in np.dot(A,B):
            for a in range(lenght):
                matriz_cifrada.append(k[a]%26)
                
        print("Matriz")
        print(matriz_cifrada)

    texto_cifrado = input_to_letters(matriz_cifrada)
    print("Texto cifrado: ", texto_cifrado )

    return texto_cifrado,texto_claro_cifrar_clean,clave_table,lenght


def decode(texto_cifrado, clave_table,lenght):
    
    for i in range(lenght):        
        for j in range(lenght):
            clave_table[i][j] = clean_celda(clave_table[i][j])


    texto_cifrado_descifrar_clean = clean_input(texto_cifrado)
    if len(texto_cifrado_descifrar_clean)%lenght!=0:
        for i in range(lenght-(len(texto_cifrado_descifrar_clean)%lenght)):
            texto_cifrado_descifrar_clean = texto_cifrado_descifrar_clean+"Z"

    matriz_descifrada = []
    for i in range(0,len(texto_cifrado_descifrar_clean),lenght):
        string_aux = texto_cifrado_descifrar_clean[i:i+lenght]
        matriz_aux = input_to_single_numbers(string_aux)
        A=np.array(np.array(matriz_aux)).reshape(1,lenght)
        B=np.array(clave_table).reshape(lenght,lenght)
        B_I = getMatrixInverse(B)
        test= np.dot(B,B_I)
        print("A")
        print(A)
        print("B")
        print(B)
        print("B_I")
        print(B_I)
        print("Matriz")
        print(np.dot(A,B_I))
        print("Test")
        print(test)
        for k in np.dot(A,B_I):
            for a in range(lenght):
                matriz_descifrada.append(k[a]%26)
                
        print("Matriz")
        print(matriz_descifrada)

    # texto_claro = input_to_letters(matriz_descifrada)
    texto_claro = "Este módulo aún está en construcción"
    print("Texto cifrado: ", texto_cifrado )
    print("clave")
    print(clave_table)
    return texto_claro,texto_cifrado_descifrar_clean,clave_table,lenght


def generate_key(size):
    clave=[]
    if size is None or size == "":
        lenght = random.randint(2, 10)
    else:
        largo=""
        for i in size:
            if i.isdigit():
                largo = largo+str(i)
        lenght = int(largo)
        if lenght>10:
            lenght = 10
        if lenght<2:
            lenght = 2

    for i in range(lenght):
        aux = []
        for j in range(lenght):
            aux.append(random.randint(0, 25))
        clave.append(aux)


    
    return clave, lenght


def generate_matrix(size):
    clave=[]
    if size is None or size == "":
        lenght = random.randint(2, 10)
    else:
        largo=""
        for i in size:
            if i.isdigit():
                largo = largo+str(i)
        lenght = int(largo)
        if lenght>10:
            lenght = 10
        if lenght<2:
            lenght = 2

    for i in range(lenght):
        aux = []
        for j in range(lenght):
            aux.append(0)
        clave.append(aux)


    
    return clave, lenght



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
    
    return key_numbers

def clean_celda(key):
    key_numbers = ""
    for character in key:
        if character.isdigit():
            key_numbers += character
    celda_int = int(key_numbers)
    if celda_int>25:
        celda_int = celda_int%26
        
    key_as_list_of_numbers = list(map(int, key_numbers.split()))
    
    return celda_int

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)%26
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors