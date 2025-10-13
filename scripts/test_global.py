"""Test global rapide pour vérifier le fonctionnement des agents du chatbot."""

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
        "Nous devons mettre à jour notre charte informatique pour rester "
        "conformes au RGPD.",
    ),
    (
        "cv",
        "Peux-tu améliorer cette expérience : j'ai dirigé le déploiement SAP "
        "avec 8 personnes en 6 mois ?",
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
    """Associe chaque intention à sa fonction de traitement."""
    return {
        "cv": lambda text, ctx: improve_text(bot, text, context=ctx),
        "ml": lambda text, ctx: learn_ml(bot, text, context=ctx),
        "test": lambda text, ctx: agent_test(bot, text, context=ctx),
        "legal": lambda text, ctx: handle_legal_request(bot, text, context=ctx),
    }


def afficher_ligne(
    index: int,
    total: int,
    attendu: str,
    agent: str,
    route_time: float,
    answer_time: float,
    extrait: str,
    ok: bool,
) -> None:
    statut = "OK" if ok else "KO"
    print(
        f"[{statut}] Question {index}/{total} "
        f"(attendue : {attendu}, détectée : {agent})"
    )
    print(f"    Routage : {route_time:.2f}s | Réponse : {answer_time:.2f}s")
    print(f"    Aperçu  : {extrait}\n")


def run_global_test(args: argparse.Namespace) -> None:
    """Exécute la série de prompts et affiche un résumé lisible."""
    config = load_config()
    default_model = config.get("llm", {}).get("model")
    bot = ChatbotCore(model_name=args.model or default_model)
    router = Router()
    agents = build_agents(bot)
    contexte: List[str] = []

    print("=== Test rapide du chatbot ===")
    total = len(PROMPTS)
    for index, (attendu, prompt) in enumerate(PROMPTS, start=1):
        if index > 1 and args.pause > 0:
            time.sleep(args.pause)

        contexte_texte = "\n".join(contexte[-6:])
        debut_routage = time.perf_counter()
        agent = router.get_agent_for_input(prompt)
        temps_routage = time.perf_counter() - debut_routage

        handler = agents.get(agent, lambda text, ctx: bot.ask(text, context=ctx))
        debut_reponse = time.perf_counter()
        try:
            reponse = handler(prompt, contexte_texte)
            succes = True
        except SDKError as exc:
            succes = False
            reponse = (
                "[Info] API Mistral momentanément saturée. "
                f"Détail : {exc}. Réessaie après une courte pause."
            )
        except Exception as exc:  # pragma: no cover
            succes = False
            reponse = f"[Erreur inattendue] {exc}"
        temps_reponse = time.perf_counter() - debut_reponse

        contexte.append(f"User: {prompt}\nAI: {reponse}")
        extrait = reponse.replace("\n", " ")[:160]
        afficher_ligne(
            index,
            total,
            attendu,
            agent,
            temps_routage,
            temps_reponse,
            extrait,
            succes,
        )

    print("=== Fin du test ===")


def parse_args() -> argparse.Namespace:
    """Analyse les paramètres CLI."""
    parser = argparse.ArgumentParser(
        description="Vérifie rapidement que chaque agent répond correctement."
    )
    parser.add_argument(
        "--model",
        help="Nom du modèle Mistral à utiliser (défaut : configuration YAML).",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=3.0,
        help="Pause en secondes entre deux prompts (défaut : 3.0).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    run_global_test(parse_args())
