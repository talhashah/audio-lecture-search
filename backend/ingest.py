# backend/ingest.py
# This script is used to ingest transcripts into the vector database.
# One-time run to populate DB.

import os
from embeddings import get_embedding_model
from db import get_chroma_client, get_or_create_collection
from chunking import chunk_transcript

TRANSCRIPT_DIR = "data/transcripts"

embedding_model = get_embedding_model()
client = get_chroma_client()
collection = get_or_create_collection(client)

def ingest_transcripts():
    for filename in os.listdir(TRANSCRIPT_DIR):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(TRANSCRIPT_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            print(f"[WARN] Skipping empty file: {filename}")
            continue

        chunks = chunk_transcript(text)

        if not chunks:
            print(f"[WARN] No chunks created for: {filename}")
            continue

        print(f"[INFO] Ingesting {len(chunks)} chunks from {filename}...")

        embeddings = embedding_model.embed_documents(chunks)

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"{filename}_{i}" for i in range(len(chunks))],
            metadatas=[{"source": filename}] * len(chunks)
        )

    print("✅ Ingest complete.")
    print("📊 Total documents in collection:", collection.count())

if __name__ == "__main__":
    ingest_transcripts()
