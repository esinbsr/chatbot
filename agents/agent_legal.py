import time
from typing import Dict, List
from utils.logger import get_logger
from utils.config import load_config

logger = get_logger(__name__)

AGENT_CONFIG = load_config()["agents"]["legal"]
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

class LegalAgent :

    def _get_loda(self):
        """Renvoie un client LODA fraichement initialisé."""
        if LegifranceClient is None or Loda is None:
            return None
        try:
            client = LegifranceClient()
            return Loda(client)
        except Exception as exc:  # pragma: no cover
            logger.warning("Initialisation Legifrance impossible : %s", exc)
            return None


    def _match_use_case(self, user_input: str):
        """Renvoie (clé, configuration) du cas d'usage le plus pertinent."""
        lowered = user_input.lower()
        for key, data in USE_CASES.items():
            for keyword in data.get("keywords", []):
                if keyword in lowered:
                    return key, data
        # Retourne le premier cas configuré ou un fallback.
        default_key = next(iter(USE_CASES), "document_compliance")
        return default_key, USE_CASES.get(default_key, {})


    def _query_legifrance(self, user_input: str, keywords: List[str]) -> List[str]:
        """Interroge Legifrance à partir des mots-clés fournis."""
        start_time = time.perf_counter()
        loda_client = self._get_loda()
        if loda_client is None or SearchRequest is None:
            return []
        search_terms = (keywords or user_input.lower().split())[:8]
        query = " ".join(search_terms)[:80].strip()
        if not query:
            return []
        try:
            request = SearchRequest(
                text=query,
                champ="ARTICLE",
                type_recherche="TOUS_LES_MOTS_DANS_UN_CHAMP",
            )
            results = loda_client.search(request)
        except Exception as exc:  # pragma: no cover
            elapsed = time.perf_counter() - start_time
            logger.warning("Recherche Legifrance impossible (%.2fs) : %s", elapsed, exc)
            return []

        # Limite volontairement les références retournées pour garder la réponse concise.
        references = []
        for texte in results[:2]:
            titre = texte.titre or texte.titre_long or "Référence sans titre"
            cid = texte.cid.value if texte.cid else "CID indisponible"
            references.append(f"{titre} (CID : {cid})")
        elapsed = time.perf_counter() - start_time
        logger.info("Legifrance a retourné %d référence(s) en %.2fs", len(references), elapsed)
        return references


    def handle_legal_request(self, bot_core, user_input: str, context: str = "") -> str:
        """Produit la réponse juridique en s'appuyant sur PyLegifrance lorsque disponible."""
        use_case_key, use_case = self._match_use_case(user_input)
        keywords = use_case.get("keywords", [])
        references = self._query_legifrance(user_input, keywords)
        references_block = "\n".join(references) or "Aucune référence Legifrance disponible."
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