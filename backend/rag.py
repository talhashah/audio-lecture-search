import re
import ollama
import gradio as gr
import os
import requests
import random
import openai
from openai import OpenAI
from typing import Optional
from embeddings import get_embedding_model
from db import get_chroma_client, get_or_create_collection


embedding_model = get_embedding_model()
chroma_client = get_chroma_client()
collection = get_or_create_collection(chroma_client, name="audio_index")

#region LLM functions
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = ollama.chat(
        model="qwen2.5:3b", # "deepseek-r1:1.5b" or "deepseek-r1:7b or "deepseek-r1:8b" or "llama3:8b" or "qwen2.5:3b"
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    response_content = response["message"]["content"]
    # Remove content between <think> and </think> tags to remove thinking output
    final_answer = re.sub(r"<think>.*?</think>", "", response_content, flags=re.DOTALL).strip()
    return final_answer

def deepseek_llm(question, context, model="deepseek-chat", api_key=None):
    """
    Calls the DeepSeek API with a question and context
    
    Args:
        question (str): The question to ask
        context (str): Relevant context for the question
        model (str): Model to use (default: "deepseek-chat")
        api_key (str): Your DeepSeek API key (if required)
    
    Returns:
        str: The model's response with <think> tags removed
    """
    # Format the prompt
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    
    # API endpoint (check for the latest public API URL)
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # Prepare payload
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": formatted_prompt}
        ],
        "temperature": 0.7,  # Adjust as needed
        "max_tokens": 2000   # Adjust as needed
    }
    
    try:
        # Make the API request
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        
        # Extract the response content
        response_content = response.json()["choices"][0]["message"]["content"]
        
        # Remove content between <think> and </think> tags
        final_answer = re.sub(r"<think>.*?</think>", "", response_content, flags=re.DOTALL).strip()
        
        return final_answer
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return f"Error: {str(e)}"

def openai_llm(
    question: str,
    context: str,
    model: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,  # For Azure or custom endpoints
    temperature: float = 0.7,
    max_tokens: int = 1000,
    system_message: Optional[str] = None
) -> str:
    """
    Calls the OpenAI API with a question and context using the new v1.0+ client
    
    Args:
        question: The question to ask
        context: Relevant context for the question
        model: Model to use (default: "gpt-3.5-turbo")
        api_key: Your API key
        base_url: Custom endpoint URL (for Azure or other)
        temperature: Creativity parameter (0-2)
        max_tokens: Maximum length of response
        system_message: Optional system prompt
    
    Returns:
        The model's response with <think> tags removed
    """
    # Initialize the client
    client = OpenAI(
        api_key=api_key or None,  # Falls back to OPENAI_API_KEY env var
        base_url=base_url or None  # None uses default OpenAI endpoint
    )
    
    # Format the prompt
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    
    # Prepare messages
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": formatted_prompt})
    
    try:
        # Make the API request
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Extract the response content
        response_content = response.choices[0].message.content
        
        # Remove content between <think> and </think> tags
        final_answer = re.sub(r"<think>.*?</think>", "", response_content, flags=re.DOTALL).strip()
        
        return final_answer
    
    except Exception as e:
        print(f"OpenAI API request failed: {e}")
        return f"Error: {str(e)}"
#endregion

def rag_chain(question):
    query_embedding = embedding_model.embed_query(question)
    print("Query: " + question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        include=["documents", "metadatas"]
    )
    docs = results["documents"][0]
    formatted_content = "\n\n".join(docs)
    return ollama_llm(question, formatted_content)
    #rturn openai_llm(question, formatted_content, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
    #return deepseek_llm(question, formatted_content, api_key=os.getenv("DEEPSEEK_API_KEY"))

def ask_question(question):
    return rag_chain(question)
    # return random.choice(['yes', 'no', 'maybe'])

interface = gr.Interface(
    fn=ask_question,
    inputs=[
        gr.Textbox(label="Ask a question"),
    ],
    outputs="text",
    title="Ask questions about SLC Talks",
    description="Use AI to answer your questions about the uploaded SLC Talks.",
)

interface.launch()