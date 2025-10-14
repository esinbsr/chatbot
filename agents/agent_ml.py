from utils.config import load_config

# Config dédiée aux réponses pédagogiques sur le machine learning.
AGENT_CONFIG = load_config()["agents"]["ml"]

def learn_ml(bot_core, user_input, context=""):
    """Explique un concept de machine learning en s'adaptant au ton configuré."""
    references = bot_core.get_legifrance_references(user_input)
    references_block = bot_core.format_legifrance_block(references)

    prompt_parts = [
        f"Rôle : {AGENT_CONFIG['role']}",
        f"Objectif : {AGENT_CONFIG['goal']}",
        f"Style : {AGENT_CONFIG['style']}",
    ]
    if references_block:
        prompt_parts.append(references_block)
    prompt_parts.extend(
        [
            f"Question : {user_input}",
            "Réponse :",
        ]
    )
    prompt = "\n".join(prompt_parts)
    response = bot_core.ask(prompt, context=context)
    return response
