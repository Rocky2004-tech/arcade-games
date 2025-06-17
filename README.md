# Arcade Game Hub

A collection of Python-based arcade games built with Pygame.

## Games

The Arcade Game Hub includes the following games:

1. **Bullet Bounce** - A fast-paced 1v1 arena shooter where bullets bounce off walls. Players must time shots precisely and use rebounds to outsmart opponents. Features power-ups, neon visuals, and local multiplayer.
2. **Stack Dash** - A reflex game about stacking blocks perfectly
3. **Ghost Chase** - A maze game where you avoid ghosts and collect power-ups

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Rocky2004-tech/arcade-games.git
   cd arcade-games
   ```

2. Install the required dependencies:
   ```
   pip install -r arcade_game_hub/requirements.txt
   ```

## Running the Game Hub

Launch the game hub with:
```
python arcade_game_hub/main.py
```

## Sound and Music Files

Some games require sound and music files. The repository includes placeholder files, but you'll need to add your own sound and music files for the full experience.

If you encounter missing sound files or sound-related errors, run the included sound file generator:
```
python arcade_game_hub/fix_sounds.py
```
This will create placeholder sound files for all games.

## Controls

### Launcher
- Use the mouse to select games
- Click on game buttons to launch them
- Click "Quit" to exit

### Bullet Bounce
- WASD: Move player 1
- Arrow Keys: Move player 2
- Q/E: Rotate player 1
- ,/.: Rotate player 2
- Space: Player 1 shoot
- Enter: Player 2 shoot
- P: Pause game
- ESC: Return to launcher

## Project Structure

The project follows a modular structure:

```
arcade_game_hub/
│
├── assets/           # Game assets (images, sounds, etc.)
├── games/            # Individual game modules
├── launcher/         # Game selection menu
├── utils/            # Shared utility functions
├── config.py         # Global configuration
└── main.py           # Entry point
```

## Development

To add a new game:

1. Create a new folder in `games/`
2. Implement the game with at least a `game.py` file with a `Game` class
3. Add game assets in the `assets/` directory
4. Update the launcher to include the new game

## License

This project is licensed under the MIT License - see the LICENSE file for details.
