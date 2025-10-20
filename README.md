<a id="top"></a>

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" alt="Microsoft" height="60">
</p>

<h1 align="center">Chatbot IA multi-agents</h1>

<p align="center">
  <a href="#a-propos">À propos</a> ·
  <a href="#stack--outils">Stack & outils</a> ·
  <a href="#fonctionnalites">Fonctionnalités</a> ·
  <a href="#agents-conversationnels">Agents conversationnels</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#squelette-du-projet">Squelette du projet</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#configuration">Configuration</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#tests">Tests</a> ·
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

Cette branche `main` héberge un chatbot multi-agents conçu pour aider les dirigeants de PME/ETI françaises à identifier des cas d’usage IA tout en offrant un accompagnement RH. L’application combine un routage hybride (mots-clés + similarité sémantique) et un cœur de réponse propulsé par Ollama. Un outil dédié simplifie également la récupération de références juridiques via Legifrance. Ce README centralise les informations indispensables pour prendre en main le projet.

<p align="right"><a href="#top">Retour en haut</a></p>

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
        <img src="https://www.sbert.net/_static/logo.png" alt="Sentence Transformers" height="48" />
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
  <tr>
    <td align="center" width="150">
      <a href="https://www.sqlite.org/index.html" target="_blank" rel="noreferrer">
        <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg" alt="SQLite" height="48" />
        <br /><sub><strong>SQLite</strong></sub>
      </a>
    </td>
    <td align="center" width="150">
      <a href="https://git-scm.com/" target="_blank" rel="noreferrer">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" alt="Git" height="48" />
        <br /><sub><strong>Git</strong></sub>
      </a>
    </td>
  </tr>
</table>

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Fonctionnalités

- **Routage hybride** : le router combine recherche rapide sur mots-clés et index FAISS pour sélectionner l’agent le plus pertinent.
- **Cœur unifié** : `ChatbotCore` applique les règles globales de `config/agents.yaml` et délègue la génération à Ollama (`mistral:7b-instruct` par défaut).
- **Agents spécialisés** : un expert adoption IA et un consultant CV disposent de prompts dédiés pour guider leurs réponses.
- **Outil Legifrance** : `tools/legifrance.py` initialise PyLegifrance, gère l’authentification et formate les références juridiques utilisées par l’agent `legal`.
- **Préparation RAG** : le dossier `rag/` centralise loader, retriever et vectorstore pour enrichir le contexte conversationnel.
- **Stockage SQLite léger** : `sqlite3/bdd.py` prépare la table `data_form` pour tracer les cas d’usage identifiés.
- **Journalisation centralisée** : `utils/logger.py` configure un logger partagé qui alimente `logs/app.log`.
- **Contexte persistant** : l’historique est ajouté au fil des échanges pour conserver la cohérence de la session CLI.

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Agents conversationnels

- **ia_pme** : accompagne les dirigeants dans l’identification de cas d’usage IA, des formations et aides disponibles.
- **cv** : fournit des conseils pour améliorer CV et lettres de motivation.
- **legal** : délivre des informations juridiques synthétiques en s’appuyant sur des références Legifrance mises à jour.
- **fallback générique** : si aucun agent ne correspond, la requête repasse par le cœur du chatbot pour une réponse neutre ou un refus.

Les rôles, objectifs, styles et mots-clés sont configurés dans `config/agents.yaml`.

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Architecture

1. Le `router` tente d’abord un matching rapide sur les mots-clés déclarés.
2. Sinon, il calcule une similarité via Sentence Transformers + FAISS pour trouver l’agent le plus proche.
3. L’agent identifié assemble son prompt (règles globales + instructions spécifiques) puis appelle `ChatbotCore`.
4. Le contexte conversationnel est mis à jour après chaque échange.
5. Les informations structurées peuvent être persistées via la base SQLite initialisée dans `sqlite3/bdd.py`.

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Squelette du projet

```text
chatbot-microsoft/
├── agents/
│   ├── agent_cv.py
│   ├── agent_ia_pme.py
│   └── agent_legal.py
├── config/
│   └── agents.yaml
├── data/
│   ├── inputs/
│   └── outputs/
├── rag/
│   ├── get_embedding_function.py
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
├── logs/
│   └── app.log (généré automatiquement)
├── README.md
├── scripts/            # répertoire réservé aux tests/automation
└── sqlite3/
    └── bdd.py
```

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/esinbsr/chatbot-microsoft.git
cd chatbot-microsoft
```

### Créer et activer un environnement virtuel (Linux / macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
```
<details>
  <summary>Sous Windows (PowerShell)</summary>

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
</details>

### Installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Préparer Ollama

```bash
ollama pull mistral:7b-instruct
# Vérifier que le serveur Ollama tourne (localhost:11434 par défaut)
```

<p align="right"><a href="#top">Retour en haut</a></p>

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

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Usage

### Lancer le chatbot en local
```bash
python3 main.py
```
Saisissez vos questions directement dans le terminal. Tapez `exit` pour fermer la session.

<details>
  <summary>Sous Windows (PowerShell)</summary>

  ```powershell
  python main.py
  ```
</details>

> Les échanges et avertissements sont journalisés dans `logs/app.log` (créé automatiquement).

### Initialiser la base SQLite
```bash
python sqlite3/bdd.py
```
Ce script crée le fichier `data_form.db` (s’il n’existe pas) avec la table `data_form`. Vous pouvez ensuite l’inspecter via `sqlite3 data_form.db` ou tout outil compatible.

### Intégrer Legifrance dans vos prompts
```python
from tools.legifrance import fetch_legifrance_references, format_legifrance_block

refs = fetch_legifrance_references("contrat de travail temps partiel", max_results=3)
print(format_legifrance_block(refs))
```

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Tests

Le script `scripts/test_modele.py` exécute une batterie légère d’unitaires qui :

- Valident le routage (mots-clés) pour chacun des agents actifs (`ia_pme`, `cv`, `legal`).
- Vérifient que l’agent `legal` cite correctement les références Legifrance lorsqu’elles sont disponibles.
- Journalisent un flux de bout en bout avec un cœur de chatbot simulé (`DummyCore`) pour garder le test lisible et compatible PEP 8.

```bash
python3 scripts/test_modele.py
```

<details>
  <summary>Sous Windows (PowerShell)</summary>

  ```powershell
  python scripts/test_modele.py
  ```
</details>

Les dépendances externes (Ollama, Sentence Transformers, FAISS) sont simulées afin que le test reste déterministe et rapide.

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Roadmap

- [ ] Affiner les seuils FAISS et la détection hors-scope.
- [ ] Brancher le pipeline RAG sur les agents nécessitant un contexte enrichi.
- [ ] Ajouter des tests automatisés (CLI + unitaires) pour valider routes et prompts.
- [ ] Documenter un agent « garde-fou » dédié à la conformité.

<p align="right"><a href="#top">Retour en haut</a></p>

---

## Soutiens

Projet porté par Esin, Yasmine, Silene, Gautier et Valentin.<br>
Merci à Microsoft pour l’accompagnement et le sponsoring du défi « À vous l’IA ».

---

<p align="right">
  <a href="#top">Retour en haut</a>
</p>
