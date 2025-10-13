"""
Simple smoke test for the multi-agent chatbot.

Usage
-----
python scripts/smoke_test.py --delay 2

Parameters are optional; use `--help` to inspect them. The command prints
a short report for chaque prompt afin de vérifier que le routage,
la génération et Legifrance fonctionnent depuis la ligne de commande.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from mistralai.models.sdkerror import SDKError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from agents.agent_cv import improve_text
from agents.agent_legal import handle_legal_request
from agents.agent_ml import learn_ml
from agents.agent_test import test as agent_test
from core import ChatbotCore
from router import Router
from utils.config import load_config

PROMPTS: List[Tuple[str, str]] = [
    (
        "legal",
        (
            "Nous devons mettre à jour notre charte informatique pour rester "
            "conformes au RGPD."
        ),
    ),
    (
        "cv",
        (
            "Peux-tu améliorer cette expérience : j'ai dirigé le déploiement "
            "SAP avec 8 personnes en 6 mois ?"
        ),
    ),
    (
        "ml",
        "Explique simplement ce qu'est une forêt aléatoire et quand l'utiliser.",
    ),
    (
        "test",
        "Quels types de demandes devons-nous refuser selon nos règles ?",
    ),
]


def build_agents(bot: ChatbotCore) -> Dict[str, Callable[[str, str], str]]:
    """Associe chaque intention au handler correspondant."""
    return {
        "cv": lambda text, ctx: improve_text(bot, text, context=ctx),
        "ml": lambda text, ctx: learn_ml(bot, text, context=ctx),
        "test": lambda text, ctx: agent_test(bot, text, context=ctx),
        "legal": lambda text, ctx: handle_legal_request(bot, text, context=ctx),
    }


def run_smoke_test(args: argparse.Namespace) -> None:
    """Exécute la série de prompts et affiche un rapport concis."""
    config = load_config()
    default_model = config.get("llm", {}).get("model")
    bot = ChatbotCore(
        model_name=args.model or default_model,
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
    )
    router = Router()
    agents = build_agents(bot)
    context_history: List[str] = []

    print("=== DÉMARRAGE DU SMOKE TEST ===")
    for index, (expected_agent, prompt) in enumerate(PROMPTS, start=1):
        if index > 1 and args.delay > 0:
            time.sleep(args.delay)

        context = "\n".join(context_history[-6:])
        start_route = time.perf_counter()
        agent_name = router.get_agent_for_input(prompt)
        route_time = time.perf_counter() - start_route

        handler = agents.get(agent_name, lambda text, ctx: bot.ask(text, context=ctx))
        start_answer = time.perf_counter()
        try:
            response = handler(prompt, context)
            success = True
        except SDKError as exc:
            success = False
            response = (
                f"[Erreur API Mistral] {exc}. Patientez quelques secondes "
                "ou réduisez la fréquence des appels."
            )
        except Exception as exc:  # pragma: no cover - diagnostic
            success = False
            response = f"[Erreur inattendue] {exc}"
        answer_time = time.perf_counter() - start_answer

        context_history.append(f"User: {prompt}\nAI: {response}")
        summary = response.replace("\n", " ")[:160]
        status = "OK" if success else "KO"
        print(
            f"[{status}] Prompt {index}/{len(PROMPTS)} "
            f"(attendu: {expected_agent}, obtenu: {agent_name})\n"
            f"     Routage : {route_time:.2f}s | Réponse : {answer_time:.2f}s\n"
            f"     Aperçu  : {summary}"
        )

    print("=== FIN DU SMOKE TEST ===")


def parse_args() -> argparse.Namespace:
    """Déclare les paramètres CLI."""
    parser = argparse.ArgumentParser(
        description="Vérifie que le chatbot répond correctement à quelques prompts."
    )
    parser.add_argument(
        "--model",
        help="Nom du modèle Mistral à utiliser (défaut: configuration YAML).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Température pour la génération (override).",
    )
    parser.add_argument(
        "--top-p",
        type=float,
        help="Paramètre top-p pour la génération (override).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Nombre maximum de tokens générés (override).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=3.0,
        help="Pause en secondes entre les prompts (défaut: 3.0).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    run_smoke_test(parse_args())
