import chromadb
from chromadb.config import Settings

def get_chroma_client():
    return chromadb.PersistentClient(path="./chroma_db")

def get_or_create_collection(client, name="audio_index"):
    return client.get_or_create_collection(name=name)
