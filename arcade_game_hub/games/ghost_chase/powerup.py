"""
Powerup classes for Ghost Chase game.
"""
import pygame
from games.ghost_chase.ghost import Ghost

class Orb:
    """Orb collectible class."""
    
    def __init__(self, x, y):
        """Initialize the orb.
        
        Args:
            x: X position
            y: Y position
        """
        self.x = x
        self.y = y
        self.collected = False
        self.pulse_size = 0
        self.pulse_growing = True
    
    def update(self):
        """Update orb animation."""
        # Pulsing animation
        if self.pulse_growing:
            self.pulse_size += 0.05
            if self.pulse_size >= 1.0:
                self.pulse_growing = False
        else:
            self.pulse_size -= 0.05
            if self.pulse_size <= 0.0:
                self.pulse_growing = True
    
    def collect(self):
        """Mark the orb as collected."""
        self.collected = True


class PowerUp:
    """Base class for power-ups."""
    
    def __init__(self, x, y, power_type):
        """Initialize the power-up.
        
        Args:
            x: X position
            y: Y position
            power_type: Type of power-up
        """
        self.x = x
        self.y = y
        self.type = power_type
        self.collected = False
    
    def collect(self):
        """Mark the power-up as collected."""
        self.collected = True


class SpeedBoost(PowerUp):
    """Speed boost power-up."""
    
    def __init__(self, x, y):
        """Initialize the speed boost power-up.
        
        Args:
            x: X position
            y: Y position
        """
        super().__init__(x, y, "speed")
    
    def apply(self, player):
        """Apply the speed boost effect to the player.
        
        Args:
            player: Player object to apply the effect to
        """
        if isinstance(player, Ghost):
            player.activate_speed_boost()
        else:  # Runner
            player.sprint()


class Invisibility(PowerUp):
    """Invisibility power-up."""
    
    def __init__(self, x, y):
        """Initialize the invisibility power-up.
        
        Args:
            x: X position
            y: Y position
        """
        super().__init__(x, y, "invisibility")
        self.duration = 180  # 3 seconds at 60 FPS
    
    def apply(self, player):
        """Apply the invisibility effect to the player.
        
        Args:
            player: Player object to apply the effect to
        """
        player.invisible = True
        player.invisibility_timer = self.duration
