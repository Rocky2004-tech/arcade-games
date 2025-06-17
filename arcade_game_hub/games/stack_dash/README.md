# Stack Dash

A high-speed side-scrolling platformer where the player collects tiles and stacks them on their back. The more they stack, the slower they get—but they must build bridges and paths to reach the finish line!

## Game Overview

Stack Dash is a platformer game that combines speed, strategy, and resource management. Players must collect tiles scattered throughout the level while navigating platforms and gaps. The collected tiles are stacked on the player's back, slowing them down but providing resources to build bridges across gaps. The goal is to reach the finish line as quickly as possible with the highest score.

## Controls

- **Arrow Keys / WASD**: Move left/right
- **Space**: Jump
- **P**: Pause game
- **ESC**: Return to launcher

## Gameplay Mechanics

1. **Tile Collection**: Run over tiles to collect them. They stack on your back.
2. **Weight System**: The more tiles you carry, the slower you move.
3. **Bridge Building**: When you run off a platform, a tile is automatically used to build a bridge.
4. **Power-ups**:
   - **Speed Boost** (Yellow): Temporarily increases movement speed
   - **Jump Boost** (Green): Temporarily increases jump height
   - **Tile Magnet** (Purple): Attracts nearby tiles

## Scoring

- **Tile Collection**: +10 points per tile
- **Time Bonus**: Faster completion = higher bonus
- **Tile Bonus**: Remaining tiles at finish line = bonus points

## Development Notes

### File Structure

- `game.py`: Main game class and loop
- `player.py`: Player character logic and rendering
- `level.py`: Level generation, platforms, and collectibles
- `ui.py`: User interface elements

### Asset Requirements

- Character sprites (idle, run, jump)
- Tile graphics
- Platform textures
- Background parallax layers
- Power-up icons
- Sound effects for jumping, collecting, and building

## Future Enhancements

- Multiple levels with increasing difficulty
- Custom themes (City Run, Candy Land, Lava Factory)
- Multiplayer split-screen mode
- Endless mode with procedurally generated platforms
