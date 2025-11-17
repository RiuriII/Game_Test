# Platformer Game

A simple yet engaging 2D platformer game built with **Pygame Zero**, featuring a hero character that must defeat enemies across multiple platforms to achieve victory.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Controls](#controls)
- [Gameplay](#gameplay)
- [Project Structure](#project-structure)
- [Game Mechanics](#game-mechanics)
- [Audio](#audio)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Smooth Platforming Mechanics**: Jump, move, and interact with platforms
- **Enemy AI**: Enemies patrol platforms, detect the hero, and chase/attack dynamically
- **Animation System**: Fluid sprite animations for idle, running, attacking, and death states
- **Projectile System**: Fire projectiles to defeat enemies
- **Score System**: Track defeated enemies and reach a target to win
- **Sound Effects**: Jump and attack sound effects (when configured)
- **Main Menu & Game States**: Menu, playing, game over, and victory screens
- **Collision Detection**: Proper platform and enemy collision handling
- **Horizontal Flipping**: Dynamically flip sprites based on character direction

## 🎯 Requirements

- **Python 3.8+**
- **Pygame Zero** 2.0+
- **Pygame** 2.0+

## 📥 Installation

### 1. Clone or download the repository

```bash
git clone https://github.com/RiuriII/Game_Test.git
cd Game_Test
```

### 2. Install dependencies

Using **pip**:

```bash
pip install pygame-zero pygame
```

Or using **conda** (if you use Anaconda/Miniconda):

```bash
conda install pygame pygame-zero
```

### 3. Prepare assets

The game expects the following asset folders:

```
game_python/
├── images/           # Sprite sheets and background images
├── sounds/           # Sound effect files (.wav or .ogg)
└── music/            # Background music files (.wav or .ogg)
```

**Sprite naming convention** (must be placed in the `images/` folder):
- Hero: `hero_idle1.png`, `hero_idle2.png`, `hero_idle3.png`, `hero_attack1.png`, ..., `hero_death1.png`, etc.
- Enemy: `enemy_idle1.png`, ..., `enemy_run1.png`, ..., `enemy_attack1.png`, ..., `enemy_dead1.png`, etc.
- Background: `background.png`

**Audio naming convention** (must be placed in `sounds/` and `music/` folders):
- Jump sound: `jump.wav` or `jump.ogg`
- Attack sound: `attack.wav` or `attack.ogg`
- Background music: `background.wav` or `background.ogg`

## 🚀 How to Run

From the project root directory, run:

```bash
python main.py
```

The game window will open and display the main menu.

## 🎮 Controls

| Key | Action |
|-----|--------|
| **LEFT ARROW** | Move left |
| **RIGHT ARROW** | Move right |
| **SPACE** | Jump |
| **Z** | Attack / Shoot projectile |
| **M** | Return to menu (during gameplay) |
| **ENTER** | Select menu option or continue |
| **ESC** | Exit game (from menu) |
| **Mouse Click** | Interact with menu buttons |

## 🎲 Gameplay

### Objective

Defeat all enemies on the screen to win the game. Avoid taking damage from enemies; your health is displayed as "Lives" on the HUD.

### Game States

1. **Menu**: Start the game, toggle sound, or exit.
2. **Playing**: Navigate platforms, defeat enemies, and reach the victory condition.
3. **Game Over**: Your hero died. Press ENTER to return to the menu.
4. **Victory**: All enemies defeated. Press ENTER to return to the menu.

### Enemy Behavior

- **Patrol**: Enemies walk back and forth on their platform.
- **Chase**: When they detect the hero within range, they pursue and attack.
- **Attack**: Enemies swing and deal damage when close to the hero.
- **Death**: Enemies animate a death sequence and become inactive.

### Hero Mechanics

- **Health**: Start with 100 health points. Taking damage reduces this value.
- **Jumping**: Press SPACE to jump (only when on ground).
- **Attacking**: Press Z to shoot a projectile. Projectiles travel in the direction you're facing.
- **Platforms**: Walk on platforms and jump between them. Falling off resets your position.

## 📁 Project Structure

```
game_python/
│
├── main.py                    # Main game loop and state management
├── README.md                  # This file
│
├── modules/
│   ├── Hero.py               # Hero class (movement, animation, attacks)
│   ├── Enemy.py              # Enemy class (AI, animation, attacks)
│   ├── Projectile.py         # Projectile class (bullets)
│   ├── Platform.py           # Platform class (spawn points, patrol zones)
│   ├── Sprite.py             # SpriteManager (sprite flipping/caching utilities)
│   └── __pycache__/          # Python cache (auto-generated)
│
├── images/                   # Sprite images
├── sounds/                   # Sound effects
├── music/                    # Background music 
```

## 🎨 Game Mechanics

### Collision System

- **Platform Collision**: The hero collides with platforms when moving down or up.
- **Enemy Collision**: Enemies attack the hero when in range; projectiles damage enemies on contact.
- **Screen Bounds**: Projectiles deactivate when leaving the screen.

### Animation System

All characters use frame-based animation with configurable frame delays:

- **Idle**: Default animation when standing still.
- **Run**: Plays when chasing an enemy.
- **Attack**: Plays when attacking; damage is applied mid-animation.
- **Death**: Plays when health reaches 0.

### Sprite Direction

Characters automatically flip horizontally when changing direction, handled by the `SpriteManager` utility class with caching.

## 🔊 Audio

The game includes:

- **Background Music**: Loops continuously during gameplay.
- **Jump Sound**: Plays when the hero jumps.
- **Attack Sound**: Plays when the hero attacks.

If audio files are missing, the game continues without errors.

## 🤝 Contributing

To contribute to this project:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request.

## 📝 License

This project is open source. Feel free to use and modify it as needed.

---

**Enjoy the game! 🎮**
