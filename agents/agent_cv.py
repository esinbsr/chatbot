from chatbot.core import ChatbotCore

bot_core = ChatbotCore()

def improve_text(user_input, purpose='CV'):

    prompt = f"""
    Tu es un expert RH. Améliore ce texte pour qu'il soit clair, concis et convaincant.
    Type de document : {purpose}
    Texte à améliorer : 
    {user_input}
    
    Version améliorée :
    """
    return bot_core.ask(prompt)