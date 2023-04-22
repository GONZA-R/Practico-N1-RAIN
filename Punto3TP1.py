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

#################################
# funcion para eliminar stop word
def eliminarstopwords(texto,stopwords):
    return ' '.join([word for word in texto.split(' ') if word not in stopwords])

##########################################



import re

def limpiar_texto(texto):
    # Convertir todo el texto en minúsculas
    texto = texto.lower()
    
    # Eliminar números y puntuaciones
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = re.sub(r'\d+', '', texto)
    
    # Eliminar espacios en blanco adicionales
    texto = re.sub(r'\s+', ' ', texto).strip()


    return texto


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
            dictionary[word].append(("documento " + str(doc_id), "posicion " + str(position)))

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
    

    # Esta seccion es opcional
    #Solo permite guardar por separado cada documento con la lista de palabras extraidas
    nombre_doc = "Doc0" + str(cont_aux+1)+".txt"
    guardar_en_archivo(nombre_doc, texto_completo)    
    cont_aux += 1
    ##########################

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

