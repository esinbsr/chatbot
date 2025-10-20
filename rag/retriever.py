from langchain_chroma import Chroma
from rag.get_embedding_function import get_embedding_function

def get_retriever(persist_directory="chroma"):
    embedding_fn = get_embedding_function()
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_fn)
    retriever = db.as_retriever()
    return retriever
