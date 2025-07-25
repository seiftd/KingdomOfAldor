"""
Kingdom of Aldoria - Game Configuration
Contains all game settings, constants, and balance values
"""

import os
import json
from enum import Enum

class Difficulty(Enum):
    """Game difficulty levels"""
    EASY = 0.8
    NORMAL = 1.0
    HARD = 1.2
    NIGHTMARE = 1.5

class GameConfig:
    """Main game configuration class"""
    
    # Display Settings
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    VSYNC = True
    
    # Mobile Optimizations
    TEXTURE_QUALITY = "high"  # high, medium, low
    PARTICLE_DENSITY = 1.0
    AUDIO_QUALITY = "high"
    
    # Game Balance
    MAX_STAMINA_DEFAULT = 10
    MAX_STAMINA_WEEKLY = 20
    MAX_STAMINA_MONTHLY = 25
    STAMINA_RECHARGE_TIME = 20 * 60  # 20 minutes in seconds
    
    # World Configuration
    TOTAL_WORLDS = 10
    STAGES_PER_WORLD = 30
    BOSS_INTERVAL = 5  # Boss every 5 stages
    
    # Currency
    GEMS_PER_AD = 3
    MAX_ADS_PER_DAY = 30
    GEMS_FROM_ADS_DAILY = 90  # 30 ads * 3 gems
    
    # Subscription Benefits
    WEEKLY_SUB_GEMS_DAILY = 25
    MONTHLY_SUB_GEMS_DAILY = 40
    WEEKLY_SUB_PRICE = 4.99
    MONTHLY_SUB_PRICE = 15.99
    
    # Player Progression
    BASE_XP_REQUIREMENT = 100
    XP_SCALING_FACTOR = 1.15
    MAX_PLAYER_LEVEL = 100
    
    # Combat System
    BASE_DAMAGE = 100
    DAMAGE_SCALING = 1.1
    BOSS_HP_MULTIPLIER = 5.0
    BOSS_DAMAGE_MULTIPLIER = 1.5
    
    # Skill System
    SKILL_COOLDOWNS = {
        "speed_boost": 30.0,     # seconds
        "instant_heal": 60.0,
        "time_rewind": 120.0,
        "damage_doubler": 90.0
    }
    
    SKILL_DURATIONS = {
        "speed_boost": 5.0,      # seconds
        "damage_doubler": 7.0,
        "time_rewind": 3.0,      # rewind window
        "instant_heal": 0.0      # instant effect
    }
    
    # File Paths
    SAVE_FILE = "save_data.json"
    CONFIG_FILE = "game_config.json"
    ASSETS_PATH = "assets"
    
    # World Names and Themes
    WORLD_DATA = {
        1: {
            "name": "Forest of Shadows",
            "theme": "forest",
            "description": "Ancient woods filled with mystical creatures",
            "unlock_requirement": 0
        },
        2: {
            "name": "Desert of Souls",
            "theme": "desert", 
            "description": "Endless sands hiding ancient secrets",
            "unlock_requirement": 30
        },
        3: {
            "name": "Ice Peaks",
            "theme": "ice",
            "description": "Frozen mountains of eternal winter",
            "unlock_requirement": 60
        },
        4: {
            "name": "Volcanic Wastes",
            "theme": "volcano",
            "description": "Burning lands of molten rock",
            "unlock_requirement": 90
        },
        5: {
            "name": "Mystic Swamps",
            "theme": "swamp",
            "description": "Treacherous wetlands of dark magic",
            "unlock_requirement": 120
        },
        6: {
            "name": "Crystal Caverns",
            "theme": "cave",
            "description": "Underground realm of precious gems",
            "unlock_requirement": 150
        },
        7: {
            "name": "Sky Citadel",
            "theme": "sky",
            "description": "Floating islands in the clouds",
            "unlock_requirement": 180
        },
        8: {
            "name": "Dark Kingdom",
            "theme": "dark",
            "description": "Realm of shadows and nightmares",
            "unlock_requirement": 210
        },
        9: {
            "name": "Light Fortress",
            "theme": "light",
            "description": "Bastion of divine radiance",
            "unlock_requirement": 240
        },
        10: {
            "name": "Void Nexus",
            "theme": "void",
            "description": "The final battleground between worlds",
            "unlock_requirement": 270
        }
    }
    
    # Character Skins with Special Abilities
    CHARACTER_SKINS = {
        "default_knight": {
            "name": "Knight Arin",
            "description": "The default brave knight",
            "skill": None,
            "unlock_cost": 0,
            "rarity": "common"
        },
        "forest_scout": {
            "name": "Forest Scout",
            "description": "Ranger in green cloak with speed mastery",
            "skill": "speed_boost",
            "unlock_cost": 500,
            "rarity": "rare"
        },
        "desert_nomad": {
            "name": "Desert Nomad",
            "description": "Warrior with healing knowledge",
            "skill": "instant_heal",
            "unlock_cost": 800,
            "rarity": "epic"
        },
        "void_knight": {
            "name": "Void Knight",
            "description": "Dark knight with time manipulation",
            "skill": "time_rewind",
            "unlock_cost": 1200,
            "rarity": "legendary"
        },
        "solar_paladin": {
            "name": "Solar Paladin",
            "description": "Divine warrior with damage amplification",
            "skill": "damage_doubler",
            "unlock_cost": 1000,
            "rarity": "epic"
        }
    }
    
    # Weapon System
    WEAPON_DATA = {
        "bronze_sword": {
            "name": "Bronze Sword",
            "damage": 100,
            "description": "A simple but reliable blade",
            "rarity": "common",
            "unlock_cost": 0
        },
        "iron_blade": {
            "name": "Iron Blade", 
            "damage": 150,
            "description": "Sturdy iron forged weapon",
            "rarity": "common",
            "unlock_cost": 200
        },
        "mystic_saber": {
            "name": "Mystic Saber",
            "damage": 200,
            "description": "Enchanted blade with magical properties",
            "rarity": "rare",
            "unlock_cost": 500
        },
        "void_scythe": {
            "name": "Void Scythe",
            "damage": 300,
            "description": "Cosmic weapon from the void realm",
            "rarity": "epic",
            "unlock_cost": 1000
        },
        "solar_flare_sword": {
            "name": "Solar Flare Sword",
            "damage": 400,
            "description": "Golden blade burning with solar energy",
            "rarity": "legendary",
            "unlock_cost": 2000
        }
    }
    
    # Enemy Types per World
    ENEMY_DATA = {
        1: ["shadow_wolf", "forest_goblin", "dark_sprite"],
        2: ["sand_scorpion", "desert_bandit", "sand_pharaoh"],
        3: ["ice_troll", "frost_elemental", "ice_yeti"],
        4: ["lava_beast", "fire_demon", "magma_golem"],
        5: ["swamp_witch", "poison_frog", "bog_monster"],
        6: ["crystal_spider", "gem_guardian", "cave_dragon"],
        7: ["wind_spirit", "cloud_giant", "sky_serpent"],
        8: ["shadow_knight", "dark_mage", "nightmare_beast"],
        9: ["light_guardian", "radiant_angel", "holy_dragon"],
        10: ["void_creature", "chaos_lord", "reality_breaker"]
    }
    
    # Localization Support
    SUPPORTED_LANGUAGES = ["en", "ar", "fr"]
    DEFAULT_LANGUAGE = "en"
    
    # Audio Settings
    MASTER_VOLUME = 0.7
    MUSIC_VOLUME = 0.5
    SFX_VOLUME = 0.8
    
    # Performance Settings
    MAX_PARTICLES = 100
    MAX_ENEMIES_ON_SCREEN = 10
    TEXTURE_CACHE_SIZE = 50
    
    # Ad Configuration
    AD_NETWORKS = {
        "admob": {
            "app_id": "ca-app-pub-test~test",
            "banner_id": "ca-app-pub-test/test-banner",
            "interstitial_id": "ca-app-pub-test/test-interstitial",
            "rewarded_id": "ca-app-pub-test/test-rewarded"
        }
    }
    
    @classmethod
    def load_custom_config(cls, config_path=None):
        """Load custom configuration from JSON file"""
        if config_path is None:
            config_path = cls.CONFIG_FILE
            
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    custom_config = json.load(f)
                    
                # Update class attributes with custom values
                for key, value in custom_config.items():
                    if hasattr(cls, key):
                        setattr(cls, key, value)
                        
            except Exception as e:
                print(f"Failed to load custom config: {e}")
    
    @classmethod
    def save_config(cls, config_path=None):
        """Save current configuration to JSON file"""
        if config_path is None:
            config_path = cls.CONFIG_FILE
            
        # Collect all class attributes that are configuration values
        config_data = {}
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and not callable(getattr(cls, attr_name)):
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, (int, float, str, bool, list, dict)):
                    config_data[attr_name] = attr_value
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    @classmethod
    def get_enemy_hp(cls, world, stage, player_level):
        """Calculate enemy HP based on world, stage, and player level"""
        base_hp = 100
        world_multiplier = 1 + (world - 1) * 0.3
        stage_multiplier = 1 + (stage - 1) * 0.05
        level_multiplier = 1 + (player_level - 1) * 0.02
        
        return int(base_hp * world_multiplier * stage_multiplier * level_multiplier)
    
    @classmethod
    def get_enemy_damage(cls, world, stage, player_level):
        """Calculate enemy damage based on world, stage, and player level"""
        base_damage = 50
        world_multiplier = 1 + (world - 1) * 0.25
        stage_multiplier = 1 + (stage - 1) * 0.03
        level_multiplier = 1 + (player_level - 1) * 0.015
        
        return int(base_damage * world_multiplier * stage_multiplier * level_multiplier)
    
    @classmethod
    def get_xp_requirement(cls, level):
        """Calculate XP required for a specific level"""
        return int(cls.BASE_XP_REQUIREMENT * (cls.XP_SCALING_FACTOR ** (level - 1)))
    
    @classmethod
    def get_stage_reward_gold(cls, world, stage):
        """Calculate gold reward for completing a stage"""
        base_gold = 10
        world_bonus = world * 5
        stage_bonus = stage * 2
        return base_gold + world_bonus + stage_bonus
    
    @classmethod
    def get_stage_reward_xp(cls, world, stage):
        """Calculate XP reward for completing a stage"""
        base_xp = 25
        world_bonus = world * 10
        stage_bonus = stage * 3
        return base_xp + world_bonus + stage_bonus