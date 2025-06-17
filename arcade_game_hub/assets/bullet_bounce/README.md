# Bullet Bounce Assets

This directory contains the assets for the Bullet Bounce game.

## Asset Structure

```
bullet_bounce/
├── backgrounds/    # Background images and textures
├── sounds/         # Sound effects and music
└── sprites/        # Player, bullet, and power-up sprites
```

## Required Assets

### Sprites
- `player_blue.png` - Blue player character
- `player_red.png` - Red player character
- `bullet_blue.png` - Blue player's bullet
- `bullet_red.png` - Red player's bullet
- `powerup_shield.png` - Shield power-up
- `powerup_speed.png` - Speed boost power-up
- `powerup_double.png` - Double shot power-up
- `shield.png` - Shield effect
- `avatar_blue.png` - Blue player avatar for UI
- `avatar_red.png` - Red player avatar for UI

### Backgrounds
- `arena.png` - Main game arena background
- `wall.png` - Wall texture

### Sounds
- `shoot.wav` - Bullet firing sound
- `bounce.wav` - Bullet bounce sound
- `hit.wav` - Player hit sound
- `powerup.wav` - Power-up collection sound
- `victory.wav` - Round victory sound
- `round_start.wav` - Round start sound
- `background.mp3` - Background music

## Creating Assets

To generate placeholder assets, run the `create_assets.py` script in the root directory:

```bash
# Install pygame if not already installed
pip install pygame

# Run the asset creation script
python create_assets.py
```

You can replace these placeholder assets with your own custom assets as needed.
