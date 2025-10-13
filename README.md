<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" alt="Microsoft" height="48">
</p>

# Chatbot IA multi-agents

## Aperçu
Ce projet propose une architecture de chatbot en Python reposant sur plusieurs agents spécialisés
et un routeur qui sélectionne automatiquement l'agent le plus pertinent pour répondre à
l'utilisateur. Le cœur du bot s'appuie sur le SDK `mistralai` et, par défaut, sur le modèle cloud
`mistral-small-latest` (configurable).

## **Contexte du projet**
Microsoft nous engage pour créer un chatbot open source destiné à accompagner les ETI/TPE/PME françaises.  
L'objectif est de proposer un agent conversationnel (à terme déployé sur une page GitHub publique) capable de :
- Identifier des cas d’usage pertinents pour l’IA générative selon le profil de l’entreprise.
- Répondre aux questions sur la formation des collaborateurs et les aides disponibles.

Notes internes et documentation de travail :  
<a href="https://www.notion.so/PROJET-MICROSOFT-A-vous-l-IA-276b73b4f1d480fc91d4e18c799c5c0a#276b73b4f1d480fc91d4e18c799c5c0a" target="_blank" rel="noreferrer">Documentation Notion du projet</a>

## Prérequis
- Python 3.10 ou supérieur
- Un compte Mistral AI avec une clé API valide
- Accès API Legifrance (client_id + client_secret) pour activer l'agent juridique

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # sous Windows : .venv\Scripts\activate
pip install --upgrade pip
pip install mistralai pyyaml pylegifrance
# (optionnel) pip install beautifulsoup4  # pour un nettoyage plus lisible du texte Legifrance
```

## Configuration Legifrance
Renseignez vos identifiants API avant de lancer le chatbot :
```bash
export LEGIFRANCE_CLIENT_ID="votre_id"
export LEGIFRANCE_CLIENT_SECRET="votre_secret"
```
Vous pouvez également les placer dans un fichier `.env` à la racine du projet (grâce à `python-dotenv` installé avec PyLegifrance).

## Configuration de l'API Mistral
Définissez la clé API avant d'exécuter le chatbot :
```bash
export MISTRAL_API_KEY="votre_cle_api"
```
Vous pouvez également l'inscrire dans un fichier `.env` et utiliser un chargeur d'environnement si besoin.

## Lancement du chatbot
```bash
python main.py
```
Le programme ouvre une boucle interactive dans le terminal. Tapez `exit` pour quitter la session.

## Squelette du projet
```text
chatbot-microsoft/
├── agents/
│   ├── agent_cv.py
│   ├── agent_legal.py
│   ├── agent_ml.py
│   └── agent_test.py
├── config/
│   └── agents.yaml
├── scripts/
│   └── test_global.py
├── utils/
│   ├── config.py
│   ├── llm.py
│   └── logger.py
├── core.py
├── main.py
├── router.py
├── README.md
└── logs/
    └── app.log
```

## Architecture des fichiers
- `core.py` : point d'entrée vers le LLM. Injecte les règles globales, applique les options
  Mistral définies dans la configuration et mesure les durées d'appel.
- `router.py` : tente d'abord une classification par mots-clés (rapide), puis interroge un
  modèle Mistral si besoin.
- `config/agents.yaml` : définit les règles globales, les profils de chaque agent
  (rôle, objectif, style) ainsi que les paramètres LLM/router.
- `agents/` : agents spécialisés (CV, juridique, ML, test) préconfigurés.
- `utils/` : utilitaires de configuration, client LLM et journalisation.
- `scripts/test_global.py` : vérifie rapidement que chaque agent répond correctement.
- `logs/` : stocke le journal applicatif (`logs/app.log`).
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
- Ajustez les règles globales, les descriptions d'agents ou les paramètres `llm` / `router` dans `config/agents.yaml`.
- Ajoutez/peaufinez les mots-clés `router.keywords` pour capter vos cas d'usage et éviter la classification LLM.
- Ajoutez de nouveaux agents en créant un fichier dans `agents/` puis en l'enregistrant dans
  `AGENTS_FUNCTIONS` et dans la configuration YAML.

## Tests et benchmark
- Utilisez `test_core.py` pour valider rapidement la connexion au modèle.
- Lancez le test global :  
  `python scripts/test_global.py --pause 3`  
  Paramètres utiles :
  - `--model mistral-tiny-latest` pour comparer un autre modèle.
  - `--temperature 0.5` / `--max-tokens 256` pour ajuster la génération.
- Surveillez `logs/app.log` en parallèle : les durées de routage, de génération LLM et de Legifrance y sont journalisées.
