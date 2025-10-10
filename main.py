from chatbot.core import ChatbotCore
from agents.agent_cv import improve_text

bot = ChatbotCore()
context= ""

while True :
    print("Pour quitter, taper 'exit'")
    user_input = input('Toi : ')
    if user_input.lower() == 'exit':
        print('A bientôt !')
        break

    response = improve_text(user_input, purpose='CV')
    print("Bot: ", response)
    context += f":\nUser: {user_input}\nAI: {response}"