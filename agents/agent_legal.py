"""Agent légal s'appuyant sur Legifrance pour proposer des références fiables."""

from __future__ import annotations

from tools.legifrance import (
    fetch_legifrance_references,
    format_legifrance_block,
)


def provide_legal_guidance(bot_core, user_input, context: str = "", agent_info=None):
    """Produire une réponse juridique en s'appuyant sur Legifrance."""
    print(f"[Agent] Appelé : {agent_info['id']} pour la question : {user_input}")

    references = fetch_legifrance_references(user_input)
    references_block = format_legifrance_block(references)

    if references_block:
        sources_note = (
            "Appuie ta réponse sur les références suivantes et cite-les clairement."
        )
    else:
        sources_note = (
            "Aucune référence n'a été trouvée, rappelle que l'utilisateur doit vérifier."
        )

    prompt = f"""
Tu es {agent_info['role']}.
Objectif : {agent_info['goal']}
Style : {agent_info['style']}

{sources_note}

Références disponibles :
{references_block or "Aucune référence disponible"}

Question utilisateur :
{user_input}

Donne une réponse synthétique, structurée et cite les textes lorsque présents.
"""
    response = bot_core.ask(prompt, context=context)

    if references_block:
        response = f"{response}\n\n{references_block}"

    return response


__all__ = ["provide_legal_guidance"]

