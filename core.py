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

# Charger le yaml global pour règles générales
with open("config/agents.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)
GLOBAL_RULES = CONFIG["global"]

class ChatbotCore:
    def __init__(self, model_name='mistral:7b-instruct'):
        self.llm = OllamaLLM(model=model_name)

    def ask(self, prompt_text, context=''):
        # j'ininclus les règles globales et le contexte
        prompt = f"""
        Langue : {GLOBAL_RULES['language']}
        Ton : {GLOBAL_RULES['tone']}
        Règles : {', '.join(GLOBAL_RULES['rules'])}

        Contexte de conversation : {context}
        Question : {prompt_text}
        """
        result = self.llm.invoke(prompt)

        if isinstance(result, dict):
            return result.get('text', '')
        else:
            return str(result).strip()
