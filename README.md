# BetTheWeather

BetTheWeather est une application web où les utilisateurs peuvent parier sur la météo dans différentes villes. Chaque utilisateur dispose d’un crédit initial et peut parier “Oui” ou “Non” sur un événement météorologique. Si la prévision est correcte, il double sa mise !
 
- Fonctionnalités -

Inscription et connexion sécurisée avec mot de passe hashé via Flask-Bcrypt.

Gestion des crédits : 
chaque utilisateur commence avec un montant initial et voit ses crédits évoluer selon ses paris.

Pari sur la météo :
Les utilisateurs parient sur la pluie dans différentes villes.
Chaque pari comporte une date et un lieu.
Possibilité de miser une somme précise de Serbananes, une monnaie fictive.
Vérification automatique des paris via l’API OpenWeatherMap.

Interface web simple : 
pages de login, inscription et tableau de paris.

- Aperçu des pages -

1. Login (login.html)
Formulaire pour se connecter avec nom d’utilisateur et mot de passe.
Lien vers la page d’inscription.
2. Inscription (register.html)
Crée un compte avec nom d’utilisateur, mot de passe et montant initial de crédits.
Gestion des erreurs (nom déjà utilisé, montant invalide).
3. Accueil 
Liste des paris disponibles pour l’utilisateur.
Formulaire pour miser sur chaque pari (“Oui” / “Non”).
Affichage du crédit actuel et de l’historique des paris.
Sections explicatives pour aider l’utilisateur à comprendre le fonctionnement.

- Utilisation -

1. Inscription
Créez un compte sur /register.
Indiquez un montant initial pour vos crédits.

2. Connexion
Connectez-vous sur /login.

3. Parier
Sur la page d’accueil /, choisissez un pari et misez un montant.
Sélectionnez Oui ou Non.
Les paris sont validés automatiquement à 13h tous les jours.

4. Vérification des gains
Le script weather_check.py (ou la fonction verifier_paris) vérifie les conditions météo via l’API OpenWeatherMap.
Les crédits sont mis à jour automatiquement selon vos prédictions.


- Sécurité -

Les mots de passe sont stockés hachés avec bcrypt.
Les paris sont associés à l’utilisateur via user_id pour éviter les manipulations.
Sessions sécurisées avec app.secret_key.

- API utilisée -

OpenWeatherMap API
Pour récupérer la météo actuelle d’une ville.
Vérifie la présence de pluie (rain).
(Permet de déterminer si un pari est gagné ou perdu.)

# Docker Setup
Ce projet utilise Docker pour faciliter l'exécution de l'application dans un environnement isolé et cohérent. Voici une description des différentes étapes de configuration et de ce que chaque partie du fichier `Dockerfile` fait.

## Dockerfile

1. **Base Image**  
   Le projet utilise l'image `python:3.12-alpine`, une image légère et optimisée pour exécuter des applications Python dans un conteneur.

2. **Préparation de l'environnement Python**  
   Les variables d'environnement `PYTHONDONTWRITEBYTECODE` et `PYTHONUNBUFFERED` sont définies pour éviter la création de fichiers `.pyc` et pour forcer Python à ne pas mettre en tampon ses sorties, ce qui est utile pour les logs dans un conteneur.

3. **Installation des dépendances système**  
   Nous installons les dépendances nécessaires pour le bon fonctionnement des bibliothèques Python suivantes : `requests`, `Flask`, `flask_bcrypt` et SQLite. Ces bibliothèques requièrent des outils de développement comme `gcc`, `musl-dev`, `libffi-dev`, `openssl-dev` et `sqlite-dev`.

4. **Installation des dépendances Python**  
   Le fichier `requirements.txt` est copié dans le conteneur, et les dépendances Python spécifiées sont installées avec `pip` à l'aide de la commande `RUN pip install --no-cache-dir -r requirements.txt`.

5. **Copie du code source**  
   Une fois les dépendances installées, l'intégralité du code source du projet est copiée dans le conteneur.

6. **Exposition du port**  
   Le conteneur expose le port 5000, ce qui permet d'accéder à l'application Flask via ce port.

7. **Démarrage de l'application**  
   La commande `CMD` lance l'application Flask avec `python app.py` lorsque le conteneur démarre.

## requirements.txt

Le fichier `requirements.txt` contient les dépendances Python nécessaires pour l'exécution de l'application :

- `requests` : Une bibliothèque HTTP pour effectuer des requêtes vers des API externes.
- `flask` : Un framework web léger pour créer des applications web.
- `flask_bcrypt` : Une extension Flask pour intégrer le hachage sécurisé des mots de passe.

## Lancement du projet avec Docker

1. **Construire l'image Docker :**

  dans le bash pour creer l'image
   docker build -t bettheweather:v3 .
  et pour la lancer
   docker run -p 5000:5000 bettheweather:v3

L'utilisation de Docker simplifie le déploiement et l'exécution du projet dans un environnement contrôlé, garantissant que l'application fonctionne de manière cohérente sur toutes les machines.

