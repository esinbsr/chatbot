import logging
import unicodedata

from mistralai.models.sdkerror import SDKError

from core import ChatbotCore
from router import Router
from agents.agent_cv import improve_text
from agents.agent_ml import learn_ml
from agents.agent_test import test
from agents.agent_legal import handle_legal_request
from agents.agent_onboarding import handle_onboarding
from agents.agent_reloc import handle_relocation
from utils.logger import get_logger

# Initialisation des composants principaux du chatbot.
bot = ChatbotCore()
router = Router("config/agents.yaml")
logger = get_logger("main")
context_history: list[str] = []

# Réduire le bruit des librairies externes dans la console.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("pylegifrance").setLevel(logging.WARNING)

# Référencer chaque intention sur la fonction agent correspondante.
AGENTS_FUNCTIONS = {
    "cv": lambda text, ctx: improve_text(bot, text, context=ctx),
    "ml": lambda text, ctx: learn_ml(bot, text, context=ctx),
    "test": lambda text, ctx: test(bot, text, context=ctx),
    "legal": lambda text, ctx: handle_legal_request(bot, text, context=ctx),
    "onboarding": lambda text, ctx: handle_onboarding(bot, text, context=ctx),
    "reloc": lambda text, ctx: handle_relocation(bot, text, context=ctx),
}

print("Bienvenue ! Tape 'exit' pour quitter.")

while True:
    user_input = input("Toi : ")
    if user_input.lower() == "exit":
        print("À bientôt !")
        break

    normalized_input = unicodedata.normalize("NFD", user_input).encode("ascii", "ignore").decode().lower()
    if "qui t a cree" in normalized_input or "qui ta cree" in normalized_input:
        response = "J'ai été créé par Esin, Valentin, Yasmine, Gautier et Silene."
        print("Bot:", response)
        context_history.append(f"User: {user_input}\nAI: {response}")
        logger.info("Réponse créateurs fournie sans routage.")
        continue

    # Conserve un historique limité pour alimenter les agents sans alourdir le prompt.
    current_context = "\n".join(context_history[-6:])

    # Le routeur détermine quel agent doit répondre.
    agent_name = router.get_agent_for_input(user_input)
    logger.info("Intention choisie: %s", agent_name)

    agent_function = AGENTS_FUNCTIONS.get(
        agent_name, lambda text, ctx: bot.ask(text, context=ctx)
    )

    try:
        response = agent_function(user_input, current_context)
        print("Bot:", response)
        context_history.append(f"User: {user_input}\nAI: {response}")
        logger.info("Interaction stockée dans le contexte.")
    except SDKError as exc:
        cooldown_msg = (
            "[Info] Service Mistral temporairement saturé (429). "
            "Patiente quelques secondes et réessaie."
        )
        print(cooldown_msg)
        logger.warning("Erreur Mistral 429 : %s", exc)
    except Exception as e:
        logger.exception("Erreur lors du traitement de la requête.")
        print(f"[Erreur] Impossible de traiter la requête : {e}")
