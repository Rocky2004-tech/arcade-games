"""
Ghost class for Ghost Chase game.
"""
import pygame

class Ghost:
    """Ghost player class."""
    
    def __init__(self, x, y):
        """Initialize the ghost.
        
        Args:
            x: Initial x position
            y: Initial y position
        """
        self.x = x
        self.y = y
        self.sonar_active = False
        self.sonar_radius = 0
        self.sonar_max_radius = 5
        self.sonar_charge = 100  # Percentage
        self.sonar_recharge_rate = 0.5  # Percentage per frame
        self.sonar_cost = 30  # Percentage
        self.speed_boost_active = False
        self.speed_boost_timer = 0
    
    def move(self, dx, dy, maze):
        """Move the ghost.
        
        Args:
            dx: X direction (-1, 0, 1)
            dy: Y direction (-1, 0, 1)
            maze: Maze object for collision detection
        """
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if the new position is valid (not a wall or is a ghost path)
        if not maze.is_wall(new_x, new_y) or maze.is_ghost_path(new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    def activate_sonar(self):
        """Activate the sonar ability to locate the runner."""
        if self.sonar_charge >= self.sonar_cost and not self.sonar_active:
            self.sonar_active = True
            self.sonar_radius = 1
            self.sonar_charge -= self.sonar_cost
            return True
        return False
    
    def activate_speed_boost(self):
        """Activate speed boost ability."""
        if self.sonar_charge >= 50 and not self.speed_boost_active:
            self.speed_boost_active = True
            self.speed_boost_timer = 60  # 60 frames = 1 second at 60 FPS
            self.sonar_charge -= 50
    
    def update(self):
        """Update ghost state."""
        # Update sonar
        if self.sonar_active:
            self.sonar_radius += 0.2
            if self.sonar_radius >= self.sonar_max_radius:
                self.sonar_active = False
                self.sonar_radius = 0
        
        # Recharge sonar
        if self.sonar_charge < 100:
            self.sonar_charge += self.sonar_recharge_rate
            if self.sonar_charge > 100:
                self.sonar_charge = 100
        
        # Update speed boost
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
