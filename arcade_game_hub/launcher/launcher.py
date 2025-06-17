"""
Game Launcher module for the Arcade Game Hub.
Provides a menu interface to select and launch games.
"""
import pygame
import importlib
import sys
import os

from launcher.button import Button
import config
from utils.sound_manager import SoundManager

class GameLauncher:
    """Main launcher class for the Arcade Game Hub."""
    
    def __init__(self, screen):
        """Initialize the game launcher.
        
        Args:
            screen: Pygame surface for rendering
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)  # Default font until assets are loaded
        self.title_font = pygame.font.Font(None, 48)
        self.sound_manager = SoundManager()
        
        # Try to load custom font if available
        try:
            if os.path.exists(config.FONT_PATH):
                self.font = pygame.font.Font(config.FONT_PATH, 36)
                self.title_font = pygame.font.Font(config.FONT_PATH, 48)
        except:
            print("Could not load custom font, using default")
        
        # Create game buttons
        self.buttons = []
        self._create_game_buttons()
        
        # Current active game
        self.active_game = None
    
    def _create_game_buttons(self):
        """Create buttons for each available game."""
        games = [
            (config.BULLET_BOUNCE, config.GAME_NAMES[config.BULLET_BOUNCE]),
            (config.STACK_DASH, config.GAME_NAMES[config.STACK_DASH]),
            (config.GHOST_CHASE, config.GAME_NAMES[config.GHOST_CHASE])
        ]
        
        button_width = 300
        button_height = 60
        spacing = 20
        start_y = 150
        
        for i, (game_id, game_name) in enumerate(games):
            y_pos = start_y + i * (button_height + spacing)
            x_pos = (config.SCREEN_WIDTH - button_width) // 2
            
            button = Button(
                x_pos, y_pos, 
                button_width, button_height,
                game_name,
                lambda g=game_id: self.launch_game(g)
            )
            self.buttons.append(button)
        
        # Add quit button
        quit_button = Button(
            (config.SCREEN_WIDTH - button_width) // 2,
            start_y + len(games) * (button_height + spacing),
            button_width, button_height,
            "Quit",
            self.quit_game
        )
        self.buttons.append(quit_button)
    
    def launch_game(self, game_id):
        """Launch the selected game.
        
        Args:
            game_id: Identifier for the game to launch
        """
        try:
            # Import the game module dynamically
            game_module = importlib.import_module(f"games.{game_id}.game")
            
            try:
                # Create game instance
                self.active_game = game_module.Game(self.screen)
                print(f"Launched {game_id}")
            except pygame.error as e:
                print(f"Pygame error when launching {game_id}: {e}")
                # Display error message on screen
                self._show_error_message(f"Error launching {game_id}: {e}")
            except Exception as e:
                print(f"Error creating game instance for {game_id}: {e}")
                import traceback
                traceback.print_exc()
                # Display error message on screen
                self._show_error_message(f"Error launching {game_id}: {e}")
        except (ImportError, AttributeError) as e:
            print(f"Error importing game module {game_id}: {e}")
            # Display error message on screen
            self._show_error_message(f"Error loading {game_id}: {e}")
    
    def _show_error_message(self, message):
        """Display an error message on screen.
        
        Args:
            message: Error message to display
        """
        # Clear the screen
        self.screen.fill(config.BLACK)
        
        # Draw error title
        error_title = self.title_font.render("Error", True, (255, 0, 0))
        title_rect = error_title.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        self.screen.blit(error_title, title_rect)
        
        # Draw error message (handle long messages by splitting)
        words = message.split()
        lines = []
        current_line = words[0]
        
        for word in words[1:]:
            if self.font.size(current_line + " " + word)[0] < config.SCREEN_WIDTH - 100:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        
        lines.append(current_line)
        
        for i, line in enumerate(lines):
            error_text = self.font.render(line, True, (255, 255, 255))
            text_rect = error_text.get_rect(center=(config.SCREEN_WIDTH // 2, 180 + i * 40))
            self.screen.blit(error_text, text_rect)
        
        # Draw continue message
        continue_text = self.font.render("Press any key to continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100))
        self.screen.blit(continue_text, continue_rect)
        
        # Update display
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
    
    def quit_game(self):
        """Exit the application."""
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event):
        """Process pygame events.
        
        Args:
            event: Pygame event to process
        """
        if self.active_game:
            # If a game is active, pass events to it
            result = self.active_game.handle_event(event)
            # If the game returns False, it means it wants to exit
            if result is False:
                self.active_game = None
        else:
            # Otherwise handle launcher events
            for button in self.buttons:
                button.handle_event(event)
    
    def update(self):
        """Update game state."""
        if self.active_game:
            self.active_game.update()
        else:
            for button in self.buttons:
                button.update()
    
    def render(self):
        """Render the launcher or active game."""
        # Clear the screen
        self.screen.fill(config.BLACK)
        
        if self.active_game:
            # If a game is active, let it render
            self.active_game.render()
        else:
            # Otherwise render the launcher UI
            # Draw title
            title = self.title_font.render("Arcade Game Hub", True, config.THEME_COLOR)
            title_rect = title.get_rect(center=(config.SCREEN_WIDTH // 2, 70))
            self.screen.blit(title, title_rect)
            
            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)
