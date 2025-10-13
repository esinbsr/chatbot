from utils.config import load_config

# Paramètres spécialisés pour l'agent CV.
AGENT_CONFIG = load_config()["agents"]["cv"]


def improve_text(bot_core, user_input, purpose="CV", context=""):
    """Retourne une version améliorée du texte fourni pour un usage professionnel."""
    prompt = (
        f"Rôle : {AGENT_CONFIG['role']}\n"
        f"Objectif : {AGENT_CONFIG['goal']}\n"
        f"Style : {AGENT_CONFIG['style']}\n"
        f"Document : {purpose}\n"
        f"Texte : {user_input}\n"
        "Version améliorée :"
    )

    response = bot_core.ask(prompt, context=context)
    return response
