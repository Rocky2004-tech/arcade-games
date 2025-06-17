# Bullet Bounce

A fast-paced 1v1 arena shooter where bullets bounce off walls. Players must time shots precisely and use rebounds to outsmart opponents.

## How to Play

### Objective
- Score points by hitting your opponent with bullets
- First player to reach 5 points wins the round
- Best of 3 rounds wins the match

### Controls

#### Player 1 (Blue)
- **W, A, S, D**: Move up, left, down, right
- **Q, E**: Rotate left, right
- **SPACE**: Shoot

#### Player 2 (Red)
- **Arrow Keys**: Move up, left, down, right
- **Comma (,), Period (.)**: Rotate left, right
- **ENTER**: Shoot

#### General Controls
- **P**: Pause game
- **ESC**: Return to launcher

### Power-ups
- **Shield (Cyan)**: Blocks one hit
- **Speed Boost (Yellow)**: Temporarily increases movement speed
- **Double Shot (Green)**: Next shot fires two bullets at once

### Tips
- Bullets bounce off walls up to 3 times
- Use wall bounces to hit opponents from unexpected angles
- Collect power-ups to gain advantages
- If time runs out, the player with the most points wins the round

## Troubleshooting

If you encounter issues with missing sound files, run the fix_sounds.py script:

```
python arcade_game_hub/games/bullet_bounce/fix_sounds.py
```

This will create placeholder sound files for the game.
