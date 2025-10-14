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

- **Routage intelligent** : combine mots-clés et classification Mistral pour choisir l'agent adapté.
- **Références Legifrance mutualisées** : un outil commun récupère et formate les références juridiques pour tous les agents.
- **Agents spécialisés** : CV/RH, juridique, machine learning, onboarding, relocalisation et garde-fou.
- **Historique contextuel** : chaque interaction utilise un contexte léger pour garder la cohérence des échanges.
- **Test global automatisé** : un script dédié vérifie en série le bon fonctionnement des agents.

---

## Agents conversationnels

- **cv** : valorise expériences et réalisations dans les CV et lettres de motivation.
- **legal** : propose des recommandations conformes en s'appuyant sur Legifrance.
- **ml** : explique des concepts de machine learning avec exemples concrets.
- **onboarding** : construit des plans d'intégration personnalisés pour les nouvelles recrues.
- **reloc** : aide à rédiger les politiques de mobilité interne ou internationale.
- **test** : rappelle les règles d'usage et refuse les demandes sensibles.

---

## Outils partagés

- `tools/legifrance.py` : encapsule l'invocation de PyLegifrance (initialisation, recherche, formatage des références).
- `core.py` : expose des helpers pour récupérer/formater les références et interroger Mistral.
- `router.py` : routeur hybride mots-clés / LLM pour sélectionner l'agent pertinent.
- `scripts/test_global.py` : test cli évaluant l'ensemble des agents avec des prompts représentatifs.

---

## Squelette du projet

```text
chatbot-microsoft/
├── agents/
│   ├── agent_cv.py
│   ├── agent_legal.py
│   ├── agent_ml.py
│   ├── agent_onboarding.py
│   ├── agent_reloc.py
│   └── agent_test.py
├── config/
│   └── agents.yaml
├── tools/
│   ├── __init__.py
│   └── legifrance.py
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
