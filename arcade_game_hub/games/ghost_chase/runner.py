"""
Runner class for Ghost Chase game.
"""
import pygame

class Runner:
    """Runner player class."""
    
    def __init__(self, x, y):
        """Initialize the runner.
        
        Args:
            x: Initial x position
            y: Initial y position
        """
        self.x = x
        self.y = y
        self.sprint_active = False
        self.sprint_timer = 0
        self.sprint_cooldown = 0
        self.sprint_energy = 100  # Percentage
        self.sprint_cost = 30  # Percentage
        self.sprint_recharge_rate = 0.5  # Percentage per frame
        self.decoy_placed = False
        self.decoy_x = 0
        self.decoy_y = 0
        self.has_decoy = True  # Player starts with one decoy
    
    def move(self, dx, dy, maze):
        """Move the runner.
        
        Args:
            dx: X direction (-1, 0, 1)
            dy: Y direction (-1, 0, 1)
            maze: Maze object for collision detection
        """
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if the new position is valid (not a wall)
        if not maze.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    def sprint(self):
        """Activate sprint ability to move faster.
        
        Returns:
            bool: True if sprint was activated, False otherwise
        """
        if self.sprint_energy >= self.sprint_cost and self.sprint_cooldown <= 0:
            self.sprint_active = True
            self.sprint_timer = 30  # 30 frames = 0.5 seconds at 60 FPS
            self.sprint_energy -= self.sprint_cost
            return True
        return False
    
    def place_decoy(self):
        """Place a decoy to distract the ghost.
        
        Returns:
            bool: True if decoy was placed, False otherwise
        """
        if self.has_decoy and not self.decoy_placed:
            self.decoy_placed = True
            self.decoy_x = self.x
            self.decoy_y = self.y
            self.has_decoy = False  # Use up the decoy
            return True
        return False
    
    def update(self):
        """Update runner state."""
        # Update sprint
        if self.sprint_active:
            self.sprint_timer -= 1
            if self.sprint_timer <= 0:
                self.sprint_active = False
                self.sprint_cooldown = 60  # 1 second cooldown
        
        # Update sprint cooldown
        if self.sprint_cooldown > 0:
            self.sprint_cooldown -= 1
        
        # Recharge sprint energy
        if self.sprint_energy < 100:
            self.sprint_energy += self.sprint_recharge_rate
            if self.sprint_energy > 100:
                self.sprint_energy = 100
