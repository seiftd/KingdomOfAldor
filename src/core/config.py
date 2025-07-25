"""
Kingdom of Aldoria - Enhanced Game Configuration
Contains all game constants, settings, and configuration parameters
"""

import pygame
from pathlib import Path

class Config:
    """Main configuration class for Kingdom of Aldoria"""

    # Game Info
    GAME_TITLE = "Kingdom of Aldoria"
    VERSION = "1.0.0"
    DEBUG = True  # Set to False for production

    # Screen Settings
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    FULLSCREEN = False

    # Colors (RGB)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)

    # UI Colors
    UI_BACKGROUND = (25, 25, 35)
    UI_PANEL = (45, 45, 55)
    UI_BUTTON = (70, 70, 80)
    UI_BUTTON_HOVER = (90, 90, 100)
    UI_TEXT = (255, 255, 255)
    UI_TEXT_SECONDARY = (180, 180, 180)
    UI_ACCENT = (100, 200, 255)
    UI_SUCCESS = (100, 255, 100)
    UI_WARNING = (255, 200, 100)
    UI_ERROR = (255, 100, 100)

    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    ASSETS_DIR = BASE_DIR / "assets"
    SPRITES_DIR = ASSETS_DIR / "sprites"
    AUDIO_DIR = ASSETS_DIR / "audio"
    UI_DIR = ASSETS_DIR / "ui"
    WORLDS_DIR = ASSETS_DIR / "worlds"
    SAVE_DIR = BASE_DIR / "saves"

    # Game Balance
    MAX_STAMINA_DEFAULT = 10
    STAMINA_RECHARGE_MINUTES = 20
    STAMINA_PER_STAGE = 1

    # Currency
    GEMS_PER_AD = 3
    MAX_ADS_PER_DAY = 30
    GOLD_TO_GEM_RATIO = 100  # 100 gold = 1 gem

    # Enhanced Ad System
    AD_REWARD_GEMS_MIN = 1
    AD_REWARD_GEMS_MAX = 5
    AD_REWARD_GOLD_MIN = 50
    AD_REWARD_GOLD_MAX = 200
    AD_SOURCES = [
        "AdMob", "Unity Ads", "AppLovin", "IronSource", "Vungle",
        "Facebook Audience Network", "TikTok Ads", "Chartboost"
    ]
    AD_DAILY_LIMIT_DEFAULT = 30
    AD_DAILY_LIMIT_VIP = 50
    AD_COOLDOWN_SECONDS = 30

    # Subscription Benefits
    WEEKLY_SUB_GEMS_PER_DAY = 25
    WEEKLY_SUB_MAX_STAMINA = 20
    MONTHLY_SUB_GEMS_PER_DAY = 40
    MONTHLY_SUB_MAX_STAMINA = 25

    # Pricing (USD)
    WEEKLY_SUB_PRICE = 4.99
    MONTHLY_SUB_PRICE = 15.99
    STARTER_PACK_PRICE = 0.99
    LEGENDARY_ITEM_PRICE_MIN = 3.99
    LEGENDARY_ITEM_PRICE_MAX = 14.99

    # World Settings
    WORLDS_COUNT = 10
    STAGES_PER_WORLD = 30
    BOSS_STAGE_INTERVAL = 5

    # World Names
    WORLD_NAMES = [
        "Forest of Shadows",
        "Desert of Souls",
        "Ice Peaks",
        "Dark Kingdom",
        "Light Fortress",
        "Mountain Realm",
        "Ocean Depths",
        "Sky Citadel",
        "Underground Caves",
        "Volcanic Wasteland"
    ]

    # Player Settings
    PLAYER_START_LEVEL = 1
    PLAYER_START_HP = 100
    PLAYER_START_ATTACK = 10
    PLAYER_START_DEFENSE = 5
    PLAYER_START_SPEED = 8

    # Progression
    XP_PER_LEVEL = 100  # Base XP required for level 2
    STAT_INCREASE_PER_LEVEL = 0.05  # 5% increase per level

    # Enhanced Heroes System
    HEROES = {
        "knight_arin": {
            "name": "Knight Arin",
            "rarity": "common",
            "base_hp": 100,
            "base_attack": 10,
            "base_defense": 8,
            "skill": "Divine Strike",
            "unlock_type": "default"
        },
        "forest_scout": {
            "name": "Forest Scout",
            "rarity": "common",
            "base_hp": 80,
            "base_attack": 12,
            "base_defense": 6,
            "skill": "Speed Boost",
            "unlock_type": "gems",
            "cost": 100
        },
        "desert_nomad": {
            "name": "Desert Nomad",
            "rarity": "uncommon",
            "base_hp": 90,
            "base_attack": 11,
            "base_defense": 7,
            "skill": "Sand Storm",
            "unlock_type": "gems",
            "cost": 250
        },
        "void_knight": {
            "name": "Void Knight",
            "rarity": "epic",
            "base_hp": 120,
            "base_attack": 15,
            "base_defense": 12,
            "skill": "Time Rewind",
            "unlock_type": "payment_only",
            "cost": 9.99
        },
        "dragon_slayer": {
            "name": "Dragon Slayer",
            "rarity": "legendary",
            "base_hp": 150,
            "base_attack": 20,
            "base_defense": 15,
            "skill": "Dragon Fury",
            "unlock_type": "payment_only",
            "cost": 19.99
        },
        "celestial_mage": {
            "name": "Celestial Mage",
            "rarity": "legendary",
            "base_hp": 100,
            "base_attack": 25,
            "base_defense": 10,
            "skill": "Meteor Strike",
            "unlock_type": "payment_only",
            "cost": 24.99
        },
        "shadow_assassin": {
            "name": "Shadow Assassin",
            "rarity": "epic",
            "base_hp": 80,
            "base_attack": 18,
            "base_defense": 8,
            "skill": "Shadow Clone",
            "unlock_type": "gems",
            "cost": 500
        },
        "ice_queen": {
            "name": "Ice Queen",
            "rarity": "legendary",
            "base_hp": 130,
            "base_attack": 22,
            "base_defense": 14,
            "skill": "Frozen Time",
            "unlock_type": "payment_only",
            "cost": 29.99
        }
    }

    # Enhanced Weapons System
    WEAPONS = {
        "bronze_sword": {
            "name": "Bronze Sword",
            "rarity": "common",
            "attack": 5,
            "special": "None",
            "unlock_type": "default"
        },
        "iron_blade": {
            "name": "Iron Blade",
            "rarity": "common",
            "attack": 8,
            "special": "Critical +5%",
            "unlock_type": "gold",
            "cost": 500
        },
        "silver_sword": {
            "name": "Silver Sword",
            "rarity": "uncommon",
            "attack": 12,
            "special": "Undead Damage +50%",
            "unlock_type": "gems",
            "cost": 50
        },
        "void_scythe": {
            "name": "Void Scythe",
            "rarity": "epic",
            "attack": 18,
            "special": "Dark Energy Drain",
            "unlock_type": "gems",
            "cost": 200
        },
        "solar_flare_sword": {
            "name": "Solar Flare Sword",
            "rarity": "epic",
            "attack": 20,
            "special": "Fire Damage +100%",
            "unlock_type": "payment_only",
            "cost": 7.99
        },
        "excalibur": {
            "name": "Excalibur",
            "rarity": "legendary",
            "attack": 30,
            "special": "Holy Light +200%",
            "unlock_type": "payment_only",
            "cost": 14.99
        },
        "dragon_fang": {
            "name": "Dragon Fang",
            "rarity": "legendary",
            "attack": 35,
            "special": "Dragon Slayer +300%",
            "unlock_type": "payment_only",
            "cost": 19.99
        },
        "cosmic_blade": {
            "name": "Cosmic Blade",
            "rarity": "legendary",
            "attack": 40,
            "special": "Reality Tear",
            "unlock_type": "payment_only",
            "cost": 24.99
        },
        "infinity_edge": {
            "name": "Infinity Edge",
            "rarity": "mythic",
            "attack": 50,
            "special": "Infinite Power",
            "unlock_type": "payment_only",
            "cost": 49.99
        }
    }

    # Enhanced Skins System
    SKINS = {
        "default": {
            "name": "Default Knight",
            "rarity": "common",
            "bonus": "None",
            "unlock_type": "default"
        },
        "forest_guardian": {
            "name": "Forest Guardian",
            "rarity": "uncommon",
            "bonus": "Nature Resistance +25%",
            "unlock_type": "gems",
            "cost": 75
        },
        "desert_warrior": {
            "name": "Desert Warrior",
            "rarity": "uncommon",
            "bonus": "Heat Resistance +25%",
            "unlock_type": "gems",
            "cost": 75
        },
        "ice_champion": {
            "name": "Ice Champion",
            "rarity": "rare",
            "bonus": "Cold Immunity",
            "unlock_type": "gems",
            "cost": 150
        },
        "void_lord": {
            "name": "Void Lord",
            "rarity": "epic",
            "bonus": "Dark Magic +50%",
            "unlock_type": "payment_only",
            "cost": 4.99
        },
        "golden_emperor": {
            "name": "Golden Emperor",
            "rarity": "legendary",
            "bonus": "Gold Gain +100%",
            "unlock_type": "payment_only",
            "cost": 9.99
        },
        "celestial_avatar": {
            "name": "Celestial Avatar",
            "rarity": "legendary",
            "bonus": "All Stats +25%",
            "unlock_type": "payment_only",
            "cost": 14.99
        },
        "dragon_emperor": {
            "name": "Dragon Emperor",
            "rarity": "legendary",
            "bonus": "Dragon Powers",
            "unlock_type": "payment_only",
            "cost": 19.99
        },
        "cosmic_overlord": {
            "name": "Cosmic Overlord",
            "rarity": "mythic",
            "bonus": "Reality Control",
            "unlock_type": "payment_only",
            "cost": 39.99
        }
    }

    # Premium Legendary Skins (Payment Only)
    SKINS = {
        "default": {
            "name": "Default Knight",
            "rarity": "common",
            "bonus": "None",
            "unlock_type": "default"
        },
        "forest_guardian": {
            "name": "Forest Guardian",
            "rarity": "uncommon",
            "bonus": "Nature Resistance +25%",
            "unlock_type": "gems",
            "cost": 75
        },
        "desert_warrior": {
            "name": "Desert Warrior",
            "rarity": "uncommon",
            "bonus": "Heat Resistance +25%",
            "unlock_type": "gems",
            "cost": 75
        },
        "ice_champion": {
            "name": "Ice Champion",
            "rarity": "rare",
            "bonus": "Cold Immunity",
            "unlock_type": "gems",
            "cost": 150
        },
        "void_lord": {
            "name": "Void Lord",
            "rarity": "epic",
            "bonus": "Dark Magic +50%",
            "unlock_type": "payment_only",
            "cost": 4.99
        },
        "golden_emperor": {
            "name": "Golden Emperor",
            "rarity": "legendary",
            "bonus": "Gold Gain +100%",
            "unlock_type": "payment_only",
            "cost": 9.99
        },
        "celestial_avatar": {
            "name": "Celestial Avatar",
            "rarity": "legendary",
            "bonus": "All Stats +25%",
            "unlock_type": "payment_only",
            "cost": 14.99
        },
        "dragon_emperor": {
            "name": "Dragon Emperor",
            "rarity": "legendary",
            "bonus": "Dragon Powers",
            "unlock_type": "payment_only",
            "cost": 19.99
        },
        "cosmic_overlord": {
            "name": "Cosmic Overlord",
            "rarity": "mythic",
            "bonus": "Reality Control",
            "unlock_type": "payment_only",
            "cost": 39.99
        },
        "dragon_knight": {
            "name": "Dragon Knight Arin",
            "description": "Legendary dragon-forged armor with fire immunity",
            "rarity": "legendary",
            "price": 2500,  # Gems only
            "currency": "gems",
            "payment_only": True,
            "skills": ["fire_immunity", "dragon_breath", "flame_aura"],
            "stats_bonus": {"attack": 50, "defense": 40, "speed": 30, "health": 100}
        },
        "shadow_assassin": {
            "name": "Shadow Assassin Arin",
            "description": "Master of stealth and critical strikes",
            "rarity": "legendary",
            "price": 2200,
            "currency": "gems",
            "payment_only": True,
            "skills": ["stealth", "critical_master", "shadow_clone"],
            "stats_bonus": {"attack": 60, "defense": 20, "speed": 70, "health": 50}
        },
        "arcane_mage": {
            "name": "Arcane Mage Arin",
            "description": "Wielder of ancient magical powers",
            "rarity": "legendary",
            "price": 2800,
            "currency": "gems",
            "payment_only": True,
            "skills": ["mana_shield", "arcane_blast", "time_stop"],
            "stats_bonus": {"attack": 80, "defense": 35, "speed": 45, "health": 75}
        },
        "celestial_guardian": {
            "name": "Celestial Guardian Arin",
            "description": "Blessed by the gods themselves",
            "rarity": "legendary",
            "price": 3000,
            "currency": "gems",
            "payment_only": True,
            "skills": ["divine_protection", "healing_aura", "celestial_strike"],
            "stats_bonus": {"attack": 45, "defense": 60, "speed": 35, "health": 120}
        },
        "void_reaper": {
            "name": "Void Reaper Arin",
            "description": "Harvester of souls from the void realm",
            "rarity": "legendary",
            "price": 2600,
            "currency": "gems",
            "payment_only": True,
            "skills": ["soul_drain", "void_step", "death_mark"],
            "stats_bonus": {"attack": 70, "defense": 30, "speed": 55, "health": 80}
        }
    }

    # New Heroes (Additional Characters)
    HEROES = {
        "arin": {
            "name": "Knight Arin",
            "description": "Brave knight of Aldoria",
            "base_stats": {"attack": 100, "defense": 80, "speed": 60, "health": 200},
            "unlock_cost": 0,
            "rarity": "common"
        },
        # Premium Legendary Heroes (Payment Only)
        "seraphina": {
            "name": "Princess Seraphina",
            "description": "Royal mage with divine powers",
            "base_stats": {"attack": 120, "defense": 90, "speed": 70, "health": 180},
            "unlock_cost": 3500,
            "currency": "gems",
            "rarity": "legendary",
            "payment_only": True,
            "special_abilities": ["royal_decree", "divine_intervention", "mana_overflow"]
        },
        "thorven": {
            "name": "Thorven the Berserker",
            "description": "Fierce warrior from the northern clans",
            "base_stats": {"attack": 150, "defense": 70, "speed": 50, "health": 250},
            "unlock_cost": 3200,
            "currency": "gems",
            "rarity": "legendary",
            "payment_only": True,
            "special_abilities": ["berserker_rage", "intimidating_roar", "weapon_mastery"]
        },
        "luna": {
            "name": "Luna Shadowblade",
            "description": "Master assassin of the thieves guild",
            "base_stats": {"attack": 130, "defense": 60, "speed": 100, "health": 160},
            "unlock_cost": 2800,
            "currency": "gems",
            "rarity": "legendary",
            "payment_only": True,
            "special_abilities": ["stealth_mastery", "poison_blade", "shadow_step"]
        },
        "magnus": {
            "name": "Archmage Magnus",
            "description": "Ancient wizard with forbidden knowledge",
            "base_stats": {"attack": 90, "defense": 50, "speed": 40, "health": 140},
            "unlock_cost": 4000,
            "currency": "gems",
            "rarity": "legendary",
            "payment_only": True,
            "special_abilities": ["forbidden_magic", "spell_amplify", "mana_manipulation"]
        }
    }

    # Enhanced Weapons System
    WEAPONS = {
        "bronze_sword": {
            "name": "Bronze Sword",
            "rarity": "common",
            "attack": 5,
            "special": "None",
            "unlock_type": "default"
        },
        "iron_blade": {
            "name": "Iron Blade",
            "rarity": "common",
            "attack": 8,
            "special": "Critical +5%",
            "unlock_type": "gold",
            "cost": 500
        },
        "silver_sword": {
            "name": "Silver Sword",
            "rarity": "uncommon",
            "attack": 12,
            "special": "Undead Damage +50%",
            "unlock_type": "gems",
            "cost": 50
        },
        "void_scythe": {
            "name": "Void Scythe",
            "rarity": "epic",
            "attack": 18,
            "special": "Dark Energy Drain",
            "unlock_type": "gems",
            "cost": 200
        },
        "solar_flare_sword": {
            "name": "Solar Flare Sword",
            "rarity": "epic",
            "attack": 20,
            "special": "Fire Damage +100%",
            "unlock_type": "payment_only",
            "cost": 7.99
        },
        "excalibur": {
            "name": "Excalibur",
            "rarity": "legendary",
            "attack": 30,
            "special": "Holy Light +200%",
            "unlock_type": "payment_only",
            "cost": 14.99
        },
        "dragon_fang": {
            "name": "Dragon Fang",
            "rarity": "legendary",
            "attack": 35,
            "special": "Dragon Slayer +300%",
            "unlock_type": "payment_only",
            "cost": 19.99
        },
        "cosmic_blade": {
            "name": "Cosmic Blade",
            "rarity": "legendary",
            "attack": 40,
            "special": "Reality Tear",
            "unlock_type": "payment_only",
            "cost": 24.99
        },
        "infinity_edge": {
            "name": "Infinity Edge",
            "rarity": "mythic",
            "attack": 50,
            "special": "Infinite Power",
            "unlock_type": "payment_only",
            "cost": 49.99
        },
        "dragonslayer": {
            "name": "Dragonslayer Greatsword",
            "description": "Forged from dragon scales and meteoric steel",
            "attack": 200,
            "rarity": "legendary",
            "price": 3000,
            "currency": "gems",
            "payment_only": True,
            "special_effects": ["dragon_bane", "fire_damage", "critical_surge"]
        },
        "voidcutter": {
            "name": "Voidcutter Blade",
            "description": "Cuts through reality itself",
            "attack": 180,
            "rarity": "legendary",
            "price": 2700,
            "currency": "gems",
            "payment_only": True,
            "special_effects": ["void_slice", "armor_pierce", "dimensional_cut"]
        },
        "stormbreaker": {
            "name": "Stormbreaker Hammer",
            "description": "Channels the power of thunder and lightning",
            "attack": 220,
            "rarity": "legendary",
            "price": 3200,
            "currency": "gems",
            "payment_only": True,
            "special_effects": ["lightning_strike", "thunder_crash", "storm_aura"]
        },
        "soulreaper": {
            "name": "Soulreaper Scythe",
            "description": "Harvests the essence of fallen enemies",
            "attack": 190,
            "rarity": "legendary",
            "price": 2900,
            "currency": "gems",
            "payment_only": True,
            "special_effects": ["soul_harvest", "life_steal", "death_mark"]
        },
        "celestial_bow": {
            "name": "Celestial Longbow",
            "description": "Blessed by the moon and stars",
            "attack": 160,
            "rarity": "legendary",
            "price": 2500,
            "currency": "gems",
            "payment_only": True,
            "special_effects": ["star_shot", "lunar_blessing", "infinite_arrows"]
        },
        "frostmourne": {
            "name": "Frostmourne",
            "description": "Cursed blade that freezes the soul",
            "attack": 210,
            "rarity": "legendary",
            "price": 3100,
            "currency": "gems",
            "payment_only": True,
            "special_effects": ["frost_damage", "soul_freeze", "undead_command"]
        }
    }

    # Skills
    SKILL_SPEED_BOOST_DURATION = 5.0  # seconds
    SKILL_HEAL_PERCENTAGE = 0.30  # 30% of max HP
    SKILL_DAMAGE_DOUBLE_DURATION = 7.0  # seconds
    SKILL_COOLDOWN_BASE = 30.0  # seconds

    # Combat
    TURN_DURATION = 2.0  # seconds per turn
    CRITICAL_HIT_CHANCE = 0.15  # 15%
    CRITICAL_HIT_MULTIPLIER = 1.5

    # Enemy Scaling
    ENEMY_POWER_SCALE_PER_STAGE = 1.10  # 10% increase per stage
    BOSS_POWER_MULTIPLIER = 2.5

    # Audio
    MASTER_VOLUME = 0.7
    MUSIC_VOLUME = 0.5
    SFX_VOLUME = 0.8

    # Animation
    SPRITE_ANIMATION_SPEED = 0.1  # seconds per frame
    UI_ANIMATION_SPEED = 0.05

    # File Formats
    IMAGE_FORMAT = "webp"
    AUDIO_FORMAT = "ogg"

    # Localization
    DEFAULT_LANGUAGE = "en"
    SUPPORTED_LANGUAGES = ["en", "ar", "fr"]

    # Save System
    SAVE_VERSION = "1.0"
    AUTO_SAVE_INTERVAL = 30  # seconds

    # Performance
    MAX_PARTICLES = 100
    MAX_SOUNDS_CONCURRENT = 8
    ASSET_CACHE_SIZE = 50  # MB

    # Network
    CONNECTION_TIMEOUT = 10  # seconds
    RETRY_ATTEMPTS = 3

    # Enhanced Ad System Configuration
    ADS_CONFIG = {
        "enabled": True,
        "max_daily_ads": 20,  # Can be upgraded
        "max_rewarded_ads": 15,  # Can be upgraded
        "max_interstitial_ads": 10,  # Can be upgraded
        "ad_cooldown": 30,  # seconds between ads
        "gem_reward_per_ad": 10,  # base gems per rewarded ad
        "bonus_multiplier": 1.0,  # can be upgraded

        # Ad Networks Configuration
        "networks": {
            "primary": {
                "name": "AdMob",
                "app_id": "ca-app-pub-1234567890123456~1234567890",
                "rewarded_unit_id": "ca-app-pub-1234567890123456/1234567890",
                "interstitial_unit_id": "ca-app-pub-1234567890123456/0987654321",
                "banner_unit_id": "ca-app-pub-1234567890123456/1122334455",
                "enabled": True,
                "priority": 1
            },
            "secondary": {
                "name": "Unity Ads",
                "game_id": "1234567",
                "rewarded_placement": "rewardedVideo",
                "interstitial_placement": "video",
                "enabled": True,
                "priority": 2
            },
            "tertiary": {
                "name": "IronSource",
                "app_key": "abcdefgh",
                "enabled": False,
                "priority": 3
            }
        },

        # Upgrade Levels
        "upgrades": {
            "daily_limit": {
                "level_1": {"cost": 500, "currency": "gems", "max_ads": 25},
                "level_2": {"cost": 1000, "currency": "gems", "max_ads": 30},
                "level_3": {"cost": 2000, "currency": "gems", "max_ads": 40},
                "level_4": {"cost": 3500, "currency": "gems", "max_ads": 50}
            },
            "gem_multiplier": {
                "level_1": {"cost": 800, "currency": "gems", "multiplier": 1.5},
                "level_2": {"cost": 1500, "currency": "gems", "multiplier": 2.0},
                "level_3": {"cost": 2500, "currency": "gems", "multiplier": 2.5},
                "level_4": {"cost": 4000, "currency": "gems", "multiplier": 3.0}
            }
        }
    }

    # Dashboard Configuration
    DASHBOARD_CONFIG = {
        "admin_email": "seiftouatilol@gmail.com",
        "admin_password": "seif0662",  # In production, this should be hashed
        "session_timeout": 3600,  # 1 hour in seconds
        "max_login_attempts": 5,
        "lockout_duration": 900,  # 15 minutes in seconds
        "analytics_retention_days": 90,
        "backup_frequency_hours": 24
    }

class GameStates:
    """Game state constants"""
    LOADING = "loading"
    MAIN_MENU = "main_menu"
    WORLD_MAP = "world_map"
    BATTLE = "battle"
    SHOP = "shop"
    INVENTORY = "inventory"
    SETTINGS = "settings"
    PAUSE = "pause"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class SkillTypes:
    """Player skill types"""
    SPEED_BOOST = "speed_boost"
    INSTANT_HEAL = "instant_heal"
    TIME_REWIND = "time_rewind"
    DAMAGE_DOUBLER = "damage_doubler"

class ItemTypes:
    """Item classification"""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    MATERIAL = "material"

class Rarities:
    """Item rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"

class CurrencyTypes:
    """Currency types"""
    GOLD = "gold"
    GEMS = "gems"

class AdTypes:
    """Advertisement types"""
    REWARDED = "rewarded"
    INTERSTITIAL = "interstitial"
    BANNER = "banner"

class EnemyTypes:
    """Enemy classifications"""
    NORMAL = "normal"
    ELITE = "elite"
    BOSS = "boss"
    MINI_BOSS = "mini_boss"

# Premium Heroes (Gems/Payment Only)
PREMIUM_HEROES = {
    "shadow_assassin": {
        "name": "Shadow Assassin",
        "description": "Master of stealth and critical strikes",
        "rarity": Rarities.LEGENDARY,
        "cost": 2500,
        "currency": CurrencyTypes.GEMS,
        "stats": {"attack": 85, "defense": 60, "speed": 95, "health": 180},
        "special_skill": "Shadow Strike",
        "skill_description": "Deal 300% damage and become invisible for 2 turns"
    },
    "arcane_mage": {
        "name": "Arcane Mage",
        "description": "Wielder of ancient magical powers",
        "rarity": Rarities.LEGENDARY,
        "cost": 3000,
        "currency": CurrencyTypes.GEMS,
        "stats": {"attack": 95, "defense": 50, "speed": 75, "health": 160},
        "special_skill": "Arcane Blast",
        "skill_description": "Deal massive AoE damage to all enemies"
    },
    "dragon_knight": {
        "name": "Dragon Knight",
        "description": "Elite warrior blessed by dragons",
        "rarity": Rarities.LEGENDARY,
        "cost": 4000,
        "currency": CurrencyTypes.GEMS,
        "stats": {"attack": 90, "defense": 95, "speed": 70, "health": 250},
        "special_skill": "Dragon's Fury",
        "skill_description": "Summon dragon fire for massive damage"
    },
    "celestial_guardian": {
        "name": "Celestial Guardian",
        "description": "Divine protector from the heavens",
        "rarity": Rarities.LEGENDARY,
        "cost": 5000,
        "currency": CurrencyTypes.GEMS,
        "stats": {"attack": 80, "defense": 100, "speed": 80, "health": 300},
        "special_skill": "Divine Shield",
        "skill_description": "Grant immunity to all allies for 3 turns"
    }
}

# Premium Weapons (Gems/Payment Only)
PREMIUM_WEAPONS = {
    "excalibur": {
        "name": "Excalibur",
        "description": "The legendary sword of kings",
        "rarity": Rarities.LEGENDARY,
        "cost": 3500,
        "currency": CurrencyTypes.GEMS,
        "attack_bonus": 150,
        "special_effect": "30% chance to deal double damage"
    },
    "scythe_of_souls": {
        "name": "Scythe of Souls",
        "description": "Harvests the essence of enemies",
        "rarity": Rarities.LEGENDARY,
        "cost": 4000,
        "currency": CurrencyTypes.GEMS,
        "attack_bonus": 180,
        "special_effect": "Heal 20% of damage dealt"
    },
    "storm_hammer": {
        "name": "Storm Hammer",
        "description": "Channels the power of thunder",
        "rarity": Rarities.LEGENDARY,
        "cost": 3000,
        "currency": CurrencyTypes.GEMS,
        "attack_bonus": 140,
        "special_effect": "Lightning chains to nearby enemies"
    },
    "void_blade": {
        "name": "Void Blade",
        "description": "Cuts through reality itself",
        "rarity": Rarities.LEGENDARY,
        "cost": 4500,
        "currency": CurrencyTypes.GEMS,
        "attack_bonus": 200,
        "special_effect": "Ignores 50% of enemy defense"
    },
    "phoenix_staff": {
        "name": "Phoenix Staff",
        "description": "Reborn from eternal flames",
        "rarity": Rarities.LEGENDARY,
        "cost": 3800,
        "currency": CurrencyTypes.GEMS,
        "attack_bonus": 160,
        "special_effect": "Revive with 50% HP when defeated"
    }
}

# Premium Skins (Gems/Payment Only)
PREMIUM_SKINS = {
    "nightmare_lord": {
        "name": "Nightmare Lord",
        "description": "Rule over the realm of shadows",
        "rarity": Rarities.LEGENDARY,
        "cost": 2000,
        "currency": CurrencyTypes.GEMS,
        "special_skill": "Fear Aura",
        "skill_description": "Reduce all enemy stats by 20%"
    },
    "golden_emperor": {
        "name": "Golden Emperor",
        "description": "Adorned in divine gold armor",
        "rarity": Rarities.LEGENDARY,
        "cost": 2500,
        "currency": CurrencyTypes.GEMS,
        "special_skill": "Midas Touch",
        "skill_description": "Gain 50% more gold from battles"
    },
    "ice_queen": {
        "name": "Ice Queen",
        "description": "Frozen beauty with deadly power",
        "rarity": Rarities.LEGENDARY,
        "cost": 2200,
        "currency": CurrencyTypes.GEMS,
        "special_skill": "Frozen Domain",
        "skill_description": "Freeze all enemies for 2 turns"
    },
    "demon_hunter": {
        "name": "Demon Hunter",
        "description": "Slayer of the underworld",
        "rarity": Rarities.LEGENDARY,
        "cost": 2800,
        "currency": CurrencyTypes.GEMS,
        "special_skill": "Demon Slayer",
        "skill_description": "Deal 200% damage to demon enemies"
    },
    "angel_of_war": {
        "name": "Angel of War",
        "description": "Divine warrior from paradise",
        "rarity": Rarities.LEGENDARY,
        "cost": 3200,
        "currency": CurrencyTypes.GEMS,
        "special_skill": "Divine Intervention",
        "skill_description": "Prevent death once per battle"
    }
}

# Ads Configuration System
ADS_CONFIG = {
    "daily_limit": 50,  # Maximum ads per day
    "rewarded_gems": 10,  # Gems per rewarded ad
    "interstitial_frequency": 3,  # Show after every X stage completions
    "revive_cost_reduction": 50,  # Percentage reduction in gem cost for revive
    "sources": [
        {
            "name": "AdMob",
            "enabled": True,
            "priority": 1,
            "app_id": "ca-app-pub-3940256099942544~3347511713",  # Test ID
            "rewarded_unit_id": "ca-app-pub-3940256099942544/5224354917",
            "interstitial_unit_id": "ca-app-pub-3940256099942544/1033173712"
        },
        {
            "name": "Unity Ads",
            "enabled": True,
            "priority": 2,
            "game_id": "4374282",  # Test ID
            "rewarded_placement": "Rewarded_Android",
            "interstitial_placement": "Interstitial_Android"
        },
        {
            "name": "Facebook Audience Network",
            "enabled": False,
            "priority": 3,
            "app_id": "YOUR_FB_APP_ID",
            "rewarded_placement": "YOUR_REWARDED_PLACEMENT_ID",
            "interstitial_placement": "YOUR_INTERSTITIAL_PLACEMENT_ID"
        }
    ],
    "analytics": {
        "track_impressions": True,
        "track_revenue": True,
        "track_completion_rate": True
    }
}

# Dashboard Analytics
DASHBOARD_CONFIG = {
    "admin_email": "seiftouatilol@gmail.com",
    "admin_password": "seif0662",
    "session_timeout": 3600,  # 1 hour in seconds
    "data_retention_days": 365,
    "refresh_interval": 30,  # seconds for auto-refresh
    "charts_enabled": True
}

# Premium Heroes (Gem/Payment Only)
PREMIUM_HEROES = {
    'shadow_assassin': {
        'name': 'Shadow Assassin',
        'description': 'Master of stealth and critical strikes',
        'cost': 5000,  # gems
        'rarity': 'Legendary',
        'stats': {'attack': 120, 'defense': 80, 'speed': 150, 'health': 800},
        'special_ability': 'Shadow Strike - 300% critical damage',
        'unlock_level': 25
    },
    'arcane_mage': {
        'name': 'Arcane Mage', 
        'description': 'Wielder of ancient magical powers',
        'cost': 7500,  # gems
        'rarity': 'Legendary',
        'stats': {'attack': 160, 'defense': 60, 'speed': 90, 'health': 700},
        'special_ability': 'Arcane Blast - Area damage to all enemies',
        'unlock_level': 35
    },
    'divine_paladin': {
        'name': 'Divine Paladin',
        'description': 'Holy warrior with healing powers',
        'cost': 10000,  # gems
        'rarity': 'Legendary',
        'stats': {'attack': 100, 'defense': 140, 'speed': 70, 'health': 1200},
        'special_ability': 'Divine Shield - Immunity + heal for 3 turns',
        'unlock_level': 50
    },
    'dragon_rider': {
        'name': 'Dragon Rider',
        'description': 'Commands the power of ancient dragons',
        'cost': 15000,  # gems
        'rarity': 'Legendary',
        'stats': {'attack': 180, 'defense': 100, 'speed': 120, 'health': 1000},
        'special_ability': 'Dragon Breath - Massive fire damage',
        'unlock_level': 75
    }
}

# Premium Weapons (Gem/Payment Only)
PREMIUM_WEAPONS = {
    'excalibur': {
        'name': 'Excalibur',
        'description': 'The legendary sword of kings',
        'cost': 8000,  # gems
        'rarity': 'Legendary',
        'attack_bonus': 80,
        'special_effect': 'Divine Strike - 50% chance for double damage',
        'unlock_level': 30
    },
    'staff_of_eternity': {
        'name': 'Staff of Eternity',
        'description': 'Ancient staff pulsing with magical energy',
        'cost': 12000,  # gems
        'rarity': 'Legendary',
        'attack_bonus': 100,
        'special_effect': 'Mana Surge - 30% chance to cast spell twice',
        'unlock_level': 45
    },
    'shadowbane_dagger': {
        'name': 'Shadowbane Dagger',
        'description': 'Forged from shadow essence and starlight',
        'cost': 6000,  # gems
        'rarity': 'Legendary',
        'attack_bonus': 60,
        'special_effect': 'Shadow Step - 25% chance to dodge and counter',
        'unlock_level': 20
    },
    'dragonscale_hammer': {
        'name': 'Dragonscale Hammer',
        'description': 'Crafted from the scales of an elder dragon',
        'cost': 15000,  # gems
        'rarity': 'Legendary',
        'attack_bonus': 120,
        'special_effect': 'Earthquake - Area damage to all enemies',
        'unlock_level': 60
    }
}

# Premium Skins (Gem/Payment Only)
PREMIUM_SKINS = {
    'golden_emperor': {
        'name': 'Golden Emperor',
        'description': 'Radiant armor that commands respect',
        'cost': 5000,  # gems
        'rarity': 'Legendary',
        'stat_bonus': {'attack': 25, 'defense': 25, 'speed': 15},
        'special_effect': 'Royal Presence - +20% gold from battles',
        'unlock_level': 25
    },
    'shadow_lord': {
        'name': 'Shadow Lord',
        'description': 'Dark armor infused with shadow magic',
        'cost': 7500,  # gems
        'rarity': 'Legendary',
        'stat_bonus': {'attack': 35, 'defense': 15, 'speed': 25},
        'special_effect': 'Shadow Cloak - 15% chance to dodge attacks',
        'unlock_level': 35
    },
    'crystal_guardian': {
        'name': 'Crystal Guardian',
        'description': 'Crystalline armor that reflects damage',
        'cost': 10000,  # gems
        'rarity': 'Legendary',
        'stat_bonus': {'attack': 20, 'defense': 40, 'speed': 10},
        'special_effect': 'Crystal Reflection - 30% damage reflected',
        'unlock_level': 45
    },
    'inferno_champion': {
        'name': 'Inferno Champion',
        'description': 'Fiery armor that burns enemies',
        'cost': 12000,  # gems
        'rarity': 'Legendary',
        'stat_bonus': {'attack': 45, 'defense': 20, 'speed': 20},
        'special_effect': 'Burning Aura - Enemies take fire damage each turn',
        'unlock_level': 55
    },
    'celestial_warrior': {
        'name': 'Celestial Warrior',
        'description': 'Divine armor blessed by the heavens',
        'cost': 15000,  # gems
        'rarity': 'Legendary',
        'stat_bonus': {'attack': 30, 'defense': 35, 'speed': 25},
        'special_effect': 'Divine Blessing - Immunity to status effects',
        'unlock_level': 65
    }
}

# Ads Configuration System
ADS_CONFIG = {
    'daily_limit': 50,  # Default daily limit
    'reward_per_ad': 25,  # Gems per ad
    'cooldown_minutes': 5,  # Minutes between ads
    'sources': {
        'admob': {
            'enabled': True,
            'app_id': 'ca-app-pub-3940256099942544~3347511713',  # Test ID
            'rewarded_ad_unit': 'ca-app-pub-3940256099942544/5224354917',
            'interstitial_ad_unit': 'ca-app-pub-3940256099942544/1033173712',
            'weight': 70  # Percentage of ads from this source
        },
        'unity_ads': {
            'enabled': True,
            'game_id': '4374880',  # Test ID
            'placement_id_rewarded': 'Rewarded_Android',
            'placement_id_interstitial': 'Interstitial_Android',
            'weight': 20
        },
        'applovin': {
            'enabled': False,
            'sdk_key': 'test_sdk_key',
            'rewarded_ad_unit': 'test_rewarded',
            'interstitial_ad_unit': 'test_interstitial',
            'weight': 10
        }
    },
    'revenue_tracking': {
        'enabled': True,
        'revenue_per_ad': 0.02,  # USD per ad view
        'currency': 'USD'
    },
    'analytics': {
        'track_impressions': True,
        'track_clicks': True,
        'track_revenue': True,
        'track_user_engagement': True
    }
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'admin_email': 'seiftouatilol@gmail.com',
    'admin_password_hash': 'b8c6f8b8a3c4d5e6f7a8b9c0d1e2f3a4',  # Hash of 'seif0662'
    'session_timeout': 3600,  # 1 hour in seconds
    'auto_refresh_interval': 30,  # seconds
    'data_retention_days': 90,
    'export_formats': ['json', 'csv', 'xlsx']
}

# Analytics Tracking
ANALYTICS_CONFIG = {
    'track_user_sessions': True,
    'track_level_completion': True,
    'track_purchases': True,
    'track_ad_interactions': True,
    'track_retention': True,
    'daily_active_users': True,
    'monthly_active_users': True,
    'revenue_tracking': True
}