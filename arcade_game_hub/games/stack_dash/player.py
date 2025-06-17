"""
Player module for Stack Dash game.
"""
import pygame
import os
import math

import config
from utils.game_utils import load_image

class Player:
    """Player class for Stack Dash."""
    
    def __init__(self, x, y):
        """Initialize the player.
        
        Args:
            x: Initial x position
            y: Initial y position
        """
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = True  # Start on the ground
        self.jump_safety = 0   # Counter to prevent gap detection right after jumping
        
        # Tile stack properties
        self.tile_count = 0
        self.max_tiles = 20
        self.tile_height = 10
        
        # Power-up states
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.jump_boost = False
        self.jump_boost_timer = 0
        self.tile_magnet = False
        self.tile_magnet_timer = 0
        self.magnet_range = 100
        
        # Animation properties
        self.facing_right = True
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        
        # Load player sprites
        self._load_sprites()
    
    def _load_sprites(self):
        """Load player sprite images."""
        self.sprites = {
            "idle": None,
            "run": [],
            "jump": None
        }
        
        # Try to load sprites if they exist
        try:
            sprite_path = os.path.join(config.ASSETS_DIR, "stack_dash", "characters")
            
            # Load idle sprite
            idle_path = os.path.join(sprite_path, "player_idle.png")
            if os.path.exists(idle_path):
                self.sprites["idle"] = load_image(idle_path, (self.width, self.height), True)
            
            # Load jump sprite
            jump_path = os.path.join(sprite_path, "player_jump.png")
            if os.path.exists(jump_path):
                self.sprites["jump"] = load_image(jump_path, (self.width, self.height), True)
            
            # Load run spritesheet
            run_path = os.path.join(sprite_path, "player_run_spritesheet.png")
            if os.path.exists(run_path):
                # Assuming 6 frames in the spritesheet
                spritesheet = load_image(run_path, None, True)
                frame_width = spritesheet.get_width() // 6
                frame_height = spritesheet.get_height()
                
                for i in range(6):
                    frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                    frame.blit(spritesheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
                    frame = pygame.transform.scale(frame, (self.width, self.height))
                    self.sprites["run"].append(frame)
        except Exception as e:
            print(f"Error loading player sprites: {e}")
            
        # Create placeholder sprites if loading failed
        if not self.sprites["idle"]:
            self.sprites["idle"] = self._create_placeholder_sprite()
        if not self.sprites["jump"]:
            self.sprites["jump"] = self._create_placeholder_sprite()
        if not self.sprites["run"]:
            for _ in range(6):
                self.sprites["run"].append(self._create_placeholder_sprite())
    
    def _create_placeholder_sprite(self):
        """Create a placeholder sprite if loading fails.
        
        Returns:
            pygame.Surface: A placeholder sprite
        """
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, self.width, self.height))
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, self.width, self.height), 2)
        return surf
    
    def handle_event(self, event):
        """Handle input events.
        
        Args:
            event: Pygame event
        """
        # Handle jump events for immediate response
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w] and self.on_ground:
                self.jump()
                
        # Other keyboard events are handled in the update method
    
    def update(self):
        """Update player state."""
        # Handle keyboard input
        keys = pygame.key.get_pressed()
        
        # Calculate base speed (affected by tile count and power-ups)
        base_speed = self.speed * (1 - self.tile_count / (self.max_tiles * 2))
        if self.speed_boost:
            base_speed *= 1.5
        
        # Horizontal movement
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -base_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = base_speed
            self.facing_right = True
        
        # Apply gravity if not on ground
        if not self.on_ground:
            self.vel_y += self.gravity
        
        # Check for continuous jump input
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.jump()
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Update jump safety counter
        if self.jump_safety > 0:
            self.jump_safety -= 1
        
        # Update power-up timers
        if self.speed_boost:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost = False
        
        if self.jump_boost:
            self.jump_boost_timer -= 1
            if self.jump_boost_timer <= 0:
                self.jump_boost = False
        
        if self.tile_magnet:
            self.tile_magnet_timer -= 1
            if self.tile_magnet_timer <= 0:
                self.tile_magnet = False
        
        # Update animation
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.sprites["run"])
    
    def jump(self):
        """Make the player jump.
        
        Returns:
            bool: True if jump was successful, False otherwise
        """
        if self.on_ground:
            # Calculate jump strength based on power-ups
            jump_strength = self.jump_power
            if self.jump_boost:
                jump_strength *= 1.3
                
            # Apply jump velocity
            self.vel_y = jump_strength
            self.on_ground = False
            
            # Add a small upward boost to ensure the player leaves the ground
            self.y -= 2
            
            # Add a small delay before gap detection can occur
            self.jump_safety = 10  # 10 frames of safety
            
            return True
        return False
    
    def add_tile(self):
        """Add a tile to the player's stack."""
        if self.tile_count < self.max_tiles:
            self.tile_count += 1
    
    def remove_tile(self):
        """Remove a tile from the player's stack.
        
        Returns:
            bool: True if a tile was removed, False if no tiles
        """
        if self.tile_count > 0:
            self.tile_count -= 1
            return True
        return False
    
    def fall(self):
        """Make the player fall (game over)."""
        self.vel_y = 15  # Strong downward velocity
    
    def activate_speed_boost(self):
        """Activate speed boost power-up."""
        self.speed_boost = True
        self.speed_boost_timer = 300  # 5 seconds at 60 FPS
    
    def activate_jump_boost(self):
        """Activate jump boost power-up."""
        self.jump_boost = True
        self.jump_boost_timer = 300  # 5 seconds at 60 FPS
    
    def activate_tile_magnet(self):
        """Activate tile magnet power-up."""
        self.tile_magnet = True
        self.tile_magnet_timer = 300  # 5 seconds at 60 FPS
    
    def get_rect(self):
        """Get the player's bounding rectangle.
        
        Returns:
            pygame.Rect: The player's bounding rectangle
        """
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, 
                          self.width, self.height)
    
    def draw(self, screen, camera_x=0):
        """Draw the player.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x offset
        """
        # Determine which sprite to use
        if not self.on_ground:
            sprite = self.sprites["jump"]
        elif abs(self.vel_x) > 0.5:
            sprite = self.sprites["run"][self.animation_frame]
        else:
            sprite = self.sprites["idle"]
        
        # Flip sprite if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Draw player at position (adjusted for camera)
        screen_x = self.x - camera_x
        screen_y = self.y
        screen.blit(sprite, (screen_x - self.width // 2, screen_y - self.height // 2))
        
        # Draw tile stack
        self._draw_tile_stack(screen, screen_x, screen_y)
        
        # Draw power-up indicators
        if self.speed_boost or self.jump_boost or self.tile_magnet:
            self._draw_powerup_indicators(screen, screen_x, screen_y)
    
    def _draw_tile_stack(self, screen, screen_x, screen_y):
        """Draw the stack of tiles on the player's back.
        
        Args:
            screen: Pygame surface to draw on
            screen_x: Screen x position
            screen_y: Screen y position
        """
        if self.tile_count == 0:
            return
            
        # Draw tiles stacked on player's back
        tile_width = 30
        
        for i in range(self.tile_count):
            # Calculate position (tiles stack upward from player's back)
            tile_x = screen_x
            tile_y = screen_y - self.height // 2 - (i + 1) * self.tile_height
            
            # Add slight wobble based on movement
            wobble = math.sin(pygame.time.get_ticks() / 200 + i * 0.2) * min(2, i * 0.3)
            tile_x += wobble
            
            # Draw tile
            pygame.draw.rect(screen, (50, 150, 250), 
                           (tile_x - tile_width // 2, tile_y, tile_width, self.tile_height))
            pygame.draw.rect(screen, (20, 100, 200), 
                           (tile_x - tile_width // 2, tile_y, tile_width, self.tile_height), 2)
    
    def _draw_powerup_indicators(self, screen, screen_x, screen_y):
        """Draw power-up indicator icons.
        
        Args:
            screen: Pygame surface to draw on
            screen_x: Screen x position
            screen_y: Screen y position
        """
        indicator_size = 15
        indicator_y = screen_y - self.height // 2 - 25
        
        # Draw speed boost indicator
        if self.speed_boost:
            pygame.draw.circle(screen, (255, 255, 0), 
                             (screen_x - 20, indicator_y), indicator_size)
            pygame.draw.circle(screen, (200, 200, 0), 
                             (screen_x - 20, indicator_y), indicator_size, 2)
        
        # Draw jump boost indicator
        if self.jump_boost:
            pygame.draw.circle(screen, (0, 255, 0), 
                             (screen_x, indicator_y), indicator_size)
            pygame.draw.circle(screen, (0, 200, 0), 
                             (screen_x, indicator_y), indicator_size, 2)
        
        # Draw tile magnet indicator
        if self.tile_magnet:
            pygame.draw.circle(screen, (255, 0, 255), 
                             (screen_x + 20, indicator_y), indicator_size)
            pygame.draw.circle(screen, (200, 0, 200), 
                             (screen_x + 20, indicator_y), indicator_size, 2)
