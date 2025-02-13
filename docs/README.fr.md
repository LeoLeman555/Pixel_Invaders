# Pixel Invaders

[🇬🇧 English](../README.md) | [🇫🇷 Français](README.fr.md)

*"Pixel Invaders"* est un jeu d'arcade rétro où vous pilotez un vaisseau spatial pour détruire des vagues d’envahisseurs extraterrestres. Conçu en Python avec la bibliothèque Pyxel, il mêle pixel art classique et action pour une expérience à la fois dynamique et nostalgique.

Ce projet sert d'exercice d'introduction pour explorer la puissance de GitHub, en se concentrant sur des fonctionnalités clés telles que les demandes d'extraction et les actions GitHub.

## Aperçu

| ![Screenshot 1](../assets/images/screenshots/screenshot_1.png) | ![Screenshot 2](../assets/images/screenshots/screenshot_2.png) | ![Screenshot 3](../assets/images/screenshots/screenshot_3.png) | ![Screenshot 4](../assets/images/screenshots/screenshot_4.png) |
|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| ![Screenshot 5](../assets/images/screenshots/screenshot_5.png) | ![../Screenshot 6](../assets/images/screenshots/screenshot_6.png) | ![Screenshot 7](../assets/images/screenshots/screenshot_7.png) | ![Screenshot 8](../assets/images/screenshots/screenshot_8.png) |


## Table des matières

- [Prérequis](#prérequis)
- [Fonctionnalités](#fonctionnalités)
- [Contrôles](#contrôles)
- [Installation](#installation)
- [Licence](#licence)
- [Contact](#contact)

## Prérequis

Ce projet nécessite que [Python 3.6+](https://www.python.org/) et [Git](https://git-scm.com/) soient installés sur votre machine. Si vous avez besoin de les installer, cliquez sur les liens respectifs.

## Fonctionnalités

#### Gameplay  

- Pilotez un vaisseau spatial pour défendre la galaxie contre des vagues d'ennemis implacables.  
- Tirez des lasers classiques ou des missiles intelligents qui se dirigent vers l'ennemi le plus proche.  
- Le mécanisme de surchauffe empêche le spamming et favorise le tir stratégique.  
- Les ennemis deviennent plus forts à chaque vague.  
- Combats de boss aux vagues 5, 10, 15..., avec des attaques explosives spéciales.  
- Accumulez les points et survivez le plus longtemps possible.
- Perdez toutes vos vies et c'est la fin du jeu.

- Power-ups:
  - Accélération - Traverse l'espace avec une plus grosse vitesse
  - Tir rapide - Permet de faire un barrage temporaire de tirs.
  - Vie supplémentaire - Octroie une vie supplémentaire.  
  - Big Shot - Tire des projectiles plus puissants et plus rapides.
  - Ralentir les ennemis - Réduit temporairement la vitesse de déplacement des ennemis.

#### Architecture

- Programmation orientée objet (POO) - Classes dédiées à chaque composant du jeu.  
- Gestion dynamique des vagues - Configurable via JSON pour une personnalisation facile.  
- Gestion optimisée des images - Traitement efficace des spritesheets.  
- Style de code automatisé - Black pour un formatage Python propre, appliqué via les actions GitHub.

## Contrôles

| Action        | Touche               |
|---------------|----------------------|
| Gauche        | Flèche Gauche ou A/Q |
| Droite        | Flèche Droite ou D   |
| Tirer         | Barre d'espace       |
| Recommencer   | R                    |
| Quitter       | Échap (Esc)          |

## Installation

Pour exécuter le jeu localement, suivez ces instructions :

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/LeoLeman555/Pixel_Invaders.git
   ```
2. Naviguer dans le répertoire du projet :
   ```bash
   cd Pixel_Invaders
   ```
3. Créer un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   ```
4. Activer l'environnement virtuel :
   - **Sur Windows**:
   ```bash
   venv\Scripts\activate
   ```
   - **Sur macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```
5. Installer les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```
6. Commencer le jeu :
   ```bash
   python ./main.py
   ```

## Licence

Ce projet est placé sous la licence MIT. Voir la [LICENCE](../LICENSE) pour plus de détails.

## Contact

Pour toute question ou commentaire, n'hésitez pas à me contacter :

- **Léo Leman** : [Mon profil GitHub](https://github.com/LeoLeman555)
