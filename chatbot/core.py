from langchain_ollama import OllamaLLM

class ChatbotCore:
    def __init__(self, model_name='mistral:7b-instruct'):
        self.llm = OllamaLLM(model=model_name)

    def ask(self, question, context=''):
        prompt_text = f"""
        You are an expert in AI and helping French SMEs/TPE/ETI.
        Conversation history: {context}
        User question: {question}
        Answer in a clear and pedagogical way:
    """
        result = self.llm.invoke(prompt_text)

        if isinstance(result, dict):
            return result.get('text', '')
        else:
            return str(result)