from typing import Sequence

from utils.config import load_config

# Paramètres pour l'agent dédié à l'onboarding des collaborateurs.
AGENT_CONFIG = load_config()["agents"]["onboarding"]


def handle_onboarding(bot_core, user_input: str, context: str = "") -> str:
    """Produit des recommandations d'onboarding en rappelant le message clé."""
    legifrance_keywords: Sequence[str] | None = AGENT_CONFIG.get("legifrance_keywords")
    references = bot_core.get_legifrance_references(user_input, legifrance_keywords)
    references_block = bot_core.format_legifrance_block(references)

    prompt_parts = [
        f"Rôle : {AGENT_CONFIG['role']}",
        f"Objectif : {AGENT_CONFIG['goal']}",
        f"Style : {AGENT_CONFIG['style']}",
        f"Message clé : {AGENT_CONFIG['key_message']}",
    ]
    if references_block:
        prompt_parts.append(references_block)
    prompt_parts.extend(
        [
            f"Demande : {user_input}",
            "Réponse :",
        ]
    )
    prompt = "\n".join(prompt_parts)
    return bot_core.ask(prompt, context=context)
