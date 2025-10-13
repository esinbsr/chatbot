from functools import lru_cache
from typing import Dict, List

import yaml

from utils.logger import get_logger

logger = get_logger(__name__)

with open("config/agents.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

AGENT_CONFIG = config["agents"]["legal"]
USE_CASES: Dict[str, Dict[str, List[str] | str]] = AGENT_CONFIG.get("use_cases", {})

try:
    from pylegifrance import LegifranceClient
    from pylegifrance.fonds.loda import Loda
    from pylegifrance.models.loda.search import SearchRequest
except ImportError:  # pragma: no cover - dépendance optionnelle
    LegifranceClient = None  # type: ignore
    Loda = None  # type: ignore
    SearchRequest = None  # type: ignore
    logger.warning(
        "PyLegifrance n'est pas installé. L'agent juridique utilisera uniquement le modèle."
    )


@lru_cache(maxsize=1)
def _get_loda():
    """Renvoie un client LODA réutilisable."""
    if LegifranceClient is None or Loda is None:
        return None

    try:
        client = LegifranceClient.create()
        return Loda(client)
    except Exception as exc:  # pragma: no cover
        logger.warning("Initialisation Legifrance impossible : %s", exc)
        return None


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


def _query_legifrance(user_input: str, keywords: List[str]) -> List[str]:
    """Interroge Legifrance à partir des mots-clés fournis."""
    loda_client = _get_loda()
    if loda_client is None or SearchRequest is None:
        return []

    # Construire une requête courte : mots-clés connus ou premiers mots de la question.
    base_terms = keywords[:3] or user_input.lower().split()[:6]
    query = " ".join(base_terms).strip()

    try:
        request = SearchRequest(search=query or user_input[:80], page_size=3)
        results = loda_client.search(request)
    except Exception as exc:  # pragma: no cover
        logger.warning("Appel Legifrance impossible : %s", exc)
        return []

    references = []
    for texte in results[:3]:
        titre = texte.titre or texte.titre_long or "Référence sans titre"
        cid = texte.cid.value if texte.cid else "CID indisponible"
        references.append(f"{titre} (CID : {cid})")
    return references


def handle_legal_request(bot_core, user_input: str, context: str = "") -> str:
    """Produit la réponse juridique en s'appuyant sur PyLegifrance lorsque disponible."""
    use_case_key, use_case = _match_use_case(user_input)
    keywords = use_case.get("keywords", [])
    references = _query_legifrance(user_input, keywords)
    references_block = "\n".join(f"- {ref}" for ref in references) or (
        "Aucune référence Legifrance n'a pu être récupérée. Indique-le à l'utilisateur."
    )

    prompt = f"""
    Tu es {AGENT_CONFIG['role']}.
    Objectif : {AGENT_CONFIG['goal']}
    Style : {AGENT_CONFIG['style']}

    Cas d'usage identifié : {use_case.get('label', use_case_key)}
    Consignes spécifiques : {use_case.get('instructions', 'Détaille un plan d’action clair.')}

    Références Legifrance disponibles :
    {references_block}

    Demande de l'utilisateur :
    {user_input}

    Réponse :
    """
    logger.info("Agent juridique - cas d'usage : %s", use_case_key)
    return bot_core.ask(prompt, context=context)