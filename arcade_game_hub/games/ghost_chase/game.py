"""
Ghost Chase - A maze game where players take turns as Ghost and Runner.
"""
import pygame
import sys
import random
import math
from enum import Enum

import config
from games.ghost_chase.maze import Maze
from games.ghost_chase.ghost import Ghost
from games.ghost_chase.runner import Runner
from games.ghost_chase.powerup import Orb

class GameState(Enum):
    """Game state enumeration."""
    MENU = 0
    PLAYING = 1
    ROUND_END = 2
    GAME_OVER = 3
    PAUSED = 4

class Game:
    """Main Ghost Chase game class."""
    
    def __init__(self, screen):
        """Initialize the game.
        
        Args:
            screen: Pygame surface for rendering
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Try to load custom font if available
        try:
            if pygame.font.get_init() and pygame.font.get_fonts():
                self.font = pygame.font.Font(config.FONT_PATH, 36)
                self.small_font = pygame.font.Font(config.FONT_PATH, 24)
        except:
            print("Could not load custom font, using default")
        
        # Game state
        self.state = GameState.MENU
        self.round_number = 1
        self.max_rounds = 3
        self.ghost_wins = 0
        self.runner_wins = 0
        self.current_player_is_ghost = True  # First player starts as ghost
        self.round_time = 90  # 90 seconds per round
        self.time_remaining = self.round_time
        self.last_time = pygame.time.get_ticks()
        
        # Load assets
        self.load_assets()
        
        # Create game objects
        self.reset_round()
    
    def load_assets(self):
        """Load game assets."""
        # Load sounds with error handling
        self.sounds = {
            'orb_collect': None,
            'ghost_ping': None,
            'chase_nearby': None,
            'win': None,
            'ambient': None
        }
        
        try:
            # Define sound files to load
            sound_files = {
                'orb_collect': 'orb_collect.wav',
                'ghost_ping': 'ghost_ping.wav',
                'chase_nearby': 'chase_nearby.wav',
                'win': 'win_theme.wav',
                'ambient': 'ambient_loop.mp3'
            }
            
            # Try to load each sound file
            for sound_name, file_name in sound_files.items():
                try:
                    # Try different possible paths
                    paths_to_try = [
                        f'arcade_game_hub/assets/ghost_chase/sounds/{file_name}',
                        f'assets/ghost_chase/sounds/{file_name}',
                        f'./arcade_game_hub/assets/ghost_chase/sounds/{file_name}'
                    ]
                    
                    # Try each path
                    for path in paths_to_try:
                        try:
                            if pygame.mixer.get_init():  # Check if mixer is initialized
                                self.sounds[sound_name] = pygame.mixer.Sound(path)
                                self.sounds[sound_name].set_volume(config.SFX_VOLUME)
                                print(f"Loaded sound: {sound_name} from {path}")
                                break
                        except (FileNotFoundError, pygame.error):
                            continue
                            
                    # If we couldn't load the sound, try the fixed orb sound as fallback
                    if self.sounds[sound_name] is None:
                        fallback_path = 'arcade_game_hub/assets/ghost_chase/sounds/orb_fixed.wav'
                        if pygame.mixer.get_init():
                            self.sounds[sound_name] = pygame.mixer.Sound(fallback_path)
                            self.sounds[sound_name].set_volume(config.SFX_VOLUME)
                            print(f"Using fallback sound for {sound_name}")
                            
                except Exception as e:
                    print(f"Error loading sound {sound_name}: {e}")
                    
            print("Sound loading complete")
                
        except Exception as e:
            print(f"Error in sound loading process: {e}")
            # Sounds dictionary is already initialized with None values
    
    def reset_round(self):
        """Reset the game for a new round."""
        # Create maze
        self.maze = Maze(12, 12)  # 12x12 maze
        
        # Create ghost and runner at opposite corners
        self.ghost = Ghost(1, 1)
        self.runner = Runner(self.maze.width - 2, self.maze.height - 2)
        
        # Create orbs (5 orbs to collect)
        self.orbs = []
        self.create_orbs(5)
        
        # Reset timer
        self.time_remaining = self.round_time
        self.last_time = pygame.time.get_ticks()
        
        # Reset game state
        self.state = GameState.PLAYING
        self.exit_open = False
    
    def create_orbs(self, count):
        """Create orbs at random positions in the maze.
        
        Args:
            count: Number of orbs to create
        """
        self.orbs = []
        available_cells = []
        
        # Find all available cells (not walls, not where ghost or runner starts)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (not self.maze.is_wall(x, y) and 
                    not (x == self.ghost.x and y == self.ghost.y) and
                    not (x == self.runner.x and y == self.runner.y)):
                    available_cells.append((x, y))
        
        # Randomly select positions for orbs
        if len(available_cells) >= count:
            orb_positions = random.sample(available_cells, count)
            for x, y in orb_positions:
                self.orbs.append(Orb(x, y))
    
    def handle_event(self, event):
        """Process pygame events.
        
        Args:
            event: Pygame event to process
            
        Returns:
            False if the game should exit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Stop ambient sound when returning to launcher
                if self.sounds['ambient']:
                    self.sounds['ambient'].stop()
                return False
            
            if event.key == pygame.K_p:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                    self.last_time = pygame.time.get_ticks()  # Reset timer reference
            
            # Handle player input based on game state
            if self.state == GameState.PLAYING:
                # Ghost controls
                if self.current_player_is_ghost:
                    if event.key == pygame.K_w:
                        self.ghost.move(0, -1, self.maze)
                    elif event.key == pygame.K_s:
                        self.ghost.move(0, 1, self.maze)
                    elif event.key == pygame.K_a:
                        self.ghost.move(-1, 0, self.maze)
                    elif event.key == pygame.K_d:
                        self.ghost.move(1, 0, self.maze)
                    elif event.key == pygame.K_SPACE:
                        if self.ghost.activate_sonar():
                            try:
                                if self.sounds['ghost_ping']:
                                    self.sounds['ghost_ping'].play()
                            except Exception as e:
                                print(f"Error playing sonar sound: {e}")
                # Runner controls
                else:
                    if event.key == pygame.K_w:
                        self.runner.move(0, -1, self.maze)
                    elif event.key == pygame.K_s:
                        self.runner.move(0, 1, self.maze)
                    elif event.key == pygame.K_a:
                        self.runner.move(-1, 0, self.maze)
                    elif event.key == pygame.K_d:
                        self.runner.move(1, 0, self.maze)
                    elif event.key == pygame.K_SPACE:
                        if self.runner.sprint():
                            try:
                                if self.sounds['chase_nearby']:
                                    self.sounds['chase_nearby'].play()
                            except Exception as e:
                                print(f"Error playing sprint sound: {e}")
                    elif event.key == pygame.K_e:
                        if self.runner.place_decoy():
                            try:
                                if self.sounds['ghost_ping']:
                                    self.sounds['ghost_ping'].play()
                            except Exception as e:
                                print(f"Error playing decoy sound: {e}")
            
            elif self.state == GameState.ROUND_END or self.state == GameState.GAME_OVER:
                if event.key == pygame.K_SPACE:
                    if self.state == GameState.ROUND_END:
                        # Switch roles and start next round
                        self.current_player_is_ghost = not self.current_player_is_ghost
                        self.round_number += 1
                        self.reset_round()
                    else:  # GAME_OVER
                        # Reset game completely
                        self.round_number = 1
                        self.ghost_wins = 0
                        self.runner_wins = 0
                        self.current_player_is_ghost = True
                        self.reset_round()
            
            elif self.state == GameState.MENU:
                if event.key == pygame.K_SPACE:
                    self.state = GameState.PLAYING
        
        return True
    
    def update(self):
        """Update game state."""
        if self.state != GameState.PLAYING:
            return
        
        # Update timer
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000:  # 1 second has passed
            self.time_remaining -= 1
            self.last_time = current_time
        
        # Check if time is up
        if self.time_remaining <= 0:
            self.end_round(winner="ghost")
            return
        
        # Check for orb collection
        for orb in self.orbs[:]:
            if self.runner.x == orb.x and self.runner.y == orb.y:
                self.orbs.remove(orb)
                try:
                    if self.sounds['orb_collect']:
                        self.sounds['orb_collect'].play()
                except Exception as e:
                    print(f"Error playing sound: {e}")
                
                # Check if all orbs are collected
                if len(self.orbs) == 0:
                    self.exit_open = True
        
        # Check if runner reached exit when it's open
        if self.exit_open and self.runner.x == self.maze.width - 2 and self.runner.y == self.maze.height - 2:
            self.end_round(winner="runner")
            return
        
        # Check for ghost catching runner
        if self.ghost.x == self.runner.x and self.ghost.y == self.runner.y:
            self.end_round(winner="ghost")
            return
        
        # Update ghost and runner
        self.ghost.update()
        self.runner.update()
        
        # Play nearby sound if ghost is close to runner
        distance = math.sqrt((self.ghost.x - self.runner.x)**2 + (self.ghost.y - self.runner.y)**2)
        if distance < 3:  # If ghost is within 3 cells
            try:
                if self.sounds['chase_nearby']:
                    self.sounds['chase_nearby'].play()
            except Exception as e:
                print(f"Error playing sound: {e}")
    
    def end_round(self, winner):
        """End the current round.
        
        Args:
            winner: String indicating the winner ("ghost" or "runner")
        """
        if winner == "ghost":
            self.ghost_wins += 1
        else:
            self.runner_wins += 1
        
        try:
            if self.sounds['win']:
                self.sounds['win'].play()
        except Exception as e:
            print(f"Error playing win sound: {e}")
        
        # Check if game is over
        if self.round_number >= self.max_rounds or self.ghost_wins > self.max_rounds/2 or self.runner_wins > self.max_rounds/2:
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.ROUND_END
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(config.BLACK)
        
        if self.state == GameState.MENU:
            self.render_menu()
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            self.render_game()
            if self.state == GameState.PAUSED:
                self.render_pause_overlay()
        elif self.state == GameState.ROUND_END:
            self.render_round_end()
        elif self.state == GameState.GAME_OVER:
            self.render_game_over()
    
    def render_menu(self):
        """Render the game menu."""
        title = self.font.render("Ghost Chase", True, config.PURPLE)
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        instructions = [
            "A maze game where one player hunts in darkness,",
            "while the other collects orbs to escape.",
            "",
            "Ghost: WASD to move, SPACE for sonar",
            "Runner: WASD to move, SPACE to sprint, E for decoy",
            "",
            "Press SPACE to start"
        ]
        
        for i, line in enumerate(instructions):
            text = self.small_font.render(line, True, config.WHITE)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, 200 + i * 30))
            self.screen.blit(text, text_rect)
    
    def render_game(self):
        """Render the game play screen."""
        # Calculate cell size based on maze dimensions
        cell_size = min(
            (config.SCREEN_WIDTH - 100) // self.maze.width,
            (config.SCREEN_HEIGHT - 150) // self.maze.height
        )
        
        # Calculate offset to center the maze
        offset_x = (config.SCREEN_WIDTH - self.maze.width * cell_size) // 2
        offset_y = (config.SCREEN_HEIGHT - self.maze.height * cell_size) // 2 + 50  # Extra space for UI
        
        # Render maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size,
                    cell_size
                )
                
                # Draw walls and floor
                if self.maze.is_wall(x, y):
                    pygame.draw.rect(self.screen, config.BLUE, rect)
                    # Add glow effect
                    pygame.draw.rect(self.screen, config.CYAN, rect, 1)
                else:
                    pygame.draw.rect(self.screen, (20, 20, 30), rect)
                
                # Draw exit
                if x == self.maze.width - 2 and y == self.maze.height - 2:
                    if self.exit_open:
                        pygame.draw.rect(self.screen, config.GREEN, rect)
                    else:
                        pygame.draw.rect(self.screen, config.RED, rect)
        
        # Render orbs
        for orb in self.orbs:
            orb_rect = pygame.Rect(
                offset_x + orb.x * cell_size + cell_size // 4,
                offset_y + orb.y * cell_size + cell_size // 4,
                cell_size // 2,
                cell_size // 2
            )
            pygame.draw.ellipse(self.screen, config.YELLOW, orb_rect)
        
        # Render ghost
        ghost_rect = pygame.Rect(
            offset_x + self.ghost.x * cell_size + cell_size // 4,
            offset_y + self.ghost.y * cell_size + cell_size // 4,
            cell_size // 2,
            cell_size // 2
        )
        pygame.draw.ellipse(self.screen, config.PURPLE, ghost_rect)
        
        # Render runner
        runner_rect = pygame.Rect(
            offset_x + self.runner.x * cell_size + cell_size // 4,
            offset_y + self.runner.y * cell_size + cell_size // 4,
            cell_size // 2,
            cell_size // 2
        )
        pygame.draw.ellipse(self.screen, config.CYAN, runner_rect)
        
        # Render sonar effect if active
        if self.ghost.sonar_active:
            sonar_radius = self.ghost.sonar_radius * cell_size
            pygame.draw.circle(
                self.screen,
                (100, 50, 150, 100),  # Semi-transparent purple
                (offset_x + self.ghost.x * cell_size + cell_size // 2,
                 offset_y + self.ghost.y * cell_size + cell_size // 2),
                sonar_radius,
                2  # Line width
            )
        
        # Render decoy if placed
        if self.runner.decoy_placed:
            decoy_rect = pygame.Rect(
                offset_x + self.runner.decoy_x * cell_size + cell_size // 4,
                offset_y + self.runner.decoy_y * cell_size + cell_size // 4,
                cell_size // 2,
                cell_size // 2
            )
            pygame.draw.ellipse(self.screen, (100, 200, 255, 150), decoy_rect)
        
        # Render UI
        self.render_ui()
    
    def render_ui(self):
        """Render the game UI elements."""
        # Timer
        timer_text = self.font.render(f"Time: {self.time_remaining}", True, config.WHITE)
        self.screen.blit(timer_text, (config.SCREEN_WIDTH // 2 - 50, 20))
        
        # Orb count
        orbs_collected = 5 - len(self.orbs)
        orb_text = self.font.render(f"Orbs: {orbs_collected}/5", True, config.YELLOW)
        self.screen.blit(orb_text, (50, 20))
        
        # Ghost charge meter
        charge_text = self.font.render(f"Sonar: {self.ghost.sonar_charge}%", True, config.PURPLE)
        self.screen.blit(charge_text, (config.SCREEN_WIDTH - 150, 20))
        
        # Current role
        role_text = self.font.render(
            f"Playing as: {'Ghost' if self.current_player_is_ghost else 'Runner'}", 
            True, 
            config.PURPLE if self.current_player_is_ghost else config.CYAN
        )
        self.screen.blit(role_text, (50, config.SCREEN_HEIGHT - 40))
        
        # Score
        score_text = self.font.render(
            f"Ghost {self.ghost_wins} - {self.runner_wins} Runner", 
            True, 
            config.WHITE
        )
        self.screen.blit(score_text, (config.SCREEN_WIDTH - 250, config.SCREEN_HEIGHT - 40))
    
    def render_pause_overlay(self):
        """Render the pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font.render("PAUSED", True, config.WHITE)
        pause_rect = pause_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instructions = self.small_font.render("Press P to resume", True, config.WHITE)
        instructions_rect = instructions.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instructions, instructions_rect)
    
    def render_round_end(self):
        """Render the round end screen."""
        # Background
        self.render_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Round result
        if self.ghost_wins > self.runner_wins:
            winner_text = "Ghost wins this round!"
            color = config.PURPLE
        else:
            winner_text = "Runner wins this round!"
            color = config.CYAN
        
        result_text = self.font.render(winner_text, True, color)
        result_rect = result_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(result_text, result_rect)
        
        # Score
        score_text = self.font.render(
            f"Ghost {self.ghost_wins} - {self.runner_wins} Runner", 
            True, 
            config.WHITE
        )
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Next round info
        next_text = self.font.render(
            f"Next round: Playing as {'Runner' if self.current_player_is_ghost else 'Ghost'}", 
            True, 
            config.CYAN if self.current_player_is_ghost else config.PURPLE
        )
        next_rect = next_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(next_text, next_rect)
        
        # Continue prompt
        continue_text = self.small_font.render("Press SPACE to continue", True, config.WHITE)
        continue_rect = continue_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(continue_text, continue_rect)
    
    def render_game_over(self):
        """Render the game over screen."""
        # Background
        self.screen.fill(config.BLACK)
        
        # Game over text
        game_over_text = self.font.render("GAME OVER", True, config.RED)
        game_over_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final result
        if self.ghost_wins > self.runner_wins:
            winner_text = "Ghost wins the game!"
            color = config.PURPLE
        else:
            winner_text = "Runner wins the game!"
            color = config.CYAN
        
        result_text = self.font.render(winner_text, True, color)
        result_rect = result_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(result_text, result_rect)
        
        # Final score
        score_text = self.font.render(
            f"Final Score: Ghost {self.ghost_wins} - {self.runner_wins} Runner", 
            True, 
            config.WHITE
        )
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Restart prompt
        restart_text = self.small_font.render("Press SPACE to play again", True, config.WHITE)
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        # Exit prompt
        exit_text = self.small_font.render("Press ESC to return to menu", True, config.WHITE)
        exit_rect = exit_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(exit_text, exit_rect)
