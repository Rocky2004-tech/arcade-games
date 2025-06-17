"""
Global configuration settings for the Arcade Game Hub.
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Theme settings
THEME_COLOR = PURPLE
BUTTON_COLOR = BLUE
BUTTON_HOVER_COLOR = CYAN
TEXT_COLOR = WHITE

# Asset paths
ASSETS_DIR = "assets"
COMMON_ASSETS = f"{ASSETS_DIR}/common"
FONT_PATH = f"{COMMON_ASSETS}/fonts/main_font.ttf"

# Game IDs
BULLET_BOUNCE = "bullet_bounce"
STACK_DASH = "stack_dash"
GHOST_CHASE = "ghost_chase"

# Game display names
GAME_NAMES = {
    BULLET_BOUNCE: "Bullet Bounce",
    STACK_DASH: "Stack Dash",
    GHOST_CHASE: "Ghost Chase"
}

# Sound settings
SOUND_ENABLED = True
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7
