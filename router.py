import yaml
from core import ChatbotCore
from agents.registry import AGENT_REGISTRY

class AgentRouter:
    def __init__(self, config_path="config/agents.yaml", model_name="mistral:7b-instruct"):
        self.core = ChatbotCore(model_name=model_name)
        self.agents = self.load_agents(config_path)

    def load_agents(self, path):
        with open(path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        agents = {}
        for agent_cfg in config.get("agents", []):
            name = agent_cfg["name"]
            system_prompt = agent_cfg.get("system_prompt")
            agent_type = agent_cfg.get("type")

            agent_class = AGENT_REGISTRY.get(agent_type)
            if not agent_class:
                raise ValueError(f"Type d'agent inconnu : {agent_type}")

            agents[name] = agent_class(
                name=name,
                core=self.core,
                system_prompt=system_prompt
            )
        return agents

    def route(self, user_input, agent_name, context=""):
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' non défini.")
        return self.agents[agent_name].generate(user_input, context=context)
