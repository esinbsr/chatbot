"""Tests d'intégration simplifiés du routage et des agents."""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

dummy_utils = types.ModuleType("utils")
dummy_logger = types.ModuleType("utils.logger")


class _DummyLogger:
    def info(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None


def _get_logger(_name):
    return _DummyLogger()


dummy_logger.get_logger = _get_logger
dummy_utils.logger = dummy_logger

sys.modules.setdefault("utils", dummy_utils)
sys.modules.setdefault("utils.logger", dummy_logger)

dummy_langchain = types.ModuleType("langchain_ollama")


class _DummyOllamaLLM:
    def __init__(self, model: str):
        self.model = model

    def invoke(self, prompt: str):
        return "Réponse simulée"


dummy_langchain.OllamaLLM = _DummyOllamaLLM
sys.modules.setdefault("langchain_ollama", dummy_langchain)

dummy_sentence_transformers = types.ModuleType("sentence_transformers")


class _FakeMatrix(list):
    @property
    def shape(self):
        if not self:
            return (0, 0)
        return (len(self), len(self[0]))


class _DummySentenceTransformer:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def encode(self, texts, convert_to_numpy=True):
        if isinstance(texts, str):
            texts = [texts]
        data = [[float(len(t))] for t in texts]
        return _FakeMatrix(data)


dummy_sentence_transformers.SentenceTransformer = _DummySentenceTransformer
sys.modules.setdefault("sentence_transformers", dummy_sentence_transformers)

dummy_faiss = types.ModuleType("faiss")


class _DummyIndexFlatL2:
    def __init__(self, dim: int):
        self.dim = dim
        self.vectors: _FakeMatrix | None = None

    def add(self, vectors: _FakeMatrix):
        self.vectors = vectors

    def search(self, queries: _FakeMatrix, k: int = 1):
        if self.vectors is None:
            raise ValueError("No vectors indexed")

        distances = []
        indices = []
        for query in queries:
            best_idx = 0
            best_dist = float("inf")
            for idx, vector in enumerate(self.vectors):
                dist = sum((vector[i] - query[i]) ** 2 for i in range(self.dim))
                if dist < best_dist:
                    best_dist = dist
                    best_idx = idx
            distances.append([best_dist])
            indices.append([best_idx])
        return distances, indices


dummy_faiss.IndexFlatL2 = _DummyIndexFlatL2
sys.modules.setdefault("faiss", dummy_faiss)

from agents import agent_legal  # noqa: E402
from agents.agent_cv import improve_cv  # noqa: E402
from agents.agent_ia_pme import identify_use_case  # noqa: E402
from agents.agent_legal import provide_legal_guidance  # noqa: E402
from core import ChatbotCore  # noqa: E402
from router import agents as agent_configs  # noqa: E402
from router import router  # noqa: E402
from tools import legifrance  # noqa: E402


class DummyCore(ChatbotCore):
    """Stub de cœur de chatbot pour capturer les prompts."""

    def __init__(self):
        super().__init__(model_name="dummy")
        self.invocations: List[str] = []

    def ask(self, prompt_text, context: str = "") -> str:
        self.invocations.append(prompt_text)
        return "Réponse simulée"


class RoutingTestCase(unittest.TestCase):
    """Vérifie que le routage sélectionne les bons agents selon les entrées."""

    def test_router_selects_ia_agent(self) -> None:
        result = router("Comment lancer un projet IA dans ma PME ?")
        self.assertEqual(result, "ia_pme")

    def test_router_selects_cv_agent(self) -> None:
        result = router("Peux-tu améliorer mon CV de développeur Python ?")
        self.assertEqual(result, "cv")

    def test_router_selects_legal_agent(self) -> None:
        result = router("Quels articles de loi encadrent le temps partiel ?")
        self.assertEqual(result, "legal")


class LegalAgentIntegrationCase(unittest.TestCase):
    """Teste l'agent légal avec des références Legifrance simulées."""

    def setUp(self) -> None:
        self.original_fetch_tool = legifrance.fetch_legifrance_references
        self.original_format_tool = legifrance.format_legifrance_block
        self.original_fetch_agent = agent_legal.fetch_legifrance_references
        self.original_format_agent = agent_legal.format_legifrance_block

        def fake_fetch(*_args, **_kwargs):
            return ["Code du travail - Article L3123-1 (CID : LEGITEXT000006072050)"]

        def fake_format(refs):
            return "Références Legifrance :\n- " + "\n- ".join(refs)

        legifrance.fetch_legifrance_references = fake_fetch
        legifrance.format_legifrance_block = fake_format
        agent_legal.fetch_legifrance_references = fake_fetch
        agent_legal.format_legifrance_block = fake_format

    def tearDown(self) -> None:
        legifrance.fetch_legifrance_references = self.original_fetch_tool
        legifrance.format_legifrance_block = self.original_format_tool
        agent_legal.fetch_legifrance_references = self.original_fetch_agent
        agent_legal.format_legifrance_block = self.original_format_agent

    def test_legal_agent_cites_legifrance(self) -> None:
        dummy_core = DummyCore()
        agent_info = next(a for a in agent_configs if a["id"] == "legal")
        response = provide_legal_guidance(
            dummy_core,
            "Quelles sont les règles du temps partiel ?",
            context="",
            agent_info=agent_info,
        )
        self.assertTrue(dummy_core.invocations, "Le modèle n'a pas été appelé")
        self.assertIn("Références Legifrance", dummy_core.invocations[-1])
        self.assertIn("Références Legifrance", response)


class FullFlowSmokeTest(unittest.TestCase):
    """Test bout-en-bout simplifié sur chaque agent."""

    def setUp(self) -> None:
        self.dummy_core = DummyCore()
        self.agent_map: Dict[str, Dict[str, str]] = {
            agent["id"]: agent for agent in agent_configs
        }

    def _dispatch(self, user_input: str) -> str:
        agent_id = router(user_input)
        agent_info = self.agent_map.get(agent_id)
        handlers = {
            "ia_pme": identify_use_case,
            "cv": improve_cv,
            "legal": provide_legal_guidance,
        }
        handler = handlers.get(agent_id)
        if handler is None or agent_info is None:
            return self.dummy_core.ask(user_input)
        return handler(
            self.dummy_core,
            user_input,
            context="",
            agent_info=agent_info,
        )

    def test_each_agent_flow(self) -> None:
        prompts = {
            "ia_pme": "Quels cas d'usage IA sont pertinents pour une PME de retail ?",
            "cv": "Donne-moi des conseils pour mon CV de data analyst junior.",
            "legal": "Quel article couvre le contrat à durée déterminée ?",
        }
        for agent_id, question in prompts.items():
            with self.subTest(agent=agent_id):
                response = self._dispatch(question)
                self.assertTrue(self.dummy_core.invocations)
                self.assertIsInstance(response, str)
                self.dummy_core.invocations.clear()


if __name__ == "__main__":
    unittest.main()
