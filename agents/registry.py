from agents.base_agent import BaseAgent
from agents.summarizer_agent import SummarizerAgent
from agents.slider_agent import SliderAgent

AGENT_REGISTRY = {
    "base": BaseAgent,
    "summarizer": SummarizerAgent,
    "slider": SliderAgent,
}
