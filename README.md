# Pixel Invaders

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/LeoLeman555/Pixel_Invaders/releases)
[![License](https://img.shields.io/github/license/LeoLeman555/Pixel_Invaders)](LICENSE)
![Status](https://img.shields.io/badge/status-development-orange)
![Built with Pyxel](https://img.shields.io/badge/built%20with-pyxel-purple)
![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

[![English](https://img.shields.io/badge/language-English-darkred)](README.md)
[![Français](https://img.shields.io/badge/langue-Français-darkblue)](docs/README.fr.md)

*"Pixel Invaders"* is a retro arcade game where you pilot a spaceship to destroy waves of alien invaders. Designed in Python with the Pyxel library, it blends classic pixel art and action for a dynamic yet nostalgic experience.

This project is an introductory exercise in leveraging GitHub's capabilities, including pull requests, issues, and GitHub Actions. Additionally, it serves as a learning experience for packaging and publishing on PyPI.

## Preview

| ![Demo 1](pixel_invaders/assets/images/demo/menu.gif) | ![Demo 2](pixel_invaders/assets/images/demo/gameplay.gif) |
|-----------------------------------------|-----------------------------------------|
| ![Demo 3](pixel_invaders/assets/images/demo/boss_fight_1.gif) | ![Demo 4](pixel_invaders/assets/images/demo/boss_fight_2.gif) |

## Table of Contents

- [Prerequisites](#prerequisites)
- [Features](#features)
- [Controls](#controls)
- [Installation](#installation)
- [License](#license)
- [Credits](#credits)
- [Contact](#contact)

## Prerequisites

This project requires [Python 3.11](https://www.python.org/) installed on your machine. If you haven't installed it yet, you can download it from the official Python website.

## Features

#### Gameplay  

- Pilot a spaceship to defend the galaxy against relentless enemy waves.  
- Fire classic lasers or smart missiles that home in on the nearest enemy.  
- Overheat mechanism prevents spamming, promoting strategic shooting.  
- Enemies grow stronger with each wave.  
- Face powerful bosses at waves 5, 10, 15… each with unique attacks like explosive blasts or defensive barriers.
- Rack up points and survive for as long as possible. 
- Lose all your lives, and it's game over.
- Track your stats and upgrade them

- Power-ups:
  - Speed Boost – Dash through space with increased velocity.
  - Rapid Fire – Unleash a temporary barrage of shots.
  - Extra Life – Grants an additional life.  
  - Big Shot – Fire stronger, faster projectiles.
  - Slow Down Enemies – Temporarily reduces enemy movement speed.

#### Architecture

- Object-Oriented Programming (OOP) – Dedicated classes for each game component.  
- Dynamic Wave Management – Configurable via JSON for easy customization.  
- Optimized Asset Management – Efficient handling of spritesheets.  
- Automated Code Styling – Black for clean Python formatting, enforced via GitHub Actions.

## Installation

To run the game locally, you have two options: installing it via pip or cloning the repository manually.

### Install via pip

1. When the game is published on PyPI, you can install it directly with:
   ```bash
   pip install pixel-invaders
   ```
2. Then, launch the game with:
   ```bash
   pixel-invaders
   ```

> The project is currently under development and will soon be available on PyPI. If you haven't already done so, please follow the instructions below to install the game.

### Clone the repository

1. Clone the repository:
   ```bash
   git clone https://github.com/LeoLeman555/Pixel_Invaders.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Pixel_Invaders
   ```
3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - **On Windows**:
   ```bash
   venv\Scripts\activate
   ```
   - **On macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the game:
   ```bash
   python ./main.py
   ```

## Controls

| Action        | Key               |
|---------------|-------------------|
| Move Left     | Left Arrow or A/Q |
| Move Right    | Right Arrow or D  |
| Fire          | Spacebar          |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Credits
   - Code and Game design: [Léo Leman](https://github.com/LeoLeman555)
   - Spritesheets and Art: Santi
   - Built with: [Pyxel](https://github.com/kitao/pyxel)

Special thanks to the open-source community for tools and inspiration!

## Contact

For any questions or feedback, feel free to contact me:

- **Léo Leman** : [My GitHub Profile](https://github.com/LeoLeman555)
