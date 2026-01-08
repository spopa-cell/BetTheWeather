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



