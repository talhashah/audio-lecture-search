# 🎧 Semantic Search in Audio Transcripts

This project is a full-stack web application that allows users to perform **semantic search** across transcribed audio content using **vector embeddings** and **LLMs** (e.g., DeepSeek or OpenAI).

> ⚠️ **Note:** This app is currently under active development and is **not production-ready**. Use for testing, experimentation, or local demos only.

## 🔧 Tech Stack

- **Frontend**: React + Vite
- **Backend**: FastAPI
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store**: ChromaDB
- **LLM**: DeepSeek (via LangChain)
- **Transcription**: Whisper AI (preprocessed)

---

## Run the app

- Run backend API
  `uvicorn main:app --reload`

- Run frontend API
  `npm run dev.`
