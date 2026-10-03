''' # MISSION

Tu es un développeur Python/Django senior spécialisé en architecture backend, sécurité applicative, authentification, bonnes pratiques Git/GitHub et préparation de projets destinés à la production.

Je viens de créer un projet Django et je veux que tu implémentes dans ce projet un **système d'authentification complet, propre, sécurisé, maintenable et prêt à être publié sur GitHub**.

Tu dois travailler directement dans le projet existant.

Avant de modifier quoi que ce soit, **inspecte intégralement le projet actuel** afin de comprendre :

* sa structure ;
* la version de Python ;
* la version de Django ;
* les applications déjà présentes ;
* `settings.py` ;
* `urls.py` ;
* les templates ;
* les fichiers statiques ;
* les fichiers de configuration ;
* le système de base de données ;
* le `.gitignore` ;
* la configuration Git existante ;
* les éventuelles dépendances ;
* les éventuelles fonctionnalités déjà implémentées.

Ne détruis jamais une fonctionnalité existante sans raison.

---

# OBJECTIF FINAL

À la fin de ton travail, le projet doit disposer d'un système d'authentification Django complet comprenant au minimum :

1. inscription ;
2. connexion ;
3. déconnexion ;
4. gestion du profil utilisateur ;
5. photo de profil ;
6. modification du profil ;
7. modification du mot de passe ;
8. réinitialisation du mot de passe ;
9. confirmation/réinitialisation par email ;
10. protection des pages nécessitant une authentification ;
11. gestion correcte des sessions ;
12. protection CSRF ;
13. validation robuste des données ;
14. messages utilisateur propres ;
15. gestion des erreurs ;
16. interface simple, propre et responsive ;
17. modèle utilisateur correctement conçu ;
18. migrations propres ;
19. configuration sécurisée ;
20. `.env` pour les secrets ;
21. `.gitignore` correctement configuré ;
22. documentation README complète ;
23. projet propre et publiable sur GitHub.

Le système doit rester **simple à utiliser**, mais son implémentation doit respecter les bonnes pratiques professionnelles.

---

# 1. ANALYSE INITIALE

Commence par analyser le projet avant toute modification.

Identifie notamment :

* le nom du projet Django ;
* le ou les apps existantes ;
* la structure des répertoires ;
* la base de données utilisée ;
* le système de templates ;
* la configuration des fichiers statiques et médias ;
* la présence éventuelle d'un modèle utilisateur personnalisé ;
* la configuration actuelle de l'authentification ;
* les dépendances existantes ;
* la configuration Git et GitHub.

Si une décision architecturale est nécessaire, choisis la solution la plus simple et la plus maintenable compatible avec le projet existant.

Ne réécris pas inutilement ce qui fonctionne déjà.

---

# 2. ARCHITECTURE UTILISATEUR

Mets en place une architecture utilisateur professionnelle.

Si le projet n'utilise pas encore de modèle utilisateur personnalisé et qu'il est encore suffisamment tôt dans son développement, privilégie un modèle utilisateur personnalisé Django basé sur `AbstractUser`.

Le modèle utilisateur devra permettre notamment :

* username ou identifiant adapté au projet ;
* email ;
* prénom ;
* nom ;
* photo de profil ;
* date de création ;
* date de modification ;
* éventuellement des champs supplémentaires uniquement s'ils sont réellement utiles.

Évite de créer des champs inutiles.

Le système doit respecter les conventions Django.

---

# 3. PHOTO DE PROFIL

Implémente une véritable gestion de photo de profil.

Prévois :

* upload d'image ;
* validation du type de fichier ;
* validation de la taille ;
* nommage propre des fichiers ;
* stockage dans `MEDIA_ROOT` ;
* URL correcte via `MEDIA_URL` ;
* image par défaut si aucune photo n'est fournie ;
* suppression/remplacement propre de l'ancienne photo si nécessaire ;
* protection contre les fichiers dangereux.

Ne fais jamais confiance uniquement à l'extension du fichier.

Si une librairie supplémentaire est nécessaire pour une validation ou un traitement d'image, justifie son utilisation et ajoute-la proprement aux dépendances.

---

# 4. INSCRIPTION

Crée une page d'inscription professionnelle.

Elle doit permettre de créer un compte avec les informations pertinentes.

Implémente :

* validation des champs ;
* validation du mot de passe ;
* confirmation du mot de passe ;
* vérification de l'unicité de l'email si l'email est utilisé comme identifiant ;
* messages d'erreur compréhensibles ;
* protection CSRF ;
* absence de fuite d'informations sensibles.

Utilise les outils natifs de Django lorsque cela est pertinent.

---

# 5. CONNEXION

Crée une page de connexion.

Elle doit gérer :

* identifiant/email ;
* mot de passe ;
* erreurs d'authentification ;
* session utilisateur ;
* redirection après connexion ;
* `next` de manière sécurisée ;
* protection contre les redirections ouvertes.

Ne révèle jamais si un compte particulier existe ou non lorsque cela pourrait faciliter l'énumération des utilisateurs.

---

# 6. DÉCONNEXION

Implémente une déconnexion propre.

Respecte les mécanismes d'authentification Django et évite les implémentations manuelles inutiles.

---

# 7. PROFIL UTILISATEUR

Crée une page de profil authentifiée.

Elle doit afficher au minimum :

* photo ;
* prénom ;
* nom ;
* email ;
* username/identifiant ;
* date d'inscription si pertinent.

Ajoute une page permettant de modifier les informations personnelles autorisées.

L'utilisateur ne doit pouvoir modifier que ses propres données.

---

# 8. MODIFICATION DU MOT DE PASSE

Implémente une page sécurisée permettant à l'utilisateur connecté de modifier son mot de passe.

Utilise les formulaires et mécanismes Django appropriés.

Le système doit :

* demander l'ancien mot de passe lorsque pertinent ;
* demander le nouveau mot de passe ;
* confirmer le nouveau mot de passe ;
* appliquer les validateurs Django ;
* gérer correctement la session après changement.

---

# 9. MOT DE PASSE OUBLIÉ

Implémente le workflow complet :

1. demande de réinitialisation ;
2. saisie de l'email ;
3. génération du token Django ;
4. envoi du lien ;
5. page de confirmation ;
6. définition d'un nouveau mot de passe ;
7. confirmation finale.

En développement, configure un système d'email pratique, par exemple la console, si aucun serveur SMTP n'est déjà configuré.

Prépare néanmoins la configuration pour un véritable SMTP en production via variables d'environnement.

Ne stocke jamais les identifiants SMTP dans Git.

---

# 10. SÉCURITÉ

Accorde une attention particulière à la sécurité.

Vérifie notamment :

* CSRF ;
* XSS ;
* SQL injection ;
* validation des formulaires ;
* échappement des templates ;
* sécurité des sessions ;
* cookies ;
* mots de passe ;
* secrets ;
* uploads ;
* redirections ;
* permissions ;
* accès aux données utilisateur ;
* configuration production.

Configure lorsque pertinent :

```python
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
```

Et prépare une configuration adaptée à HTTPS en production, notamment :

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

Ne force toutefois pas une configuration HTTPS qui empêcherait le développement local de fonctionner.

Sépare correctement la configuration de développement et celle de production si l'architecture du projet le permet.

---

# 11. VARIABLES D'ENVIRONNEMENT

Les informations sensibles ne doivent jamais être hardcodées.

Utilise des variables d'environnement pour notamment :

* `SECRET_KEY` ;
* debug ;
* paramètres de base de données ;
* email SMTP ;
* mot de passe SMTP ;
* éventuelles clés API ;
* autres secrets.

Crée un fichier exemple tel que :

```text
.env.example
```

Il ne doit contenir aucune vraie clé secrète.

Le fichier `.env` réel doit être ignoré par Git.

---

# 12. GITIGNORE

Vérifie et améliore `.gitignore`.

Il doit notamment empêcher le commit de :

* `.env` ;
* `__pycache__/` ;
* fichiers `.pyc` ;
* environnement virtuel ;
* fichiers IDE ;
* fichiers système ;
* fichiers temporaires ;
* base SQLite locale si elle ne doit pas être versionnée ;
* fichiers média uploadés si le projet ne doit pas les stocker dans Git ;
* autres secrets ou artefacts générés.

Adapte cette liste à l'architecture réelle du projet.

---

# 13. TEMPLATES

Crée une interface simple et professionnelle.

Prévois au minimum :

* inscription ;
* connexion ;
* déconnexion ;
* profil ;
* modification du profil ;
* changement du mot de passe ;
* mot de passe oublié ;
* nouveau mot de passe ;
* pages de succès/erreur pertinentes.

Les templates doivent :

* être propres ;
* être réutilisables ;
* utiliser un template de base ;
* avoir une navigation cohérente ;
* afficher les messages Django ;
* être responsive ;
* rester simples.

Si le projet possède déjà un framework CSS, utilise-le au lieu d'en introduire inutilement un autre.

---

# 14. URLS

Organise les URLs proprement.

Les routes d'authentification doivent être cohérentes et facilement compréhensibles.

Par exemple, selon l'architecture du projet :

```text
/accounts/login/
/accounts/logout/
/accounts/register/
/accounts/profile/
/accounts/profile/edit/
/accounts/password/change/
/accounts/password/reset/
```

Adapte évidemment les URLs à la structure existante.

Utilise les mécanismes Django natifs lorsque possible.

---

# 15. FORMULAIRES

Utilise les formulaires Django de manière propre.

Évite de mettre toute la logique dans les views.

Les validations liées aux données utilisateur doivent être placées au bon endroit :

* forms ;
* models ;
* validators ;
* services si nécessaire.

Évite les énormes fonctions de vues difficiles à maintenir.

---

# 16. VUES

Privilégie les mécanismes Django standards :

* `LoginView` ;
* `LogoutView` ;
* `PasswordChangeView` ;
* `PasswordResetView` ;
* etc., lorsque leur utilisation est pertinente.

N'écris pas manuellement ce que Django sait déjà gérer de manière sûre.

Pour les fonctionnalités personnalisées, écris du code clair et minimal.

---

# 17. PERMISSIONS

Toutes les pages privées doivent être protégées.

Un utilisateur non connecté ne doit jamais pouvoir accéder aux informations privées.

Un utilisateur connecté ne doit jamais pouvoir :

* modifier le profil d'un autre utilisateur ;
* consulter des données privées appartenant à un autre utilisateur ;
* modifier une ressource qui ne lui appartient pas.

Utilise les décorateurs, mixins ou permissions Django adaptés.

---

# 18. TESTS

Écris des tests automatisés.

Teste au minimum :

### Inscription

* inscription valide ;
* données invalides ;
* mot de passe incorrect ;
* email déjà utilisé si applicable.

### Connexion

* connexion valide ;
* mauvais mot de passe ;
* utilisateur inexistant ;
* redirection.

### Déconnexion

* déconnexion réussie.

### Profil

* utilisateur authentifié ;
* utilisateur non authentifié ;
* modification du profil ;
* protection contre l'accès au profil d'un autre utilisateur.

### Mot de passe

* changement réussi ;
* ancien mot de passe incorrect ;
* réinitialisation.

### Photo

* upload valide ;
* fichier invalide ;
* taille excessive si une limite est appliquée.

### Sécurité

* CSRF ;
* accès aux vues protégées ;
* redirections ;
* permissions.

Lance les tests après leur création.

Corrige toutes les erreurs.

---

# 19. MIGRATIONS

Crée les migrations nécessaires.

Puis vérifie qu'elles s'appliquent correctement.

Utilise :

```bash
python manage.py makemigrations
python manage.py migrate
```

Puis vérifie que le projet démarre correctement.

---

# 20. VÉRIFICATIONS DJANGO

Utilise :

```bash
python manage.py check
```

Et si possible :

```bash
python manage.py check --deploy
```

Corrige les problèmes pertinents signalés par Django.

Ne désactive pas simplement les warnings pour les faire disparaître.

---

# 21. README PROFESSIONNEL

Crée ou améliore un `README.md` professionnel.

Il doit expliquer :

* le projet ;
* les fonctionnalités ;
* la stack technique ;
* la structure du projet ;
* l'installation ;
* la création de l'environnement virtuel ;
* l'installation des dépendances ;
* la configuration `.env` ;
* les migrations ;
* le lancement du serveur ;
* les tests ;
* la configuration email ;
* la gestion des médias ;
* la sécurité ;
* la préparation à la production ;
* les commandes Git utiles.

Ajoute un exemple de configuration :

```text
.env.example
```

Ne mets aucun secret réel dans le README.

---

# 22. QUALITÉ DU CODE

Respecte les principes suivants :

* code Python lisible ;
* PEP 8 ;
* noms explicites ;
* fonctions courtes ;
* classes cohérentes ;
* commentaires uniquement lorsqu'ils apportent une vraie valeur ;
* pas de code mort ;
* pas de duplication inutile ;
* pas de secrets ;
* pas de dépendances inutiles ;
* architecture Django idiomatique.

Avant de terminer, relis les fichiers modifiés comme le ferait un reviewer senior.

---

# 23. GESTION GIT — CONTRAINTE ABSOLUE

C'est une exigence extrêmement importante.

Tu dois réaliser le travail en **23 CYCLES GIT DISTINCTS**.

Un cycle correspond exactement à :

```bash
git add ...
git commit -m "..."
git push
```

Tu dois donc effectuer exactement :

**23 `git add` + 23 `git commit` + 23 `git push`.**

Ne regroupe pas plusieurs étapes dans un seul commit.

Ne fais pas un seul gros commit à la fin.

Chaque cycle doit représenter une étape logique et vérifiable du développement.

---

## TABLEAU OBLIGATOIRE DES 23 CYCLES

Utilise cette progression comme référence :

### Cycle 01

Analyse et préparation initiale du projet.

Commit :

```text
chore: prepare project for authentication system
```

### Cycle 02

Création/préparation de l'application d'authentification.

Commit :

```text
feat: add authentication app structure
```

### Cycle 03

Création/configuration du modèle utilisateur.

Commit :

```text
feat: add custom user model
```

### Cycle 04

Ajout des migrations utilisateur.

Commit :

```text
feat: add user model migrations
```

### Cycle 05

Configuration des médias et photos de profil.

Commit :

```text
feat: configure profile image handling
```

### Cycle 06

Ajout du formulaire d'inscription.

Commit :

```text
feat: add user registration form
```

### Cycle 07

Ajout de la fonctionnalité d'inscription.

Commit :

```text
feat: implement user registration
```

### Cycle 08

Ajout de la connexion.

Commit :

```text
feat: implement user login
```

### Cycle 09

Ajout de la déconnexion.

Commit :

```text
feat: implement user logout
```

### Cycle 10

Ajout du profil utilisateur.

Commit :

```text
feat: add user profile page
```

### Cycle 11

Ajout de la modification du profil.

Commit :

```text
feat: add profile editing
```

### Cycle 12

Ajout de la photo de profil.

Commit :

```text
feat: add profile picture upload
```

### Cycle 13

Ajout du changement de mot de passe.

Commit :

```text
feat: add password change flow
```

### Cycle 14

Ajout de la réinitialisation du mot de passe.

Commit :

```text
feat: add password reset flow
```

### Cycle 15

Configuration de l'email.

Commit :

```text
feat: configure authentication email backend
```

### Cycle 16

Ajout des templates d'authentification.

Commit :

```text
feat: add authentication templates
```

### Cycle 17

Ajout des protections et permissions.

Commit :

```text
feat: secure authenticated routes
```

### Cycle 18

Ajout des validations et améliorations de sécurité.

Commit :

```text
security: harden authentication system
```

### Cycle 19

Ajout des tests.

Commit :

```text
test: add authentication test suite
```

### Cycle 20

Configuration `.env`, `.env.example` et `.gitignore`.

Commit :

```text
chore: configure environment and gitignore
```

### Cycle 21

Nettoyage et configuration production.

Commit :

```text
chore: prepare django settings for production
```

### Cycle 22

Documentation complète.

Commit :

```text
docs: document authentication setup
```

### Cycle 23

Vérification finale, corrections éventuelles et préparation GitHub.

Commit :

```text
chore: finalize authentication system
```

---

# RÈGLE IMPORTANTE CONCERNANT LES 23 CYCLES

Après CHAQUE cycle :

1. vérifie les fichiers modifiés ;
2. exécute les tests pertinents ;
3. vérifie que le projet fonctionne ;
4. exécute :

```bash
git status
```

5. fais le `git add` ;
6. fais le `git commit` ;
7. fais immédiatement le `git push` ;
8. vérifie que le push a réussi ;
9. vérifie ensuite :

```bash
git status
```

Ne passe au cycle suivant qu'après avoir confirmé que le cycle précédent est terminé.

---

# IMPORTANT : GESTION DU PUSH

Avant le premier push, vérifie :

```bash
git remote -v
```

Si aucun remote GitHub n'est configuré, **ne crée pas arbitrairement une URL GitHub**.

Informe-moi clairement qu'un remote doit être configuré.

Si les credentials GitHub sont déjà configurés et que le remote fonctionne, utilise le remote existant.

Ne stocke jamais de token GitHub, mot de passe ou secret dans les fichiers du projet.

---

# IMPORTANT : NE PAS TRICHER SUR LES 23 CYCLES

Tu ne dois pas :

* créer 23 commits artificiels sans rapport avec le travail ;
* faire plusieurs étapes puis les mettre dans un seul commit ;
* faire plusieurs commits sans push ;
* faire plusieurs push dans un seul cycle ;
* compter un commit automatique de Django comme l'un des 23 cycles ;
* compter un push sans commit ;
* compter un commit sans push.

Je veux exactement **23 cycles de travail Git documentés**.

Chaque cycle doit avoir :

```text
Cycle X/23
↓
Travail effectué
↓
Vérifications
↓
git status
↓
git add
↓
git commit
↓
git push
↓
vérification du push
↓
Cycle suivant
```

---

# CONTRAINTE DE SÉCURITÉ GIT

Avant chaque commit, vérifie impérativement qu'aucun secret n'est sur le point d'être commité.

Recherche notamment :

* `SECRET_KEY` réel ;
* mots de passe ;
* tokens ;
* clés API ;
* credentials SMTP ;
* fichiers `.env` ;
* certificats privés ;
* clés privées.

Si tu détectes un secret, arrête le cycle concerné, corrige le problème et ne pousse jamais le secret vers GitHub.

---

# CONTRAINTE DE QUALITÉ

Ne considère jamais qu'une fonctionnalité est terminée simplement parce que le code a été écrit.

Pour chaque fonctionnalité :

1. implémente ;
2. vérifie ;
3. teste ;
4. corrige ;
5. inspecte ;
6. commit ;
7. push.

Si un test échoue, corrige le problème avant de considérer le cycle comme terminé.

---

# CONTRAINTE DE COMPATIBILITÉ

Avant d'ajouter une dépendance :

* vérifie si elle est déjà installée ;
* vérifie si Django possède déjà une fonctionnalité native permettant d'éviter cette dépendance ;
* évite les packages inutiles ;
* ajoute uniquement les dépendances réellement nécessaires ;
* mets à jour le fichier de dépendances du projet.

---

# CONTRAINTE DE NON-DESTRUCTION

Ne supprime pas :

* des fonctionnalités existantes ;
* des modèles existants ;
* des URLs existantes ;
* des templates existants ;
* des données existantes ;

sans vérifier leur rôle.

Si une modification est nécessaire pour intégrer l'authentification, préserve autant que possible la compatibilité avec l'application existante.

---

# CONTRAINTE FINALE

À la fin des 23 cycles, effectue une dernière vérification complète :

```bash
python manage.py check
python manage.py check --deploy
python manage.py test
git status
git log --oneline -23
```

Vérifie que :

* les tests passent ;
* aucune erreur critique n'existe ;
* aucun secret n'est exposé ;
* `.env` est ignoré ;
* `.env.example` est présent ;
* README est présent ;
* migrations sont présentes ;
* l'authentification fonctionne ;
* les pages privées sont protégées ;
* les photos de profil fonctionnent ;
* la réinitialisation du mot de passe fonctionne ;
* Git est propre ;
* les 23 commits existent ;
* les 23 cycles ont chacun donné lieu à un push réussi.

---

# RAPPORT FINAL

À la toute fin, donne-moi un rapport synthétique contenant :

### Architecture

* applications créées/modifiées ;
* modèle utilisateur ;
* système d'authentification ;
* gestion des médias.

### Sécurité

* protections mises en place ;
* gestion des secrets ;
* configuration production.

### Tests

* nombre de tests ;
* résultat ;
* éventuels problèmes rencontrés et corrigés.

### Git

Présente exactement :

```text
23/23 cycles terminés
23 commits effectués
23 pushes effectués
```

Puis donne-moi un tableau :

| Cycle | Fonctionnalité | Commit | Push |
| ----- | -------------- | ------ | ---- |
| 1     | ...            | ...    | OK   |
| 2     | ...            | ...    | OK   |
| ...   | ...            | ...    | ...  |
| 23    | ...            | ...    | OK   |

N'affirme jamais qu'un push a réussi sans l'avoir réellement vérifié.

---

# RÈGLE DE COMMUNICATION PENDANT LE TRAVAIL

Pendant que tu travailles, informe-moi régulièrement de l'avancement.

À chaque cycle, indique brièvement :

```text
Cycle X/23 — EN COURS
```

Puis :

```text
Cycle X/23 — TERMINÉ
Commit : ...
Push : OK
```

Ne me donne pas de longues explications inutiles pendant l'implémentation.

Concentre-toi sur l'exécution réelle du travail.

---

# COMMENCE MAINTENANT

Commence par inspecter le projet existant.

**Ne modifie aucun fichier avant d'avoir compris la structure actuelle.**

Ensuite, commence le **Cycle 1/23**.

Tu dois réellement exécuter les commandes, modifier les fichiers, tester le résultat, committer et pousser.

N'invente aucun résultat de commande.

N'invente aucun push réussi.

Travaille comme un développeur senior responsable d'un dépôt GitHub destiné à être partagé publiquement.
'''