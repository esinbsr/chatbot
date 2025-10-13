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
