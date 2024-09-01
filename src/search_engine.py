import os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def coseno_similitud(textos, query, verbose, nuevos_valores):
    # Crear el vectorizador TF-IDF
    vectorizador = TfidfVectorizer(lowercase=True, stop_words=None, max_df=1.0, min_df=1)
    
    # Transformar los textos en vectores TF-IDF
    vectores_tfidf_array = vectorizador.fit_transform(textos).toarray()
    
    # Obtener el vocabulario del vectorizador
    vocabulario = vectorizador.vocabulary_
    
    palabras_query = query.split(" ")
    
    i = 0
    # Modificar los valores de TF-IDF del vector de la query
    for palabra, nuevo_valor in zip(palabras_query, nuevos_valores):
        if palabra in vocabulario:
            indice = vocabulario[palabra]
            if verbose:
                vectores_tfidf_array[-1][indice] = nuevo_valor
            else:
                nuevos_valores[i] = round(vectores_tfidf_array[-1][indice], 2)
            i += 1
    
    # Calcular la similitud del coseno
    similitud = cosine_similarity(vectores_tfidf_array)
    
    return similitud, nuevos_valores

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

def search(query, verbose, values):
        
    # Procesar la query
    processed_query = process_query(query)
    
    # Leer los documentos
    documents = read_documents_from_folder()
    
    # Unir los documentos con la query en una sola lista
    texts = list(documents.values())
    texts.append(processed_query)
    
    # Calcular el TF-IDF de cada documento y de la query
    matrix, final_values = coseno_similitud(texts, query, verbose, values)
    
    # Mapear los documentos con sus TF-IDF
    doc_tfidf = dict(zip(documents.keys(), matrix[-1][:-1]))
    
    # Ordenar el diccionario por los valores de mayor a menor
    diccionario_ordenado = dict(sorted(doc_tfidf.items(), key=lambda item: item[1], reverse=True))
    
    # Devolver los 10 primeros elementos
    imprimir = dict(list(diccionario_ordenado.items())[:10])
    
    return imprimir.keys(), final_values