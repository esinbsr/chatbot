from utils.config import load_config

# Paramètres destinés aux requêtes de test ou de garde-fous.
AGENT_CONFIG = load_config()["agents"]["test"]


def test(bot_core, user_input, context=""):
    """Répond aux requêtes de test en appliquant les règles définies."""
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
            f"Prompt : {user_input}",
            "Réponse :",
        ]
    )
    prompt = "\n".join(prompt_parts)
    return bot_core.ask(prompt, context=context)
