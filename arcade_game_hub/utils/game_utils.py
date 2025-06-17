"""
Shared utility functions for the Arcade Game Hub.
"""
import math
import pygame
import config

def distance(point1, point2):
    """Calculate the distance between two points.
    
    Args:
        point1: (x, y) tuple for first point
        point2: (x, y) tuple for second point
        
    Returns:
        Float distance between the points
    """
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def angle_between(point1, point2):
    """Calculate the angle between two points in radians.
    
    Args:
        point1: (x, y) tuple for first point
        point2: (x, y) tuple for second point
        
    Returns:
        Angle in radians
    """
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

def load_image(path, scale=None, alpha=False):
    """Load an image from file with optional scaling.
    
    Args:
        path: Path to the image file
        scale: Optional (width, height) tuple to scale the image
        alpha: Whether to include alpha channel
        
    Returns:
        Loaded pygame Surface
    """
    try:
        if alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
            
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf

def draw_text(surface, text, font, color, x, y, align="center"):
    """Draw text on a surface with alignment options.
    
    Args:
        surface: Pygame surface to draw on
        text: Text to render
        font: Pygame font object
        color: Text color (RGB tuple)
        x, y: Position coordinates
        align: Text alignment ("left", "center", or "right")
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "left":
        text_rect.topleft = (x, y)
    elif align == "center":
        text_rect.center = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
        
    surface.blit(text_surface, text_rect)
