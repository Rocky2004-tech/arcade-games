"""
Stack Dash game module.
A high-speed side-scrolling platformer where the player collects tiles and stacks them.
"""
import pygame
import sys
import os
import random

import config
from utils.sound_manager import SoundManager
from utils.game_utils import draw_text, load_image
from games.stack_dash.player import Player
from games.stack_dash.level import Level
from games.stack_dash.ui import GameUI

class Game:
    """Main game class for Stack Dash."""
    
    # Game states
    STATE_STARTING = "starting"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    STATE_LEVEL_COMPLETE = "level_complete"
    
    def __init__(self, screen):
        """Initialize the game.
        
        Args:
            screen: Pygame surface for rendering
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.sound_manager = SoundManager()
        
        # Load game assets
        self._load_assets()
        
        # Create game objects
        self.player = Player(100, config.SCREEN_HEIGHT - 100)
        self.level = Level()
        self.ui = GameUI()
        
        # Game state
        self.state = Game.STATE_STARTING
        self.state_timer = 180  # 3 seconds at 60 FPS
        
        # Game settings
        self.score = 0
        self.timer = 0  # Time in frames
        self.high_score = self._load_high_score()
        
        # Camera/viewport settings
        self.camera_x = 0
        
        # Start background music
        self.sound_manager.play_music(os.path.join(config.ASSETS_DIR, "stack_dash", "music", "main_theme.mp3"), -1)
    
    def _load_assets(self):
        """Load game assets like sounds and images."""
        # Load sound effects
        sounds_dir = os.path.join(config.ASSETS_DIR, "stack_dash", "sounds")
        
        # Define sound files to load
        sound_files = {
            "jump": "jump.wav",
            "pickup": "pickup.wav",
            "drop": "drop.wav",
            "fall": "fall.wav",
            "powerup": "powerup.wav",
            "success": "success.wav"
        }
        
        # Load each sound if it exists
        for sound_name, file_name in sound_files.items():
            sound_path = os.path.join(sounds_dir, file_name)
            if os.path.exists(sound_path):
                self.sound_manager.load_sound(sound_name, sound_path)
            else:
                print(f"Warning: Sound file not found: {sound_path}")
    
    def _load_high_score(self):
        """Load high score from file.
        
        Returns:
            int: The high score
        """
        try:
            score_file = os.path.join(config.ASSETS_DIR, "stack_dash", "high_score.txt")
            if os.path.exists(score_file):
                with open(score_file, 'r') as f:
                    return int(f.read().strip())
            return 0
        except:
            return 0
    
    def _save_high_score(self):
        """Save high score to file."""
        if self.score > self.high_score:
            try:
                score_file = os.path.join(config.ASSETS_DIR, "stack_dash", "high_score.txt")
                os.makedirs(os.path.dirname(score_file), exist_ok=True)
                with open(score_file, 'w') as f:
                    f.write(str(self.score))
                self.high_score = self.score
            except Exception as e:
                print(f"Error saving high score: {e}")
    
    def handle_event(self, event):
        """Process pygame events.
        
        Args:
            event: Pygame event to process
            
        Returns:
            False if the game should exit, None otherwise
        """
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            if event.key == pygame.K_p:
                if self.state == Game.STATE_PLAYING:
                    self.state = Game.STATE_PAUSED
                elif self.state == Game.STATE_PAUSED:
                    self.state = Game.STATE_PLAYING
            
            # Handle jump keys
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                if self.state == Game.STATE_PLAYING:
                    if self.player.jump():
                        try:
                            self.sound_manager.play_sound("jump")
                        except Exception as e:
                            print(f"Error playing jump sound: {e}")
                elif self.state == Game.STATE_GAME_OVER or self.state == Game.STATE_LEVEL_COMPLETE:
                    self._restart_game()
        
        # Handle player input
        if self.state == Game.STATE_PLAYING:
            self.player.handle_event(event)
    
    def _restart_game(self):
        """Restart the game."""
        # Save high score before restarting
        self._save_high_score()
        
        # Reset game state
        self.player = Player(100, config.SCREEN_HEIGHT - 100)
        self.level = Level()
        self.score = 0
        self.timer = 0
        self.camera_x = 0
        
        # Set state to starting
        self.state = Game.STATE_STARTING
        self.state_timer = 180
    
    def update(self):
        """Update game state."""
        # Handle different game states
        if self.state == Game.STATE_STARTING:
            # Count down the starting timer
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = Game.STATE_PLAYING
                
        elif self.state == Game.STATE_PLAYING:
            # Update timer
            self.timer += 1
            
            # Update player
            self.player.update()
            
            # Update level
            self.level.update()
            
            # Check for platform collisions
            self.level.check_collision(self.player)
            
            # Check for tile collection
            collected_tile = self.level.check_tile_collection(self.player)
            if collected_tile:
                self.player.add_tile()
                self.score += 10
                self.sound_manager.play_sound("pickup")
            
            # Check for gaps and bridge building - only if player is falling (not during initial jump)
            if self.player.vel_y > 2.0 and self.level.check_gap(self.player):
                if self.player.tile_count > 0:
                    self.player.remove_tile()
                    self.level.build_bridge(self.player.x, self.player.y)
                    self.sound_manager.play_sound("drop")
                else:
                    # Player falls if no tiles to build bridge
                    self.player.fall()
                    self.sound_manager.play_sound("fall")
                    self.state = Game.STATE_GAME_OVER
            
            # Check for power-ups
            powerup = self.level.check_powerup_collision(self.player)
            if powerup:
                self._apply_powerup(powerup)
                self.sound_manager.play_sound("powerup")
            
            # Update camera position to follow player
            target_camera_x = self.player.x - config.SCREEN_WIDTH // 3
            self.camera_x += (target_camera_x - self.camera_x) * 0.1
            
            # Check if player reached the finish line
            if self.level.check_finish_line(self.player):
                self.state = Game.STATE_LEVEL_COMPLETE
                self.sound_manager.play_sound("success")
                
                # Calculate bonus points based on time and remaining tiles
                time_bonus = max(0, 10000 - self.timer // 60 * 10)
                tile_bonus = self.player.tile_count * 50
                self.score += time_bonus + tile_bonus
            
            # Check if player fell off the screen (give more room for jumps)
            if self.player.y > config.SCREEN_HEIGHT + 200:
                self.state = Game.STATE_GAME_OVER
                self.sound_manager.play_sound("fall")
            
        elif self.state == Game.STATE_PAUSED:
            # Do nothing while paused
            pass
    
    def _apply_powerup(self, powerup_type):
        """Apply power-up effect to player.
        
        Args:
            powerup_type: Type of power-up to apply
        """
        if powerup_type == "speed":
            self.player.activate_speed_boost()
        elif powerup_type == "jump":
            self.player.activate_jump_boost()
        elif powerup_type == "magnet":
            self.player.activate_tile_magnet()
    
    def render(self):
        """Render the game."""
        # Clear the screen
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw parallax background
        self.level.draw_background(self.screen, self.camera_x)
        
        # Draw level
        self.level.draw(self.screen, self.camera_x)
        
        # Draw player
        self.player.draw(self.screen, self.camera_x)
        
        # Calculate progress for UI (player position / level width)
        progress = min(1.0, max(0.0, self.player.x / self.level.level_width))
        
        # Draw UI based on game state
        if self.state == Game.STATE_STARTING:
            self.ui.draw_starting(self.screen, self.state_timer // 60 + 1)
        elif self.state == Game.STATE_PLAYING:
            self.ui.draw_playing(self.screen, self.score, self.timer // 60, self.player.tile_count, progress)
        elif self.state == Game.STATE_GAME_OVER:
            self.ui.draw_game_over(self.screen, self.score, self.high_score)
        elif self.state == Game.STATE_LEVEL_COMPLETE:
            self.ui.draw_level_complete(self.screen, self.score, self.high_score, self.timer // 60)
        
        # Draw pause menu if paused
        if self.state == Game.STATE_PAUSED:
            self.ui.draw_pause_menu(self.screen)
