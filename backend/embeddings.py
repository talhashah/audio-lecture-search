from langchain_huggingface import HuggingFaceEmbeddings

# def get_embedding_model():
#     model_name = "intfloat/multilingual-e5-base"
#     return HuggingFaceEmbeddings(model_name=model_name)

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )