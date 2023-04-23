"""
Cree una aplicación que “indexe” los siguientes 5 documentos. 
Debe formar una colección con todas las palabras, asegúrese de eliminar las stop-words. 
La aplicación debe leer los documentos .PDF previamente descargados a una ubicación del disco rígido 
y armar un fichero invertido con frecuencia y por separado un fichero invertido posicional. 
Con la última representación, genere 4 consultas distintas y muestre los resultados.

"""

import os
import fitz


#Consigue la ruta donde se encuentran almacenados los documentos PDFs

ruta_directorio = r"..\TPN1" # Reemplaza con la ruta de tu directorio de PDFs
lista_archivos = os.listdir(ruta_directorio)
lista_archivos_pdf = [archivo for archivo in lista_archivos if archivo.endswith('.pdf')]



#Devuelve una lista con todas las lineas del archivo. Sin duda comoda y sencilla de implementar:

with open("stopwords.txt", "r") as stopwords:
   listastopword = [linea.rstrip() for linea in stopwords]

###################################################

def eliminarstopwords(texto, stopwords):
    # Eliminar acentos de las stop words
    stopwords_sin_acentos = [eliminar_acentos(stopword) for stopword in stopwords]
    # Eliminar las stop words del texto
    palabras = texto.split()
    palabras_sin_stopwords = [palabra for palabra in palabras if palabra.lower() not in stopwords_sin_acentos]
    # Unir las palabras sin stopwords en una sola cadena de texto
    texto_sin_stopwords = ' '.join(palabras_sin_stopwords)
    return texto_sin_stopwords


import re

def limpiar_texto(texto):
    # Convertir todo el texto en minúsculas
    texto = texto.lower()
    
    # Eliminar números y puntuaciones
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = re.sub(r'\d+', '', texto)
    
    # Eliminar espacios en blanco adicionales
    texto = re.sub(r'\s+', ' ', texto).strip()
    texto=eliminar_acentos(texto)



    return texto


##################
import unicodedata

def eliminar_acentos(cadena):
    #Función que recibe una cadena de texto y retorna la misma cadena sin acentos.
    return ''.join(c for c in unicodedata.normalize('NFD', cadena) if unicodedata.category(c) != 'Mn')

##################


# Leer cada uno de los PDFs

def leer_pdf(nombre_archivo,contenido):
    
    with fitz.open(nombre_archivo) as doc:
        for pagina in doc:
            contenido += pagina.get_text()
        
    # llama a la funcion para eliminar stopwords
    contenido= eliminarstopwords(contenido,listastopword)

    # llama a la funcion para limpiar el texto
    contenido=limpiar_texto(contenido)

    contenido = contenido.split()

    return contenido

####################################################################

# Aqui guarda los resultado en un archivo de texto

def guardar_en_archivo(nombre_archivo, texto):
    with open(nombre_archivo, "wb") as archivo:
        archivo.write("Palabras del documento ".encode("utf-8")+ nombre_archivo.encode("utf-8") + '\n'.encode("utf-8")+ '\n'.encode("utf-8"))
        archivo.write(texto.encode("utf-8"))

####################################################


def crear_fichero_invertido(docs):
    # Crear un diccionario que contenga todas las palabras en los documentos
    dictionary = {}
    for doc in docs:
        for word in doc.split():
            if word not in dictionary:
                dictionary[word] = []

    # Asociar cada palabra con una lista de documentos que la contienen y su frecuencia de aparición en cada documento
    for i, doc in enumerate(docs):
        for word in doc.split():
            count = doc.count(word)
            if any(i+1 == d[0] for d in dictionary[word]):
                continue
            dictionary[word].append((i+1, count))

    # Crear el diccionario con la información de frecuencia de cada palabra en cada documento
    frecuencias = {}
    for word in dictionary:
        for doc in dictionary[word]:
            if word not in frecuencias:
                frecuencias[word] = []
            frecuencias[word].append((f'documento {doc[0]}', f'frecuencia {doc[1]}'))

    # Devolver el archivo invertido con frecuencia
    return frecuencias

def escribir_fichero_invertido(inverted_index, filename):
    # Abrir el archivo en modo escritura
    with open(filename, "w", encoding="utf-8") as f:
        # Escribir cada palabra seguida de sus ocurrencias en los documentos
        for word in inverted_index:
            # Escribir la palabra
            f.write(word + " ")
            # Escribir cada documento y su frecuencia
            for doc, freq in inverted_index[word]:
                f.write(str(doc) + ":" + str(freq) + " ")
            # Escribir un salto de línea para pasar a la siguiente palabra
            f.write("\n")

######################################

def crear_fichero_invertido_posicional(docs):
    # Crear un diccionario que contenga todas las palabras en los documentos
    dictionary = {}
    for doc_id, doc in enumerate(docs, start=1):
        for position, word in enumerate(doc.split(), start=1):
            if word not in dictionary:
                dictionary[word] = []
            #dictionary[word].append(("documento " + str(doc_id), "posicion " + str(position)))
            dictionary[word].append((doc_id, position))
    
    # Devolver el archivo invertido posicional
    return dictionary



def eliminar_tuplas_repetidas(dictionary):
    for key, value in dictionary.items():
        dictionary[key] = list(set(value))
    return dictionary

def ordenar_diccionario(diccionario):
    for key in diccionario:
        diccionario[key].sort(key=lambda tup: tup[0])
    return diccionario

"""
def buscar_adyacentes(palabra1, palabra2, rango_adyacencia, indice_invertido):
    # Buscar las listas de posiciones de cada palabra en el índice invertido
    posiciones_palabra1 = indice_invertido.get(palabra1, [])
    posiciones_palabra2 = indice_invertido.get(palabra2, [])

    # Verificar si alguna posición de palabra1 está adyacente a alguna posición de palabra2
    for pos1 in posiciones_palabra1:
        for pos2 in posiciones_palabra2:
            #if abs(pos1[1] - pos2[1]) <= rango_adyacencia:  # Convertir tuplas a enteros
            if pos2[0] == pos1[0] and abs(pos1[1] - pos2[1]) <= rango_adyacencia:
                return True

    # Si no se encontró ninguna adyacencia, retornar False
    return False
"""
def buscar_adyacentes(palabra_1, palabra_2, fichero_invertido_posicional):
    # Obtener la lista de ocurrencias de ambas palabras en el archivo invertido posicional
    ocurrencias_palabra_1 = fichero_invertido_posicional.get(palabra_1, [])
    ocurrencias_palabra_2 = fichero_invertido_posicional.get(palabra_2, [])

    # Inicializar la lista de adyacencias encontradas
    adyacencias_encontradas = []

    # Recorrer todas las ocurrencias de la primera palabra
    for ocurrencia_palabra_1 in ocurrencias_palabra_1:
        documento_palabra_1, posicion_palabra_1 = ocurrencia_palabra_1

        # Buscar ocurrencias de la segunda palabra en el mismo documento y cercanas a la primera palabra
        for ocurrencia_palabra_2 in ocurrencias_palabra_2:
            documento_palabra_2, posicion_palabra_2 = ocurrencia_palabra_2
            if documento_palabra_1 == documento_palabra_2 and abs(posicion_palabra_1 - posicion_palabra_2) <= 10:
                adyacencias_encontradas.append((documento_palabra_1, posicion_palabra_1, posicion_palabra_2))

    # Devolver la lista de adyacencias encontradas
    return adyacencias_encontradas


############################
#Borrar pantalla
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
############################






############################################33
documentos = []
cont_aux=0
contenido=''

for archivo in lista_archivos_pdf:
    # Leer el archivo PDF de la lista de PDFs
    texto_documentos = leer_pdf(archivo,contenido)

    # Convertir la lista de cadenas de texto en una única cadena de texto
    texto_completo = "\n".join(texto_documentos)
    documentos.append(texto_completo)

    #Aqui esta creando el fichero invertido con frecuencias
    fichero_invertido = crear_fichero_invertido(documentos)
    
    """
    # Esta seccion es opcional
    #Solo permite guardar por separado cada documento con la lista de palabras extraidas
    nombre_doc = "Doc0" + str(cont_aux+1)+".txt"
    guardar_en_archivo(nombre_doc, texto_completo)    
    cont_aux += 1
    ##########################
    """

#Eliminas tuplas repetidas del diccionario completo
eliminar_tuplas_repetidas(fichero_invertido)
#Es necesario ordenarlas
ordenar_diccionario(fichero_invertido)
# Y se guarda en un archivo de texto
escribir_fichero_invertido(fichero_invertido,"Fichero_Invertido_Completo.txt")


###############
#Crea el fichero invertido posicional
fichero_invertido_posicional = crear_fichero_invertido_posicional(documentos)
escribir_fichero_invertido(fichero_invertido_posicional, "Fichero_Invertido_Posicional.txt")
###################


################


while True:
    clear_screen()
    print("Sistema de recuperacion de Informacion..."+"\n")
    print("1. Buscar adyacencia entre palabras")
    print("2. Buscar que tan cerca esta una palabra de otra")
    print("3. Opción 3")
    print("4. Opción 3")
    print("5. Salir")
    opcion = input("Ingrese una opción: ")
    if opcion == "1":
        clear_screen()
        # Código para la opción 1
        print("Se va a buscar si existe adyacencia entre dos palabras...")
        palabra_1 = input("Ingrese la primer palabra: ")
        palabra_2 = input("Ingrese la segunda palabra: ")
        encontrado=buscar_adyacentes(palabra_1, palabra_2, fichero_invertido_posicional)
        if encontrado:
            print(f"Se encontró al menos una adyacencia entre '{palabra_1}' y '{palabra_2}'")
            input("Presione enter para continuar...")
        else:
            print(f"No se encontraron adyacencias entre '{palabra_1}' y '{palabra_2}'")
            input("Presione enter para continuar...")

        pass
    elif opcion == "2":
        clear_screen()
        # Código para la opción 2
        pass
    elif opcion == "3":
        clear_screen()
        # Código para la opción 3
        pass
    elif opcion == "4":
        clear_screen()
        # Código para la opción 3
        pass
    elif opcion == "5":
        clear_screen()
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida, por favor intente de nuevo.")
