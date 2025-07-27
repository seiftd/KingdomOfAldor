"""
Kingdom of Aldoria - Asset Manager
Handles loading, caching, and management of game assets
"""

import pygame
import logging
import json
import os
from pathlib import Path
from typing import Dict, Optional, Any, Tuple
from PIL import Image
import threading
import asyncio

from ..core.config import Config

class AssetManager:
    """Manages loading and caching of game assets"""
    
    def __init__(self):
        """Initialize the asset manager"""
        self.logger = logging.getLogger(__name__)
        
        # Asset caches
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music: Dict[str, str] = {}  # Store file paths for music
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.data: Dict[str, Any] = {}
        
        # Loading state
        self.loading_queue = []
        self.loaded_assets = set()
        self.failed_assets = set()
        
        # Cache management
        self.cache_size = 0
        self.max_cache_size = Config.ASSET_CACHE_SIZE * 1024 * 1024  # MB to bytes
        
        # Threading for async loading
        self.loading_thread = None
        self.loading_lock = threading.Lock()
        
        self.logger.info("AssetManager initialized")
        self._create_missing_directories()
    
    def _create_missing_directories(self):
        """Create missing asset directories"""
        directories = [
            Config.ASSETS_DIR,
            Config.SPRITES_DIR,
            Config.AUDIO_DIR,
            Config.UI_DIR,
            Config.WORLDS_DIR,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_image(self, path: str, convert_alpha: bool = True) -> Optional[pygame.Surface]:
        """Load an image asset
        
        Args:
            path: Relative path to image file
            convert_alpha: Whether to convert for alpha blending
            
        Returns:
            Pygame surface or None if failed
        """
        if path in self.images:
            return self.images[path]
        
        full_path = Config.SPRITES_DIR / path
        
        try:
            # Try multiple extensions
            extensions = ['.webp', '.png', '.jpg', '.jpeg']
            actual_path = None
            
            for ext in extensions:
                test_path = full_path.with_suffix(ext)
                if test_path.exists():
                    actual_path = test_path
                    break
            
            if not actual_path:
                # Create placeholder if file doesn't exist
                self.logger.warning(f"Image not found: {path}, creating placeholder")
                return self._create_placeholder_image(64, 64)
            
            # Load image
            if actual_path.suffix.lower() == '.webp':
                # Use PIL for WebP, then convert to pygame surface
                pil_image = Image.open(actual_path)
                if pil_image.mode != 'RGBA':
                    pil_image = pil_image.convert('RGBA')
                
                # Convert PIL to pygame surface
                surface = pygame.image.fromstring(
                    pil_image.tobytes(), pil_image.size, pil_image.mode
                )
            else:
                surface = pygame.image.load(str(actual_path))
            
            # Convert surface for better performance
            if convert_alpha:
                surface = surface.convert_alpha()
            else:
                surface = surface.convert()
            
            # Cache the image
            self.images[path] = surface
            self._update_cache_size(surface)
            
            self.logger.debug(f"Loaded image: {path}")
            return surface
            
        except Exception as e:
            self.logger.error(f"Failed to load image {path}: {e}")
            self.failed_assets.add(path)
            return self._create_placeholder_image(64, 64)
    
    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound effect
        
        Args:
            path: Relative path to sound file
            
        Returns:
            Pygame Sound object or None if failed
        """
        if path in self.sounds:
            return self.sounds[path]
        
        full_path = Config.AUDIO_DIR / path
        
        try:
            # Try multiple extensions
            extensions = ['.ogg', '.wav', '.mp3']
            actual_path = None
            
            for ext in extensions:
                test_path = full_path.with_suffix(ext)
                if test_path.exists():
                    actual_path = test_path
                    break
            
            if not actual_path:
                self.logger.warning(f"Sound not found: {path}")
                return None
            
            if pygame.mixer.get_init():
                sound = pygame.mixer.Sound(str(actual_path))
                sound.set_volume(Config.SFX_VOLUME)
            else:
                self.logger.warning(f"Cannot load sound {path} - audio not available")
                return None
            
            self.sounds[path] = sound
            self.logger.debug(f"Loaded sound: {path}")
            return sound
            
        except Exception as e:
            self.logger.error(f"Failed to load sound {path}: {e}")
            self.failed_assets.add(path)
            return None
    
    def load_music(self, path: str) -> bool:
        """Load background music
        
        Args:
            path: Relative path to music file
            
        Returns:
            True if successful
        """
        if path in self.music:
            return True
        
        full_path = Config.AUDIO_DIR / path
        
        try:
            # Try multiple extensions
            extensions = ['.ogg', '.mp3', '.wav']
            actual_path = None
            
            for ext in extensions:
                test_path = full_path.with_suffix(ext)
                if test_path.exists():
                    actual_path = test_path
                    break
            
            if not actual_path:
                self.logger.warning(f"Music not found: {path}")
                return False
            
            self.music[path] = str(actual_path)
            self.logger.debug(f"Registered music: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register music {path}: {e}")
            self.failed_assets.add(path)
            return False
    
    def load_font(self, path: str, size: int) -> Optional[pygame.font.Font]:
        """Load a font
        
        Args:
            path: Relative path to font file (or None for default)
            size: Font size
            
        Returns:
            Pygame Font object
        """
        cache_key = f"{path}_{size}"
        
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        try:
            if path is None:
                font = pygame.font.Font(None, size)
            else:
                full_path = Config.ASSETS_DIR / "fonts" / path
                if full_path.exists():
                    font = pygame.font.Font(str(full_path), size)
                else:
                    self.logger.warning(f"Font not found: {path}, using default")
                    font = pygame.font.Font(None, size)
            
            self.fonts[cache_key] = font
            self.logger.debug(f"Loaded font: {path} size {size}")
            return font
            
        except Exception as e:
            self.logger.error(f"Failed to load font {path}: {e}")
            return pygame.font.Font(None, size)
    
    def load_data(self, path: str) -> Optional[Any]:
        """Load JSON data file
        
        Args:
            path: Relative path to data file
            
        Returns:
            Parsed data or None if failed
        """
        if path in self.data:
            return self.data[path]
        
        full_path = Config.ASSETS_DIR / "data" / path
        
        try:
            if not full_path.exists():
                self.logger.warning(f"Data file not found: {path}")
                return None
            
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.data[path] = data
            self.logger.debug(f"Loaded data: {path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load data {path}: {e}")
            self.failed_assets.add(path)
            return None
    
    def _create_placeholder_image(self, width: int, height: int) -> pygame.Surface:
        """Create a placeholder image for missing assets
        
        Args:
            width: Image width
            height: Image height
            
        Returns:
            Pygame surface with placeholder pattern
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Create a checkerboard pattern
        block_size = min(width, height) // 4
        for x in range(0, width, block_size):
            for y in range(0, height, block_size):
                color = Config.PURPLE if (x // block_size + y // block_size) % 2 else Config.DARK_GRAY
                pygame.draw.rect(surface, color, (x, y, block_size, block_size))
        
        return surface
    
    def _update_cache_size(self, surface: pygame.Surface):
        """Update cache size tracking
        
        Args:
            surface: Surface to calculate size for
        """
        # Rough calculation of surface memory usage
        size = surface.get_width() * surface.get_height() * 4  # RGBA
        self.cache_size += size
        
        # Clean cache if over limit
        if self.cache_size > self.max_cache_size:
            self._clean_cache()
    
    def _clean_cache(self):
        """Clean asset cache to free memory"""
        self.logger.info("Cleaning asset cache")
        
        # Simple strategy: remove half of cached images
        items_to_remove = len(self.images) // 2
        keys_to_remove = list(self.images.keys())[:items_to_remove]
        
        for key in keys_to_remove:
            del self.images[key]
        
        # Recalculate cache size
        self.cache_size = sum(
            img.get_width() * img.get_height() * 4
            for img in self.images.values()
        )
        
        self.logger.info(f"Cache cleaned, new size: {self.cache_size / 1024 / 1024:.1f}MB")
    
    def preload_assets(self, asset_list: list):
        """Preload a list of assets
        
        Args:
            asset_list: List of asset paths to preload
        """
        self.logger.info(f"Preloading {len(asset_list)} assets")
        
        for asset_path in asset_list:
            if asset_path.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                self.load_image(asset_path)
            elif asset_path.endswith(('.ogg', '.wav', '.mp3')):
                if 'music' in asset_path:
                    self.load_music(asset_path)
                else:
                    self.load_sound(asset_path)
            elif asset_path.endswith('.json'):
                self.load_data(asset_path)
    
    def get_image(self, path: str) -> Optional[pygame.Surface]:
        """Get a loaded image
        
        Args:
            path: Image path
            
        Returns:
            Cached surface or loads it if not cached
        """
        return self.load_image(path)
    
    def get_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """Get a loaded sound
        
        Args:
            path: Sound path
            
        Returns:
            Cached sound or loads it if not cached
        """
        return self.load_sound(path)
    
    def get_font(self, path: str = None, size: int = 24) -> pygame.font.Font:
        """Get a loaded font
        
        Args:
            path: Font path (None for default)
            size: Font size
            
        Returns:
            Font object
        """
        return self.load_font(path, size)
    
    def play_music(self, path: str, loops: int = -1, volume: float = None):
        """Play background music
        
        Args:
            path: Music path
            loops: Number of loops (-1 for infinite)
            volume: Music volume (None to use default)
        """
        if not pygame.mixer.get_init():
            self.logger.warning("Cannot play music - audio not available")
            return
            
        if self.load_music(path):
            file_path = self.music[path]
            try:
                pygame.mixer.music.load(file_path)
                if volume is not None:
                    pygame.mixer.music.set_volume(volume * Config.MUSIC_VOLUME)
                else:
                    pygame.mixer.music.set_volume(Config.MUSIC_VOLUME)
                pygame.mixer.music.play(loops)
                self.logger.debug(f"Playing music: {path}")
            except Exception as e:
                self.logger.error(f"Failed to play music {path}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except pygame.error:
            pass  # Audio not available
    
    def cleanup(self):
        """Clean up all cached assets"""
        self.logger.info("Cleaning up AssetManager")
        
        # Stop any playing music (if audio is available)
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except pygame.error:
            pass  # Audio not available
        
        # Clear all caches
        self.images.clear()
        self.sounds.clear()
        self.music.clear()
        self.fonts.clear()
        self.data.clear()
        
        self.cache_size = 0
        self.loaded_assets.clear()
        self.failed_assets.clear()
        
        self.logger.info("AssetManager cleanup complete")