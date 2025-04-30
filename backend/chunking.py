from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_transcript(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_text(text)
