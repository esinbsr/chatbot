from langchain_ollama import OllamaLLM

class ChatbotCore:
    
    def __init__(self, model_name='mistral:7b-instruct'):
        self.llm = OllamaLLM(model=model_name)

    def ask(self, prompt_text):
        result = self.llm.invoke(prompt_text)
        return result.get("text", "") if isinstance(result, dict) else str(result)