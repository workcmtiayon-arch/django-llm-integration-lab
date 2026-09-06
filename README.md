# Django LLM Integration Lab

Ce projet est un laboratoire de formation destiné à expérimenter l’intégration de fournisseurs de modèles de langage (LLM) dans Django. Gemini sera le premier fournisseur étudié ; aucune fonctionnalité d’appel LLM n’est encore implémentée.

## Installation

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Copier le modèle de variables d’environnement :

```bash
cp .env.example .env
```

Placer ensuite la clé Gemini dans `GEMINI_API_KEY` dans le fichier `.env`. Ne jamais versionner ce fichier.

## Vérifications et lancement

```bash
python manage.py check
python manage.py migrate
python manage.py runserver 8001
```

L’application `llm_tests` constitue l’espace réservé aux prochaines expérimentations de formation.
