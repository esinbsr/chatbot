from typing import Sequence

from utils.config import load_config

# Paramètres pour l'agent spécialisé en mobilité et relocalisation.
AGENT_CONFIG = load_config()["agents"]["reloc"]


def handle_relocation(bot_core, user_input: str, context: str = "") -> str:
    """Fournit un accompagnement sur les politiques de mobilité et relocalisation."""
    legifrance_keywords: Sequence[str] | None = AGENT_CONFIG.get("legifrance_keywords")
    references = bot_core.get_legifrance_references(user_input, legifrance_keywords)
    references_block = bot_core.format_legifrance_block(references)
    if not references_block:
        references_block = "Références Legifrance : Aucune référence disponible pour cette requête."

    prompt_parts = [
        f"Rôle : {AGENT_CONFIG['role']}",
        f"Objectif : {AGENT_CONFIG['goal']}",
        f"Style : {AGENT_CONFIG['style']}",
        references_block,
        "Consigne : Cite explicitement les références ci-dessus ou précise clairement qu'elles sont indisponibles.",
        f"Demande : {user_input}",
        "Réponse :",
    ]
    prompt = "\n".join(prompt_parts)
    return bot_core.ask(prompt, context=context)
