from utils.config import load_config

# Paramètres spécialisés pour l'agent CV.
AGENT_CONFIG = load_config()["agents"]["cv"]


def improve_text(bot_core, user_input, purpose="CV", context=""):
    """Retourne une version améliorée du texte fourni pour un usage professionnel."""
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
            f"Document : {purpose}",
            f"Texte : {user_input}",
            "Version améliorée :",
        ]
    )
    prompt = "\n".join(prompt_parts)

    response = bot_core.ask(prompt, context=context)
    return response
