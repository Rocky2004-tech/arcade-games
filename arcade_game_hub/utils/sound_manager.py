"""
Sound Manager for the Arcade Game Hub.
Handles playing, pausing, and managing sound effects and music.
"""
import pygame
import os
import config

class SoundManager:
    """Manages sound effects and music for the games."""
    
    def __init__(self):
        """Initialize the sound manager."""
        self.sounds = {}
        self.music_playing = False
        
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Set initial volumes
        pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
    
    def load_sound(self, sound_id, file_path):
        """Load a sound effect.
        
        Args:
            sound_id: Identifier for the sound
            file_path: Path to the sound file
        """
        if os.path.exists(file_path):
            try:
                self.sounds[sound_id] = pygame.mixer.Sound(file_path)
                self.sounds[sound_id].set_volume(config.SFX_VOLUME)
                return True
            except:
                print(f"Error loading sound: {file_path}")
        else:
            print(f"Sound file not found: {file_path}")
        return False
    
    def play_sound(self, sound_id):
        """Play a sound effect.
        
        Args:
            sound_id: Identifier for the sound to play
        """
        if not config.SOUND_ENABLED:
            return
            
        try:
            if sound_id in self.sounds:
                self.sounds[sound_id].play()
        except Exception as e:
            print(f"Error playing sound {sound_id}: {e}")
    
    def play_music(self, music_id, loops=-1):
        """Play background music.
        
        Args:
            music_id: Identifier for the music to play
            loops: Number of times to loop (-1 for infinite)
        """
        if not config.SOUND_ENABLED:
            return
            
        try:
            if music_id in self.sounds:
                music_path = self.sounds[music_id].get_filename()
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play(loops)
                    self.music_playing = True
        except Exception as e:
            print(f"Error playing music {music_id}: {e}")
    
    def stop_music(self):
        """Stop the currently playing music."""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def pause_music(self):
        """Pause the currently playing music."""
        if self.music_playing:
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the music."""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """Set the music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    
    def set_sound_volume(self, volume):
        """Set the sound effect volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(volume)
