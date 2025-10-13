from rag.retriever import get_retriever
from langchain.chains import RetrievalQA
from chatbot.core import ChatbotCore

bot_core = ChatbotCore()

retriever = get_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=bot_core.llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

def help_integr(user_input, purpose='Doc'):
    
    rag_result = qa_chain.invoke({"query": user_input})
    context = rag_result["result"]

    prompt = f"""
    Tu es un expert RH. Ton rôle est d’aider à créer et améliorer des documents d’intégration,
    listes de contrôle et tâches pour les nouvelles recrues selon leur rôle.

    Type de document : {purpose}

    Contexte extrait des documents RH internes :
    {context}

    Texte à améliorer ou générer :
    {user_input}

    Version améliorée :
    """

    return bot_core.ask(prompt)
