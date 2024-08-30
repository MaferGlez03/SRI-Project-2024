import math
import os
import numpy as np
import pickle
from collections import Counter
from nltk.stem import PorterStemmer
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def coseno_similitud(textos, query):
    # Crear el vectorizador TF-IDF
    vectorizador = TfidfVectorizer(lowercase=True, stop_words=None, max_df=1.0, min_df=1)
    
    # Transformar los textos en vectores TF-IDF
    vectores_tfidf = vectorizador.fit_transform(textos)
    
    # Transformar los textos en vectores TF-IDF
    vectores_tfidf_array = vectorizador.fit_transform(textos).toarray()
    
    # Obtener el vocabulario del vectorizador
    vocabulario = vectorizador.vocabulary_
    
    palabras_query, nuevos_valores = new_value(query)
    
    # Modificar los valores de TF-IDF del vector de la query
    for palabra, nuevo_valor in zip(palabras_query, nuevos_valores):
        if palabra in vocabulario:
            indice = vocabulario[palabra]
            vectores_tfidf_array[-1][indice] = nuevo_valor
    
    # Calcular la similitud del coseno
    similitud = cosine_similarity(vectores_tfidf_array)
    
    return similitud

def new_value(query):
    query_array = query.split(" ")
    values = np.zeros(len(query_array))
    i = 0
    for word in query_array:
        value_string = input(f"Valor del TF-IDF de {word}: ")
        value = float(value_string)
        # while value < 0 or value > 1:
        #     print("El valor tiene que estar entre 0 y 1.")
        #     value = input(f"Valor del TF-IDF de {word}: ")
        values[i] = value
        i += 1
    return query_array, values

# Función para leer documentos desde una carpeta
def read_documents_from_folder():
    documents = []
    # Obtener la ruta absoluta de la carpeta actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta absoluta a la carpeta 'data'
    folder_path = os.path.join(current_dir, 'data')
    
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

def process_query(query):
    tokens = word_tokenize(query)
    normal = [token.lower() for token in tokens]
    
    stop_words = set(stopwords.words('spanish'))
    normal = [word for word in normal if word not in stop_words]
    
    stemmer = PorterStemmer()
    stemming = [stemmer.stem(token) for token in tokens]
    
    return ' '.join(stemming)

def main():
    # Leer query
    query = input("Introduce tu busqueda: ")
    
    # Procesar la query
    processed_query = process_query(query)
    
    # Leer los documentos
    documents = read_documents_from_folder()
    
    # Unir los documentos con la query en una sola lista
    texts = list(documents.values())
    texts.append(processed_query)
    
    # Calcular el TF-IDF de cada documento y de la query
    matrix = coseno_similitud(texts, query)
    
    # Mapear los documentos con sus TF-IDF
    doc_tfidf = dict(zip(documents.keys(), matrix[-1][:-1]))
    
    # Ordenar el diccionario por los valores de mayor a menor
    diccionario_ordenado = dict(sorted(doc_tfidf.items(), key=lambda item: item[1], reverse=True))
    
    # Devolver los 10 primeros elementos
    imprimir = dict(list(diccionario_ordenado.items())[:10])
    
    print(f"Ha buscado: {processed_query}. Los resultados son:")
    for clave, valor in imprimir.items():
        print(f"{clave}: {valor}")

main()