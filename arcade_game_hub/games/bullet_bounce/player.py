"""
Player class for Bullet Bounce game.
"""
import pygame
import math
import os

import config
from utils.game_utils import load_image

class Player:
    """Player character for Bullet Bounce."""
    
    def __init__(self, x, y, player_id=1):
        """Initialize the player.
        
        Args:
            x: Initial x position
            y: Initial y position
            player_id: Player identifier (1 for blue, 2 for red)
        """
        self.x = x
        self.y = y
        self.angle = 0  # Angle in radians
        self.speed = 5
        self.health = 100
        self.radius = 20
        self.player_id = player_id
        self.score = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.double_shot = False
        
        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.rotating_left = False
        self.rotating_right = False
        
        # Try to load player sprite
        self.sprite = None
        self.shield_sprite = None
        
        # Load appropriate sprite based on player_id
        sprite_name = "player_blue.png" if player_id == 1 else "player_red.png"
        sprite_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "sprites", sprite_name)
        if os.path.exists(sprite_path):
            self.sprite = load_image(sprite_path, (self.radius * 2, self.radius * 2), True)
            
        # Load shield sprite
        shield_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "sprites", "shield.png")
        if os.path.exists(shield_path):
            self.shield_sprite = load_image(shield_path, (self.radius * 2.5, self.radius * 2.5), True)
    
    def handle_event(self, event):
        """Process pygame events for player control.
        
        Args:
            event: Pygame event to process
        """
        # Player 1 controls (WASD + Q/E for rotation, SPACE for shooting)
        if self.player_id == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.moving_up = True
                elif event.key == pygame.K_s:
                    self.moving_down = True
                elif event.key == pygame.K_a:
                    self.moving_left = True
                elif event.key == pygame.K_d:
                    self.moving_right = True
                elif event.key == pygame.K_q:
                    self.rotating_left = True
                elif event.key == pygame.K_e:
                    self.rotating_right = True
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.moving_up = False
                elif event.key == pygame.K_s:
                    self.moving_down = False
                elif event.key == pygame.K_a:
                    self.moving_left = False
                elif event.key == pygame.K_d:
                    self.moving_right = False
                elif event.key == pygame.K_q:
                    self.rotating_left = False
                elif event.key == pygame.K_e:
                    self.rotating_right = False
        
        # Player 2 controls (Arrow keys + , and . for rotation, ENTER for shooting)
        elif self.player_id == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.moving_down = True
                elif event.key == pygame.K_LEFT:
                    self.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = True
                elif event.key == pygame.K_COMMA:
                    self.rotating_left = True
                elif event.key == pygame.K_PERIOD:
                    self.rotating_right = True
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.moving_down = False
                elif event.key == pygame.K_LEFT:
                    self.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = False
                elif event.key == pygame.K_COMMA:
                    self.rotating_left = False
                elif event.key == pygame.K_PERIOD:
                    self.rotating_right = False
    
    def update(self):
        """Update player position and state."""
        # Handle movement
        current_speed = self.speed * 1.5 if self.speed_boost_active else self.speed
        
        if self.moving_up:
            self.y -= current_speed
        if self.moving_down:
            self.y += current_speed
        if self.moving_left:
            self.x -= current_speed
        if self.moving_right:
            self.x += current_speed
            
        # Handle rotation
        rotation_speed = 0.1
        if self.rotating_left:
            self.angle -= rotation_speed
        if self.rotating_right:
            self.angle += rotation_speed
            
        # Keep angle in [0, 2π) range
        self.angle %= 2 * math.pi
        
        # Keep player within screen bounds
        self.x = max(self.radius, min(config.SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(config.SCREEN_HEIGHT - self.radius, self.y))
        self.x = max(self.radius, min(config.SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(config.SCREEN_HEIGHT - self.radius, self.y))
        
        # Update power-up timers
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
    
    def activate_shield(self, duration=300):
        """Activate player shield.
        
        Args:
            duration: Shield duration in frames
        """
        self.shield_active = True
        self.shield_timer = duration
    
    def activate_speed_boost(self, duration=300):
        """Activate speed boost.
        
        Args:
            duration: Speed boost duration in frames
        """
        self.speed_boost_active = True
        self.speed_boost_timer = duration
    
    def activate_double_shot(self):
        """Activate double shot for next bullet."""
        self.double_shot = True
    
    def take_damage(self, amount):
        """Reduce player health.
        
        Args:
            amount: Amount of damage to take
            
        Returns:
            True if player is still alive, False otherwise
        """
        # If shield is active, block damage
        if self.shield_active:
            self.shield_active = False
            self.shield_timer = 0
            return True
            
        # Otherwise, reduce health
        self.health -= amount
        
        # Check if player is still alive
        return self.health > 0
    
    def draw(self, surface):
        """Draw the player on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw shield if active
        if self.shield_active and self.shield_sprite:
            shield_rect = self.shield_sprite.get_rect(center=(self.x, self.y))
            surface.blit(self.shield_sprite, shield_rect)
        
        if self.sprite:
            # Rotate sprite to match player angle
            rotated_sprite = pygame.transform.rotate(
                self.sprite, -math.degrees(self.angle)
            )
            # Get the rect for the rotated sprite to center it
            rect = rotated_sprite.get_rect(center=(self.x, self.y))
            surface.blit(rotated_sprite, rect)
        else:
            # Draw a simple triangle if no sprite is available
            color = config.BLUE if self.player_id == 1 else config.RED
            points = [
                (
                    self.x + self.radius * math.cos(self.angle),
                    self.y + self.radius * math.sin(self.angle)
                ),
                (
                    self.x + self.radius * math.cos(self.angle + 2.5),
                    self.y + self.radius * math.sin(self.angle + 2.5)
                ),
                (
                    self.x + self.radius * math.cos(self.angle - 2.5),
                    self.y + self.radius * math.sin(self.angle - 2.5)
                )
            ]
            pygame.draw.polygon(surface, color, points)
            
            # Draw a small circle at the center
            pygame.draw.circle(surface, config.WHITE, (int(self.x), int(self.y)), 3)
            
        # Visual indicator for speed boost
        if self.speed_boost_active:
            pygame.draw.circle(surface, config.YELLOW, (int(self.x), int(self.y)), 
                              self.radius + 5, 2)
            
        # Visual indicator for double shot
        if self.double_shot:
            pygame.draw.circle(surface, config.GREEN, (int(self.x), int(self.y)), 
                              self.radius + 8, 2)
    def has_won(self):
        """Check if the player has won (reached 5 points).
        
        Returns:
            True if the player has won, False otherwise
        """
        return self.score >= 5
    def increment_score(self):
        """Increment the player's score.
        
        Returns:
            The new score
        """
        self.score += 1
        return self.score
