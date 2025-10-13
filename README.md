<a id="top"></a>

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" alt="Microsoft" height="60">
</p>

<h1 align="center">Chatbot IA multi-agents</h1>

<p align="center">
  <a href="#a-propos">À propos</a> ·
  <a href="#fonctionnalités">Fonctionnalités</a> ·
  <a href="#installation">Installation</a> ·
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

Ce projet open source, soutenu par Microsoft, vise à accompagner les ETI/TPE/PME françaises dans leur transition vers l'IA générative. L'objectif est de proposer un agent conversationnel déployable sur GitHub qui :

- identifie des cas d'usage IA pertinents selon le profil de l'entreprise ;
- répond aux questions sur la formation des collaborateurs et les aides disponibles ;
- s'appuie sur des sources fiables (Legifrance) pour les aspects juridiques.

> Notes internes : <a href="https://www.notion.so/PROJET-MICROSOFT-A-vous-l-IA-276b73b4f1d480fc91d4e18c799c5c0a#276b73b4f1d480fc91d4e18c799c5c0a" target="_blank" rel="noreferrer">Documentation Notion du projet</a>

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
      <a href="https://mistral.ai/" target="_blank" rel="noreferrer">
        <img src="https://avatars.githubusercontent.com/u/146620074?s=200&v=4" alt="Mistral AI" height="48" />
        <br /><sub><strong>Mistral AI</strong></sub>
      </a>
    </td>
    <td align="center" width="150">
      <a href="https://pylegifrance.github.io/pylegifrance/" target="_blank" rel="noreferrer">
        <img src="https://pylegifrance.github.io/pylegifrance/assets/images/logo.svg" alt="PyLegifrance" height="48" />
        <br /><sub><strong>PyLegifrance</strong></sub>
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

---

## Fonctionnalités

- **Routage intelligent** : combine mots-clés et classification Mistral pour choisir l'agent adapté (CV, juridique, ML, test).
- **Agent juridique** : interroge Legifrance pour proposer des références fiables (contrats, litiges, veille réglementaire).
- **Agent RH/CV** : améliore CV, lettres de motivation et profils professionnels.
- **Agent pédagogique ML** : vulgarise les concepts de machine learning avec des exemples concrets.
- **Gardien des règles** : l'agent test rappelle les limitations et refus de contenus sensibles.
- **Historique contextuel** : chaque interaction utilise un contexte léger pour garder la cohérence des échanges.

---

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

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/esinbsr/chatbot-microsoft.git
cd chatbot-microsoft

# Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate

# Installer les dépendances
pip install --upgrade pip
pip install mistralai pylegifrance pyyaml
# Optionnel : meilleure mise en forme des données Legifrance
pip install beautifulsoup4
```

---

## Configuration

### API Legifrance
```bash
export LEGIFRANCE_CLIENT_ID="votre_id"
export LEGIFRANCE_CLIENT_SECRET="votre_secret"
```
<details>
  <summary>Sous Windows (PowerShell)</summary>

  ```powershell
  $Env:LEGIFRANCE_CLIENT_ID = "votre_id"
  $Env:LEGIFRANCE_CLIENT_SECRET = "votre_secret"
  ```
</details>

### API Mistral
```bash
export MISTRAL_API_KEY="votre_cle_api"
```

_Placez ces variables dans un fichier `.env` si vous utilisez un chargeur d'environnement._


<details>
  <summary>Sous Windows (PowerShell)</summary>

  ```powershell
  $Env:MISTRAL_API_KEY = "votre_cle_api"
  ```
</details>

---

## Usage

### Lancer le chatbot
```bash
python main.py
```
Tapez `exit` pour quitter la session.

### Test global
```bash
python scripts/test_global.py --pause 3
```
Options utiles :
- `--model mistral-tiny-latest` pour tester un modèle plus léger.
- `--temperature 0.5` et `--max-tokens 256` pour ajuster la génération.

Les temps de routage / réponse et les erreurs éventuelles sont visibles dans le terminal et dans `logs/app.log`.

---

## Roadmap

- [ ] À compléter (prochaines étapes à définir avec l'équipe).

---

## Soutiens

Projet porté par Esin, Yasmine, Silene, Gautier et Valentin.<br>
Merci à Microsoft pour l'accompagnement et le sponsoring du défi « À vous l’IA ».

---

<p align="right">
  <a href="#top">⬆ Retour en haut</a>
</p>
