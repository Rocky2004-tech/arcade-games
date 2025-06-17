"""
Bullet class for Bullet Bounce game.
"""
import pygame
import math
import os
import random

import config
from utils.game_utils import load_image

class Bullet:
    """Bullet projectile that bounces off walls."""
    
    def __init__(self, x, y, angle, speed=10, owner_id=1):
        """Initialize a bullet.
        
        Args:
            x: Starting x position
            y: Starting y position
            angle: Direction angle in radians
            speed: Bullet speed
            owner_id: ID of the player who fired this bullet
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = 5
        self.bounces = 0
        self.max_bounces = 3
        self.lifetime = 300  # frames (5 seconds at 60 FPS)
        self.owner_id = owner_id
        
        # Trail effect
        self.trail = []
        self.max_trail_length = 10
        
        # Calculate velocity components
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # Try to load bullet sprite
        self.sprite = None
        sprite_name = "bullet_blue.png" if owner_id == 1 else "bullet_red.png"
        sprite_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "sprites", sprite_name)
        if os.path.exists(sprite_path):
            self.sprite = load_image(sprite_path, (self.radius * 2, self.radius * 2), True)
    
    def update(self):
        """Update bullet position."""
        # Store current position for trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
            
        # Update position
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    
    def bounce(self, wall_rect=None):
        """Handle bullet bouncing off a surface.
        
        Args:
            wall_rect: Rectangle of the wall that was hit (optional)
        """
        # If wall_rect is provided, use it for more accurate bouncing
        if wall_rect:
            # Determine which side of the wall was hit
            bullet_center = pygame.Vector2(self.x, self.y)
            wall_center = pygame.Vector2(wall_rect.center)
            
            # Calculate the vector from wall center to bullet
            diff = bullet_center - wall_center
            
            # Check if collision is more horizontal or vertical
            if abs(diff.x) * wall_rect.height > abs(diff.y) * wall_rect.width:
                # Horizontal collision (left/right walls)
                self.vx = -self.vx
            else:
                # Vertical collision (top/bottom walls)
                self.vy = -self.vy
        else:
            # Simplified bounce logic if no wall_rect provided
            if abs(self.x - 0) < 10 or abs(self.x - config.SCREEN_WIDTH) < 10:
                self.vx = -self.vx
            if abs(self.y - 0) < 10 or abs(self.y - config.SCREEN_HEIGHT) < 10:
                self.vy = -self.vy
            
        # Add slight randomness to bounce for more interesting gameplay
        angle_variation = random.uniform(-0.1, 0.1)
        current_speed = math.sqrt(self.vx**2 + self.vy**2)
        new_angle = math.atan2(self.vy, self.vx) + angle_variation
        
        self.vx = math.cos(new_angle) * current_speed
        self.vy = math.sin(new_angle) * current_speed
            
        # Update angle based on new velocity
        self.angle = math.atan2(self.vy, self.vx)
        
        # Count the bounce
        self.bounces += 1
    
    def should_remove(self):
        """Check if the bullet should be removed.
        
        Returns:
            True if the bullet should be removed
        """
        # Remove if out of bounds
        if (self.x < -50 or self.x > config.SCREEN_WIDTH + 50 or
            self.y < -50 or self.y > config.SCREEN_HEIGHT + 50):
            return True
            
        # Remove if exceeded max bounces
        if self.bounces > self.max_bounces:
            return True
            
        # Remove if lifetime expired
        if self.lifetime <= 0:
            return True
            
        return False
    
    def draw(self, surface):
        """Draw the bullet on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw trail
        if len(self.trail) > 1:
            # Calculate trail color based on owner
            if self.owner_id == 1:
                trail_color = config.BLUE
            else:
                trail_color = config.RED
                
            # Draw trail with fading opacity
            for i in range(len(self.trail) - 1):
                # Calculate opacity based on position in trail
                alpha = int(255 * (i / len(self.trail)))
                # Create a surface for the trail segment
                trail_surf = pygame.Surface((3, 3), pygame.SRCALPHA)
                trail_color_with_alpha = (*trail_color[:3], alpha)
                pygame.draw.circle(trail_surf, trail_color_with_alpha, (1, 1), 1)
                # Draw the trail segment
                surface.blit(trail_surf, (self.trail[i][0] - 1, self.trail[i][1] - 1))
        
        # Draw the bullet
        if self.sprite:
            # Rotate sprite to match bullet angle
            rotated_sprite = pygame.transform.rotate(
                self.sprite, -math.degrees(self.angle)
            )
            # Get the rect for the rotated sprite to center it
            rect = rotated_sprite.get_rect(center=(self.x, self.y))
            surface.blit(rotated_sprite, rect)
        else:
            # Draw a simple circle if no sprite is available
            color = config.BLUE if self.owner_id == 1 else config.RED
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
            
            # Add a white center for glow effect
            pygame.draw.circle(surface, config.WHITE, (int(self.x), int(self.y)), self.radius // 2)
