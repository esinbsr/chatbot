from langchain.document_loaders import PyPDFDirectoryLoader

def load_documents(data_path="data"):
    loader = PyPDFDirectoryLoader(data_path)
    documents = loader.load()
    return documents
