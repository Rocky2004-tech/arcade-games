"""
Level module for Stack Dash game.
"""
import pygame
import os
import random
import math

import config
from utils.game_utils import load_image

class Platform:
    """Platform class for Stack Dash."""
    
    def __init__(self, x, y, width, height):
        """Initialize a platform.
        
        Args:
            x: X position
            y: Y position
            width: Width of platform
            height: Height of platform
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (100, 100, 100)
        self.border_color = (50, 50, 50)
    
    def get_rect(self):
        """Get the platform's bounding rectangle.
        
        Returns:
            pygame.Rect: The platform's bounding rectangle
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen, camera_x=0):
        """Draw the platform.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x offset
        """
        pygame.draw.rect(screen, self.color, 
                       (self.x - camera_x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.border_color, 
                       (self.x - camera_x, self.y, self.width, self.height), 2)


class Tile:
    """Collectible tile class for Stack Dash."""
    
    def __init__(self, x, y):
        """Initialize a tile.
        
        Args:
            x: X position
            y: Y position
        """
        self.x = x
        self.y = y
        self.width = 30
        self.height = 10
        self.color = (50, 150, 250)
        self.border_color = (20, 100, 200)
        self.collected = False
        
        # Animation properties
        self.hover_offset = 0
        self.hover_speed = random.uniform(0.02, 0.05)
        self.hover_range = random.uniform(3, 6)
        self.original_y = y
    
    def update(self):
        """Update tile animation."""
        self.hover_offset += self.hover_speed
        self.y = self.original_y + math.sin(self.hover_offset) * self.hover_range
    
    def get_rect(self):
        """Get the tile's bounding rectangle.
        
        Returns:
            pygame.Rect: The tile's bounding rectangle
        """
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, 
                          self.width, self.height)
    
    def draw(self, screen, camera_x=0):
        """Draw the tile.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x offset
        """
        if not self.collected:
            pygame.draw.rect(screen, self.color, 
                           (self.x - self.width // 2 - camera_x, 
                            self.y - self.height // 2, 
                            self.width, self.height))
            pygame.draw.rect(screen, self.border_color, 
                           (self.x - self.width // 2 - camera_x, 
                            self.y - self.height // 2, 
                            self.width, self.height), 2)


class PowerUp:
    """Power-up class for Stack Dash."""
    
    TYPES = ["speed", "jump", "magnet"]
    
    def __init__(self, x, y, powerup_type=None):
        """Initialize a power-up.
        
        Args:
            x: X position
            y: Y position
            powerup_type: Type of power-up (speed, jump, magnet)
        """
        self.x = x
        self.y = y
        self.radius = 15
        self.type = powerup_type or random.choice(PowerUp.TYPES)
        self.collected = False
        
        # Set color based on type
        if self.type == "speed":
            self.color = (255, 255, 0)  # Yellow
            self.border_color = (200, 200, 0)
        elif self.type == "jump":
            self.color = (0, 255, 0)  # Green
            self.border_color = (0, 200, 0)
        else:  # magnet
            self.color = (255, 0, 255)  # Purple
            self.border_color = (200, 0, 200)
        
        # Animation properties
        self.pulse_size = 0
        self.pulse_speed = 0.1
        self.pulse_direction = 1
    
    def update(self):
        """Update power-up animation."""
        self.pulse_size += self.pulse_speed * self.pulse_direction
        if self.pulse_size > 3:
            self.pulse_direction = -1
        elif self.pulse_size < -3:
            self.pulse_direction = 1
    
    def get_rect(self):
        """Get the power-up's bounding rectangle.
        
        Returns:
            pygame.Rect: The power-up's bounding rectangle
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def draw(self, screen, camera_x=0):
        """Draw the power-up.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x offset
        """
        if not self.collected:
            # Draw pulsing circle
            radius = self.radius + self.pulse_size
            pygame.draw.circle(screen, self.color, 
                             (self.x - camera_x, self.y), radius)
            pygame.draw.circle(screen, self.border_color, 
                             (self.x - camera_x, self.y), radius, 2)


class FinishLine:
    """Finish line class for Stack Dash."""
    
    def __init__(self, x, y, height=200):
        """Initialize the finish line.
        
        Args:
            x: X position
            y: Y position
            height: Height of the finish line
        """
        self.x = x
        self.y = y
        self.width = 20
        self.height = height
        self.color = (255, 215, 0)  # Gold
        self.border_color = (218, 165, 32)  # Goldenrod
        
        # Animation properties
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
    
    def update(self):
        """Update finish line animation."""
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def get_rect(self):
        """Get the finish line's bounding rectangle.
        
        Returns:
            pygame.Rect: The finish line's bounding rectangle
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen, camera_x=0):
        """Draw the finish line.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x offset
        """
        # Draw finish line pole
        pygame.draw.rect(screen, self.color, 
                       (self.x - camera_x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.border_color, 
                       (self.x - camera_x, self.y, self.width, self.height), 2)
        
        # Draw checkered flag at top
        flag_width = 60
        flag_height = 40
        flag_x = self.x - camera_x
        flag_y = self.y - flag_height
        
        # Draw flag background
        pygame.draw.rect(screen, (255, 255, 255), 
                       (flag_x, flag_y, flag_width, flag_height))
        
        # Draw checkered pattern
        square_size = 10
        offset = self.animation_frame * 5  # Animate flag
        
        for row in range(4):
            for col in range(6):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, (0, 0, 0), 
                                   (flag_x + col * square_size + offset % square_size, 
                                    flag_y + row * square_size, 
                                    square_size, square_size))


class Level:
    """Level class for Stack Dash."""
    
    def __init__(self):
        """Initialize the level."""
        self.platforms = []
        self.tiles = []
        self.power_ups = []
        self.finish_line = None
        
        # Level properties
        self.level_width = 5000
        self.ground_height = config.SCREEN_HEIGHT - 50
        
        # Generate level
        self._generate_level()
        
        # Load background images
        self._load_backgrounds()
    
    def _load_backgrounds(self):
        """Load background images for parallax scrolling."""
        self.backgrounds = []
        
        # Try to load background layers
        try:
            bg_path = os.path.join(config.ASSETS_DIR, "stack_dash", "backgrounds")
            
            for i in range(1, 4):
                layer_path = os.path.join(bg_path, f"parallax_layer{i}.png")
                if os.path.exists(layer_path):
                    self.backgrounds.append({
                        "image": load_image(layer_path, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)),
                        "speed": 0.2 * i  # Different speeds for parallax effect
                    })
        except Exception as e:
            print(f"Error loading background images: {e}")
        
        # Create placeholder backgrounds if loading failed
        if not self.backgrounds:
            for i in range(3):
                surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                color_val = 50 + i * 50
                surf.fill((color_val, color_val, color_val))
                self.backgrounds.append({
                    "image": surf,
                    "speed": 0.2 * (i + 1)
                })
    
    def _generate_level(self):
        """Generate the level layout."""
        import math  # Import here to avoid circular import
        
        # Create ground platform
        ground = Platform(0, self.ground_height, self.level_width, 50)
        self.platforms.append(ground)
        
        # Create platforms with gaps
        platform_width = 300
        gap_width = 100
        platform_height = 20
        
        x = 500  # Start first platform after some space
        while x < self.level_width - 500:  # Leave space at the end
            # Add platform
            platform_y = self.ground_height - random.randint(100, 200)
            platform = Platform(x, platform_y, platform_width, platform_height)
            self.platforms.append(platform)
            
            # Add tiles on platform
            self._add_tiles_on_platform(platform)
            
            # Occasionally add power-up
            if random.random() < 0.3:
                power_up = PowerUp(
                    x + random.randint(50, platform_width - 50),
                    platform_y - 30
                )
                self.power_ups.append(power_up)
            
            # Move to next platform position
            x += platform_width + gap_width
            
            # Vary gap width for next gap
            gap_width = random.randint(80, 150)
        
        # Add finish line at the end
        self.finish_line = FinishLine(
            self.level_width - 300,
            self.ground_height - 200,
            200
        )
    
    def _add_tiles_on_platform(self, platform):
        """Add collectible tiles on a platform.
        
        Args:
            platform: Platform to add tiles to
        """
        # Add 2-5 tiles on the platform
        num_tiles = random.randint(2, 5)
        
        for _ in range(num_tiles):
            tile_x = platform.x + random.randint(30, platform.width - 30)
            tile_y = platform.y - random.randint(30, 60)
            
            tile = Tile(tile_x, tile_y)
            self.tiles.append(tile)
    
    def update(self):
        """Update level elements."""
        # Update tiles
        for tile in self.tiles:
            tile.update()
        
        # Update power-ups
        for power_up in self.power_ups:
            power_up.update()
        
        # Update finish line
        if self.finish_line:
            self.finish_line.update()
    
    def check_tile_collection(self, player):
        """Check if player collects any tiles.
        
        Args:
            player: Player object
            
        Returns:
            Tile: The collected tile or None
        """
        player_rect = player.get_rect()
        
        for tile in self.tiles:
            if not tile.collected and player_rect.colliderect(tile.get_rect()):
                tile.collected = True
                return tile
                
        return None
    
    def check_powerup_collision(self, player):
        """Check if player collects any power-ups.
        
        Args:
            player: Player object
            
        Returns:
            str: The power-up type or None
        """
        player_rect = player.get_rect()
        
        for power_up in self.power_ups:
            if not power_up.collected and player_rect.colliderect(power_up.get_rect()):
                power_up.collected = True
                return power_up.type
                
        return None
    
    def check_gap(self, player):
        """Check if player is over a gap and needs to build a bridge.
        
        Args:
            player: Player object
            
        Returns:
            bool: True if player is over a gap, False otherwise
        """
        # Don't check for gaps if the player just jumped (safety period)
        if player.jump_safety > 0:
            return False
            
        # Only check for gaps if player is moving horizontally, falling, and not on ground
        # Also, don't check during the peak of a jump (when velocity is near zero)
        if (player.vel_y > 2.0 and  # Only when falling at a certain speed
            not player.on_ground and 
            abs(player.vel_x) > 0.5):  # Only when moving horizontally
            
            # Create a ray cast downward from player
            ray_rect = pygame.Rect(
                player.x - 5,
                player.y,
                10,
                100  # Check 100 pixels below
            )
            
            # Check if ray intersects with any platform
            for platform in self.platforms:
                if ray_rect.colliderect(platform.get_rect()):
                    return False
            
            # If no platform below, player is over a gap
            return True
        
        return False
    
    def build_bridge(self, x, y):
        """Build a bridge at the specified position.
        
        Args:
            x: X position
            y: Y position
        """
        # Create a small platform at the position
        bridge = Platform(x - 20, y + 20, 40, 10)
        bridge.color = (50, 150, 250)  # Blue color for bridges
        bridge.border_color = (20, 100, 200)
        self.platforms.append(bridge)
    
    def check_finish_line(self, player):
        """Check if player reached the finish line.
        
        Args:
            player: Player object
            
        Returns:
            bool: True if player reached finish line, False otherwise
        """
        if self.finish_line and player.get_rect().colliderect(self.finish_line.get_rect()):
            return True
        return False
    
    def check_collision(self, player):
        """Check and handle collisions between player and platforms.
        
        Args:
            player: Player object
        """
        # Store previous position for better collision resolution
        prev_x = player.x
        prev_y = player.y
        player_rect = player.get_rect()
        
        # Reset on_ground flag before checking collisions
        was_on_ground = player.on_ground
        player.on_ground = False
        
        # Check for ground collision first (optimization)
        for platform in self.platforms:
            platform_rect = platform.get_rect()
            
            # Check if player is directly above the platform (potential ground)
            if (abs(player.x - (platform.x + platform.width/2)) < platform.width/2 + player.width/2 and
                player.y + player.height/2 >= platform.y - 5 and 
                player.y + player.height/2 <= platform.y + 10 and
                player.vel_y >= 0):
                
                # Land on platform
                player.y = platform.y - player.height/2
                player.vel_y = 0
                player.on_ground = True
                return
        
        # Check for other collisions if not on ground
        for platform in self.platforms:
            platform_rect = platform.get_rect()
            
            if player_rect.colliderect(platform_rect):
                # Determine collision direction by checking which side has the smallest overlap
                
                # Calculate overlaps
                left_overlap = (platform.x + platform.width) - (player.x - player.width/2)
                right_overlap = (player.x + player.width/2) - platform.x
                top_overlap = (platform.y + platform.height) - (player.y - player.height/2)
                bottom_overlap = (player.y + player.height/2) - platform.y
                
                # Find minimum overlap
                min_overlap = min(left_overlap, right_overlap, top_overlap, bottom_overlap)
                
                # Resolve collision based on minimum overlap
                if min_overlap == bottom_overlap and player.vel_y < 0:
                    # Collision from below
                    player.y = platform.y + platform.height + player.height/2
                    player.vel_y = 0
                elif min_overlap == left_overlap and player.vel_x > 0:
                    # Collision from left
                    player.x = platform.x - player.width/2
                    player.vel_x = 0
                elif min_overlap == right_overlap and player.vel_x < 0:
                    # Collision from right
                    player.x = platform.x + platform.width + player.width/2
                    player.vel_x = 0
                elif min_overlap == top_overlap and player.vel_y > 0:
                    # Collision from above
                    player.y = platform.y - player.height/2
                    player.vel_y = 0
                    player.on_ground = True
        
        # If player was on ground but now falling with no velocity, start falling
        if was_on_ground and not player.on_ground and player.vel_y == 0:
            player.vel_y = 0.1
    
    def draw_background(self, screen, camera_x):
        """Draw parallax scrolling background.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x offset
        """
        # Draw each background layer with parallax effect
        for bg in self.backgrounds:
            # Calculate parallax offset
            offset = int(camera_x * bg["speed"]) % config.SCREEN_WIDTH
            
            # Draw first copy
            screen.blit(bg["image"], (-offset, 0))
            
            # Draw second copy to fill the gap
            if offset > 0:
                screen.blit(bg["image"], (config.SCREEN_WIDTH - offset, 0))
    
    def draw(self, screen, camera_x):
        """Draw the level.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x offset
        """
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen, camera_x)
        
        # Draw tiles
        for tile in self.tiles:
            tile.draw(screen, camera_x)
        
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(screen, camera_x)
        
        # Draw finish line
        if self.finish_line:
            self.finish_line.draw(screen, camera_x)
