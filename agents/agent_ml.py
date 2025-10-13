from utils.config import load_config

# Config dédiée aux réponses pédagogiques sur le machine learning.
AGENT_CONFIG = load_config()["agents"]["ml"]

def learn_ml(bot_core, user_input, context=""):
    """Explique un concept de machine learning en s'adaptant au ton configuré."""
    prompt = (
        f"Rôle : {AGENT_CONFIG['role']}\n"
        f"Objectif : {AGENT_CONFIG['goal']}\n"
        f"Style : {AGENT_CONFIG['style']}\n"
        f"Question : {user_input}\n"
        "Réponse :"
    )
    response = bot_core.ask(prompt, context=context)
    return response
