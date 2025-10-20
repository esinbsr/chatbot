<a id="top"></a>

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" alt="Microsoft" height="60">
</p>

<h1 align="center">Chatbot IA multi-agents</h1>

<p align="center">
  <a href="#a-propos">À propos</a> ·
  <a href="#fonctionnalites">Fonctionnalités</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#configuration">Configuration</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="#soutiens">Soutiens</a>
</p>

<p align="center">
  <a href="https://github.com/esinbsr/chatbot-microsoft/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/esinbsr/chatbot-microsoft.svg?style=for-the-badge&color=0e75b6" alt="Contributors">
  </a>
</p>

---

## À propos

Cette branche `main` héberge un chatbot multi-agents conçu pour aider les dirigeants de PME/ETI françaises à identifier des cas d’usage IA tout en offrant un accompagnement RH. L’application combine un routage hybride (mots-clés + similarité sémantique) et un cœur de réponse propulsé par Ollama. Un outil dédié simplifie également la récupération de références juridiques via Legifrance.

---

## Stack & outils

<table align="center">
  <tr>
    <td align="center" width="150">
      <a href="https://www.python.org/" target="_blank" rel="noreferrer">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" height="48" />
        <br /><sub><strong>Python 3.10+</strong></sub>
      </a>
    </td>
    <td align="center" width="150">
      <a href="https://ollama.com/" target="_blank" rel="noreferrer">
        <img src="https://avatars.githubusercontent.com/u/16943930?s=200&v=4" alt="Ollama" height="48" />
        <br /><sub><strong>Ollama + Mistral 7B</strong></sub>
      </a>
    </td>
    <td align="center" width="150">
      <a href="https://www.sbert.net/" target="_blank" rel="noreferrer">
        <img src="https://avatars.githubusercontent.com/u/22535074?s=200&v=4" alt="Sentence Transformers" height="48" />
        <br /><sub><strong>Sentence Transformers</strong></sub>
      </a>
    </td>
    <td align="center" width="150">
      <a href="https://pylegifrance.github.io/pylegifrance/" target="_blank" rel="noreferrer">
        <img src="https://pylegifrance.github.io/pylegifrance/assets/images/logo.svg" alt="PyLegifrance" height="48" />
        <br /><sub><strong>PyLegifrance</strong></sub>
      </a>
    </td>
  </tr>
</table>

---

## Fonctionnalités

- **Routage hybride** : le router combine recherche rapide sur mots-clés et index FAISS pour sélectionner l’agent le plus pertinent.
- **Cœur unifié** : `ChatbotCore` applique les règles globales de `config/agents.yaml` et délègue la génération à Ollama (`mistral:7b-instruct` par défaut).
- **Agents spécialisés** : un expert adoption IA et un consultant CV disposent de prompts dédiés pour guider leurs réponses.
- **Outil Legifrance** : `tools/legifrance.py` initialise PyLegifrance, gère l’authentification et formate les références juridiques utilisées par l’agent `legal`.
- **Préparation RAG** : le dossier `rag/` centralise loader, retriever et vectorstore pour enrichir le contexte conversationnel.
- **Contexte persistant** : l’historique est ajouté au fil des échanges pour conserver la cohérence de la session CLI.

---

## Agents conversationnels

- **ia_pme** : accompagne les dirigeants dans l’identification de cas d’usage IA, des formations et aides disponibles.
- **cv** : fournit des conseils pour améliorer CV et lettres de motivation.
- **legal** : délivre des informations juridiques synthétiques en s’appuyant sur des références Legifrance mises à jour.
- **fallback générique** : si aucun agent ne correspond, la requête repasse par le cœur du chatbot pour une réponse neutre ou un refus.

Les rôles, objectifs, styles et mots-clés sont configurés dans `config/agents.yaml`.

---

## Architecture

1. Le `router` tente d’abord un matching rapide sur les mots-clés déclarés.
2. Sinon, il calcule une similarité via Sentence Transformers + FAISS pour trouver l’agent le plus proche.
3. L’agent identifié assemble son prompt (règles globales + instructions spécifiques) puis appelle `ChatbotCore`.
4. Le contexte conversationnel est mis à jour après chaque échange.

---

## Squelette du projet

```text
chatbot-microsoft/
├── agents/
│   ├── agent_cv.py
│   └── agent_ia_pme.py
├── config/
│   └── agents.yaml
├── data/
├── rag/
│   ├── loader.py
│   ├── retriever.py
│   └── vectorstore.py
├── tools/
│   └── legifrance.py
├── utils/
│   ├── config.py
│   ├── llm.py
│   └── logger.py
├── core.py
├── main.py
├── router.py
├── README.md
└── scripts/
    └── test_global.py (à compléter selon besoins)
```

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/esinbsr/chatbot-microsoft.git
cd chatbot-microsoft

# Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate

# Installer les dépendances principales
pip install --upgrade pip
pip install langchain-ollama sentence-transformers faiss-cpu pylegifrance pyyaml python-dotenv
```

### Préparer Ollama

```bash
ollama pull mistral:7b-instruct
# Vérifier que le serveur Ollama tourne (localhost:11434 par défaut)
```

---

## Configuration

> Astuce : ajoutez ces variables dans un fichier `.env` et chargez-le avec votre outil préféré (`python-dotenv`, `direnv`, etc.).

### API Legifrance
```bash
export LEGIFRANCE_CLIENT_ID="votre_id_legifrance"
export LEGIFRANCE_CLIENT_SECRET="votre_secret_legifrance"
```
<details>
  <summary>Sous Windows (PowerShell)</summary>

  ```powershell
  $Env:LEGIFRANCE_CLIENT_ID = "votre_id_legifrance"
  $Env:LEGIFRANCE_CLIENT_SECRET = "votre_secret_legifrance"
  ```
</details>

### Ollama / modèle
```bash
export OLLAMA_HOST="http://127.0.0.1:11434"  # valeur par défaut
```

---

## Usage

### Lancer le chatbot en local
```bash
python main.py
```
Saisissez vos questions directement dans le terminal. Tapez `exit` pour fermer la session.

### Intégrer Legifrance dans vos prompts
```python
from tools.legifrance import fetch_legifrance_references, format_legifrance_block

refs = fetch_legifrance_references("contrat de travail temps partiel", max_results=3)
print(format_legifrance_block(refs))
```

---

## Roadmap

- [ ] Affiner les seuils FAISS et la détection hors-scope.
- [ ] Brancher le pipeline RAG sur les agents nécessitant un contexte enrichi.
- [ ] Ajouter des tests automatisés (CLI + unitaires) pour valider routes et prompts.
- [ ] Documenter un agent « garde-fou » dédié à la conformité.

---

## Soutiens

Projet porté par Esin, Yasmine, Silene, Gautier et Valentin.<br>
Merci à Microsoft pour l’accompagnement et le sponsoring du défi « À vous l’IA ».

---

<p align="right">
  <a href="#top">⬆ Retour en haut</a>
</p>
