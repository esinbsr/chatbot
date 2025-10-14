from typing import Dict, List

from utils.logger import get_logger
from utils.config import load_config

logger = get_logger(__name__)

AGENT_CONFIG = load_config()["agents"]["legal"]
USE_CASES: Dict[str, Dict[str, List[str] | str]] = AGENT_CONFIG.get("use_cases", {})

def _match_use_case(user_input: str):
    """Renvoie (clé, configuration) du cas d'usage le plus pertinent."""
    lowered = user_input.lower()
    for key, data in USE_CASES.items():
        for keyword in data.get("keywords", []):
            if keyword in lowered:
                return key, data
    # Retourne le premier cas configuré ou un fallback.
    default_key = next(iter(USE_CASES), "document_compliance")
    return default_key, USE_CASES.get(default_key, {})


def handle_legal_request(bot_core, user_input: str, context: str = "") -> str:
    """Produit la réponse juridique en s'appuyant sur PyLegifrance lorsque disponible."""
    use_case_key, use_case = _match_use_case(user_input)
    keywords = use_case.get("keywords", [])
    references = bot_core.get_legifrance_references(user_input, keywords)
    formatted_refs = bot_core.format_legifrance_block(references)
    references_block = formatted_refs or "Aucune référence Legifrance disponible."
    prompt = (
        f"Rôle : {AGENT_CONFIG['role']}\n"
        f"Objectif : {AGENT_CONFIG['goal']}\n"
        f"Style : {AGENT_CONFIG['style']}\n"
        f"Cas d'usage : {use_case.get('label', use_case_key)}\n"
        f"Consignes : {use_case.get('instructions', 'Détaille un plan d’action clair.')}\n"
        f"Références : {references_block}\n"
        f"Demande : {user_input}\n"
        "Réponse :"
    )
    logger.info("Agent juridique - cas d'usage : %s", use_case_key)
    return bot_core.ask(prompt, context=context)
