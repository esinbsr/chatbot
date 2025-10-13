from core import ChatbotCore
from router import Router
from agents.agent_cv import improve_text
from agents.agent_ml import learn_ml
from agents.agent_test import test
from utils.logger import get_logger

# Initialisation des composants principaux du chatbot.
bot = ChatbotCore()
router = Router("config/agents.yaml")
logger = get_logger("main")
context = ""

# Référencer chaque intention sur la fonction agent correspondante.
AGENTS_FUNCTIONS = {
    "cv": lambda text: improve_text(bot, text, context=context),
    "ml": lambda text: learn_ml(bot, text, context=context),
    "test": lambda text: test(text, context=context),
}

print("Bienvenue ! Tape 'exit' pour quitter.")

while True:
    user_input = input("Toi : ")
    if user_input.lower() == "exit":
        print("À bientôt !")
        break

    # Le routeur détermine quel agent doit répondre.
    agent_name = router.get_agent_for_input(user_input)
    logger.info("Intention choisie: %s", agent_name)

    agent_function = AGENTS_FUNCTIONS.get(agent_name, lambda x: bot.ask(x, context=context))

    try:
        response = agent_function(user_input)
        print("Bot:", response)
        context += f"\nUser: {user_input}\nAI: {response}"
        logger.info("Interaction stockée dans le contexte.")
    except Exception as e:
        logger.exception("Erreur lors du traitement de la requête.")
        print(f"[Erreur] Impossible de traiter la requête : {e}")
