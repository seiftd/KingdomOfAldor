"""
Kingdom of Aldoria - Audio Manager
Handles music, sound effects, and audio optimization for mobile devices
"""

import pygame
import os
from typing import Dict, Optional
from .config import GameConfig

class AudioManager:
    """Manages all audio in the game with mobile optimizations"""
    
    def __init__(self):
        """Initialize the audio manager"""
        self.master_volume = GameConfig.MASTER_VOLUME
        self.music_volume = GameConfig.MUSIC_VOLUME
        self.sfx_volume = GameConfig.SFX_VOLUME
        
        # Current music state
        self.current_music = None
        self.music_paused = False
        self.music_position = 0
        
        # Sound effect pools for optimization
        self.sound_pools: Dict[str, list] = {}
        self.max_sounds_per_type = 5
        
        # Audio quality settings
        self.audio_quality = GameConfig.AUDIO_QUALITY
        
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            if self.audio_quality == "high":
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            elif self.audio_quality == "medium":
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
            else:  # low quality
                pygame.mixer.init(frequency=11025, size=-16, channels=1, buffer=2048)
        
        # Set initial volumes
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        
        # Music tracks mapping
        self.music_tracks = {
            "main_menu": "main_theme.ogg",
            "forest": "forest_ambient.ogg",
            "desert": "desert_winds.ogg",
            "ice": "ice_caves.ogg",
            "volcano": "volcanic_fury.ogg",
            "swamp": "mystic_swamp.ogg",
            "cave": "crystal_echoes.ogg",
            "sky": "sky_citadel.ogg",
            "dark": "dark_kingdom.ogg",
            "light": "light_fortress.ogg",
            "void": "void_nexus.ogg",
            "boss_battle": "boss_battle.ogg",
            "victory": "victory_fanfare.ogg"
        }
        
        # Sound effects mapping
        self.sfx_mapping = {
            "button_click": "ui_click.ogg",
            "button_hover": "ui_hover.ogg",
            "sword_hit": "sword_impact.ogg",
            "magic_cast": "magic_spell.ogg",
            "enemy_death": "enemy_death.ogg",
            "level_up": "level_up.ogg",
            "item_pickup": "item_pickup.ogg",
            "skill_activate": "skill_use.ogg",
            "heal": "healing.ogg",
            "damage_taken": "player_hurt.ogg",
            "coin_collect": "coin_pickup.ogg",
            "gem_collect": "gem_pickup.ogg",
            "page_turn": "page_turn.ogg",
            "purchase": "purchase_success.ogg",
            "error": "error_sound.ogg",
            "notification": "notification.ogg"
        }
    
    def play_music(self, track_name: str, loops: int = -1, fade_in: float = 0):
        """Play background music"""
        if track_name not in self.music_tracks:
            print(f"Warning: Music track '{track_name}' not found")
            return
        
        music_file = self.music_tracks[track_name]
        music_path = os.path.join("assets", "audio", "music", music_file)
        
        # Create placeholder music if file doesn't exist
        if not os.path.exists(music_path):
            print(f"Warning: Music file not found: {music_path}")
            return
        
        try:
            if self.current_music != track_name:
                pygame.mixer.music.load(music_path)
                
                if fade_in > 0:
                    pygame.mixer.music.play(loops, fade_ms=int(fade_in * 1000))
                else:
                    pygame.mixer.music.play(loops)
                
                self.current_music = track_name
                self.music_paused = False
                
        except Exception as e:
            print(f"Error playing music {track_name}: {e}")
    
    def stop_music(self, fade_out: float = 0):
        """Stop background music"""
        if fade_out > 0:
            pygame.mixer.music.fadeout(int(fade_out * 1000))
        else:
            pygame.mixer.music.stop()
        
        self.current_music = None
        self.music_paused = False
    
    def pause_music(self):
        """Pause background music"""
        if not self.music_paused:
            pygame.mixer.music.pause()
            self.music_paused = True
    
    def resume_music(self):
        """Resume background music"""
        if self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False
    
    def play_sfx(self, sound_name: str, volume: float = 1.0) -> bool:
        """Play a sound effect with volume control"""
        if sound_name not in self.sfx_mapping:
            print(f"Warning: Sound effect '{sound_name}' not found")
            return False
        
        # Get or create sound pool
        if sound_name not in self.sound_pools:
            self.sound_pools[sound_name] = []
        
        sound_pool = self.sound_pools[sound_name]
        
        # Find an available sound or create a new one
        available_sound = None
        for sound in sound_pool:
            if not sound.get_num_channels():  # Sound is not playing
                available_sound = sound
                break
        
        if available_sound is None and len(sound_pool) < self.max_sounds_per_type:
            # Create new sound
            sound_file = self.sfx_mapping[sound_name]
            sound_path = os.path.join("assets", "audio", "sfx", sound_file)
            
            # Create placeholder sound if file doesn't exist
            if not os.path.exists(sound_path):
                self._create_placeholder_sound(sound_path)
            
            try:
                new_sound = pygame.mixer.Sound(sound_path)
                sound_pool.append(new_sound)
                available_sound = new_sound
            except Exception as e:
                print(f"Error loading sound {sound_name}: {e}")
                return False
        
        if available_sound:
            # Set volume and play
            final_volume = self.sfx_volume * self.master_volume * volume
            available_sound.set_volume(final_volume)
            available_sound.play()
            return True
        
        return False
    
    def _create_placeholder_sound(self, sound_path: str):
        """Create a placeholder sound file"""
        os.makedirs(os.path.dirname(sound_path), exist_ok=True)
        
        # Generate a simple tone as placeholder
        duration = 0.5  # seconds
        sample_rate = 22050
        
        # Create a simple sine wave
        import numpy as np
        
        frequency = 440  # A note
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            wave = np.sin(2 * np.pi * frequency * i / sample_rate)
            arr[i][0] = wave * 0.1  # Left channel
            arr[i][1] = wave * 0.1  # Right channel
        
        # Convert to 16-bit integers
        arr = (arr * 32767).astype(np.int16)
        
        # Save as WAV file (pygame can load this)
        import wave
        wav_path = sound_path.replace('.ogg', '.wav')
        
        with wave.open(wav_path, 'w') as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(arr.tobytes())
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        
        # Update music volume
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        
        # Update all sound effects volumes
        for sound_pool in self.sound_pools.values():
            for sound in sound_pool:
                current_vol = sound.get_volume()
                if current_vol > 0:  # Only update if sound was playing
                    sound.set_volume(self.sfx_volume * self.master_volume)
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def play_world_music(self, world_id: int):
        """Play music appropriate for the world"""
        world_data = GameConfig.WORLD_DATA.get(world_id, {})
        theme = world_data.get("theme", "forest")
        
        self.play_music(theme, fade_in=1.0)
    
    def play_boss_music(self):
        """Play boss battle music"""
        self.play_music("boss_battle", fade_in=0.5)
    
    def play_victory_music(self):
        """Play victory fanfare"""
        self.play_music("victory", loops=0)  # Play once
    
    def play_ui_sound(self, ui_action: str):
        """Play UI-related sound effects"""
        ui_sounds = {
            "click": "button_click",
            "hover": "button_hover", 
            "page": "page_turn",
            "buy": "purchase",
            "error": "error",
            "notify": "notification"
        }
        
        if ui_action in ui_sounds:
            self.play_sfx(ui_sounds[ui_action], volume=0.7)
    
    def play_combat_sound(self, action: str):
        """Play combat-related sound effects"""
        combat_sounds = {
            "hit": "sword_hit",
            "magic": "magic_cast",
            "death": "enemy_death",
            "hurt": "damage_taken",
            "heal": "heal",
            "skill": "skill_activate"
        }
        
        if action in combat_sounds:
            self.play_sfx(combat_sounds[action])
    
    def play_pickup_sound(self, item_type: str):
        """Play item pickup sound effects"""
        pickup_sounds = {
            "gold": "coin_collect",
            "gem": "gem_collect",
            "item": "item_pickup",
            "xp": "level_up"
        }
        
        if item_type in pickup_sounds:
            self.play_sfx(pickup_sounds[item_type], volume=0.8)
    
    def stop_all_sounds(self):
        """Stop all playing sounds"""
        pygame.mixer.stop()
        self.stop_music()
    
    def fade_out_all(self, duration: float = 1.0):
        """Fade out all audio"""
        self.stop_music(fade_out=duration)
        
        # Fade out sound effects (simplified - just lower volume)
        for sound_pool in self.sound_pools.values():
            for sound in sound_pool:
                if sound.get_num_channels() > 0:
                    current_vol = sound.get_volume()
                    sound.set_volume(current_vol * 0.1)
    
    def cleanup(self):
        """Clean up audio resources"""
        self.stop_all_sounds()
        
        # Clear sound pools
        for sound_pool in self.sound_pools.values():
            for sound in sound_pool:
                del sound
        
        self.sound_pools.clear()
        
        # Quit mixer
        pygame.mixer.quit()
    
    def get_volume_settings(self) -> Dict[str, float]:
        """Get current volume settings"""
        return {
            "master": self.master_volume,
            "music": self.music_volume,
            "sfx": self.sfx_volume
        }
    
    def set_volume_settings(self, settings: Dict[str, float]):
        """Set volume settings from dictionary"""
        if "master" in settings:
            self.set_master_volume(settings["master"])
        if "music" in settings:
            self.set_music_volume(settings["music"])
        if "sfx" in settings:
            self.set_sfx_volume(settings["sfx"])
    
    def is_music_playing(self) -> bool:
        """Check if music is currently playing"""
        return pygame.mixer.music.get_busy() and not self.music_paused
    
    def get_current_music(self) -> Optional[str]:
        """Get currently playing music track name"""
        return self.current_music if self.is_music_playing() else None