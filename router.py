import yaml
from langchain_ollama import OllamaLLM

# Router dynamique qui lit la configuration des agents depuis un fichier YAML et choisit l'agent le plus pertinent pour chaque requête utilisateur.
class Router:

    def __init__(self, yaml_path="config/agents.yaml"):
        
        # lecture du yaml
        with open(yaml_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) # transforme le contenu yaml en dictionnaire 

        # créer la liste des agents et leurs intentions associées
        self.agents_config = config['agents'] #dico
        self.agents_names = list(self.agents_config.keys()) # ['hr', 'slide', 'ml']

        # créer un petit LLM pour décider de l'intention
        self.llm = OllamaLLM(model="mistral:7b-instruct")

# envoie le nom de l'agent le plus pertinent pour le texte utilisateur en utilisant le llm pour classifier l'intention
    def get_agent_for_input(self, user_input):

        prompt = f"""
        Parmi les intentions suivantes {self.agents_names}, laquelle correspond le mieux à ce texte utilisateur :
        "{user_input}"
        Réponds uniquement par le nom de l'intention.
        """
        result = self.llm.invoke(prompt)

        # le llm peut renvoyer un dictionnaire ou une string selon la version
        if isinstance(result, dict):
            agent_name = result.get("text", "").strip()
        else:
            agent_name = str(result).strip()

        # Vérification de sécurité
        if agent_name not in self.agents_names:
            return "agent_general"
        return agent_name
