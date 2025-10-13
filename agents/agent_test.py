from utils.config import load_config

# Paramètres destinés aux requêtes de test ou de garde-fous.
AGENT_CONFIG = load_config()["agents"]["test"]


def test(bot_core, user_input, context=""):
    """Répond aux requêtes de test en appliquant les règles définies."""
    prompt = (
        f"Rôle : {AGENT_CONFIG['role']}\n"
        f"Objectif : {AGENT_CONFIG['goal']}\n"
        f"Style : {AGENT_CONFIG['style']}\n"
        f"Prompt : {user_input}\n"
        "Réponse :"
    )
    return bot_core.ask(prompt, context=context)
