#!/usr/bin/env python3
"""
Sound file generator for Arcade Game Hub.
This script creates placeholder sound files for games if they're missing.
"""
import os
import wave
import struct
import array
import math
import random

def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def create_sine_wave(filename, frequency=440, duration=1.0, volume=0.5):
    """Create a simple sine wave sound file.
    
    Args:
        filename: Output filename
        frequency: Tone frequency in Hz
        duration: Sound duration in seconds
        volume: Sound volume (0.0 to 1.0)
    """
    # Sound parameters
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    # Generate sine wave
    samples = array.array('h')
    amplitude = int(32767 * volume)
    
    for i in range(num_samples):
        sample = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(int(sample))
    
    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        wav_file.writeframes(samples.tobytes())
    
    print(f"Created sound file: {filename}")

def create_noise(filename, duration=1.0, volume=0.5):
    """Create a white noise sound file.
    
    Args:
        filename: Output filename
        duration: Sound duration in seconds
        volume: Sound volume (0.0 to 1.0)
    """
    # Sound parameters
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    # Generate white noise
    samples = array.array('h')
    amplitude = int(32767 * volume)
    
    for i in range(num_samples):
        sample = amplitude * (random.random() * 2 - 1)
        samples.append(int(sample))
    
    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        wav_file.writeframes(samples.tobytes())
    
    print(f"Created sound file: {filename}")

def create_beep(filename, duration=0.3, volume=0.5):
    """Create a simple beep sound.
    
    Args:
        filename: Output filename
        duration: Sound duration in seconds
        volume: Sound volume (0.0 to 1.0)
    """
    create_sine_wave(filename, frequency=880, duration=duration, volume=volume)

def create_victory_sound(filename, duration=2.0, volume=0.5):
    """Create a victory sound (ascending tones).
    
    Args:
        filename: Output filename
        duration: Sound duration in seconds
        volume: Sound volume (0.0 to 1.0)
    """
    # Sound parameters
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    # Generate ascending tones
    samples = array.array('h')
    amplitude = int(32767 * volume)
    
    for i in range(num_samples):
        # Frequency increases over time
        freq = 220 + (880 - 220) * (i / num_samples)
        sample = amplitude * math.sin(2 * math.pi * freq * i / sample_rate)
        samples.append(int(sample))
    
    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        wav_file.writeframes(samples.tobytes())
    
    print(f"Created sound file: {filename}")

def create_ambient_loop(filename, duration=5.0, volume=0.3):
    """Create an ambient loop sound.
    
    Args:
        filename: Output filename
        duration: Sound duration in seconds
        volume: Sound volume (0.0 to 1.0)
    """
    # Sound parameters
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    # Generate ambient sound (mix of low frequencies)
    samples = array.array('h')
    amplitude = int(32767 * volume)
    
    for i in range(num_samples):
        # Mix of low frequencies with slow modulation
        sample = (
            math.sin(2 * math.pi * 55 * i / sample_rate) * 0.5 +
            math.sin(2 * math.pi * 110 * i / sample_rate) * 0.3 +
            math.sin(2 * math.pi * 165 * i / sample_rate) * 0.2
        )
        # Add slow amplitude modulation
        mod = 0.7 + 0.3 * math.sin(2 * math.pi * 0.1 * i / sample_rate)
        samples.append(int(amplitude * sample * mod))
    
    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        wav_file.writeframes(samples.tobytes())
    
    print(f"Created sound file: {filename}")

def fix_bullet_bounce_sounds():
    """Create placeholder sounds for Bullet Bounce game."""
    sounds_dir = os.path.join('arcade_game_hub', 'assets', 'bullet_bounce', 'sounds')
    ensure_dir(sounds_dir)
    
    # Define sounds to create
    sounds = {
        'shoot.wav': lambda: create_beep(os.path.join(sounds_dir, 'shoot.wav'), duration=0.2),
        'bounce.wav': lambda: create_beep(os.path.join(sounds_dir, 'bounce.wav'), frequency=660, duration=0.1),
        'hit.wav': lambda: create_noise(os.path.join(sounds_dir, 'hit.wav'), duration=0.3),
        'powerup.wav': lambda: create_sine_wave(os.path.join(sounds_dir, 'powerup.wav'), frequency=1200, duration=0.5),
        'victory.wav': lambda: create_victory_sound(os.path.join(sounds_dir, 'victory.wav')),
        'round_start.wav': lambda: create_beep(os.path.join(sounds_dir, 'round_start.wav'), frequency=440, duration=0.5),
        'background.mp3': lambda: create_ambient_loop(os.path.join(sounds_dir, 'background.mp3'), duration=10.0)
    }
    
    # Create each sound if it doesn't exist or is too small
    for filename, create_func in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        if not os.path.exists(filepath) or os.path.getsize(filepath) < 100:
            create_func()

def fix_stack_dash_sounds():
    """Create placeholder sounds for Stack Dash game."""
    sounds_dir = os.path.join('arcade_game_hub', 'assets', 'stack_dash', 'sounds')
    ensure_dir(sounds_dir)
    
    # Define sounds to create
    sounds = {
        'jump.wav': lambda: create_beep(os.path.join(sounds_dir, 'jump.wav'), frequency=880, duration=0.2),
        'pickup.wav': lambda: create_beep(os.path.join(sounds_dir, 'pickup.wav'), frequency=1320, duration=0.1),
        'drop.wav': lambda: create_beep(os.path.join(sounds_dir, 'drop.wav'), frequency=220, duration=0.2),
        'fall.wav': lambda: create_noise(os.path.join(sounds_dir, 'fall.wav'), duration=0.5),
        'powerup.wav': lambda: create_sine_wave(os.path.join(sounds_dir, 'powerup.wav'), frequency=1200, duration=0.5),
        'success.wav': lambda: create_victory_sound(os.path.join(sounds_dir, 'success.wav'))
    }
    
    # Create each sound if it doesn't exist or is too small
    for filename, create_func in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        if not os.path.exists(filepath) or os.path.getsize(filepath) < 100:
            create_func()
    
    # Create music directory and main theme
    music_dir = os.path.join('arcade_game_hub', 'assets', 'stack_dash', 'music')
    ensure_dir(music_dir)
    
    main_theme = os.path.join(music_dir, 'main_theme.mp3')
    if not os.path.exists(main_theme) or os.path.getsize(main_theme) < 100:
        create_ambient_loop(main_theme, duration=15.0)

def fix_ghost_chase_sounds():
    """Create placeholder sounds for Ghost Chase game."""
    sounds_dir = os.path.join('arcade_game_hub', 'assets', 'ghost_chase', 'sounds')
    ensure_dir(sounds_dir)
    
    # Define sounds to create
    sounds = {
        'orb_collect.wav': lambda: create_beep(os.path.join(sounds_dir, 'orb_collect.wav'), frequency=1200, duration=0.2),
        'ghost_ping.wav': lambda: create_sine_wave(os.path.join(sounds_dir, 'ghost_ping.wav'), frequency=440, duration=0.5),
        'chase_nearby.wav': lambda: create_beep(os.path.join(sounds_dir, 'chase_nearby.wav'), frequency=220, duration=0.3),
        'win_theme.wav': lambda: create_victory_sound(os.path.join(sounds_dir, 'win_theme.wav')),
        'ambient_loop.mp3': lambda: create_ambient_loop(os.path.join(sounds_dir, 'ambient_loop.mp3'), duration=10.0),
        'orb_fixed.wav': lambda: create_beep(os.path.join(sounds_dir, 'orb_fixed.wav'), frequency=880, duration=0.2)
    }
    
    # Create each sound if it doesn't exist or is too small
    for filename, create_func in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        if not os.path.exists(filepath) or os.path.getsize(filepath) < 100:
            create_func()

def main():
    """Main function to fix all sound files."""
    print("Fixing sound files for Arcade Game Hub...")
    
    # Fix sounds for each game
    fix_bullet_bounce_sounds()
    fix_stack_dash_sounds()
    fix_ghost_chase_sounds()
    
    print("Sound file generation complete!")

if __name__ == "__main__":
    main()
