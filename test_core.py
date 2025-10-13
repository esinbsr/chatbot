from core import ChatbotCore

bot = ChatbotCore()
context=''

while True:
    user_input = input("Toi: (Tape 'exit' pour quitter) ")
    if user_input.lower() == 'exit':
        break

    response = bot.ask(user_input, context)
    print('Bot : ', response)

    context += f"\nUser: {user_input}\nAI: {response}"