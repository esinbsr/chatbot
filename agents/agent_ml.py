from chatbot.core import ChatbotCore

bot_core = ChatbotCore()

def learn_ml(user_input): 
    prompt = f"""
    Tu es un expert en Machine Learning.
    Texte à répondre : {user_input} 
    """

    return bot_core.ask(prompt)