"""
UI class for Bullet Bounce game.
"""
import pygame
import os

import config
from utils.game_utils import draw_text, load_image

class GameUI:
    """In-game user interface elements."""
    
    def __init__(self):
        """Initialize the UI."""
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 24)
        
        # Player 1 UI positions
        self.p1_avatar_pos = (20, 20)
        self.p1_score_pos = (80, 30)
        
        # Player 2 UI positions
        self.p2_avatar_pos = (config.SCREEN_WIDTH - 80, 20)
        self.p2_score_pos = (config.SCREEN_WIDTH - 100, 30)
        
        # Match timer position
        self.timer_pos = (config.SCREEN_WIDTH // 2, 30)
        
        # Round info position
        self.round_info_pos = (config.SCREEN_WIDTH // 2, 60)
        
        # Win banner position
        self.win_banner_pos = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        
        # Load avatar images
        self.p1_avatar = None
        self.p2_avatar = None
        p1_avatar_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "sprites", "avatar_blue.png")
        p2_avatar_path = os.path.join(config.ASSETS_DIR, "bullet_bounce", "sprites", "avatar_red.png")
        
        if os.path.exists(p1_avatar_path):
            self.p1_avatar = load_image(p1_avatar_path, (50, 50), True)
        if os.path.exists(p2_avatar_path):
            self.p2_avatar = load_image(p2_avatar_path, (50, 50), True)
            
        # Animation variables
        self.score_animation = {"p1": 0, "p2": 0}
        self.score_animation_target = {"p1": 0, "p2": 0}
        self.win_banner_alpha = 0
        self.win_banner_direction = 1
    
    def update(self, p1_score, p2_score):
        """Update UI animations.
        
        Args:
            p1_score: Player 1's current score
            p2_score: Player 2's current score
        """
        # Update score animation
        self.score_animation_target["p1"] = p1_score
        self.score_animation_target["p2"] = p2_score
        
        # Animate scores
        if self.score_animation["p1"] < self.score_animation_target["p1"]:
            self.score_animation["p1"] += 0.5  # Faster animation
            # Ensure we reach the exact target value
            if self.score_animation["p1"] > self.score_animation_target["p1"]:
                self.score_animation["p1"] = self.score_animation_target["p1"]
                
        if self.score_animation["p2"] < self.score_animation_target["p2"]:
            self.score_animation["p2"] += 0.5  # Faster animation
            # Ensure we reach the exact target value
            if self.score_animation["p2"] > self.score_animation_target["p2"]:
                self.score_animation["p2"] = self.score_animation_target["p2"]
            
        # Animate win banner
        self.win_banner_alpha += self.win_banner_direction * 5
        if self.win_banner_alpha >= 255:
            self.win_banner_alpha = 255
            self.win_banner_direction = -1
        elif self.win_banner_alpha <= 100:
            self.win_banner_alpha = 100
            self.win_banner_direction = 1
    
    def draw(self, surface, p1_score, p2_score, match_time, current_round=1, total_rounds=3, game_state="playing"):
        """Draw UI elements on the given surface.
        
        Args:
            surface: Pygame surface to draw on
            p1_score: Player 1's current score
            p2_score: Player 2's current score
            match_time: Current match time in seconds
            current_round: Current round number
            total_rounds: Total number of rounds
            game_state: Current game state ("playing", "round_over", "match_over")
        """
        # Update animations
        self.update(p1_score, p2_score)
        
        # Draw player 1 avatar and score
        if self.p1_avatar:
            surface.blit(self.p1_avatar, self.p1_avatar_pos)
        else:
            # Draw a blue circle if no avatar is available
            pygame.draw.circle(surface, config.BLUE, 
                             (self.p1_avatar_pos[0] + 25, self.p1_avatar_pos[1] + 25), 25)
        
        # Draw player 1 score with glow effect
        # Use the actual score value, not the animated one
        score_text = f"{int(p1_score)}"
        score_surf = self.font.render(score_text, True, config.WHITE)
        
        # Create glow effect
        glow_surf = pygame.Surface((score_surf.get_width() + 10, score_surf.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (0, 100, 255, 100), glow_surf.get_rect(), border_radius=5)
        
        # Draw score with glow
        surface.blit(glow_surf, (self.p1_score_pos[0] - 5, self.p1_score_pos[1] - 5))
        surface.blit(score_surf, self.p1_score_pos)
        
        # Draw player 2 avatar and score
        if self.p2_avatar:
            surface.blit(self.p2_avatar, self.p2_avatar_pos)
        else:
            # Draw a red circle if no avatar is available
            pygame.draw.circle(surface, config.RED, 
                             (self.p2_avatar_pos[0] + 25, self.p2_avatar_pos[1] + 25), 25)
        
        # Draw player 2 score with glow effect
        # Use the actual score value, not the animated one
        score_text = f"{int(p2_score)}"
        score_surf = self.font.render(score_text, True, config.WHITE)
        
        # Create glow effect
        glow_surf = pygame.Surface((score_surf.get_width() + 10, score_surf.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (255, 50, 50, 100), glow_surf.get_rect(), border_radius=5)
        
        # Draw score with glow - align to the right of the avatar
        score_pos = (self.p2_score_pos[0] - score_surf.get_width(), self.p2_score_pos[1])
        surface.blit(glow_surf, (score_pos[0] - 5, score_pos[1] - 5))
        surface.blit(score_surf, score_pos)
        
        # Draw match timer
        minutes = int(match_time // 60)
        seconds = int(match_time % 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"
        
        # Create timer surface with glow
        timer_surf = self.font.render(timer_text, True, config.WHITE)
        timer_glow = pygame.Surface((timer_surf.get_width() + 10, timer_surf.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(timer_glow, (100, 100, 255, 100), timer_glow.get_rect(), border_radius=5)
        
        # Draw timer with glow
        timer_rect = timer_surf.get_rect(center=self.timer_pos)
        surface.blit(timer_glow, (timer_rect.x - 5, timer_rect.y - 5))
        surface.blit(timer_surf, timer_rect)
        
        # Draw round info
        round_text = f"Round {current_round}/{total_rounds}"
        draw_text(surface, round_text, self.small_font, config.WHITE, 
                 self.round_info_pos[0], self.round_info_pos[1])
        
        # Draw "First to 5" banner at the start of the round
        if game_state == "starting":
            banner_text = "First to 5 Points Wins!"
            banner_surf = self.big_font.render(banner_text, True, config.WHITE)
            banner_rect = banner_surf.get_rect(center=self.win_banner_pos)
            
            # Create glow effect
            banner_glow = pygame.Surface((banner_surf.get_width() + 20, banner_surf.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(banner_glow, (100, 100, 255, self.win_banner_alpha), 
                           banner_glow.get_rect(), border_radius=10)
            
            # Draw banner with glow
            surface.blit(banner_glow, (banner_rect.x - 10, banner_rect.y - 10))
            surface.blit(banner_surf, banner_rect)
        
        # Draw round over banner
        if game_state == "round_over":
            # Determine winner
            winner_text = "Player 1 Wins the Round!" if p1_score >= 5 else "Player 2 Wins the Round!"
            if p1_score < 5 and p2_score < 5:
                winner_text = "Time's Up!"
                
            banner_surf = self.big_font.render(winner_text, True, config.WHITE)
            banner_rect = banner_surf.get_rect(center=self.win_banner_pos)
            
            # Create glow effect
            glow_color = (0, 100, 255, self.win_banner_alpha) if p1_score >= 5 else (255, 50, 50, self.win_banner_alpha)
            if p1_score < 5 and p2_score < 5:
                glow_color = (255, 255, 0, self.win_banner_alpha)
                
            banner_glow = pygame.Surface((banner_surf.get_width() + 20, banner_surf.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(banner_glow, glow_color, banner_glow.get_rect(), border_radius=10)
            
            # Draw banner with glow
            surface.blit(banner_glow, (banner_rect.x - 10, banner_rect.y - 10))
            surface.blit(banner_surf, banner_rect)
            
            # Draw "Press SPACE to continue" text
            continue_text = "Press SPACE to continue"
            draw_text(surface, continue_text, self.font, config.WHITE, 
                     self.win_banner_pos[0], self.win_banner_pos[1] + 50)
        
        # Draw match over banner
        if game_state == "match_over":
            # Determine match winner
            winner_text = "Player 1 Wins the Match!" if p1_score > p2_score else "Player 2 Wins the Match!"
            if p1_score == p2_score:
                winner_text = "Match Draw!"
                
            banner_surf = self.big_font.render(winner_text, True, config.WHITE)
            banner_rect = banner_surf.get_rect(center=self.win_banner_pos)
            
            # Create glow effect
            glow_color = (0, 100, 255, self.win_banner_alpha) if p1_score > p2_score else (255, 50, 50, self.win_banner_alpha)
            if p1_score == p2_score:
                glow_color = (255, 255, 0, self.win_banner_alpha)
                
            banner_glow = pygame.Surface((banner_surf.get_width() + 20, banner_surf.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(banner_glow, glow_color, banner_glow.get_rect(), border_radius=10)
            
            # Draw banner with glow
            surface.blit(banner_glow, (banner_rect.x - 10, banner_rect.y - 10))
            surface.blit(banner_surf, banner_rect)
            
            # Draw "Press ESC to return to launcher" text
            exit_text = "Press ESC to return to launcher"
            draw_text(surface, exit_text, self.font, config.WHITE, 
                     self.win_banner_pos[0], self.win_banner_pos[1] + 50)
    
    def draw_pause_menu(self, surface):
        """Draw the pause menu.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        # Draw pause text
        draw_text(surface, "PAUSED", self.big_font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50)
        
        # Draw controls
        draw_text(surface, "P: Resume Game", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20)
        draw_text(surface, "ESC: Return to Launcher", self.font, config.WHITE, 
                 config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 60)
