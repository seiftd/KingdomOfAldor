"""
Kingdom of Aldoria - Save Manager
Handles game save data, player progress, and persistent storage
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import hashlib

from ..core.config import Config

class SaveManager:
    """Manages game save data and persistent storage"""
    
    def __init__(self):
        """Initialize the save manager"""
        self.logger = logging.getLogger(__name__)
        
        # Save data
        self.player_data: Dict[str, Any] = {}
        self.game_settings: Dict[str, Any] = {}
        self.last_save_time = 0
        
        # Encryption
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Paths
        self.save_dir = Config.SAVE_DIR
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        self.player_save_file = self.save_dir / "player_data.sav"
        self.settings_file = self.save_dir / "settings.json"
        self.backup_dir = self.save_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self.logger.info("SaveManager initialized")
        self._load_all_data()
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = Config.SAVE_DIR / ".key"
        
        if key_file.exists():
            try:
                with open(key_file, 'rb') as f:
                    return f.read()
            except Exception as e:
                self.logger.warning(f"Failed to load encryption key: {e}")
        
        # Create new key
        key = Fernet.generate_key()
        try:
            Config.SAVE_DIR.mkdir(parents=True, exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            key_file.chmod(0o600)  # Restrict permissions
        except Exception as e:
            self.logger.error(f"Failed to save encryption key: {e}")
        
        return key
    
    def _load_all_data(self):
        """Load all save data"""
        self._load_player_data()
        self._load_settings()
    
    def _load_player_data(self):
        """Load player save data"""
        try:
            if self.player_save_file.exists():
                with open(self.player_save_file, 'rb') as f:
                    encrypted_data = f.read()
                
                # Decrypt data
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.player_data = json.loads(decrypted_data.decode('utf-8'))
                
                self.logger.info("Player data loaded successfully")
            else:
                self._create_new_player_data()
                
        except Exception as e:
            self.logger.error(f"Failed to load player data: {e}")
            self._create_new_player_data()
    
    def _load_settings(self):
        """Load game settings"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.game_settings = json.load(f)
                self.logger.info("Settings loaded successfully")
            else:
                self._create_default_settings()
                
        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")
            self._create_default_settings()
    
    def _create_new_player_data(self):
        """Create new player save data"""
        self.player_data = {
            "version": Config.SAVE_VERSION,
            "created_time": time.time(),
            "last_played": time.time(),
            "play_time": 0.0,
            
            # Player stats
            "player": {
                "name": "Arin",
                "level": Config.PLAYER_START_LEVEL,
                "xp": 0,
                "hp": Config.PLAYER_START_HP,
                "max_hp": Config.PLAYER_START_HP,
                "attack": Config.PLAYER_START_ATTACK,
                "defense": Config.PLAYER_START_DEFENSE,
                "speed": Config.PLAYER_START_SPEED,
                "current_skin": "default",
                "current_weapon": "bronze_sword"
            },
            
            # Game progress
            "progress": {
                "current_world": 0,
                "current_stage": 1,
                "worlds_unlocked": 1,
                "stages_completed": 0,
                "bosses_defeated": 0
            },
            
            # Resources
            "currency": {
                "gold": 100,
                "gems": 10
            },
            
            # Stamina
            "stamina": {
                "current": Config.MAX_STAMINA_DEFAULT,
                "max": Config.MAX_STAMINA_DEFAULT,
                "last_recharge": time.time()
            },
            
            # Inventory
            "inventory": {
                "weapons": ["bronze_sword"],
                "skins": ["default"],
                "items": {},
                "equipped": {
                    "weapon": "bronze_sword",
                    "skin": "default"
                }
            },
            
            # Skills
            "skills": {
                "speed_boost": {"unlocked": True, "level": 1},
                "instant_heal": {"unlocked": False, "level": 0},
                "time_rewind": {"unlocked": False, "level": 0},
                "damage_doubler": {"unlocked": False, "level": 0}
            },
            
            # Subscriptions
            "subscriptions": {
                "weekly": {"active": False, "expires": 0},
                "monthly": {"active": False, "expires": 0}
            },
            
            # Statistics
            "stats": {
                "battles_won": 0,
                "battles_lost": 0,
                "total_damage_dealt": 0,
                "total_damage_taken": 0,
                "ads_watched": 0,
                "daily_login_streak": 0,
                "last_login": time.time()
            }
        }
        
        self.logger.info("New player data created")
    
    def _create_default_settings(self):
        """Create default game settings"""
        self.game_settings = {
            "version": Config.SAVE_VERSION,
            "audio": {
                "master_volume": Config.MASTER_VOLUME,
                "music_volume": Config.MUSIC_VOLUME,
                "sfx_volume": Config.SFX_VOLUME
            },
            "graphics": {
                "fullscreen": Config.FULLSCREEN,
                "resolution": [Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT]
            },
            "gameplay": {
                "language": Config.DEFAULT_LANGUAGE,
                "auto_save": True,
                "notifications": True
            },
            "controls": {
                "touch_sensitivity": 1.0,
                "haptic_feedback": True
            }
        }
        
        self.logger.info("Default settings created")
    
    def save_game_data(self):
        """Save all game data"""
        try:
            self._save_player_data()
            self._save_settings()
            self._create_backup()
            self.last_save_time = time.time()
            self.logger.info("Game data saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save game data: {e}")
            return False
    
    def _save_player_data(self):
        """Save player data with encryption"""
        # Update last played time
        self.player_data["last_played"] = time.time()
        
        # Serialize and encrypt
        json_data = json.dumps(self.player_data, indent=2)
        encrypted_data = self.cipher.encrypt(json_data.encode('utf-8'))
        
        # Write to file
        with open(self.player_save_file, 'wb') as f:
            f.write(encrypted_data)
    
    def _save_settings(self):
        """Save game settings"""
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.game_settings, f, indent=2)
    
    def _create_backup(self):
        """Create backup of save files"""
        try:
            timestamp = int(time.time())
            backup_file = self.backup_dir / f"player_backup_{timestamp}.sav"
            
            if self.player_save_file.exists():
                import shutil
                shutil.copy2(self.player_save_file, backup_file)
            
            # Keep only last 5 backups
            self._cleanup_old_backups()
            
        except Exception as e:
            self.logger.warning(f"Failed to create backup: {e}")
    
    def _cleanup_old_backups(self):
        """Remove old backup files"""
        try:
            backups = sorted(self.backup_dir.glob("player_backup_*.sav"))
            if len(backups) > 5:
                for backup in backups[:-5]:
                    backup.unlink()
                    
        except Exception as e:
            self.logger.warning(f"Failed to cleanup backups: {e}")
    
    def get_player_data(self, key: str = None) -> Any:
        """Get player data
        
        Args:
            key: Specific key to get (None for all data)
            
        Returns:
            Player data or specific value
        """
        if key is None:
            return self.player_data.copy()
        
        keys = key.split('.')
        data = self.player_data
        
        try:
            for k in keys:
                data = data[k]
            return data
        except KeyError:
            self.logger.warning(f"Player data key not found: {key}")
            return None
    
    def set_player_data(self, key: str, value: Any):
        """Set player data
        
        Args:
            key: Dot-separated key path
            value: Value to set
        """
        keys = key.split('.')
        data = self.player_data
        
        # Navigate to parent
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        # Set value
        data[keys[-1]] = value
        
        self.logger.debug(f"Set player data: {key} = {value}")
    
    def get_setting(self, key: str) -> Any:
        """Get game setting
        
        Args:
            key: Dot-separated key path
            
        Returns:
            Setting value or None
        """
        keys = key.split('.')
        data = self.game_settings
        
        try:
            for k in keys:
                data = data[k]
            return data
        except KeyError:
            self.logger.warning(f"Setting key not found: {key}")
            return None
    
    def set_setting(self, key: str, value: Any):
        """Set game setting
        
        Args:
            key: Dot-separated key path
            value: Value to set
        """
        keys = key.split('.')
        data = self.game_settings
        
        # Navigate to parent
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        # Set value
        data[keys[-1]] = value
        
        self.logger.debug(f"Set setting: {key} = {value}")
    
    def auto_save_if_needed(self):
        """Auto-save if enough time has passed"""
        current_time = time.time()
        if current_time - self.last_save_time > Config.AUTO_SAVE_INTERVAL:
            self.save_game_data()
    
    def export_save_data(self) -> Optional[str]:
        """Export save data as JSON string
        
        Returns:
            JSON string of save data or None if failed
        """
        try:
            export_data = {
                "version": Config.SAVE_VERSION,
                "export_time": time.time(),
                "player_data": self.player_data,
                "checksum": self._calculate_checksum(self.player_data)
            }
            return json.dumps(export_data, indent=2)
            
        except Exception as e:
            self.logger.error(f"Failed to export save data: {e}")
            return None
    
    def import_save_data(self, json_data: str) -> bool:
        """Import save data from JSON string
        
        Args:
            json_data: JSON string containing save data
            
        Returns:
            True if import successful
        """
        try:
            import_data = json.loads(json_data)
            
            # Verify checksum
            if "checksum" in import_data:
                expected_checksum = self._calculate_checksum(import_data["player_data"])
                if import_data["checksum"] != expected_checksum:
                    self.logger.error("Save data checksum mismatch")
                    return False
            
            # Create backup before import
            self._create_backup()
            
            # Import data
            self.player_data = import_data["player_data"]
            self.save_game_data()
            
            self.logger.info("Save data imported successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import save data: {e}")
            return False
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum for data integrity
        
        Args:
            data: Data to calculate checksum for
            
        Returns:
            MD5 checksum string
        """
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(json_str.encode('utf-8')).hexdigest()
    
    def cleanup(self):
        """Clean up save manager"""
        self.logger.info("Cleaning up SaveManager")
        
        # Final save
        try:
            self.save_game_data()
        except Exception as e:
            self.logger.error(f"Failed final save during cleanup: {e}")
        
        self.logger.info("SaveManager cleanup complete")