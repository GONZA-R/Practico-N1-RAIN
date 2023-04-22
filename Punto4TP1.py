"""
El siguiente es un resumen que se encuentra construido con un índice invertido, 
se indica el tamaño del mismo y cada palabra posee entre corchetes la posición que ocupa dentro del texto. 
Cree una aplicación que permita recibir estos dos parámetros, el tamaño del índice y el índice invertido, 
y devuelva el resumen completo. Cree las estructuras de datos que considere necesario tanto para 
la re-construcción del texto como para el pasaje de parámetros.
"""

#Crear una función para leer el archivo de texto y convertirlo en un diccionario:
import ast

def leer_archivo(nombrearchivo):
    archivo=open(nombrearchivo).read()
    resultado=ast.literal_eval(archivo)
    return resultado

#Crear una función para crear la lista de tuplas a partir del diccionario:

def crear_tuplas(resultado, tamano_maximo_ingresado):
    cadena = []
    contador = 0
    for claves, valores in resultado.items():
        for valor in valores:
            cadena.append((valor, claves))
            contador += 1
            if contador >= tamano_maximo_ingresado:
                break
        if contador >= tamano_maximo_ingresado:
            break
    cadena = sorted(cadena)
    return cadena



#Crear una función para reconstruir el texto a partir de la lista de tuplas:
def reconstruir_texto(cadena):
    texto_tupla = cadena
    texto_tupla_ordenada = sorted(texto_tupla, key=lambda x: x[0])
    texto = ' '.join([palabra[1] for palabra in texto_tupla_ordenada])
    return texto

##################
import unicodedata

def eliminar_acentos(cadena):
    #Función que recibe una cadena de texto y retorna la misma cadena sin acentos.
    return ''.join(c for c in unicodedata.normalize('NFD', cadena) if unicodedata.category(c) != 'Mn')

##################3

#Crear una función para traducir el texto reconstruido al español:

from googletrans import Translator

def traducir_texto(texto):
    translator = Translator()
    traduccion = translator.translate(texto, dest="es")
    textotraducido=traduccion.text
    return textotraducido


#Finalmente, en la función principal, llamar a estas funciones para obtener el texto reconstruido y el texto traducido, y guardarlos en un archivo de texto:
nombrearchivo="TextoPunto4.txt"

resultado = leer_archivo(nombrearchivo)

############################################################
#Aqui defino el tamaño del indice a mostrar en el archivo de texto 
# y que haga las correspondientes validaciones del mismo

tamano_minimo = 0
tamano_maximo = 183

while True:
    tamano_maximo_ingresado = input("Ingrese el tamaño máximo del indice: ")
    try:
        tamano_maximo_ingresado = int(tamano_maximo_ingresado)
        if tamano_maximo_ingresado < tamano_minimo or tamano_maximo_ingresado > tamano_maximo:
            print("El valor ingresado debe estar entre", tamano_minimo, "y", tamano_maximo)
        else:
            break
    except ValueError:
        print("Debe ingresar un número entero.")

#############################################################


cadena = crear_tuplas(resultado,tamano_maximo_ingresado)
texto = reconstruir_texto(cadena)
textotraducido = traducir_texto(texto)
textotraducido=eliminar_acentos(textotraducido)


# Aqui guarda los resultado en un archivo de texto

with open("TextoReconstruido.txt", "w") as archivo:
    archivo.write("Texto Reconstruido" + '\n'+ '\n')
    archivo.write(texto + '\n'+ '\n')
    archivo.write("Texto Traducido al español" + '\n'+ '\n')
    archivo.write(textotraducido + '\n')


