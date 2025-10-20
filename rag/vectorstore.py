from langchain_chroma import Chroma
from rag.loader import load_documents
from rag.get_embedding_function import get_embedding_function
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

def add_to_chroma(chunks, persist_directory="chroma"):
    embedding_fn = get_embedding_function()
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_fn,
        persist_directory=persist_directory
    )

def build_vectorstore():
    print("📥 Chargement des documents...")
    documents = load_documents()
    print(f"✅ {len(documents)} documents chargés")

    print("✂️ Découpage des documents...")
    chunks = split_documents(documents)
    print(f"✅ {len(chunks)} chunks générés")

    print("📦 Indexation dans Chroma...")
    add_to_chroma(chunks)
    print("✅ Vector store créé avec succès dans 'chroma/'")

if __name__ == "__main__":
    build_vectorstore()

