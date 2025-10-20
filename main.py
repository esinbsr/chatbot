from core import ChatbotCore
from router import router, agents
from agents.agent_ia_pme import identify_use_case
from agents.agent_cv import improve_cv
from agents.agent_legal import provide_legal_guidance

# Initialisation du bot
bot = ChatbotCore()
context = ""

# Dictionnaire des fonctions d'agents
AGENTS_FUNCTIONS = {
    "ia_pme": identify_use_case,
    "cv": improve_cv,
    "legal": provide_legal_guidance,
}

AGENTS_INFO = {agent["id"]: agent for agent in agents}


def generic_response(bot_core, user_input, context="", agent_info=None):
    """Fallback lorsqu'aucun agent spécifique n'est trouvé."""
    if agent_info:
        print(
            f"[Agent] Aucun handler dédié trouvé pour {agent_info['id']}, "
            "utilisation du cœur générique."
        )
    else:
        print("[Agent] Aucun agent correspondant, utilisation du cœur générique.")
    return bot_core.ask(user_input, context=context)


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
    agent_info = AGENTS_INFO.get(agent_id)
    if agent_info is None:
        response = generic_response(bot, user_input, context=context)
    else:
        # Récupération de la fonction correspondante
        agent_function = AGENTS_FUNCTIONS.get(agent_id, generic_response)
        response = agent_function(
            bot, user_input, context=context, agent_info=agent_info
        )

    # Affichage et mise à jour du contexte
    print("Bot:", response)
    context += f"\nUser: {user_input}\nAI: {response}"
