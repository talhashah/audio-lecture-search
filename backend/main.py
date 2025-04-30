from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from embeddings import get_embedding_model
from db import get_chroma_client, get_or_create_collection
from typing import List

app = FastAPI()

# Enable frontend calls (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_model = get_embedding_model()
chroma_client = get_chroma_client()
collection = get_or_create_collection(chroma_client, name="audio_index")
# raw_collection = chroma_client.get()

# @app.get("/search")
# def search(query: str):
#     query_embedding = embedding_model.embed_query(query)
#     print("Query is " + query)
#     print(query_embedding)
#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=5
#     )
#     # results = raw_collection
#     print("Collection has " + str(collection.count()) + " documents")
#     return {"results": results}

@app.get("/search")
def search(query: str):
    results = collection.query(
        query_texts=[query],
        n_results=10,
        include=["documents", "metadatas"]
    )
    return {"results": results}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug-count")
def debug_count():
    return {"document_count": collection.count()}