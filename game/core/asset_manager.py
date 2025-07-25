"""
Kingdom of Aldoria - Asset Manager
Handles loading, caching, and optimization of all game assets
"""

import pygame
import os
import json
from typing import Dict, Any, Optional
from PIL import Image
import io
from .config import GameConfig

class AssetManager:
    """Manages all game assets with optimization for mobile devices"""
    
    def __init__(self):
        """Initialize the asset manager"""
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music: Dict[str, str] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.data: Dict[str, Any] = {}
        
        # Cache management
        self.cache_size = GameConfig.TEXTURE_CACHE_SIZE
        self.cache_usage = []
        
        # Asset paths
        self.assets_path = GameConfig.ASSETS_PATH
        self.images_path = os.path.join(self.assets_path, "images")
        self.audio_path = os.path.join(self.assets_path, "audio")
        self.fonts_path = os.path.join(self.assets_path, "fonts")
        self.data_path = os.path.join(self.assets_path, "data")
        
        # Quality settings
        self.texture_quality = GameConfig.TEXTURE_QUALITY
        self.audio_quality = GameConfig.AUDIO_QUALITY
        
        # Essential assets (always loaded)
        self.essential_assets = [
            "ui/button_normal.png",
            "ui/button_pressed.png", 
            "ui/panel_bg.png",
            "ui/health_bar.png",
            "ui/stamina_bar.png",
            "ui/gem_icon.png",
            "ui/gold_icon.png"
        ]
        
    def load_essential_assets(self):
        """Load essential assets required for the game to start"""
        print("Loading essential assets...")
        
        # Create placeholder assets if files don't exist
        self._create_placeholder_assets()
        
        # Load essential UI elements
        for asset_path in self.essential_assets:
            self.load_image(asset_path)
        
        # Load default font
        self.load_font("default", None, 24)
        self.load_font("title", None, 48)
        self.load_font("small", None, 16)
        
        print("Essential assets loaded.")
    
    def _create_placeholder_assets(self):
        """Create placeholder assets for testing if actual assets don't exist"""
        os.makedirs(self.images_path, exist_ok=True)
        os.makedirs(os.path.join(self.images_path, "ui"), exist_ok=True)
        os.makedirs(os.path.join(self.images_path, "characters"), exist_ok=True)
        os.makedirs(os.path.join(self.images_path, "enemies"), exist_ok=True)
        os.makedirs(os.path.join(self.images_path, "weapons"), exist_ok=True)
        os.makedirs(os.path.join(self.images_path, "worlds"), exist_ok=True)
        os.makedirs(os.path.join(self.images_path, "effects"), exist_ok=True)
        
        # Create placeholder UI elements
        placeholders = {
            "ui/button_normal.png": (200, 60, (100, 100, 150)),
            "ui/button_pressed.png": (200, 60, (80, 80, 120)),
            "ui/panel_bg.png": (400, 300, (50, 50, 80)),
            "ui/health_bar.png": (200, 20, (200, 50, 50)),
            "ui/stamina_bar.png": (200, 20, (50, 150, 50)),
            "ui/gem_icon.png": (32, 32, (150, 50, 200)),
            "ui/gold_icon.png": (32, 32, (200, 180, 50)),
            "characters/knight_arin.png": (64, 64, (150, 150, 200)),
            "characters/forest_scout.png": (64, 64, (50, 150, 50)),
            "characters/desert_nomad.png": (64, 64, (200, 150, 50)),
            "characters/void_knight.png": (64, 64, (100, 50, 150)),
            "enemies/shadow_wolf.png": (48, 48, (80, 80, 80)),
            "enemies/sand_pharaoh.png": (64, 64, (200, 180, 100)),
            "enemies/ice_yeti.png": (72, 72, (200, 220, 255)),
            "weapons/bronze_sword.png": (32, 48, (150, 100, 50)),
            "weapons/void_scythe.png": (32, 64, (100, 50, 200)),
            "weapons/solar_flare_sword.png": (32, 48, (255, 200, 50)),
            "worlds/forest_bg.png": (1280, 720, (20, 80, 20)),
            "worlds/desert_bg.png": (1280, 720, (200, 180, 100)),
            "worlds/ice_bg.png": (1280, 720, (200, 220, 255))
        }
        
        for asset_path, (width, height, color) in placeholders.items():
            full_path = os.path.join(self.images_path, asset_path)
            if not os.path.exists(full_path):
                # Create placeholder image
                surface = pygame.Surface((width, height))
                surface.fill(color)
                
                # Add some visual indication it's a placeholder
                font = pygame.font.Font(None, 24)
                text = font.render("PLACEHOLDER", True, (255, 255, 255))
                text_rect = text.get_rect(center=(width//2, height//2))
                surface.blit(text, text_rect)
                
                pygame.image.save(surface, full_path)
    
    def load_image(self, path: str, convert_alpha: bool = True) -> Optional[pygame.Surface]:
        """Load an image with optimization and caching"""
        if path in self.images:
            self._update_cache_usage(path)
            return self.images[path]
        
        full_path = os.path.join(self.images_path, path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Image not found: {full_path}")
            return None
        
        try:
            # Load image
            if convert_alpha:
                image = pygame.image.load(full_path).convert_alpha()
            else:
                image = pygame.image.load(full_path).convert()
            
            # Apply quality optimizations
            image = self._optimize_image(image)
            
            # Cache management
            self._manage_cache()
            self.images[path] = image
            self.cache_usage.append(path)
            
            return image
            
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    def _optimize_image(self, image: pygame.Surface) -> pygame.Surface:
        """Optimize image based on quality settings"""
        if self.texture_quality == "low":
            # Reduce resolution by 50%
            width, height = image.get_size()
            image = pygame.transform.scale(image, (width // 2, height // 2))
        elif self.texture_quality == "medium":
            # Reduce resolution by 25%
            width, height = image.get_size()
            image = pygame.transform.scale(image, (int(width * 0.75), int(height * 0.75)))
        
        return image
    
    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound effect"""
        if path in self.sounds:
            return self.sounds[path]
        
        full_path = os.path.join(self.audio_path, "sfx", path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Sound not found: {full_path}")
            return None
        
        try:
            sound = pygame.mixer.Sound(full_path)
            
            # Apply volume based on audio quality
            if self.audio_quality == "low":
                sound.set_volume(GameConfig.SFX_VOLUME * 0.7)
            else:
                sound.set_volume(GameConfig.SFX_VOLUME)
            
            self.sounds[path] = sound
            return sound
            
        except Exception as e:
            print(f"Error loading sound {path}: {e}")
            return None
    
    def load_music(self, path: str) -> str:
        """Load music file path for streaming"""
        full_path = os.path.join(self.audio_path, "music", path)
        
        if os.path.exists(full_path):
            self.music[path] = full_path
            return full_path
        else:
            print(f"Warning: Music not found: {full_path}")
            return ""
    
    def load_font(self, name: str, path: Optional[str], size: int) -> pygame.font.Font:
        """Load a font"""
        font_key = f"{name}_{size}"
        
        if font_key in self.fonts:
            return self.fonts[font_key]
        
        if path is None:
            # Use default system font
            font = pygame.font.Font(None, size)
        else:
            full_path = os.path.join(self.fonts_path, path)
            if os.path.exists(full_path):
                font = pygame.font.Font(full_path, size)
            else:
                print(f"Warning: Font not found: {full_path}, using default")
                font = pygame.font.Font(None, size)
        
        self.fonts[font_key] = font
        return font
    
    def load_data(self, path: str) -> Optional[Any]:
        """Load JSON data file"""
        if path in self.data:
            return self.data[path]
        
        full_path = os.path.join(self.data_path, path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Data file not found: {full_path}")
            return None
        
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
            
            self.data[path] = data
            return data
            
        except Exception as e:
            print(f"Error loading data {path}: {e}")
            return None
    
    def _manage_cache(self):
        """Manage image cache to prevent memory overflow"""
        if len(self.images) >= self.cache_size:
            # Remove least recently used item
            if self.cache_usage:
                oldest_key = self.cache_usage.pop(0)
                if oldest_key in self.images:
                    del self.images[oldest_key]
    
    def _update_cache_usage(self, key: str):
        """Update cache usage order"""
        if key in self.cache_usage:
            self.cache_usage.remove(key)
        self.cache_usage.append(key)
    
    def preload_world_assets(self, world_id: int):
        """Preload assets for a specific world"""
        world_data = GameConfig.WORLD_DATA.get(world_id, {})
        theme = world_data.get("theme", "forest")
        
        # Load world background
        self.load_image(f"worlds/{theme}_bg.png")
        
        # Load enemies for this world
        enemies = GameConfig.ENEMY_DATA.get(world_id, [])
        for enemy in enemies:
            self.load_image(f"enemies/{enemy}.png")
        
        # Load world-specific effects
        self.load_image(f"effects/{theme}_particle.png")
    
    def unload_world_assets(self, world_id: int):
        """Unload assets for a specific world to free memory"""
        world_data = GameConfig.WORLD_DATA.get(world_id, {})
        theme = world_data.get("theme", "forest")
        
        # Remove world-specific assets from cache
        to_remove = []
        for key in self.images.keys():
            if theme in key or f"world_{world_id}" in key:
                to_remove.append(key)
        
        for key in to_remove:
            if key not in self.essential_assets:  # Don't remove essential assets
                del self.images[key]
                if key in self.cache_usage:
                    self.cache_usage.remove(key)
    
    def get_character_image(self, skin_id: str) -> Optional[pygame.Surface]:
        """Get character image for specific skin"""
        skin_path = f"characters/{skin_id}.png"
        return self.load_image(skin_path)
    
    def get_weapon_image(self, weapon_id: str) -> Optional[pygame.Surface]:
        """Get weapon image"""
        weapon_path = f"weapons/{weapon_id}.png"
        return self.load_image(weapon_path)
    
    def get_enemy_image(self, enemy_id: str) -> Optional[pygame.Surface]:
        """Get enemy image"""
        enemy_path = f"enemies/{enemy_id}.png"
        return self.load_image(enemy_path)
    
    def get_world_background(self, world_id: int) -> Optional[pygame.Surface]:
        """Get world background image"""
        world_data = GameConfig.WORLD_DATA.get(world_id, {})
        theme = world_data.get("theme", "forest")
        bg_path = f"worlds/{theme}_bg.png"
        return self.load_image(bg_path)
    
    def clear_cache(self):
        """Clear all cached assets except essential ones"""
        to_remove = []
        for key in self.images.keys():
            if key not in self.essential_assets:
                to_remove.append(key)
        
        for key in to_remove:
            del self.images[key]
        
        self.cache_usage = [key for key in self.cache_usage if key in self.images]
        
        # Clear other caches
        self.sounds.clear()
        self.data.clear()
    
    def get_memory_usage(self) -> Dict[str, int]:
        """Get current memory usage statistics"""
        return {
            "images_loaded": len(self.images),
            "sounds_loaded": len(self.sounds),
            "data_loaded": len(self.data),
            "cache_usage": len(self.cache_usage)
        }