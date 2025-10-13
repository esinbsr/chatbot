# from langchain_ollama import OllamaLLM # classe qui permet de communiquer avec Ollama

# class ChatbotCore:
#     def __init__(self, model_name='mistral:7b-instruct'):
#         self.llm = OllamaLLM(model=model_name)

# # méthode qui permet de poser une question au modèle
#     def ask(self, prompt_text, context=''):
#         result = self.llm.invoke(prompt_text)

#         if isinstance(result, dict):
#             return result.get('text', '')
#         else:
#             return str(result)
        

from langchain_ollama import OllamaLLM
import yaml

from utils.logger import get_logger

# Charger le yaml global pour règles générales
with open("config/agents.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)
GLOBAL_RULES = CONFIG["global"]


class ChatbotCore:
    def __init__(self, model_name='mistral:7b-instruct'):
        self.llm = OllamaLLM(model=model_name)
        self.logger = get_logger(self.__class__.__name__)

    def ask(self, prompt_text, context=''):
        # Concaténer règles globales et contexte pour encadrer la question utilisateur.
        prompt = f"""
        Langue : {GLOBAL_RULES['language']}
        Ton : {GLOBAL_RULES['tone']}
        Règles : {', '.join(GLOBAL_RULES['rules'])}

        Contexte de conversation : {context}
        Question : {prompt_text}
        """
        prompt_preview = " ".join(prompt_text.split())[:120]
        self.logger.info("Requête LLM (aperçu): %s", prompt_preview)

        result = self.llm.invoke(prompt)

        if isinstance(result, dict):
            answer = result.get('text', '')
        else:
            answer = str(result).strip()

        self.logger.info("Réponse LLM (aperçu): %s", answer[:120])
        return answer
