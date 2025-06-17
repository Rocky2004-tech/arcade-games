"""
Button class for the Arcade Game Hub launcher.
"""
import pygame
import config

class Button:
    """Interactive button for UI navigation."""
    
    def __init__(self, x, y, width, height, text, action=None):
        """Initialize a new button.
        
        Args:
            x: X-coordinate position
            y: Y-coordinate position
            width: Button width
            height: Button height
            text: Button text
            action: Function to call when button is clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.Font(None, 32)
        
        # Try to load custom font if available
        try:
            if pygame.font.get_init() and pygame.font.get_fonts():
                self.font = pygame.font.Font(config.FONT_PATH, 32)
        except:
            pass
    
    def handle_event(self, event):
        """Process pygame events for the button.
        
        Args:
            event: Pygame event to process
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
    
    def update(self):
        """Update button state."""
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
    
    def draw(self, surface):
        """Draw the button on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw button background
        color = config.BUTTON_HOVER_COLOR if self.is_hovered else config.BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, config.WHITE, self.rect, 2, border_radius=10)
        
        # Draw button text
        text_surf = self.font.render(self.text, True, config.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
