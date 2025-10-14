# Ce fichier permet de tester le modèle en voyant quel agent il appel selon la requête de l'utilisateur
from router import router, agents
from agents.agent_ia_pme import identify_use_case
from core import ChatbotCore

bot = ChatbotCore()
context = ""

test_phrases = [
    "Donne-moi des exemples d'utilisation de l'intelligence artificielle pour automatiser mes tâches.",
    "Quels types de formation IA sont disponibles pour mes employés ?",
    "Je voudrais savoir comment l'IA peut m'aider dans mes ventes.",
    "Parle-moi de recettes de cuisine."  # phrase complètement hors contexte
]

for phrase in test_phrases:
    print("\n---")
    print(f"Question : {phrase}")
    agent_id = router(phrase)
    agent_info = next(a for a in agents if a["id"] == agent_id)
    response = identify_use_case(bot, phrase, context=context, agent_info=agent_info)
    print(f"Agent utilisé : {agent_id}")
    print(f"Réponse : {response[:150]}...")  # tronquer pour lisibilité
