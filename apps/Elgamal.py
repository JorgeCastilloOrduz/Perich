from operator import truediv
import random
import math
import re
import pandas as pd
import numpy as np
from sympy import *
from random import randint

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
df = pd.read_csv('apps/static/files/primos-3-mod-4.csv')
df_aux = df.head(600)
df_short = df_aux.tail(475)

def main():
    df3m4= pd.DataFrame(columns=['num_primo'])
    for index, row in df.iterrows():   
        if prime3mod4(row['num_primo']):
            df2 = pd.DataFrame({'num_primo':[int(row['num_primo'])]})
            df3m4 = pd.concat([df3m4, df2], ignore_index = True, axis = 0)
    df3m4.to_csv('apps/static/files/primos-3-mod-4.csv')

def input_to_numbers(input):
    input = input.upper()
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

def isCoprime(num1,num2): 
    hcf=0
    mn = min(num1, num2) 
    for i in range(1, mn+1): 
        if num1%i==0 and num2%i==0:
            hcf = i 
    if hcf == 1: 
        return True
    else: 
        return False

def prime3mod4(num):
    num_i = int(num)
    if (num_i-3)%4==0:
        return True
    else:
        return False
        
def modInverse(a, m):
    m0 = m
    y = 0
    x = 1
 
    if (m == 1):
        return 0
 
    while (a > 1):
 
        # q is quotient
        q = a // m
 
        t = m
 
        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y
 
        # Update x and y
        y = x - q * y
        x = t
 
    # Make x positive
    if (x < 0):
        x = x + m0
 
    return x


def code(texto_claro_cifrar,clave_cifrar_p,clave_cifrar_alpha,clave_cifrar_a,clave_cifrar_m):
    texto_claro_cifrar_clean = clean_input(texto_claro_cifrar).lower()
    lenght=2
    if len(texto_claro_cifrar_clean)%lenght!=0:
        for i in range(lenght-(len(texto_claro_cifrar_clean)%lenght)):
            texto_claro_cifrar_clean = texto_claro_cifrar_clean+"z"
    if not isprime(clave_cifrar_p):
        return texto_claro_cifrar_clean,"La clave p no es un número primo"
    if clave_cifrar_p<676:
        return texto_claro_cifrar_clean,"La clave p es muy pequeña"
    if not is_generator(clave_cifrar_alpha,clave_cifrar_p):
        return texto_claro_cifrar_clean,"La clave \u03b1 no es un generador para "+str(clave_cifrar_p)

    matriz_cifrada = []
    for i in range(0,len(texto_claro_cifrar_clean),lenght):
        beta = (clave_cifrar_alpha**clave_cifrar_a)%clave_cifrar_p
        string_aux = texto_claro_cifrar_clean[i:i+lenght]
        print("string_aux")
        print(string_aux)
        matriz_aux = input_to_numbers(string_aux) 
        print("matriz_aux")
        print(matriz_aux)
        num_aux = (matriz_aux[0]*26)+(matriz_aux[1])
        print("num_aux")
        print(num_aux)
        y_1 = (clave_cifrar_alpha**clave_cifrar_m)%clave_cifrar_p
        y_2 = ((beta**clave_cifrar_m)*num_aux)%clave_cifrar_p
        print("y1 y2")
        print("("+str(y_1)+","+str(y_2)+")")
        matriz_cifrada.append("("+str(y_1)+","+str(y_2)+")")
    print("matriz_cifrada")    
    print(matriz_cifrada)
    texto_cifrado = ""
    for i in matriz_cifrada:
        texto_cifrado = texto_cifrado+'-'+str(i)
    return texto_claro_cifrar_clean, texto_cifrado[1:]

def decode(texto_cifrado_cifrar,clave_descifrar_p,clave_descifrar_alpha,clave_descifrar_a):
    texto_cifrado_descifrar_clean = clean_text_elgamal(texto_cifrado_cifrar)
    texto_cifrado_descifrar_separado = texto_cifrado_descifrar_clean.split("-")
    texto_cifrado_ready = []
    print("texto_cifrado_descifrar_separado")
    print(texto_cifrado_descifrar_separado)

    print("texto_cifrado_descifrar_separado")
    print(texto_cifrado_descifrar_separado)

    for i in texto_cifrado_descifrar_separado:
        aux = i.replace("(","").replace(")","")
        aux_split = aux.split(",")
        print("aux_split")
        print(aux_split)
        texto_cifrado_ready.append(aux_split)

    print("texto_cifrado_ready")
    print(texto_cifrado_ready)

    if not isprime(clave_descifrar_p):
        return texto_cifrado_descifrar_clean,"La clave p no es un número primo."
    if clave_descifrar_p<676:
        return texto_cifrado_descifrar_clean,"La clave p es muy pequeña"
    if not is_generator(clave_descifrar_alpha,clave_descifrar_p):
        return texto_cifrado_descifrar_clean,"La clave \u03b1 no es un generador para "+str(clave_descifrar_p)
    
    texto_claro = ""
    for i in texto_cifrado_ready:
        y_1 = int(i[0])
        y_2 = int(i[1])

        aux1 = (y_1**clave_descifrar_a)%clave_descifrar_p
        inv_aux1 = modInverse(aux1,clave_descifrar_p)
        num_aux = (inv_aux1*y_2)%clave_descifrar_p

        print("num_aux")
        print(num_aux)
        matriz_cifrada_aux = [int((num_aux)/26), num_aux%26]


        print("matriz_cifrada_aux")
        print(matriz_cifrada_aux)

        texto_claro = texto_claro+input_to_letters(matriz_cifrada_aux) 
    
    return texto_cifrado_descifrar_clean, texto_claro.lower()

def generate_key():
    p=11
    while p<100 or p>10000:
        p = int(df_short.sample()['num_primo'].values[0])
    gens = generators(p)
    alpha = random.choice(gens)
    print(gens)
    a = randint(2,p-3)
    m = randint(2,p-3)

    return p,alpha,a,m

def generators(n):
    s = set(range(1, n))
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add((a**x) % n)
        if g == s:
            results.append(a)
            if len(results)>3:
                break
    return results

def is_generator(n,p):
    s = set(range(1, p))
    g = set()
    for x in s:
        g.add((n**x) % p)
    if g == s:
        return True        
    else:    
        return False

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


def clean_text_elgamal(key):
    key_numbers = ""
    for character in key:
        if character.isdigit() or character=='-' or character==',' or character=='(' or character==')':
            key_numbers += character
    if key_numbers=="":
        text = 0
    else:
        text = key_numbers
    return text

def gcdExtended(a, b): 
    # Base Case 
    if a == 0 :  
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y

