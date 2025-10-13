"""
Agent spécialisé en apprentissage automatique et intelligence artificielle.
"""

import yaml

with open("config/agents.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
AGENT_CONFIG = config["agents"]["ml"]

def learn_ml(bot_core, user_input, context=""):
    prompt = f"""
    Tu es {AGENT_CONFIG['role']}.
    Objectif : {AGENT_CONFIG['goal']}
    Style : {AGENT_CONFIG['style']}

    Question de l'utilisateur :
    {user_input}

    Réponse :
    """
    response = bot_core.ask(prompt,context=context)
    return response
