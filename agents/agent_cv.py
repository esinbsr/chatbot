"""
Agent spécialisé dans l'amélioration de CV, lettres de motivation et profils professionnels.
"""

import yaml

with open("config/agents.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
# Paramètres spécialisés pour l'agent CV.
AGENT_CONFIG = config["agents"]["cv"]


def improve_text(bot_core, user_input, purpose="CV", context=""):
    """Retourne une version améliorée du texte fourni pour un usage professionnel."""
    prompt = f"""
    Tu es {AGENT_CONFIG['role']}.
    Objectif : {AGENT_CONFIG['goal']}
    Style : {AGENT_CONFIG['style']}

    Type de document : {purpose}
    Texte à améliorer :
    {user_input}

    Version améliorée :
    """

    response = bot_core.ask(prompt, context=context)
    return response
