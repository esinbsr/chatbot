import time
from typing import Dict

from utils.config import load_config
from utils.logger import get_logger
from utils.llm import get_mistral_client

CONFIG = load_config()
GLOBAL_RULES = CONFIG["global"]
LLM_CONFIG = CONFIG.get("llm", {})
DEFAULT_LLM_MODEL = LLM_CONFIG.get("model", "mistral-small-latest")
DEFAULT_TEMPERATURE = float(LLM_CONFIG.get("temperature", 0.6))
DEFAULT_TOP_P = float(LLM_CONFIG.get("top_p", 0.9))
DEFAULT_MAX_TOKENS = int(LLM_CONFIG.get("max_tokens", 512))
GLOBAL_PROMPT_PREFIX = "\n".join(
    [
        f"Langue : {GLOBAL_RULES['language']}",
        f"Ton : {GLOBAL_RULES['tone']}",
        "Règles : " + ", ".join(GLOBAL_RULES["rules"]),
    ]
)


class ChatbotCore:
    """Interface minimale autour de l'API Mistral."""

    def __init__(self, model_name: str | None = None) -> None:
        self.model = model_name or DEFAULT_LLM_MODEL
        self.temperature = DEFAULT_TEMPERATURE
        self.top_p = DEFAULT_TOP_P
        self.max_tokens = DEFAULT_MAX_TOKENS
        self.client = get_mistral_client()
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(
            "Initialisation modèle '%s'", self.model
        )

    def ask(self, prompt_text: str, context: str = "") -> str:
        """Construit le prompt final et interroge le modèle."""
        start_time = time.perf_counter()
        prompt_preview = " ".join(prompt_text.split())[:120]
        self.logger.info("Requête LLM (aperçu): %s", prompt_preview)

        # Compose la requête complète : rappel des règles + message utilisateur.
        messages = [
            {"role": "system", "content": GLOBAL_PROMPT_PREFIX},
            {
                "role": "user",
                "content": (
                    f"Contexte : {context.strip() if context else 'Aucun'}\n"
                    f"Message : {prompt_text.strip()}\n"
                    "Réponse :"
                ),
            },
        ]

        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
        )
        answer = ""
        if response.choices:
            message = response.choices[0].message
            if hasattr(message, "content"):
                answer = message.content or ""
            elif isinstance(message, dict):
                answer = message.get("content", "")
        if not isinstance(answer, str):
            answer = str(answer or "")
        answer = answer.strip()

        elapsed = time.perf_counter() - start_time
        self.logger.info("Réponse LLM (%.2fs, aperçu): %s", elapsed, answer[:120])
        return answer
