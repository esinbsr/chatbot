from core import ChatbotCore
from router import router, agents 
from agents.agent_ia_pme import identify_use_case
from agents.agent_cv import improve_cv
from agents.agent_test import agent_test_function

# Initialisation du bot
bot = ChatbotCore()
context = ""

# Dictionnaire des fonctions d'agents
AGENTS_FUNCTIONS = {
    "ia_pme": identify_use_case,
    "cv": improve_cv,
    "agent_test": agent_test_function
}

# Boucle principale
print("Bienvenue ! Tape 'exit' pour quitter.")

while True:
    user_input = input("Toi : ")
    if user_input.lower() == "exit":
        print("À bientôt !")
        break

    # Le router renvoie l'ID de l'agent
    agent_id = router(user_input)

    # Récupération des infos de l'agent depuis YAML
    agent_info = next(a for a in agents if a["id"] == agent_id)

    # Récupération de la fonction correspondante
    agent_function = AGENTS_FUNCTIONS.get(agent_id, lambda text, **kwargs: bot.ask(text, context))

    # Appel de l'agent avec le contexte et les infos
    response = agent_function(bot, user_input, context=context, agent_info=agent_info)


    # Affichage et mise à jour du contexte
    print("Bot:", response)
    context += f"\nUser: {user_input}\nAI: {response}"
