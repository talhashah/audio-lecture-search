# 🎧 Semantic Search in Audio Transcripts
This project is a full-stack web application that enables **Retrieval-Augmented Generation (RAG)** for transcribed audio content. It leverages **vector embeddings** and **LLMs** (e.g., DeepSeek, OpenAI, or any model you can run on Ollama) to provide **contextually relevant** search and responses.  

📝 For those exploring RAG-based applications, I highly recommend experimenting with different embedding models and fine-tuning various LLMs on [Ollama](https://ollama.com/) to gain a deeper understanding of retrieval, ranking, and generation processes.

---
> ⚠️ **Note:** This app is currently under active development and is not production-ready. However, it is fully functional and delivers high-quality context-aware AI responses, as demonstrated in the example screenshot below. Use it for testing, experimentation, or local demos.
---


## 💡 Objective: Making Sacred Learning Center's Weekly Talks Searchable & Accessible 

<div style="background-color:#f9f9f9; padding:15px; border-radius:8px; border-left:5px solid #4A90E2;">

### **Background**  
Sacred Learning Center is dedicated to fostering spiritual growth within the community. As part of this mission, the mosque holds a weekly gathering centered on the remembrance of Allah, Most High. Each session begins with a thought-provoking talk designed to deepen attendees' connection with Allah and further their spiritual development. 

### **Current Challenge**  
Over the years, approximately **500 talks** have been recorded and published on the mosque's website. However, there is currently no efficient way to search within them or navigate directly to specific topics. This limitation makes it difficult for users to find relevant discussions and engage meaningfully with past sessions.  

### **Project Vision**  
This initiative aims to make Sacred Learning Center’s extensive collection of weekly talks more accessible and interactive by implementing an AI-powered retrieval system. Utilizing advanced AI techniques, including Retrieval-Augmented Generation (RAG), the project will:  

  - ✅ **Enable searchability** within recorded talks through structured transcripts and topic indexing.  
  - ✅ **Provide AI-driven responses** rooted in the wisdom shared in the weekly sessions, allowing users to ask questions and receive contextually relevant answers.  

By leveraging AI-powered solutions, this project seeks to **enhance the accessibility** of these discussions, allowing individuals to explore and engage with them more effectively.  

 - 🔗 **Learn more about Sacred Learning Center:** [Sacred Learning Center - Home Page](https://www.sacredlearning.org)  
 - 🔗 **Access weekly talks:** [Sacred Learning Center - Recorded Sessions](https://www.sacredlearning.org/talks/)  


### **Examples:**  
**🖼️  Example 1: Context-aware AI response:** The right side utilizes the app to generate responses rooted in the recorded talks, while the left side relies on a standard LLM response without contextual integration.
![Screenshot from 2025-05-02 12-59-38](https://github.com/user-attachments/assets/0374d6a7-b844-43c2-9cbb-9439ad2c4003)

**🖼️  Example 2: Semantic Search (No LLM ingeration):** Vector similarity search.
![Screenshot from 2025-05-02 13-40-18](https://github.com/user-attachments/assets/5ba02fcf-9308-48fd-a451-49cf328c4d6a)

---

## 🔧 Tech Stack

- **Frontend**: [React + Vite](https://react.dev/learn/build-a-react-app-from-scratch#vite)  
- **Alternate Frontend**: [Gradio](https://www.gradio.app/docs)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Embeddings**: [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  
- **Vector Store**: [ChromaDB](https://docs.trychroma.com/docs/overview/introduction)  
- **LLM**: Various models showcased in the code, including OpenAI, DeepSeek, and Qwen running locally on Ollama, integrated via [LangChain](https://www.langchain.com/).
- **Transcription**: Whisper AI (preprocessed)  - See my [audio-scribe](https://github.com/talhashah/audio-scribe) project 

---

## 📥📤 Architecture Flow Diagram

![image](https://github.com/user-attachments/assets/f855a289-9b48-4336-af10-a7813d1a3b34)

---
## 🚀 Running the Application

### Backend API
- Run backend API from the frontend folder:
  `uvicorn main:app --reload`

### Frontend Apps
- Run frontend app from the frontend folder:
  `npm run dev.`

- Run alternate frontend app from the backend folder:
  `python rag.py`

---

## 📜 License

MIT License - Free for personal/commercial use

