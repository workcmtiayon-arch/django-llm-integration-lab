# Django LLM Integration Lab

Projet de formation Django consacré à l’intégration de fournisseurs de modèles de langage. Il comprend une app d’authentification réutilisable, `accounts`, et un espace `llm_tests` pour les expérimentations Gemini.

## Fonctionnalités

- Inscription avec adresse email normalisée et connexion insensible à la casse, ainsi que la validation native des mots de passe Django.
- Connexion par email, déconnexion par POST et gestion des sessions Django.
- Profil privé avec biographie, modification de l’email et des informations personnelles.
- Réseau social : invitations d’amitié, gestion des amis et profils publics.
- Publications texte et image, publiques ou réservées aux amis, fil d’actualité, mentions « J’aime » et commentaires.
- Notifications lors d’une invitation et de son acceptation.
- Photo de profil JPEG, PNG ou WebP (5 Mo maximum), avec vérification du contenu et nom de fichier généré par l’application.
- Changement et réinitialisation de mot de passe avec les vues et jetons natifs Django.
- Protection CSRF, contrôle des redirections de connexion, routes privées et messages utilisateur.
- Configuration par environnement pour les secrets, la base de données et le courrier.

## Stack technique

- Python 3.12
- Django 6.1
- SQLite par défaut; autres moteurs Django configurables avec `DB_ENGINE` et `DB_*`.
- Pillow pour la lecture et la validation des images.
- `python-dotenv` pour charger un fichier `.env` local.

## Structure

```text
config/                 Réglages, ASGI/WSGI et URLs du projet
accounts/               Modèle utilisateur, formulaires, vues, migrations et templates
social/                 Réseau social : relations, publications, vues, permissions et templates
  core/                 Modèles de base partagés
  utils/                Enums, permissions et signaux métier
llm_tests/              Exercices d’intégration Gemini
docs/                   Notes locales d’expérimentation
manage.py               Commandes Django
requirements.txt        Dépendances Python
.env.example            Exemple sans secret
```

## Installation locale

Utilisez Python 3.12, créez un environnement virtuel, puis installez les dépendances :

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Créez votre fichier d’environnement local :

```bash
cp .env.example .env
```

Générez une clé Django aléatoire et placez le résultat dans `SECRET_KEY` de `.env` :

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Ne copiez pas cette clé dans le dépôt. `.env` est ignoré par Git. Une clé Gemini n’est nécessaire que pour exécuter les exemples correspondants; ne lancez pas les scripts Gemini avant d’avoir renseigné `GEMINI_API_KEY`.

Appliquez les migrations et lancez le serveur :

```bash
python manage.py migrate
python manage.py runserver 8001
```

L’interface d’authentification est disponible sous `/accounts/`. Créez un compte via `/accounts/register/` ou un compte administrateur avec `python manage.py createsuperuser`.

## Base de données

SQLite est utilisé par défaut. Pour un autre backend Django, définissez `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` et `DB_PORT` dans l’environnement. Installez le pilote correspondant au moteur choisi (par exemple Psycopg pour PostgreSQL) dans l’environnement de déploiement.

Le modèle `accounts.User` est configuré comme `AUTH_USER_MODEL`; gardez ce choix avant la première migration d’un nouveau déploiement. Le fichier SQLite ignoré dans ce dépôt peut provenir d’expérimentations antérieures et ne constitue pas une base de données à publier. Sauvegardez toute base contenant des données avant une mise à niveau ou une réparation de son historique de migrations. Pour une nouvelle installation, la base est créée proprement par `migrate`.

## Emails

En développement, le backend console de Django affiche les messages dans le terminal. Cela permet de tester la réinitialisation sans serveur SMTP. En production, fournissez au minimum :

```text
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=no-reply@example.com
```

Gardez les identifiants SMTP dans l’environnement du service et jamais dans Git. N’activez pas TLS et SSL simultanément.

## Médias et fichiers statiques

En local, les photos sont stockées sous `MEDIA_ROOT` (`media/`) et servies par Django uniquement lorsque `DEBUG=True`. Les fichiers uploadés et les résultats de `collectstatic` sont ignorés par Git.

En production, configurez un stockage média privé ou objet et un serveur web/CDN pour les fichiers statiques. Ne servez pas des uploads non contrôlés comme du code exécutable. Lancez :

```bash
python manage.py collectstatic
```

## Tests et contrôles

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Le contrôle de déploiement doit utiliser les réglages production et les vrais noms de domaine :

```bash
DJANGO_SETTINGS_MODULE=config.settings_production python manage.py check --deploy
```

Dans `config/settings_production.py`, HTTPS et les cookies sécurisés sont obligatoires. Définissez `SECRET_KEY` (50 caractères aléatoires ou plus), `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS`. `SECURE_HSTS_PRELOAD` est optionnel; activez-le seulement après avoir confirmé que tout le domaine et ses sous-domaines répondent durablement en HTTPS. `TRUST_X_FORWARDED_PROTO=True` ne doit être utilisé que derrière un proxy de confiance configuré pour réécrire cet en-tête.

Pour SQLite, indiquez `DB_ENGINE=django.db.backends.sqlite3` et un chemin `DB_NAME`. Pour PostgreSQL ou un autre moteur, fournissez aussi les paramètres `DB_*` et le pilote correspondant.

## URLs de compte

| Route | Usage |
| --- | --- |
| `/accounts/register/` | Inscription |
| `/accounts/login/` | Connexion par email |
| `/accounts/logout/` | Déconnexion (POST) |
| `/accounts/profile/` | Profil authentifié |
| `/accounts/profile/edit/` | Modification du profil |
| `/accounts/profile/photo/` | Téléversement/remplacement de la photo |
| `/accounts/password/change/` | Changement du mot de passe |
| `/accounts/password/reset/` | Demande de réinitialisation |

## Réseau social

Après connexion, le fil d’actualité est accessible à `/`. Les membres peuvent y publier du texte, choisir entre une visibilité publique et une visibilité réservée aux amis, aimer et commenter les publications visibles.

| Route | Usage |
| --- | --- |
| `/` | Fil d’actualité personnel |
| `/membres/` | Recherche de membres et invitations |
| `/amis/` | Liste des amis et retrait d’une relation |
| `/invitations/` | Acceptation, refus ou annulation des invitations |
| `/profil/<id>/` | Profil public et publications visibles de ce membre |

Les opérations d’écriture utilisent des requêtes POST protégées par CSRF. Les vues vérifient l’identité de l’auteur avant modification ou suppression, le destinataire avant réponse à une invitation et les relations d’amitié avant l’accès aux publications réservées. Les permissions Django comprennent `social.moderate_post` pour la modération.

Après mise à jour du dépôt, appliquez les migrations avec `python manage.py migrate`.

## Sécurité

- Les secrets sont chargés depuis l’environnement; aucun secret réel ne doit être commité.
- Les mots de passe utilisent les validateurs, le hachage et les formulaires Django.
- Django protège les formulaires contre CSRF et échappe le contenu des templates.
- Les pages du profil exigent une session authentifiée et ciblent uniquement l’utilisateur connecté.
- Le paramètre `next` est validé par `LoginView` avant redirection.
- Les cookies de session et CSRF sont `HttpOnly`; le profil production active `Secure`.
- Les fichiers photo sont limités en taille et contrôlés par leur contenu réel.

## Préparer une contribution GitHub

Avant un commit, vérifiez que `.env`, les bases locales, médias, caches et identifiants ne sont pas suivis :

```bash
git status
git check-ignore -v .env db.sqlite3 media/
git diff --check
git add <fichiers-vérifiés>
git commit -m "type: describe the change"
git push origin <branche>
```

Ne commitez jamais `.env`, une clé Gemini, une clé Django ou un mot de passe SMTP. Ajoutez uniquement les fichiers du changement concerné.
