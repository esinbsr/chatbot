from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml


@lru_cache(maxsize=1)
def load_config(path: str = "config/agents.yaml") -> Dict[str, Any]:
    """Charge le fichier YAML de configuration une seule fois."""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration introuvable : {path}")

    with config_path.open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)