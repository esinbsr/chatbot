import time
import unicodedata
from typing import Dict, List, Optional, Set

from mistralai.models.sdkerror import SDKError
from utils.config import load_config
from utils.logger import get_logger
from utils.llm import get_mistral_client

DEFAULT_FAST_KEYWORDS: Dict[str, List[str]] = {
    "legal": ["contrat", "juridique", "loi", "rgpd", "litige", "clause", "conformité", "procédure"],
    "cv": [
        "cv",
        "curriculum",
        "profil",
        "lettre",
        "candidature",
        "experience",
        "expérience",
        "sap",
        "deploiement",
        "déploiement",
        "reformuler",
    ],
    "ml": [
        "machine learning",
        "intelligence artificielle",
        "modèle",
        "modelisation",
        "entrainement",
        "classification",
        "régression",
    ],
    "test": [
        "test",
        "restriction",
        "limite",
        "politique",
        "interdit",
        "veuillez",
        "refus",
        "refuser",
        "règle",
        "regle",
    ],
}


class Router:
    """Détermine l'agent le plus adapté pour une requête utilisateur."""

    def __init__(self, yaml_path: str = "config/agents.yaml") -> None:
        self.logger = get_logger(self.__class__.__name__)
        config = load_config(yaml_path)
        self.agents_config = config["agents"]
        self.agents_names = list(self.agents_config.keys())
        router_conf = config.get("router", {})
        raw_keywords = router_conf.get("keywords", DEFAULT_FAST_KEYWORDS)
        self.fast_keywords = self._prepare_keywords(raw_keywords)
        llm_model = router_conf.get("model") or config.get("llm", {}).get("model", "mistral-small-latest")
        self.temperature = float(router_conf.get("temperature", 0.0))
        self.max_tokens = int(router_conf.get("max_tokens", 32))
        self.client = get_mistral_client()
        self.model = llm_model
        self.logger.info(
            "Routeur Mistral '%s' initialisé (temperature=%.2f, max_tokens=%d)",
            self.model,
            self.temperature,
            self.max_tokens,
        )

    def _match_keywords(self, user_input: str) -> Optional[str]:
        lowered = user_input.lower()
        normalized = (
            unicodedata.normalize("NFD", user_input).encode("ascii", "ignore").decode().lower()
        )
        for agent, keywords in self.fast_keywords.items():
            if any(keyword in lowered or keyword in normalized for keyword in keywords):
                self.logger.info("Intention trouvée par mots-clés: %s", agent)
                return agent
        return None

    def get_agent_for_input(self, user_input: str) -> str:
        """Retourne le nom de l'agent le plus pertinent."""
        match = self._match_keywords(user_input)
        if match:
            return match

        prompt = (
            f"Intentions disponibles : {', '.join(self.agents_names)}.\n"
            f'Texte utilisateur : """{user_input}"""\n'
            "Réponds uniquement par le nom de l'intention la plus adaptée."
        )
        self.logger.info("Classification LLM pour: %s", user_input[:120])
        start_time = time.perf_counter()
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un routeur qui renvoie uniquement le nom d'une intention.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1.0,
            )
        except SDKError as exc:
            self.logger.warning(
                "Classification LLM indisponible (%s). Fallback vers mot-clé.", exc
            )
            return self._match_keywords(user_input) or self.agents_names[0]
        elapsed = time.perf_counter() - start_time
        agent_name = ""
        if response.choices:
            content = response.choices[0].message.content
            agent_name = content.strip() if content else ""

        if agent_name not in self.agents_names:
            fallback = self._match_keywords(user_input) or self.agents_names[0]
            self.logger.warning(
                "Intention inconnue '%s', fallback vers '%s'.", agent_name, fallback
            )
            return fallback

        self.logger.info("Intention détectée: %s (%.2fs)", agent_name, elapsed)
        return agent_name

    @staticmethod
    def _prepare_keywords(raw_keywords: Dict[str, List[str]]) -> Dict[str, Set[str]]:
        source = raw_keywords or DEFAULT_FAST_KEYWORDS
        prepared: Dict[str, Set[str]] = {}
        for agent, words in source.items():
            if not isinstance(words, list):
                continue
            entries: Set[str] = set()
            for word in words:
                lowered = word.lower()
                entries.add(lowered)
                normalized = (
                    unicodedata.normalize("NFD", lowered).encode("ascii", "ignore").decode()
                )
                if normalized:
                    entries.add(normalized)
            if entries:
                prepared[agent] = entries
        if not prepared:
            return {agent: set(words) for agent, words in DEFAULT_FAST_KEYWORDS.items()}
        return prepared
