# Chatbot IA multi-agents

## Aperçu
Ce projet propose une architecture de chatbot en Python reposant sur plusieurs agents spécialisés
et un routeur qui sélectionne automatiquement l'agent le plus pertinent pour répondre à
l'utilisateur. Le cœur du bot s'appuie sur `langchain_ollama` et le modèle local
`mistral:7b-instruct`.

## **Contexte du projet**
Microsoft nous engage pour créer un chatbot open source destiné à accompagner les ETI/TPE/PME françaises.  
L'objectif est de proposer un agent conversationnel (à terme déployé sur une page GitHub publique) capable de :
- Identifier des cas d’usage pertinents pour l’IA générative selon le profil de l’entreprise.
- Répondre aux questions sur la formation des collaborateurs et les aides disponibles.

Notes internes et documentation de travail : https://www.notion.so/PROJET-MICROSOFT-A-vous-l-IA-276b73b4f1d480fc91d4e18c799c5c0a#276b73b4f1d480fc91d4e18c799c5c0a

## Prérequis
- Python 3.10 ou supérieur
- [Ollama](https://ollama.ai) installé localement
- Modèle `mistral:7b-instruct` téléchargé via `ollama pull mistral:7b-instruct`
- Accès API Legifrance (client_id + client_secret) pour activer l'agent juridique

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # sous Windows : .venv\Scripts\activate
pip install --upgrade pip
pip install langchain_ollama pyyaml pylegifrance
# (optionnel) pip install beautifulsoup4  # pour un nettoyage plus lisible du texte Legifrance
```

## Configuration Legifrance
Renseignez vos identifiants API avant de lancer le chatbot :
```bash
export LEGIFRANCE_CLIENT_ID="votre_id"
export LEGIFRANCE_CLIENT_SECRET="votre_secret"
```
Vous pouvez également les placer dans un fichier `.env` à la racine du projet (grâce à `python-dotenv` installé avec PyLegifrance).

## Lancement du chatbot
```bash
python main.py
```
Le programme ouvre une boucle interactive dans le terminal. Tapez `exit` pour quitter la session.

## Architecture des fichiers
- `core.py` : point d'entrée vers le LLM. Injecte les règles globales et fait transiter toutes
  les requêtes. Gère également la journalisation principale.
- `router.py` : interroge un petit modèle pour classifier l'intention et retourner le nom de
  l'agent à mobiliser.
- `config/agents.yaml` : définit les règles globales et les profils de chaque agent
  (rôle, objectif, style).
- `agents/` :
  - `agent_cv.py` : améliore CV, lettres de motivation et profils professionnels.
  - `agent_ml.py` : vulgarise des notions de machine learning.
  - `agent_test.py` : vérifie les scénarios de test et les demandes sensibles.
  - `agent_legal.py` : génère des recommandations juridiques en interrogeant PyLegifrance.
- `rag/` : squelettes des composants RAG (loader, retriever, vector store) prêts à être complétés.
- `utils/logger.py` : configuration centralisée du système de log.
- `logs/` : dossier contenant le fichier `app.log` généré automatiquement.
- `main.py` : boucle CLI principale, gère le routage et la mémoire de contexte.
- `test_core.py` : script minimal pour tester le cœur sans router.

## Cas d'usage couverts par l'agent légal
- **Documents de conformité** : propositions de clauses, politiques et plans d'action adaptés aux rôles.
- **Soutien aux litiges** : repérage des textes applicables, organisation des preuves et préparation de rapports.
- **Veille réglementaire & reporting** : calendrier des obligations, synthèse des évolutions et indicateurs de suivi.
> Sans identifiants Legifrance valides, l'agent signale l'absence de références et fournit des recommandations génériques.

## Journalisation
Le module `utils/logger.py` configure un logger partagé :
- enregistre les événements dans `logs/app.log`;
- retient également les messages sur la sortie standard pour suivre les interactions en direct;
- log l'aperçu des prompts envoyés et des réponses reçues.

## Personnalisation
- Ajustez les règles globales ou les descriptions d'agents dans `config/agents.yaml`.
- Ajoutez de nouveaux agents en créant un fichier dans `agents/` puis en l'enregistrant dans
  `AGENTS_FUNCTIONS` et dans la configuration YAML.

## Tests et debug
- Utilisez `test_core.py` pour valider rapidement la connexion au modèle.
- Surveillez `logs/app.log` en parallèle pour inspecter les prompts et les réponses.
