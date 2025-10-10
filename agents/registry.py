from agents.base_agent import BaseAgent
from agents.summarizer_agent import SummarizerAgent

AGENT_REGISTRY = {
    "base": BaseAgent,
    "summarizer": SummarizerAgent,
}
