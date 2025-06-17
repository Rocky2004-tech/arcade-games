"""
UI module for Stack Dash game.
"""
import pygame
import os

import config
from utils.game_utils import draw_text

class GameUI:
    """UI class for Stack Dash."""
    
    def __init__(self):
        """Initialize the UI."""
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Try to load custom font if available
        try:
            if os.path.exists(config.FONT_PATH):
                self.font = pygame.font.Font(config.FONT_PATH, 36)
                self.title_font = pygame.font.Font(config.FONT_PATH, 48)
                self.small_font = pygame.font.Font(config.FONT_PATH, 24)
        except:
            print("Could not load custom font, using default")
    
    def draw_starting(self, screen, countdown):
        """Draw the starting countdown UI.
        
        Args:
            screen: Pygame surface to draw on
            countdown: Countdown timer in seconds
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        draw_text(screen, "Stack Dash", self.title_font, config.THEME_COLOR, 
                 config.SCREEN_WIDTH // 2, 100, "center")
        
        # Draw countdown
        draw_text(screen, f"Starting in: {countdown}", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2, "center")
        
        # Draw instructions
        instructions = [
            "Controls:",
            "Arrow Keys / WASD: Move",
            "Space: Jump",
            "P: Pause",
            "ESC: Quit to Menu"
        ]
        
        y_pos = config.SCREEN_HEIGHT // 2 + 100
        for instruction in instructions:
            draw_text(screen, instruction, self.small_font, config.WHITE, 
                     config.SCREEN_WIDTH // 2, y_pos, "center")
            y_pos += 30
    
    def draw_playing(self, screen, score, time, tile_count, progress=0.0):
        """Draw the in-game UI.
        
        Args:
            screen: Pygame surface to draw on
            score: Current score
            time: Time elapsed in seconds
            tile_count: Number of tiles collected
            progress: Player progress through level (0.0 to 1.0)
        """
        # Draw score
        draw_text(screen, f"Score: {score}", self.font, config.WHITE, 
                 20, 20, "left")
        
        # Draw time
        minutes = time // 60
        seconds = time % 60
        draw_text(screen, f"Time: {minutes:02d}:{seconds:02d}", self.font, config.WHITE, 
                 config.SCREEN_WIDTH - 20, 20, "right")
        
        # Draw tile count
        draw_text(screen, f"Tiles: {tile_count}", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 20, "center")
        
        # Draw progress bar at bottom
        self._draw_progress_bar(screen, progress)
    
    def draw_game_over(self, screen, score, high_score):
        """Draw the game over UI.
        
        Args:
            screen: Pygame surface to draw on
            score: Final score
            high_score: High score
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        draw_text(screen, "Game Over!", self.title_font, config.RED, 
                 config.SCREEN_WIDTH // 2, 150, "center")
        
        # Draw score
        draw_text(screen, f"Score: {score}", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 250, "center")
        
        # Draw high score
        if score > high_score:
            draw_text(screen, "New High Score!", self.font, config.YELLOW, 
                     config.SCREEN_WIDTH // 2, 300, "center")
        else:
            draw_text(screen, f"High Score: {high_score}", self.font, config.WHITE, 
                     config.SCREEN_WIDTH // 2, 300, "center")
        
        # Draw restart instructions
        draw_text(screen, "Press SPACE to restart", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 400, "center")
        draw_text(screen, "Press ESC to quit", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 450, "center")
    
    def draw_level_complete(self, screen, score, high_score, time):
        """Draw the level complete UI.
        
        Args:
            screen: Pygame surface to draw on
            score: Final score
            high_score: High score
            time: Time taken in seconds
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        screen.blit(overlay, (0, 0))
        
        # Draw level complete text
        draw_text(screen, "Level Complete!", self.title_font, config.GREEN, 
                 config.SCREEN_WIDTH // 2, 100, "center")
        
        # Draw score
        draw_text(screen, f"Score: {score}", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 200, "center")
        
        # Draw time
        minutes = time // 60
        seconds = time % 60
        draw_text(screen, f"Time: {minutes:02d}:{seconds:02d}", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 250, "center")
        
        # Draw high score
        if score > high_score:
            draw_text(screen, "New High Score!", self.font, config.YELLOW, 
                     config.SCREEN_WIDTH // 2, 300, "center")
        else:
            draw_text(screen, f"High Score: {high_score}", self.font, config.WHITE, 
                     config.SCREEN_WIDTH // 2, 300, "center")
        
        # Draw restart instructions
        draw_text(screen, "Press SPACE to play again", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 400, "center")
        draw_text(screen, "Press ESC to quit", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 450, "center")
    
    def draw_pause_menu(self, screen):
        """Draw the pause menu.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Draw pause text
        draw_text(screen, "PAUSED", self.title_font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 200, "center")
        
        # Draw instructions
        draw_text(screen, "Press P to resume", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 300, "center")
        draw_text(screen, "Press ESC to quit", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, 350, "center")
    
    def _draw_progress_bar(self, screen, progress):
        """Draw a progress bar at the bottom of the screen.
        
        Args:
            screen: Pygame surface to draw on
            progress: Progress value (0.0 to 1.0)
        """
        # Clamp progress value
        progress = max(0.0, min(1.0, progress))
        
        # Bar dimensions
        bar_width = config.SCREEN_WIDTH - 100
        bar_height = 20
        bar_x = 50
        bar_y = config.SCREEN_HEIGHT - 30
        
        # Draw background
        pygame.draw.rect(screen, (50, 50, 50), 
                       (bar_x, bar_y, bar_width, bar_height))
        
        # Draw progress
        progress_width = int(bar_width * progress)
        pygame.draw.rect(screen, config.THEME_COLOR, 
                       (bar_x, bar_y, progress_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, config.WHITE, 
                       (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw player icon
        icon_size = 24
        icon_x = bar_x + progress_width - icon_size // 2
        icon_y = bar_y - icon_size // 2
        
        pygame.draw.circle(screen, config.WHITE, 
                         (icon_x, icon_y), icon_size // 2)
        pygame.draw.circle(screen, config.BLACK, 
                         (icon_x, icon_y), icon_size // 2, 2)
