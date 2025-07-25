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

    # Ad System
    AD_COOLDOWN = 30  # seconds between ads
    REWARDED_AD_TIMEOUT = 30  # seconds
    INTERSTITIAL_FREQUENCY = 5  # every X stages

    # Input
    TOUCH_DEADZONE = 10  # pixels
    LONG_PRESS_DURATION = 0.5  # seconds
    DOUBLE_TAP_MAX_INTERVAL = 0.3  # seconds

    # Admin Dashboard
    ADMIN_EMAIL = "seiftouatilol@gmail.com"
    ADMIN_PASSWORD = "seif0662"
    DASHBOARD_SECRET_KEY = "koa_admin_2024_secret_key"

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