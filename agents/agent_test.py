<<<<<<< HEAD
from chatbot.core import ChatbotCore
from docling.converting import converter

bot_core = ChatbotCore()
convert = converter()

while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = bot_core.chat(user_input)
        print(f"\nAI: {response}\n")

        # 🎯 → Ajoute ça ici
        try:
            filename = user_input[:30].replace(" ", "_").replace("?", "")
            converter.from_text(response, filename=filename)
            print(f"[✓] Réponse sauvegardée dans scratch/{filename}.md (+ json/yaml)")
        except Exception as e:
            print(f"[!] Erreur lors de la conversion du document : {e}")
=======
from core import ChatbotCore
import yaml

with open('config/agents.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
# Paramètres destinés aux requêtes de test ou de garde-fous.
AGENT_CONFIG = config['agents']['test']

bot_core = ChatbotCore()

def test(user_input, context=''):
    """Répond aux requêtes de test en appliquant les règles définies."""
    prompt = f"""
    Tu es {AGENT_CONFIG['role']}
    Objectif: {AGENT_CONFIG['goal']}
    Style : {AGENT_CONFIG['style']}

    Prompt de l'utilisateur : {user_input}
    Réponse :
    """
    return bot_core.ask(prompt, context=context)
>>>>>>> 1cd0c237cc2babf4d3e34d16137169224cace272
