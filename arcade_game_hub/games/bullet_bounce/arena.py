"""
Arena class for Bullet Bounce game.
"""
import pygame
import os
import random

import config
from utils.game_utils import load_image

class PowerUp:
    """Power-up item that can be collected by players."""
    
    SHIELD = 1
    SPEED = 2
    DOUBLE_SHOT = 3
    
    def __init__(self, x, y, power_type):
        """Initialize a power-up.
        
        Args:
            x: X position
            y: Y position
            power_type: Type of power-up (SHIELD, SPEED, or DOUBLE_SHOT)
        """
        self.x = x
        self.y = y
        self.type = power_type
        self.radius = 15
        self.pulse_size = 0
        self.pulse_growing = True
        self.lifetime = 600  # 10 seconds at 60 FPS
        
        # Try to load power-up sprite
        self.sprite = None
        sprite_name = ""
        if power_type == PowerUp.SHIELD:
            sprite_name = "powerup_shield.png"
        elif power_type == PowerUp.SPEED:
            sprite_name = "powerup_speed.png"
        elif power_type == PowerUp.DOUBLE_SHOT:
            sprite_name = "powerup_double.png"
            
        sprite_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "sprites", sprite_name)
        if os.path.exists(sprite_path):
            self.sprite = load_image(sprite_path, (self.radius * 2, self.radius * 2), True)
    
    def update(self):
        """Update power-up state."""
        # Update pulse animation
        if self.pulse_growing:
            self.pulse_size += 0.2
            if self.pulse_size >= 5:
                self.pulse_growing = False
        else:
            self.pulse_size -= 0.2
            if self.pulse_size <= 0:
                self.pulse_growing = True
                
        # Decrease lifetime
        self.lifetime -= 1
    
    def should_remove(self):
        """Check if the power-up should be removed.
        
        Returns:
            True if the power-up should be removed
        """
        return self.lifetime <= 0
    
    def draw(self, surface):
        """Draw the power-up on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        if self.sprite:
            # Draw pulsing glow effect
            glow_radius = int(self.radius + self.pulse_size)
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            
            # Choose color based on power-up type
            if self.type == PowerUp.SHIELD:
                glow_color = (0, 255, 255, 100)  # Cyan
            elif self.type == PowerUp.SPEED:
                glow_color = (255, 255, 0, 100)  # Yellow
            else:
                glow_color = (0, 255, 0, 100)  # Green
                
            pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surf, (self.x - glow_radius, self.y - glow_radius))
            
            # Draw sprite
            rect = self.sprite.get_rect(center=(self.x, self.y))
            surface.blit(self.sprite, rect)
        else:
            # Draw a simple circle if no sprite is available
            if self.type == PowerUp.SHIELD:
                color = config.CYAN
            elif self.type == PowerUp.SPEED:
                color = config.YELLOW
            else:
                color = config.GREEN
                
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, config.WHITE, (int(self.x), int(self.y)), int(self.radius + self.pulse_size), 2)

class Arena:
    """Game arena with walls and obstacles."""
    
    def __init__(self):
        """Initialize the arena."""
        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
        self.wall_thickness = 20
        self.power_ups = []
        self.power_up_timer = 600  # 10 seconds at 60 FPS
        self.power_up_spawn_rate = 600  # How often to spawn power-ups
        
        # Define walls as rectangles
        self.walls = [
            pygame.Rect(0, 0, self.width, self.wall_thickness),  # Top
            pygame.Rect(0, self.height - self.wall_thickness, self.width, self.wall_thickness),  # Bottom
            pygame.Rect(0, 0, self.wall_thickness, self.height),  # Left
            pygame.Rect(self.width - self.wall_thickness, 0, self.wall_thickness, self.height)  # Right
        ]
        
        # Add some obstacles in the arena
        self.obstacles = [
            pygame.Rect(self.width // 4, self.height // 2 - 50, 20, 100),  # Left obstacle
            pygame.Rect(self.width * 3 // 4 - 20, self.height // 2 - 50, 20, 100)  # Right obstacle
        ]
        
        # Combine walls and obstacles
        self.all_obstacles = self.walls + self.obstacles
        
        # Try to load background image
        self.background = None
        bg_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "backgrounds", "arena.png")
        if os.path.exists(bg_path):
            self.background = load_image(bg_path, (self.width, self.height))
            
        # Load wall texture
        self.wall_texture = None
        wall_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "backgrounds", "wall.png")
        if os.path.exists(wall_path):
            self.wall_texture = load_image(wall_path, (self.wall_thickness, self.wall_thickness))
    
    def update(self):
        """Update arena state."""
        # Update power-up timer
        self.power_up_timer -= 1
        if self.power_up_timer <= 0:
            self.spawn_power_up()
            self.power_up_timer = self.power_up_spawn_rate
            
        # Update existing power-ups
        for power_up in self.power_ups[:]:
            power_up.update()
            if power_up.should_remove():
                self.power_ups.remove(power_up)
    
    def spawn_power_up(self):
        """Spawn a new power-up at a random location."""
        # Choose a random power-up type
        power_type = random.choice([PowerUp.SHIELD, PowerUp.SPEED, PowerUp.DOUBLE_SHOT])
        
        # Find a valid position (not inside walls or obstacles)
        valid_position = False
        x, y = 0, 0
        
        while not valid_position:
            # Generate random position
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            
            # Check if position is valid
            valid_position = True
            for obstacle in self.all_obstacles:
                if obstacle.collidepoint(x, y):
                    valid_position = False
                    break
        
        # Create and add the power-up
        self.power_ups.append(PowerUp(x, y, power_type))
    
    def check_collision(self, bullet):
        """Check if a bullet collides with any wall or obstacle.
        
        Args:
            bullet: Bullet object to check
            
        Returns:
            Tuple (bool, Rect): True and the wall rect if collision detected, (False, None) otherwise
        """
        bullet_rect = pygame.Rect(
            bullet.x - bullet.radius,
            bullet.y - bullet.radius,
            bullet.radius * 2,
            bullet.radius * 2
        )
        
        for wall in self.all_obstacles:
            if wall.colliderect(bullet_rect):
                return True, wall
                
        return False, None
    
    def check_power_up_collision(self, player):
        """Check if a player collides with any power-up.
        
        Args:
            player: Player object to check
            
        Returns:
            PowerUp object if collision detected, None otherwise
        """
        for power_up in self.power_ups[:]:
            # Calculate distance between player and power-up
            distance = ((player.x - power_up.x) ** 2 + (player.y - power_up.y) ** 2) ** 0.5
            
            # Check if distance is less than sum of radii
            if distance < player.radius + power_up.radius:
                self.power_ups.remove(power_up)
                return power_up
                
        return None
    
    def draw(self, surface):
        """Draw the arena on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            # Draw a simple background if no image is available
            surface.fill((10, 10, 30))  # Dark blue background
            
            # Draw grid lines for a tech feel
            grid_spacing = 40
            grid_color = (30, 30, 50)
            
            # Draw vertical grid lines
            for x in range(0, self.width, grid_spacing):
                pygame.draw.line(surface, grid_color, (x, 0), (x, self.height))
                
            # Draw horizontal grid lines
            for y in range(0, self.height, grid_spacing):
                pygame.draw.line(surface, grid_color, (0, y), (self.width, y))
            
        # Draw walls and obstacles
        for obstacle in self.all_obstacles:
            if self.wall_texture:
                # Tile the texture across the obstacle
                for x in range(obstacle.left, obstacle.right, self.wall_thickness):
                    for y in range(obstacle.top, obstacle.bottom, self.wall_thickness):
                        surface.blit(self.wall_texture, (x, y))
                        
                # Draw neon outline
                pygame.draw.rect(surface, (0, 200, 255), obstacle, 2)
            else:
                # Draw a simple rectangle with neon effect if no texture is available
                pygame.draw.rect(surface, (0, 0, 100), obstacle)
                pygame.draw.rect(surface, (0, 200, 255), obstacle, 2)
                
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(surface)
