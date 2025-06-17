#!/usr/bin/env python3
"""
Arcade Game Hub - Main Entry Point
"""
import pygame
import sys
import traceback
from launcher.launcher import GameLauncher
import config

def main():
    """Initialize pygame and start the game launcher."""
    pygame.init()
    pygame.display.set_caption("Arcade Game Hub")
    
    # Set up the display
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Create and run the launcher
    launcher = GameLauncher(screen)
    
    # Main loop
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Pass events to the launcher
                try:
                    launcher.handle_event(event)
                except Exception as e:
                    print(f"Error handling event: {e}")
                    traceback.print_exc()
            
            # Update and render
            try:
                launcher.update()
                launcher.render()
            except Exception as e:
                print(f"Error in update/render: {e}")
                traceback.print_exc()
            
            pygame.display.flip()
            clock.tick(config.FPS)
        except Exception as e:
            print(f"Critical error in main loop: {e}")
            traceback.print_exc()
            running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
