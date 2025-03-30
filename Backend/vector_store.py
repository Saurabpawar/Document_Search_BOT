# vector_store.py
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import numpy as np

VECTOR_DB_PATH = "D:/project/document_search_bot/L2_POC_RAG/New_folder/chroma_store"
embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
vector_store = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)

def add_texts_to_vector_store(text_chunks, metadatas):
    vector_store.add_texts(text_chunks, metadatas=metadatas)

def search_query_in_vector_store(query, k):
    """
    Perform similarity search in Chroma and return the top k results.
    """
    # Perform the initial similarity search to retrieve k documents
    search_results = vector_store.similarity_search(query, k=k)
    
    return search_results

