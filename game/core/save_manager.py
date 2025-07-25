"""
Kingdom of Aldoria - Save Manager
Handles player data persistence, encryption, and cloud save functionality
"""

import json
import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from .config import GameConfig

class SaveManager:
    """Manages player save data with security and cloud integration"""
    
    def __init__(self):
        """Initialize the save manager"""
        self.save_file = GameConfig.SAVE_FILE
        self.backup_file = f"{GameConfig.SAVE_FILE}.backup"
        self.cloud_save_file = f"{GameConfig.SAVE_FILE}.cloud"
        
        # Default save data structure
        self.default_save_data = {
            "player": {
                "name": "Arin",
                "level": 1,
                "experience": 0,
                "gold": 100,
                "gems": 50,
                "stamina": GameConfig.MAX_STAMINA_DEFAULT,
                "max_stamina": GameConfig.MAX_STAMINA_DEFAULT,
                "last_stamina_update": 0,
                "current_skin": "default_knight",
                "current_weapon": "bronze_sword",
                "unlocked_skins": ["default_knight"],
                "unlocked_weapons": ["bronze_sword"],
                "skill_cooldowns": {},
                "stats": {
                    "hp": 100,
                    "max_hp": 100,
                    "attack": 50,
                    "defense": 25,
                    "speed": 100
                }
            },
            "progress": {
                "current_world": 1,
                "current_stage": 1,
                "worlds_unlocked": [1],
                "stages_completed": [],
                "bosses_defeated": [],
                "total_stages_completed": 0,
                "highest_stage_reached": 1
            },
            "inventory": {
                "consumables": {},
                "materials": {},
                "special_items": []
            },
            "achievements": {
                "unlocked": [],
                "progress": {}
            },
            "settings": {
                "master_volume": GameConfig.MASTER_VOLUME,
                "music_volume": GameConfig.MUSIC_VOLUME,
                "sfx_volume": GameConfig.SFX_VOLUME,
                "language": GameConfig.DEFAULT_LANGUAGE,
                "quality": GameConfig.TEXTURE_QUALITY,
                "notifications": True
            },
            "monetization": {
                "subscriptions": {
                    "weekly": {
                        "active": False,
                        "expires": 0,
                        "last_claim": 0
                    },
                    "monthly": {
                        "active": False,
                        "expires": 0,
                        "last_claim": 0
                    }
                },
                "purchases": [],
                "ad_data": {
                    "ads_watched_today": 0,
                    "last_ad_date": "",
                    "total_ads_watched": 0,
                    "last_rewarded_ad": 0
                },
                "daily_login": {
                    "streak": 0,
                    "last_login": "",
                    "rewards_claimed": []
                },
                "promo_codes_used": []
            },
            "statistics": {
                "total_playtime": 0,
                "enemies_defeated": 0,
                "gold_earned": 0,
                "gems_spent": 0,
                "skills_used": 0,
                "deaths": 0,
                "revivals": 0
            },
            "metadata": {
                "version": "1.0.0",
                "created": 0,
                "last_save": 0,
                "save_count": 0,
                "device_id": "",
                "checksum": ""
            }
        }
        
        # Current save data
        self.save_data = {}
        self.load_save_data()
        
        # Encryption key (in production, this should be more secure)
        self.encryption_key = self._generate_encryption_key()
    
    def _generate_encryption_key(self) -> str:
        """Generate encryption key for save data"""
        # In production, use a more secure method
        device_info = f"kingdom_aldoria_{os.name}"
        return hashlib.sha256(device_info.encode()).hexdigest()[:32]
    
    def _encrypt_data(self, data: str) -> str:
        """Simple encryption for save data"""
        # Simple XOR encryption (use proper encryption in production)
        encrypted = ""
        key_len = len(self.encryption_key)
        
        for i, char in enumerate(data):
            key_char = self.encryption_key[i % key_len]
            encrypted += chr(ord(char) ^ ord(key_char))
        
        return base64.b64encode(encrypted.encode()).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt save data"""
        try:
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            decrypted = ""
            key_len = len(self.encryption_key)
            
            for i, char in enumerate(decoded):
                key_char = self.encryption_key[i % key_len]
                decrypted += chr(ord(char) ^ ord(key_char))
            
            return decrypted
        except:
            return ""
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum for data integrity"""
        # Remove checksum from data for calculation
        data_copy = data.copy()
        if "metadata" in data_copy and "checksum" in data_copy["metadata"]:
            del data_copy["metadata"]["checksum"]
        
        data_str = json.dumps(data_copy, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _verify_save_data(self, data: Dict[str, Any]) -> bool:
        """Verify save data integrity"""
        if "metadata" not in data or "checksum" not in data["metadata"]:
            return False
        
        stored_checksum = data["metadata"]["checksum"]
        calculated_checksum = self._calculate_checksum(data)
        
        return stored_checksum == calculated_checksum
    
    def load_save_data(self) -> bool:
        """Load save data from file"""
        # Try to load main save file
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    encrypted_data = f.read()
                
                decrypted_data = self._decrypt_data(encrypted_data)
                if decrypted_data:
                    data = json.loads(decrypted_data)
                    
                    # Verify data integrity
                    if self._verify_save_data(data):
                        self.save_data = data
                        self._migrate_save_data()
                        print("Save data loaded successfully")
                        return True
                    else:
                        print("Save data corrupted, trying backup...")
                        
            except Exception as e:
                print(f"Error loading save data: {e}")
        
        # Try backup file
        if os.path.exists(self.backup_file):
            try:
                with open(self.backup_file, 'r') as f:
                    encrypted_data = f.read()
                
                decrypted_data = self._decrypt_data(encrypted_data)
                if decrypted_data:
                    data = json.loads(decrypted_data)
                    
                    if self._verify_save_data(data):
                        self.save_data = data
                        self._migrate_save_data()
                        print("Backup save data loaded")
                        return True
                        
            except Exception as e:
                print(f"Error loading backup save data: {e}")
        
        # Create new save data
        print("Creating new save data")
        self.save_data = self.default_save_data.copy()
        self._initialize_new_save()
        return False
    
    def _initialize_new_save(self):
        """Initialize new save data with current timestamp and device info"""
        now = datetime.now().timestamp()
        
        self.save_data["metadata"]["created"] = now
        self.save_data["metadata"]["last_save"] = now
        self.save_data["metadata"]["device_id"] = self._get_device_id()
        self.save_data["metadata"]["checksum"] = self._calculate_checksum(self.save_data)
        
        # Set last stamina update to now
        self.save_data["player"]["last_stamina_update"] = now
    
    def _get_device_id(self) -> str:
        """Get unique device identifier"""
        import platform
        import uuid
        
        device_info = f"{platform.system()}_{platform.node()}_{uuid.getnode()}"
        return hashlib.md5(device_info.encode()).hexdigest()
    
    def _migrate_save_data(self):
        """Migrate save data to current version if needed"""
        # Add missing fields from default save data
        def merge_dict(default, current):
            for key, value in default.items():
                if key not in current:
                    current[key] = value
                elif isinstance(value, dict) and isinstance(current[key], dict):
                    merge_dict(value, current[key])
        
        merge_dict(self.default_save_data, self.save_data)
    
    def save_data_to_file(self, create_backup: bool = True) -> bool:
        """Save data to file with optional backup"""
        try:
            # Update metadata
            self.save_data["metadata"]["last_save"] = datetime.now().timestamp()
            self.save_data["metadata"]["save_count"] += 1
            self.save_data["metadata"]["checksum"] = self._calculate_checksum(self.save_data)
            
            # Prepare encrypted data
            data_str = json.dumps(self.save_data, indent=2)
            encrypted_data = self._encrypt_data(data_str)
            
            # Create backup if requested
            if create_backup and os.path.exists(self.save_file):
                try:
                    with open(self.save_file, 'r') as src:
                        with open(self.backup_file, 'w') as dst:
                            dst.write(src.read())
                except:
                    pass  # Backup failed, but continue
            
            # Save main file
            with open(self.save_file, 'w') as f:
                f.write(encrypted_data)
            
            print("Save data written successfully")
            return True
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def save_all(self):
        """Save all game data"""
        self.save_data_to_file(create_backup=True)
    
    def get_player_data(self) -> Dict[str, Any]:
        """Get player data"""
        return self.save_data.get("player", {})
    
    def get_progress_data(self) -> Dict[str, Any]:
        """Get progress data"""
        return self.save_data.get("progress", {})
    
    def get_settings_data(self) -> Dict[str, Any]:
        """Get settings data"""
        return self.save_data.get("settings", {})
    
    def update_player_data(self, updates: Dict[str, Any]):
        """Update player data"""
        if "player" not in self.save_data:
            self.save_data["player"] = {}
        
        for key, value in updates.items():
            self.save_data["player"][key] = value
    
    def update_progress_data(self, updates: Dict[str, Any]):
        """Update progress data"""
        if "progress" not in self.save_data:
            self.save_data["progress"] = {}
        
        for key, value in updates.items():
            self.save_data["progress"][key] = value
    
    def update_settings_data(self, updates: Dict[str, Any]):
        """Update settings data"""
        if "settings" not in self.save_data:
            self.save_data["settings"] = {}
        
        for key, value in updates.items():
            self.save_data["settings"][key] = value
    
    def add_gold(self, amount: int):
        """Add gold to player"""
        current_gold = self.save_data["player"].get("gold", 0)
        self.save_data["player"]["gold"] = current_gold + amount
        
        # Update statistics
        stats = self.save_data.get("statistics", {})
        stats["gold_earned"] = stats.get("gold_earned", 0) + amount
    
    def spend_gold(self, amount: int) -> bool:
        """Spend gold if player has enough"""
        current_gold = self.save_data["player"].get("gold", 0)
        if current_gold >= amount:
            self.save_data["player"]["gold"] = current_gold - amount
            return True
        return False
    
    def add_gems(self, amount: int):
        """Add gems to player"""
        current_gems = self.save_data["player"].get("gems", 0)
        self.save_data["player"]["gems"] = current_gems + amount
    
    def spend_gems(self, amount: int) -> bool:
        """Spend gems if player has enough"""
        current_gems = self.save_data["player"].get("gems", 0)
        if current_gems >= amount:
            self.save_data["player"]["gems"] = current_gems - amount
            
            # Update statistics
            stats = self.save_data.get("statistics", {})
            stats["gems_spent"] = stats.get("gems_spent", 0) + amount
            return True
        return False
    
    def update_stamina(self):
        """Update stamina based on time passed"""
        now = datetime.now().timestamp()
        last_update = self.save_data["player"].get("last_stamina_update", now)
        current_stamina = self.save_data["player"].get("stamina", 0)
        max_stamina = self.save_data["player"].get("max_stamina", GameConfig.MAX_STAMINA_DEFAULT)
        
        if current_stamina < max_stamina:
            time_passed = now - last_update
            stamina_to_add = int(time_passed // GameConfig.STAMINA_RECHARGE_TIME)
            
            if stamina_to_add > 0:
                new_stamina = min(current_stamina + stamina_to_add, max_stamina)
                self.save_data["player"]["stamina"] = new_stamina
                self.save_data["player"]["last_stamina_update"] = now
    
    def use_stamina(self, amount: int = 1) -> bool:
        """Use stamina if available"""
        current_stamina = self.save_data["player"].get("stamina", 0)
        if current_stamina >= amount:
            self.save_data["player"]["stamina"] = current_stamina - amount
            return True
        return False
    
    def complete_stage(self, world: int, stage: int, rewards: Dict[str, int]):
        """Mark stage as completed and add rewards"""
        stage_id = f"{world}_{stage}"
        completed_stages = self.save_data["progress"].get("stages_completed", [])
        
        if stage_id not in completed_stages:
            completed_stages.append(stage_id)
            self.save_data["progress"]["stages_completed"] = completed_stages
            self.save_data["progress"]["total_stages_completed"] += 1
        
        # Update highest stage reached
        total_stage = (world - 1) * GameConfig.STAGES_PER_WORLD + stage
        highest = self.save_data["progress"].get("highest_stage_reached", 1)
        self.save_data["progress"]["highest_stage_reached"] = max(highest, total_stage)
        
        # Add rewards
        if "gold" in rewards:
            self.add_gold(rewards["gold"])
        if "gems" in rewards:
            self.add_gems(rewards["gems"])
        if "experience" in rewards:
            self.add_experience(rewards["experience"])
    
    def add_experience(self, amount: int):
        """Add experience and handle level ups"""
        current_xp = self.save_data["player"].get("experience", 0)
        current_level = self.save_data["player"].get("level", 1)
        
        new_xp = current_xp + amount
        self.save_data["player"]["experience"] = new_xp
        
        # Check for level up
        xp_required = GameConfig.get_xp_requirement(current_level + 1)
        while new_xp >= xp_required and current_level < GameConfig.MAX_PLAYER_LEVEL:
            current_level += 1
            new_xp -= xp_required
            xp_required = GameConfig.get_xp_requirement(current_level + 1)
            
            # Level up benefits
            self._handle_level_up(current_level)
        
        self.save_data["player"]["level"] = current_level
        self.save_data["player"]["experience"] = new_xp
    
    def _handle_level_up(self, new_level: int):
        """Handle level up effects"""
        # Increase stats
        stats = self.save_data["player"]["stats"]
        stats["max_hp"] += 10
        stats["hp"] = stats["max_hp"]  # Full heal on level up
        stats["attack"] += 5
        stats["defense"] += 3
        stats["speed"] += 2
        
        print(f"Level up! Now level {new_level}")
    
    def unlock_skin(self, skin_id: str):
        """Unlock a character skin"""
        unlocked = self.save_data["player"].get("unlocked_skins", [])
        if skin_id not in unlocked:
            unlocked.append(skin_id)
            self.save_data["player"]["unlocked_skins"] = unlocked
    
    def unlock_weapon(self, weapon_id: str):
        """Unlock a weapon"""
        unlocked = self.save_data["player"].get("unlocked_weapons", [])
        if weapon_id not in unlocked:
            unlocked.append(weapon_id)
            self.save_data["player"]["unlocked_weapons"] = unlocked
    
    def get_daily_login_data(self) -> Dict[str, Any]:
        """Get daily login data"""
        return self.save_data.get("monetization", {}).get("daily_login", {})
    
    def update_daily_login(self) -> bool:
        """Update daily login streak and return if reward is available"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_data = self.save_data["monetization"]["daily_login"]
        last_login = daily_data.get("last_login", "")
        
        if last_login != today:
            # Check if streak continues
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            if last_login == yesterday:
                daily_data["streak"] += 1
            else:
                daily_data["streak"] = 1
            
            daily_data["last_login"] = today
            return True  # Reward available
        
        return False  # Already logged in today
    
    def export_save_data(self) -> str:
        """Export save data for cloud save or transfer"""
        return json.dumps(self.save_data, indent=2)
    
    def import_save_data(self, data_str: str) -> bool:
        """Import save data from string"""
        try:
            imported_data = json.loads(data_str)
            if self._verify_save_data(imported_data):
                self.save_data = imported_data
                self.save_data_to_file()
                return True
        except:
            pass
        return False
    
    def reset_save_data(self):
        """Reset all save data to defaults"""
        self.save_data = self.default_save_data.copy()
        self._initialize_new_save()
        self.save_data_to_file()