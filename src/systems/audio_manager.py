"""
Kingdom of Aldoria - Audio Manager
Handles sound effects, music, and audio channel management
"""

import pygame
import logging
from typing import Dict, Optional, List
from ..core.config import Config

class AudioManager:
    """Manages game audio including SFX and music"""
    
    def __init__(self):
        """Initialize the audio manager"""
        self.logger = logging.getLogger(__name__)
        
        # Audio settings
        self.master_volume = Config.MASTER_VOLUME
        self.music_volume = Config.MUSIC_VOLUME
        self.sfx_volume = Config.SFX_VOLUME
        
        # Channel management
        self.max_channels = Config.MAX_SOUNDS_CONCURRENT
        pygame.mixer.set_num_channels(self.max_channels)
        
        # Currently playing sounds
        self.playing_sounds: Dict[str, pygame.mixer.Channel] = {}
        self.sound_instances: Dict[str, List[pygame.mixer.Channel]] = {}
        
        # Music state
        self.current_music = None
        self.music_paused = False
        
        self.logger.info("AudioManager initialized")
    
    def play_sound(self, sound: pygame.mixer.Sound, name: str = "", volume: float = 1.0, loops: int = 0) -> bool:
        """Play a sound effect
        
        Args:
            sound: Pygame Sound object
            name: Identifier for the sound
            volume: Volume multiplier (0.0 to 1.0)
            loops: Number of additional loops
            
        Returns:
            True if sound started playing
        """
        if not sound:
            return False
        
        try:
            # Find available channel
            channel = pygame.mixer.find_channel()
            if not channel:
                # Stop oldest sound to make room
                self._stop_oldest_sound()
                channel = pygame.mixer.find_channel()
            
            if channel:
                # Set volume
                sound.set_volume(volume * self.sfx_volume * self.master_volume)
                
                # Play sound
                channel.play(sound, loops)
                
                # Track playing sound
                if name:
                    self.playing_sounds[name] = channel
                    if name not in self.sound_instances:
                        self.sound_instances[name] = []
                    self.sound_instances[name].append(channel)
                
                self.logger.debug(f"Playing sound: {name}")
                return True
            
        except Exception as e:
            self.logger.error(f"Failed to play sound {name}: {e}")
        
        return False
    
    def stop_sound(self, name: str):
        """Stop a specific sound by name
        
        Args:
            name: Sound identifier
        """
        if name in self.playing_sounds:
            channel = self.playing_sounds[name]
            if channel and channel.get_busy():
                channel.stop()
            del self.playing_sounds[name]
            
            # Clean up sound instances
            if name in self.sound_instances:
                self.sound_instances[name] = [
                    ch for ch in self.sound_instances[name] 
                    if ch.get_busy()
                ]
                if not self.sound_instances[name]:
                    del self.sound_instances[name]
    
    def stop_all_sounds(self):
        """Stop all playing sound effects"""
        pygame.mixer.stop()
        self.playing_sounds.clear()
        self.sound_instances.clear()
        self.logger.debug("All sounds stopped")
    
    def play_music(self, music_path: str, loops: int = -1, volume: float = None):
        """Play background music
        
        Args:
            music_path: Path to music file
            loops: Number of loops (-1 for infinite)
            volume: Music volume (None to use current setting)
        """
        try:
            if volume is not None:
                self.set_music_volume(volume)
            
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops)
            
            self.current_music = music_path
            self.music_paused = False
            
            self.logger.debug(f"Playing music: {music_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to play music {music_path}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.current_music = None
        self.music_paused = False
        self.logger.debug("Music stopped")
    
    def pause_music(self):
        """Pause background music"""
        if self.current_music and not self.music_paused:
            pygame.mixer.music.pause()
            self.music_paused = True
            self.logger.debug("Music paused")
    
    def resume_music(self):
        """Resume background music"""
        if self.current_music and self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False
            self.logger.debug("Music resumed")
    
    def set_master_volume(self, volume: float):
        """Set master volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
        self.logger.debug(f"Master volume set to: {self.master_volume}")
    
    def set_music_volume(self, volume: float):
        """Set music volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        self.logger.debug(f"Music volume set to: {self.music_volume}")
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        self.logger.debug(f"SFX volume set to: {self.sfx_volume}")
    
    def _update_all_volumes(self):
        """Update volumes for all currently playing sounds"""
        # Update music volume
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        
        # Note: Individual sound volumes are set when they're played
        # Running sounds can't have their volume changed in pygame
    
    def _stop_oldest_sound(self):
        """Stop the oldest playing sound to free up a channel"""
        if self.playing_sounds:
            # Find oldest sound (first in dictionary)
            oldest_name = next(iter(self.playing_sounds))
            self.stop_sound(oldest_name)
    
    def is_music_playing(self) -> bool:
        """Check if music is currently playing
        
        Returns:
            True if music is playing
        """
        return pygame.mixer.music.get_busy()
    
    def is_music_paused(self) -> bool:
        """Check if music is paused
        
        Returns:
            True if music is paused
        """
        return self.music_paused
    
    def get_sound_count(self) -> int:
        """Get number of currently playing sounds
        
        Returns:
            Number of active sound channels
        """
        return len([ch for ch in self.playing_sounds.values() if ch.get_busy()])
    
    def cleanup(self):
        """Clean up audio resources"""
        self.logger.info("Cleaning up AudioManager")
        
        # Stop all audio
        self.stop_all_sounds()
        self.stop_music()
        
        # Clear tracking
        self.playing_sounds.clear()
        self.sound_instances.clear()
        self.current_music = None
        
        self.logger.info("AudioManager cleanup complete")