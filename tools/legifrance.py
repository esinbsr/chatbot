"""Helper around PyLegifrance to retrieve legal references for the chatbot."""

from __future__ import annotations

import os
import time
from functools import lru_cache
from typing import List, Sequence

from utils.logger import get_logger

logger = get_logger(__name__)

CLIENT_ID = os.getenv(
    "LEGIFRANCE_CLIENT_ID", "128ad58c-0665-46cb-976d-9a5a26320ab1"
)
CLIENT_SECRET = os.getenv(
    "LEGIFRANCE_CLIENT_SECRET", "f3135107-f63d-4878-9ea7-8f26a6b539b4"
)

try:  # pragma: no cover - optional dependency
    from pylegifrance import LegifranceClient
    from pylegifrance.fonds.loda import Loda
    from pylegifrance.models.loda.search import SearchRequest
except ImportError:  # pragma: no cover
    LegifranceClient = None  # type: ignore
    Loda = None  # type: ignore
    SearchRequest = None  # type: ignore
    logger.warning(
        "PyLegifrance n'est pas installé. Les références juridiques seront "
        "désactivées."
    )


@lru_cache(maxsize=1)
def _get_loda_client() -> Loda | None:
    """Return a LODA client, initialised only once."""
    if LegifranceClient is None or Loda is None:
        return None

    if not CLIENT_ID or not CLIENT_SECRET:
        logger.warning("Identifiants Legifrance manquants.")
        return None

    try:
        client = LegifranceClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        return Loda(client)
    except Exception as exc:  # pragma: no cover
        logger.warning("Initialisation Legifrance impossible : %s", exc)
        return None


def fetch_legifrance_references(
    user_input: str,
    keywords: Sequence[str] | None = None,
    max_results: int = 2,
) -> List[str]:
    """Query Legifrance and return a list of formatted references."""
    loda_client = _get_loda_client()
    if loda_client is None or SearchRequest is None:
        return []

    search_terms = list(keywords or []) or user_input.lower().split()
    query = " ".join(search_terms[:8])[:80].strip()
    if not query:
        return []

    start_time = time.perf_counter()
    try:
        request = SearchRequest(
            text=query,
            champ="ARTICLE",
            type_recherche="TOUS_LES_MOTS_DANS_UN_CHAMP",
        )
        results = loda_client.search(request)
    except Exception as exc:  # pragma: no cover
        elapsed = time.perf_counter() - start_time
        logger.warning(
            "Recherche Legifrance impossible (%.2fs) : %s", elapsed, exc
        )
        return []

    references: List[str] = []
    for texte in results[:max_results]:
        titre = texte.titre or texte.titre_long or "Référence sans titre"
        cid = texte.cid.value if texte.cid else "CID indisponible"
        references.append(f"{titre} (CID : {cid})")

    elapsed = time.perf_counter() - start_time
    if references:
        logger.info(
            "Legifrance a retourné %d référence(s) en %.2fs",
            len(references),
            elapsed,
        )
    else:
        logger.info(
            "Legifrance n'a retourné aucune référence (%.2fs)", elapsed
        )
    return references


def format_legifrance_block(references: Sequence[str]) -> str:
    """Return a textual block ready to inject into a prompt."""
    if not references:
        return ""
    lines = "\n".join(f"- {reference}" for reference in references)
    return f"Références Legifrance :\n{lines}"


__all__ = ["fetch_legifrance_references", "format_legifrance_block"]

