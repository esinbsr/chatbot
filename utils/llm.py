import os
from functools import lru_cache
from typing import Optional

from mistralai import Mistral

from utils.config import load_config


@lru_cache(maxsize=1)
def get_mistral_client(api_key: Optional[str] = None) -> Mistral:
    """Retourne un client Mistral réutilisable."""
    if api_key is None:
        config = load_config()
        api_key = os.getenv("MISTRAL_API_KEY") or config.get("llm", {}).get("api_key")
    if not api_key:
        raise RuntimeError(
            "Clé API Mistral manquante. Définis MISTRAL_API_KEY ou config.llm.api_key."
        )
    return Mistral(api_key=api_key)
