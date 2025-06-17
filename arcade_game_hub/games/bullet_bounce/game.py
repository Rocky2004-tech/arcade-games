"""
Bullet Bounce game module.
A fast-paced arena shooter where bullets bounce off walls.
"""
import pygame
import sys
import os
import math
import random

import config
from utils.sound_manager import SoundManager
from utils.game_utils import draw_text
from games.bullet_bounce.player import Player
from games.bullet_bounce.bullet import Bullet
from games.bullet_bounce.arena import Arena, PowerUp
from games.bullet_bounce.ui import GameUI

class Game:
    """Main game class for Bullet Bounce."""
    
    # Game states
    STATE_STARTING = "starting"
    STATE_PLAYING = "playing"
    STATE_ROUND_OVER = "round_over"
    STATE_MATCH_OVER = "match_over"
    STATE_PAUSED = "paused"
    
    def __init__(self, screen):
        """Initialize the game.
        
        Args:
            screen: Pygame surface for rendering
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.sound_manager = SoundManager()
        
        # Load game assets
        self._load_assets()
        
        # Create game objects
        self.arena = Arena()
        
        # Create players - player1 facing right (towards player2), player2 facing left (towards player1)
        self.player1 = Player(config.SCREEN_WIDTH // 4, config.SCREEN_HEIGHT // 2, 1)
        self.player1.angle = 0  # 0 radians = facing right
        self.player2 = Player(config.SCREEN_WIDTH * 3 // 4, config.SCREEN_HEIGHT // 2, 2)
        self.player2.angle = math.pi  # π radians = facing left
        
        self.bullets = []
        self.ui = GameUI()
        
        # Game state
        self.state = Game.STATE_STARTING
        self.state_timer = 180  # 3 seconds at 60 FPS
        
        # Match settings
        self.round_time = 60  # 60 seconds per round
        self.round_timer = self.round_time * 60  # Convert to frames
        self.current_round = 1
        self.total_rounds = 3
        self.round_wins = [0, 0]  # Player 1 and 2 round wins
        
        # Start background music
        try:
            if "background" in self.sound_manager.sounds:
                self.sound_manager.play_music("background", -1)
        except Exception as e:
            print(f"Error playing background music: {e}")
    
    def _load_assets(self):
        """Load game assets like sounds and images."""
        # Load sound effects
        sounds_dir = os.path.join(config.ASSETS_DIR, "bullet_bounce", "sounds")
        
        # Check if sounds directory exists
        if not os.path.exists(sounds_dir):
            print(f"Creating sounds directory: {sounds_dir}")
            os.makedirs(sounds_dir, exist_ok=True)
        
        # Define sound files to load
        sound_files = {
            "shoot": "shoot.wav",
            "bounce": "bounce.wav",
            "hit": "hit.wav",
            "powerup": "powerup.wav",
            "victory": "victory.wav",
            "round_start": "round_start.wav",
            "background": "background.mp3"
        }
        
        # Load each sound if it exists
        missing_sounds = []
        for sound_name, file_name in sound_files.items():
            sound_path = os.path.join(sounds_dir, file_name)
            
            # Try both with and without arcade_game_hub prefix
            alt_path = os.path.join("arcade_game_hub", sounds_dir, file_name)
            
            if os.path.exists(sound_path) and os.path.getsize(sound_path) > 100:
                self.sound_manager.load_sound(sound_name, sound_path)
            elif os.path.exists(alt_path) and os.path.getsize(alt_path) > 100:
                self.sound_manager.load_sound(sound_name, alt_path)
            else:
                missing_sounds.append(file_name)
        
        # Print warning if sounds are missing
        if missing_sounds:
            print(f"Warning: Missing sound files: {', '.join(missing_sounds)}")
            print("Run the fix_sounds.py script to create placeholder sound files.")
    
    def handle_event(self, event):
        """Process pygame events.
        
        Args:
            event: Pygame event to process
            
        Returns:
            False if the game should exit, None otherwise
        """
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            if event.key == pygame.K_p:
                if self.state == Game.STATE_PLAYING:
                    self.state = Game.STATE_PAUSED
                elif self.state == Game.STATE_PAUSED:
                    self.state = Game.STATE_PLAYING
            
            # Handle space key for shooting and continuing after round over
            if event.key == pygame.K_SPACE:
                if self.state == Game.STATE_PLAYING:
                    self._shoot_bullet(self.player1)
                elif self.state == Game.STATE_ROUND_OVER:
                    self._start_next_round()
            
            # Handle Enter key for player 2 shooting
            if event.key == pygame.K_RETURN:
                if self.state == Game.STATE_PLAYING:
                    self._shoot_bullet(self.player2)
        
        # Handle player input
        if self.state == Game.STATE_PLAYING:
            self.player1.handle_event(event)
            self.player2.handle_event(event)
    
    def _shoot_bullet(self, player):
        """Create a new bullet from the player's position.
        
        Args:
            player: Player object that is shooting
        """
        # Create bullet at player's position with player's angle
        if player.double_shot:
            # Create two bullets at slight angles
            angle_offset = 0.2
            new_bullet1 = Bullet(player.x, player.y, player.angle - angle_offset, 10, player.player_id)
            new_bullet2 = Bullet(player.x, player.y, player.angle + angle_offset, 10, player.player_id)
            self.bullets.append(new_bullet1)
            self.bullets.append(new_bullet2)
            player.double_shot = False
        else:
            new_bullet = Bullet(player.x, player.y, player.angle, 10, player.player_id)
            self.bullets.append(new_bullet)
        
        try:
            self.sound_manager.play_sound("shoot")
        except Exception as e:
            print(f"Error playing shoot sound: {e}")
    
    def _start_next_round(self):
        """Start the next round or end the match."""
        # Check if match is over
        if self.current_round >= self.total_rounds:
            self.state = Game.STATE_MATCH_OVER
            try:
                self.sound_manager.play_sound("victory")
            except Exception as e:
                print(f"Error playing victory sound: {e}")
            return
            
        # Increment round counter
        self.current_round += 1
        
        # Reset round state
        self.player1.x = config.SCREEN_WIDTH // 4
        self.player1.y = config.SCREEN_HEIGHT // 2
        self.player1.angle = 0  # 0 radians = facing right (towards player2)
        self.player1.health = 100
        self.player1.score = 0
        
        self.player2.x = config.SCREEN_WIDTH * 3 // 4
        self.player2.y = config.SCREEN_HEIGHT // 2
        self.player2.angle = math.pi  # π radians = facing left (towards player1)
        self.player2.health = 100
        self.player2.score = 0
        
        self.bullets = []
        self.arena.power_ups = []
        self.round_timer = self.round_time * 60
        
        # Set state to starting
        self.state = Game.STATE_STARTING
        self.state_timer = 180
        
        # Play round start sound
        try:
            self.sound_manager.play_sound("round_start")
        except Exception as e:
            print(f"Error playing round start sound: {e}")
    
    def _check_round_over(self):
        """Check if the current round is over."""
        # Check if any player reached 5 points
        if self.player1.has_won():
            self.round_wins[0] += 1
            self.state = Game.STATE_ROUND_OVER
            try:
                self.sound_manager.play_sound("victory")
            except Exception as e:
                print(f"Error playing victory sound: {e}")
            print(f"Round over! Player 1 wins with {self.player1.score} points! Round wins: {self.round_wins}")
            return
            
        if self.player2.has_won():
            self.round_wins[1] += 1
            self.state = Game.STATE_ROUND_OVER
            try:
                self.sound_manager.play_sound("victory")
            except Exception as e:
                print(f"Error playing victory sound: {e}")
            print(f"Round over! Player 2 wins with {self.player2.score} points! Round wins: {self.round_wins}")
            return
            
        # Check if time is up
        if self.round_timer <= 0:
            # Determine winner based on score
            if self.player1.score > self.player2.score:
                self.round_wins[0] += 1
                print(f"Time up! Player 1 wins! Round wins: {self.round_wins}")
            elif self.player2.score > self.player1.score:
                self.round_wins[1] += 1
                print(f"Time up! Player 2 wins! Round wins: {self.round_wins}")
            # If tied, both get a point
            else:
                self.round_wins[0] += 0.5
                self.round_wins[1] += 0.5
                print(f"Time up! It's a tie! Round wins: {self.round_wins}")
                
            self.state = Game.STATE_ROUND_OVER
            try:
                self.sound_manager.play_sound("victory")
            except Exception as e:
                print(f"Error playing victory sound: {e}")
    
    def _apply_power_up(self, player, power_up):
        """Apply power-up effect to player.
        
        Args:
            player: Player object to apply power-up to
            power_up: PowerUp object to apply
        """
        if power_up.type == PowerUp.SHIELD:
            player.activate_shield()
        elif power_up.type == PowerUp.SPEED:
            player.activate_speed_boost()
        elif power_up.type == PowerUp.DOUBLE_SHOT:
            player.activate_double_shot()
            
        try:
            self.sound_manager.play_sound("powerup")
        except Exception as e:
            print(f"Error playing powerup sound: {e}")
    
    def update(self):
        """Update game state."""
        # Handle different game states
        if self.state == Game.STATE_STARTING:
            # Count down the starting timer
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = Game.STATE_PLAYING
                
        elif self.state == Game.STATE_PLAYING:
            # Update round timer
            self.round_timer -= 1
            
            # Force check if any player has reached 5 points
            if self.player1.has_won() or self.player2.has_won():
                self._check_round_over()
                return
            
            if self.round_timer <= 0:
                self._check_round_over()
                
            # Update arena
            self.arena.update()
            
            # Update players
            self.player1.update()
            self.player2.update()
            
            # Check for power-up collisions
            power_up1 = self.arena.check_power_up_collision(self.player1)
            if power_up1:
                self._apply_power_up(self.player1, power_up1)
                
            power_up2 = self.arena.check_power_up_collision(self.player2)
            if power_up2:
                self._apply_power_up(self.player2, power_up2)
            
            # Update bullets
            for bullet in self.bullets[:]:
                bullet.update()
                
                # Check for collisions with arena walls
                collision, wall = self.arena.check_collision(bullet)
                if collision:
                    bullet.bounce(wall)
                    try:
                        self.sound_manager.play_sound("bounce")
                    except Exception as e:
                        print(f"Error playing bounce sound: {e}")
                
                # Check for collisions with players
                # Only check if bullet owner is not the player
                if bullet.owner_id != 1:
                    # Calculate distance between bullet and player 1
                    distance = ((bullet.x - self.player1.x) ** 2 + (bullet.y - self.player1.y) ** 2) ** 0.5
                    
                    # Check if distance is less than sum of radii
                    if distance < bullet.radius + self.player1.radius:
                        # Player 1 hit by player 2's bullet
                        if self.player1.take_damage(20):
                            # Player took damage but is still alive
                            new_score = self.player2.increment_score()
                            self.bullets.remove(bullet)
                            try:
                                self.sound_manager.play_sound("hit")
                            except Exception as e:
                                print(f"Error playing hit sound: {e}")
                            print(f"Player 2 scored! Score: {new_score}")
                            
                            # Immediately end the round if player has won
                            if new_score >= 5:
                                self.round_wins[1] += 1
                                self.state = Game.STATE_ROUND_OVER
                                try:
                                    self.sound_manager.play_sound("victory")
                                except Exception as e:
                                    print(f"Error playing victory sound: {e}")
                                print(f"Round over! Player 2 wins with {new_score} points! Round wins: {self.round_wins}")
                        continue
                
                if bullet.owner_id != 2:
                    # Calculate distance between bullet and player 2
                    distance = ((bullet.x - self.player2.x) ** 2 + (bullet.y - self.player2.y) ** 2) ** 0.5
                    
                    # Check if distance is less than sum of radii
                    if distance < bullet.radius + self.player2.radius:
                        # Player 2 hit by player 1's bullet
                        if self.player2.take_damage(20):
                            # Player took damage but is still alive
                            new_score = self.player1.increment_score()
                            self.bullets.remove(bullet)
                            try:
                                self.sound_manager.play_sound("hit")
                            except Exception as e:
                                print(f"Error playing hit sound: {e}")
                            print(f"Player 1 scored! Score: {new_score}")
                            
                            # Immediately end the round if player has won
                            if new_score >= 5:
                                self.round_wins[0] += 1
                                self.state = Game.STATE_ROUND_OVER
                                try:
                                    self.sound_manager.play_sound("victory")
                                except Exception as e:
                                    print(f"Error playing victory sound: {e}")
                                print(f"Round over! Player 1 wins with {new_score} points! Round wins: {self.round_wins}")
                        continue
                
                # Remove bullets that are out of bounds or expired
                if bullet.should_remove():
                    self.bullets.remove(bullet)
                    
            # Check if round is over
            self._check_round_over()
            
        elif self.state == Game.STATE_PAUSED:
            # Do nothing while paused
            pass
    
    def render(self):
        """Render the game."""
        # Clear the screen
        self.screen.fill(config.BLACK)
        
        # Draw the arena
        self.arena.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Draw players
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        
        # Draw UI based on game state
        if self.state == Game.STATE_STARTING:
            self.ui.draw(self.screen, self.player1.score, self.player2.score, 
                        self.round_timer / 60, self.current_round, self.total_rounds, "starting")
        elif self.state == Game.STATE_PLAYING:
            self.ui.draw(self.screen, self.player1.score, self.player2.score, 
                        self.round_timer / 60, self.current_round, self.total_rounds, "playing")
        elif self.state == Game.STATE_ROUND_OVER:
            self.ui.draw(self.screen, self.player1.score, self.player2.score, 
                        0, self.current_round, self.total_rounds, "round_over")
        elif self.state == Game.STATE_MATCH_OVER:
            self.ui.draw(self.screen, self.round_wins[0], self.round_wins[1], 
                        0, self.current_round, self.total_rounds, "match_over")
        
        # Draw pause menu if paused
        if self.state == Game.STATE_PAUSED:
            self.ui.draw_pause_menu(self.screen)
