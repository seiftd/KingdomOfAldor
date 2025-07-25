"""
Kingdom of Aldoria - Game Configuration
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