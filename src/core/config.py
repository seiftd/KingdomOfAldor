"""
Kingdom of Aldoria - Enhanced Game Configuration
Contains all game constants, settings, and configuration parameters
"""

import pygame
import json
import os
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# Kingdom of Aldoria - Game Configuration
# Core game settings and constants

import pygame
import os
from pathlib import Path

# Import premium content
try:
    from src.content.premium_content import (
        PREMIUM_HEROES, PREMIUM_WEAPONS, PREMIUM_SKINS, PREMIUM_BUNDLES,
        get_premium_content_by_type, get_premium_item_by_id
    )
except ImportError:
    PREMIUM_HEROES = {}
    PREMIUM_WEAPONS = {}
    PREMIUM_SKINS = {}
    PREMIUM_BUNDLES = {}

# Game Version and Info
GAME_VERSION = "1.0.0"
GAME_TITLE = "Kingdom of Aldoria"

# === BASIC GAME SETTINGS ===
VERSION = "1.2.0"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
DEBUG_MODE = False

# === PATHS ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SAVES_DIR = os.path.join(BASE_DIR, "saves")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

# === WORLDS AND STAGES (EXPANDED) ===
# Enhanced World Configuration with More Maps and Storyline
WORLDS = {
    1: {
        "name": "Forest of Shadows",
        "description": "Ancient woods filled with mystical creatures",
        "stages": 40,  # Increased from 30
        "unlock_level": 1,
        "background": "worlds/forest_shadows.png",
        "music": "world_forest.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [1, 15, 30],
        "enemies": ["goblin", "wolf", "orc", "dark_elf"],
        "rewards": {"gold": 50, "xp": 25}
    },
    2: {
        "name": "Desert of Souls",
        "description": "Scorching sands hiding ancient secrets",
        "stages": 40,
        "unlock_level": 10,
        "background": "worlds/desert_souls.png",
        "music": "world_desert.ogg", 
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [45, 60, 80],
        "enemies": ["sand_worm", "mummy", "scorpion", "djinn"],
        "rewards": {"gold": 75, "xp": 35}
    },
    3: {
        "name": "Crystal Caverns",
        "description": "Underground realm of sparkling crystals",
        "stages": 40,
        "unlock_level": 20,
        "background": "worlds/crystal_caverns.png",
        "music": "world_caverns.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [85, 100, 120],
        "enemies": ["crystal_golem", "cave_spider", "dwarf_miner", "crystal_elemental"],
        "rewards": {"gold": 100, "xp": 50}
    },
    4: {
        "name": "Frozen Peaks",
        "description": "Icy mountains where dragons soar",
        "stages": 40,
        "unlock_level": 30,
        "background": "worlds/frozen_peaks.png",
        "music": "world_frozen.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [125, 140, 160],
        "enemies": ["ice_giant", "frost_wolf", "yeti", "ice_dragon"],
        "rewards": {"gold": 125, "xp": 65}
    },
    5: {
        "name": "Volcanic Realm",
        "description": "Land of fire and molten lava",
        "stages": 40,
        "unlock_level": 40,
        "background": "worlds/volcanic_realm.png",
        "music": "world_volcanic.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [165, 180, 200],
        "enemies": ["fire_elemental", "lava_golem", "phoenix", "flame_demon"],
        "rewards": {"gold": 150, "xp": 80}
    },
    6: {
        "name": "Sky Citadel",
        "description": "Floating fortress among the clouds",
        "stages": 40,
        "unlock_level": 50,
        "background": "worlds/sky_citadel.png",
        "music": "world_sky.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [205, 220, 240],
        "enemies": ["wind_spirit", "cloud_guardian", "sky_knight", "storm_lord"],
        "rewards": {"gold": 175, "xp": 95}
    },
    7: {
        "name": "Abyssal Depths",
        "description": "Dark underwater kingdom of the deep",
        "stages": 40,
        "unlock_level": 60,
        "background": "worlds/abyssal_depths.png",
        "music": "world_abyss.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [245, 260, 280],
        "enemies": ["sea_serpent", "kraken", "merfolk_warrior", "leviathan"],
        "rewards": {"gold": 200, "xp": 110}
    },
    8: {
        "name": "Celestial Gardens",
        "description": "Divine realm of eternal beauty",
        "stages": 40,
        "unlock_level": 70,
        "background": "worlds/celestial_gardens.png",
        "music": "world_celestial.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [285, 300, 320],
        "enemies": ["angel_guardian", "celestial_beast", "divine_champion", "seraph"],
        "rewards": {"gold": 225, "xp": 125}
    },
    9: {
        "name": "Shadowlands",
        "description": "Realm where darkness reigns supreme",
        "stages": 40,
        "unlock_level": 80,
        "background": "worlds/shadowlands.png",
        "music": "world_shadow.ogg",
        "boss_stages": [10, 20, 30, 40],
        "story_sessions": [325, 340, 360],
        "enemies": ["shadow_demon", "void_walker", "dark_lord", "nightmare"],
        "rewards": {"gold": 250, "xp": 140}
    },
    10: {
        "name": "Nexus of Eternity",
        "description": "The ultimate realm where time stands still",
        "stages": 50,  # Final world has more stages
        "unlock_level": 90,
        "background": "worlds/nexus_eternity.png",
        "music": "world_nexus.ogg",
        "boss_stages": [10, 20, 30, 40, 50],
        "story_sessions": [365, 380, 400],
        "enemies": ["cosmic_entity", "time_guardian", "eternal_champion", "aldoria_final_boss"],
        "rewards": {"gold": 300, "xp": 160}
    }
}

# Enhanced Heroes System with Premium Integration
HEROES = {
    # Existing heroes
    "knight_arin": {
        "name": "Knight Arin",
        "base_hp": 100,
        "base_attack": 25,
        "base_defense": 20,
        "unlock_level": 1,
        "unlock_type": "default",
        "cost": 0,
        "rarity": "Common",
        "special_ability": "Shield Bash",
        "sprite_path": "heroes/knight_arin.png"
    },
    "archer_elena": {
        "name": "Archer Elena",
        "base_hp": 80,
        "base_attack": 35,
        "base_defense": 15,
        "unlock_level": 5,
        "unlock_type": "gems",
        "cost": 1000,
        "rarity": "Rare",
        "special_ability": "Multi Shot",
        "sprite_path": "heroes/archer_elena.png"
    },
    "mage_zara": {
        "name": "Mage Zara",
        "base_hp": 70,
        "base_attack": 45,
        "base_defense": 10,
        "unlock_level": 10,
        "unlock_type": "gems",
        "cost": 2500,
        "rarity": "Epic",
        "special_ability": "Fireball",
        "sprite_path": "heroes/mage_zara.png"
    },
    "paladin_marcus": {
        "name": "Paladin Marcus",
        "base_hp": 120,
        "base_attack": 30,
        "base_defense": 25,
        "unlock_level": 15,
        "unlock_type": "gems",
        "cost": 5000,
        "rarity": "Epic",
        "special_ability": "Divine Shield",
        "sprite_path": "heroes/paladin_marcus.png"
    },
    "assassin_kira": {
        "name": "Assassin Kira",
        "base_hp": 90,
        "base_attack": 40,
        "base_defense": 12,
        "unlock_level": 20,
        "unlock_type": "gems",
        "cost": 7500,
        "rarity": "Epic",
        "special_ability": "Shadow Strike",
        "sprite_path": "heroes/assassin_kira.png"
    },
    # Merge premium heroes
    **PREMIUM_HEROES
}

# Enhanced Weapons System with Premium Integration
WEAPONS = {
    # ========== WOOD RANK ==========
    "wooden_sword": {
        "name": "Wooden Sword",
        "attack_bonus": 3,
        "defense_bonus": 0,
        "unlock_level": 1,
        "unlock_type": "default",
        "cost": 0,
        "rarity": "Common",
        "rank": "Wood",
        "sprite_path": "weapons/wooden_sword.png"
    },
    "wooden_bow": {
        "name": "Wooden Bow",
        "attack_bonus": 4,
        "defense_bonus": 0,
        "unlock_level": 1,
        "unlock_type": "gold",
        "cost": 50,
        "rarity": "Common",
        "rank": "Wood",
        "sprite_path": "weapons/wooden_bow.png"
    },
    "wooden_staff": {
        "name": "Wooden Staff",
        "attack_bonus": 2,
        "defense_bonus": 1,
        "spell_power": 5,
        "unlock_level": 1,
        "unlock_type": "gold",
        "cost": 75,
        "rarity": "Common",
        "rank": "Wood",
        "sprite_path": "weapons/wooden_staff.png"
    },
    "wooden_dagger": {
        "name": "Wooden Dagger",
        "attack_bonus": 5,
        "defense_bonus": 0,
        "crit_chance": 10,
        "unlock_level": 2,
        "unlock_type": "gold",
        "cost": 100,
        "rarity": "Common",
        "rank": "Wood",
        "sprite_path": "weapons/wooden_dagger.png"
    },

    # ========== IRON RANK ==========
    "iron_sword": {
        "name": "Iron Sword",
        "attack_bonus": 8,
        "defense_bonus": 1,
        "unlock_level": 3,
        "unlock_type": "gold",
        "cost": 200,
        "rarity": "Common",
        "rank": "Iron",
        "sprite_path": "weapons/iron_sword.png"
    },
    "iron_bow": {
        "name": "Iron Bow",
        "attack_bonus": 10,
        "defense_bonus": 0,
        "range_bonus": 2,
        "unlock_level": 3,
        "unlock_type": "gold",
        "cost": 250,
        "rarity": "Common",
        "rank": "Iron",
        "sprite_path": "weapons/iron_bow.png"
    },
    "iron_staff": {
        "name": "Iron Staff",
        "attack_bonus": 6,
        "defense_bonus": 2,
        "spell_power": 12,
        "unlock_level": 4,
        "unlock_type": "gold",
        "cost": 300,
        "rarity": "Common",
        "rank": "Iron",
        "sprite_path": "weapons/iron_staff.png"
    },
    "iron_hammer": {
        "name": "Iron Hammer",
        "attack_bonus": 12,
        "defense_bonus": 3,
        "unlock_level": 4,
        "unlock_type": "gold",
        "cost": 350,
        "rarity": "Common",
        "rank": "Iron",
        "sprite_path": "weapons/iron_hammer.png"
    },
    "iron_spear": {
        "name": "Iron Spear",
        "attack_bonus": 9,
        "defense_bonus": 1,
        "reach": 1,
        "unlock_level": 5,
        "unlock_type": "gold",
        "cost": 400,
        "rarity": "Common",
        "rank": "Iron",
        "sprite_path": "weapons/iron_spear.png"
    },

    # ========== SILVER RANK ==========
    "silver_sword": {
        "name": "Silver Sword",
        "attack_bonus": 15,
        "defense_bonus": 3,
        "crit_chance": 5,
        "unlock_level": 6,
        "unlock_type": "gold",
        "cost": 800,
        "rarity": "Uncommon",
        "rank": "Silver",
        "sprite_path": "weapons/silver_sword.png"
    },
    "silver_bow": {
        "name": "Silver Bow",
        "attack_bonus": 18,
        "defense_bonus": 1,
        "range_bonus": 3,
        "crit_chance": 8,
        "unlock_level": 7,
        "unlock_type": "gold",
        "cost": 900,
        "rarity": "Uncommon",
        "rank": "Silver",
        "sprite_path": "weapons/silver_bow.png"
    },
    "silver_staff": {
        "name": "Silver Staff",
        "attack_bonus": 12,
        "defense_bonus": 4,
        "spell_power": 20,
        "mana_regen": 2,
        "unlock_level": 8,
        "unlock_type": "gold",
        "cost": 1000,
        "rarity": "Uncommon",
        "rank": "Silver",
        "sprite_path": "weapons/silver_staff.png"
    },
    "silver_dagger": {
        "name": "Silver Dagger",
        "attack_bonus": 14,
        "defense_bonus": 0,
        "crit_chance": 15,
        "speed_bonus": 5,
        "unlock_level": 8,
        "unlock_type": "gold",
        "cost": 950,
        "rarity": "Uncommon",
        "rank": "Silver",
        "sprite_path": "weapons/silver_dagger.png"
    },
    "silver_scythe": {
        "name": "Silver Scythe",
        "attack_bonus": 16,
        "defense_bonus": 2,
        "life_steal": 5,
        "unlock_level": 9,
        "unlock_type": "gems",
        "cost": 150,
        "rarity": "Uncommon",
        "rank": "Silver",
        "sprite_path": "weapons/silver_scythe.png"
    },

    # ========== GOLD RANK ==========
    "golden_sword": {
        "name": "Golden Sword",
        "attack_bonus": 25,
        "defense_bonus": 5,
        "crit_chance": 10,
        "crit_damage": 20,
        "unlock_level": 12,
        "unlock_type": "gems",
        "cost": 300,
        "rarity": "Rare",
        "rank": "Gold",
        "sprite_path": "weapons/golden_sword.png"
    },
    "golden_bow": {
        "name": "Golden Bow",
        "attack_bonus": 28,
        "defense_bonus": 2,
        "range_bonus": 4,
        "crit_chance": 12,
        "piercing": 1,
        "unlock_level": 13,
        "unlock_type": "gems",
        "cost": 350,
        "rarity": "Rare",
        "rank": "Gold",
        "sprite_path": "weapons/golden_bow.png"
    },
    "golden_staff": {
        "name": "Golden Staff",
        "attack_bonus": 20,
        "defense_bonus": 6,
        "spell_power": 35,
        "mana_regen": 4,
        "spell_crit": 8,
        "unlock_level": 14,
        "unlock_type": "gems",
        "cost": 400,
        "rarity": "Rare",
        "rank": "Gold",
        "sprite_path": "weapons/golden_staff.png"
    },
    "golden_hammer": {
        "name": "Golden Hammer",
        "attack_bonus": 32,
        "defense_bonus": 8,
        "stun_chance": 10,
        "area_damage": 15,
        "unlock_level": 15,
        "unlock_type": "gems",
        "cost": 450,
        "rarity": "Rare",
        "rank": "Gold",
        "sprite_path": "weapons/golden_hammer.png"
    },
    "golden_fists": {
        "name": "Golden Fists",
        "attack_bonus": 22,
        "defense_bonus": 4,
        "speed_bonus": 10,
        "combo_multiplier": 1.2,
        "unlock_level": 16,
        "unlock_type": "gems",
        "cost": 380,
        "rarity": "Rare",
        "rank": "Gold",
        "sprite_path": "weapons/golden_fists.png"
    },

    # ========== PLATINUM RANK ==========
    "platinum_sword": {
        "name": "Platinum Sword",
        "attack_bonus": 40,
        "defense_bonus": 8,
        "crit_chance": 15,
        "crit_damage": 35,
        "elemental_damage": 10,
        "unlock_level": 18,
        "unlock_type": "gems",
        "cost": 600,
        "rarity": "Rare",
        "rank": "Platinum",
        "sprite_path": "weapons/platinum_sword.png"
    },
    "platinum_bow": {
        "name": "Platinum Bow",
        "attack_bonus": 45,
        "defense_bonus": 3,
        "range_bonus": 6,
        "crit_chance": 18,
        "piercing": 2,
        "multishot": 2,
        "unlock_level": 19,
        "unlock_type": "gems",
        "cost": 650,
        "rarity": "Rare",
        "rank": "Platinum",
        "sprite_path": "weapons/platinum_bow.png"
    },
    "platinum_staff": {
        "name": "Platinum Staff",
        "attack_bonus": 35,
        "defense_bonus": 10,
        "spell_power": 50,
        "mana_regen": 6,
        "spell_crit": 15,
        "spell_penetration": 20,
        "unlock_level": 20,
        "unlock_type": "gems",
        "cost": 700,
        "rarity": "Rare",
        "rank": "Platinum",
        "sprite_path": "weapons/platinum_staff.png"
    },
    "platinum_dagger": {
        "name": "Platinum Dagger",
        "attack_bonus": 38,
        "defense_bonus": 2,
        "crit_chance": 25,
        "speed_bonus": 15,
        "poison_damage": 8,
        "unlock_level": 21,
        "unlock_type": "gems",
        "cost": 680,
        "rarity": "Rare",
        "rank": "Platinum",
        "sprite_path": "weapons/platinum_dagger.png"
    },
    "platinum_scythe": {
        "name": "Platinum Scythe",
        "attack_bonus": 42,
        "defense_bonus": 6,
        "life_steal": 12,
        "soul_harvest": 5,
        "dark_damage": 15,
        "unlock_level": 22,
        "unlock_type": "gems",
        "cost": 720,
        "rarity": "Rare",
        "rank": "Platinum",
        "sprite_path": "weapons/platinum_scythe.png"
    },

    # ========== EMERALD RANK ==========
    "emerald_sword": {
        "name": "Emerald Sword",
        "attack_bonus": 60,
        "defense_bonus": 12,
        "crit_chance": 20,
        "crit_damage": 50,
        "nature_damage": 20,
        "healing_aura": 3,
        "unlock_level": 25,
        "unlock_type": "gems",
        "cost": 1000,
        "rarity": "Epic",
        "rank": "Emerald",
        "sprite_path": "weapons/emerald_sword.png"
    },
    "emerald_bow": {
        "name": "Emerald Bow",
        "attack_bonus": 65,
        "defense_bonus": 5,
        "range_bonus": 8,
        "crit_chance": 22,
        "piercing": 3,
        "nature_arrows": 25,
        "entangle_chance": 15,
        "unlock_level": 26,
        "unlock_type": "gems",
        "cost": 1100,
        "rarity": "Epic",
        "rank": "Emerald",
        "sprite_path": "weapons/emerald_bow.png"
    },
    "emerald_staff": {
        "name": "Emerald Staff",
        "attack_bonus": 50,
        "defense_bonus": 15,
        "spell_power": 75,
        "mana_regen": 8,
        "spell_crit": 20,
        "nature_spells": 30,
        "growth_aura": 10,
        "unlock_level": 27,
        "unlock_type": "gems",
        "cost": 1200,
        "rarity": "Epic",
        "rank": "Emerald",
        "sprite_path": "weapons/emerald_staff.png"
    },
    "emerald_hammer": {
        "name": "Emerald Hammer",
        "attack_bonus": 70,
        "defense_bonus": 18,
        "stun_chance": 20,
        "area_damage": 30,
        "earth_shatter": 25,
        "unlock_level": 28,
        "unlock_type": "gems",
        "cost": 1150,
        "rarity": "Epic",
        "rank": "Emerald",
        "sprite_path": "weapons/emerald_hammer.png"
    },
    "emerald_spear": {
        "name": "Emerald Spear",
        "attack_bonus": 58,
        "defense_bonus": 8,
        "reach": 2,
        "crit_chance": 18,
        "wind_strike": 20,
        "charge_damage": 40,
        "unlock_level": 29,
        "unlock_type": "gems",
        "cost": 1080,
        "rarity": "Epic",
        "rank": "Emerald",
        "sprite_path": "weapons/emerald_spear.png"
    },

    # ========== DIAMOND RANK ==========
    "diamond_sword": {
        "name": "Diamond Sword",
        "attack_bonus": 85,
        "defense_bonus": 18,
        "crit_chance": 25,
        "crit_damage": 70,
        "pure_damage": 25,
        "armor_pierce": 30,
        "light_aura": 15,
        "unlock_level": 32,
        "unlock_type": "gems",
        "cost": 1500,
        "rarity": "Epic",
        "rank": "Diamond",
        "sprite_path": "weapons/diamond_sword.png"
    },
    "diamond_bow": {
        "name": "Diamond Bow",
        "attack_bonus": 90,
        "defense_bonus": 8,
        "range_bonus": 10,
        "crit_chance": 28,
        "piercing": 4,
        "crystal_arrows": 35,
        "shatter_shot": 20,
        "unlock_level": 33,
        "unlock_type": "gems",
        "cost": 1600,
        "rarity": "Epic",
        "rank": "Diamond",
        "sprite_path": "weapons/diamond_bow.png"
    },
    "diamond_staff": {
        "name": "Diamond Staff",
        "attack_bonus": 70,
        "defense_bonus": 22,
        "spell_power": 100,
        "mana_regen": 12,
        "spell_crit": 25,
        "arcane_mastery": 40,
        "spell_echo": 15,
        "unlock_level": 34,
        "unlock_type": "gems",
        "cost": 1700,
        "rarity": "Epic",
        "rank": "Diamond",
        "sprite_path": "weapons/diamond_staff.png"
    },
    "diamond_dagger": {
        "name": "Diamond Dagger",
        "attack_bonus": 80,
        "defense_bonus": 5,
        "crit_chance": 35,
        "speed_bonus": 25,
        "assassination": 20,
        "shadow_step": 15,
        "unlock_level": 35,
        "unlock_type": "gems",
        "cost": 1550,
        "rarity": "Epic",
        "rank": "Diamond",
        "sprite_path": "weapons/diamond_dagger.png"
    },
    "diamond_fists": {
        "name": "Diamond Fists",
        "attack_bonus": 75,
        "defense_bonus": 12,
        "speed_bonus": 20,
        "combo_multiplier": 1.5,
        "diamond_strikes": 30,
        "chi_burst": 25,
        "unlock_level": 36,
        "unlock_type": "gems",
        "cost": 1650,
        "rarity": "Epic",
        "rank": "Diamond",
        "sprite_path": "weapons/diamond_fists.png"
    },

    # ========== ELITE RANK ==========
    "elite_blade": {
        "name": "Elite Blade",
        "attack_bonus": 110,
        "defense_bonus": 25,
        "crit_chance": 30,
        "crit_damage": 90,
        "elite_mastery": 35,
        "perfect_balance": 20,
        "energy_wave": 25,
        "unlock_level": 40,
        "unlock_type": "gems",
        "cost": 2200,
        "rarity": "Legendary",
        "rank": "Elite",
        "sprite_path": "weapons/elite_blade.png"
    },
    "elite_crossbow": {
        "name": "Elite Crossbow",
        "attack_bonus": 115,
        "defense_bonus": 12,
        "range_bonus": 12,
        "crit_chance": 32,
        "piercing": 5,
        "explosive_bolts": 40,
        "auto_reload": 1,
        "unlock_level": 41,
        "unlock_type": "gems",
        "cost": 2300,
        "rarity": "Legendary",
        "rank": "Elite",
        "sprite_path": "weapons/elite_crossbow.png"
    },
    "elite_orb": {
        "name": "Elite Orb",
        "attack_bonus": 95,
        "defense_bonus": 30,
        "spell_power": 130,
        "mana_regen": 15,
        "spell_crit": 30,
        "reality_warp": 50,
        "cosmic_energy": 35,
        "unlock_level": 42,
        "unlock_type": "gems",
        "cost": 2400,
        "rarity": "Legendary",
        "rank": "Elite",
        "sprite_path": "weapons/elite_orb.png"
    },
    "elite_gauntlets": {
        "name": "Elite Gauntlets",
        "attack_bonus": 105,
        "defense_bonus": 20,
        "speed_bonus": 30,
        "combo_multiplier": 1.8,
        "elite_combat": 40,
        "energy_fists": 35,
        "unlock_level": 43,
        "unlock_type": "gems",
        "cost": 2250,
        "rarity": "Legendary",
        "rank": "Elite",
        "sprite_path": "weapons/elite_gauntlets.png"
    },
    "elite_reaper": {
        "name": "Elite Reaper",
        "attack_bonus": 120,
        "defense_bonus": 15,
        "life_steal": 25,
        "soul_harvest": 15,
        "death_aura": 40,
        "soul_rend": 30,
        "unlock_level": 44,
        "unlock_type": "gems",
        "cost": 2350,
        "rarity": "Legendary",
        "rank": "Elite",
        "sprite_path": "weapons/elite_reaper.png"
    },

    # ========== HYPER RANK ==========
    "hyper_katana": {
        "name": "Hyper Katana",
        "attack_bonus": 140,
        "defense_bonus": 30,
        "crit_chance": 40,
        "crit_damage": 120,
        "hyper_slash": 50,
        "time_cut": 35,
        "perfect_edge": 40,
        "unlock_level": 48,
        "unlock_type": "gems",
        "cost": 3000,
        "rarity": "Legendary",
        "rank": "Hyper",
        "sprite_path": "weapons/hyper_katana.png"
    },
    "hyper_railgun": {
        "name": "Hyper Railgun",
        "attack_bonus": 150,
        "defense_bonus": 15,
        "range_bonus": 15,
        "crit_chance": 35,
        "piercing": 8,
        "plasma_shots": 60,
        "electromagnetic_pulse": 45,
        "unlock_level": 49,
        "unlock_type": "gems",
        "cost": 3200,
        "rarity": "Legendary",
        "rank": "Hyper",
        "sprite_path": "weapons/hyper_railgun.png"
    },
    "hyper_nexus": {
        "name": "Hyper Nexus",
        "attack_bonus": 125,
        "defense_bonus": 40,
        "spell_power": 180,
        "mana_regen": 20,
        "spell_crit": 40,
        "dimensional_magic": 70,
        "nexus_core": 50,
        "unlock_level": 50,
        "unlock_type": "gems",
        "cost": 3400,
        "rarity": "Legendary",
        "rank": "Hyper",
        "sprite_path": "weapons/hyper_nexus.png"
    },
    "hyper_destroyer": {
        "name": "Hyper Destroyer",
        "attack_bonus": 160,
        "defense_bonus": 35,
        "stun_chance": 35,
        "area_damage": 60,
        "destruction_wave": 55,
        "reality_break": 40,
        "unlock_level": 51,
        "unlock_type": "gems",
        "cost": 3300,
        "rarity": "Legendary",
        "rank": "Hyper",
        "sprite_path": "weapons/hyper_destroyer.png"
    },
    "hyper_phantom": {
        "name": "Hyper Phantom",
        "attack_bonus": 135,
        "defense_bonus": 10,
        "crit_chance": 45,
        "speed_bonus": 40,
        "phase_strike": 50,
        "phantom_form": 35,
        "void_step": 45,
        "unlock_level": 52,
        "unlock_type": "gems",
        "cost": 3100,
        "rarity": "Legendary",
        "rank": "Hyper",
        "sprite_path": "weapons/hyper_phantom.png"
    },

    # ========== LEGENDARY RANK ==========
    "legendary_excalibur": {
        "name": "Legendary Excalibur",
        "attack_bonus": 200,
        "defense_bonus": 50,
        "crit_chance": 50,
        "crit_damage": 150,
        "divine_light": 80,
        "holy_aura": 60,
        "righteous_fury": 70,
        "blessing_of_kings": 50,
        "unlock_level": 55,
        "unlock_type": "gems",
        "cost": 5000,
        "rarity": "Legendary",
        "rank": "Legendary",
        "sprite_path": "weapons/legendary_excalibur.png"
    },
    "legendary_worldbreaker": {
        "name": "Legendary Worldbreaker",
        "attack_bonus": 220,
        "defense_bonus": 40,
        "range_bonus": 20,
        "crit_chance": 45,
        "piercing": 10,
        "world_shatter": 100,
        "dimensional_arrow": 80,
        "reality_pierce": 90,
        "unlock_level": 56,
        "unlock_type": "gems",
        "cost": 5500,
        "rarity": "Legendary",
        "rank": "Legendary",
        "sprite_path": "weapons/legendary_worldbreaker.png"
    },
    "legendary_omniscience": {
        "name": "Legendary Omniscience",
        "attack_bonus": 180,
        "defense_bonus": 60,
        "spell_power": 250,
        "mana_regen": 30,
        "spell_crit": 50,
        "omniscient_magic": 100,
        "universal_knowledge": 80,
        "infinite_wisdom": 90,
        "unlock_level": 57,
        "unlock_type": "gems",
        "cost": 6000,
        "rarity": "Legendary",
        "rank": "Legendary",
        "sprite_path": "weapons/legendary_omniscience.png"
    },
    "legendary_apocalypse": {
        "name": "Legendary Apocalypse",
        "attack_bonus": 240,
        "defense_bonus": 55,
        "stun_chance": 50,
        "area_damage": 100,
        "apocalypse_strike": 120,
        "end_times": 100,
        "cataclysm": 110,
        "unlock_level": 58,
        "unlock_type": "gems",
        "cost": 5800,
        "rarity": "Legendary",
        "rank": "Legendary",
        "sprite_path": "weapons/legendary_apocalypse.png"
    },
    "legendary_infinity": {
        "name": "Legendary Infinity",
        "attack_bonus": 190,
        "defense_bonus": 35,
        "crit_chance": 55,
        "speed_bonus": 50,
        "infinite_strikes": 100,
        "eternal_combo": 2.5,
        "boundless_power": 80,
        "transcendence": 70,
        "unlock_level": 59,
        "unlock_type": "gems",
        "cost": 5200,
        "rarity": "Legendary",
        "rank": "Legendary",
        "sprite_path": "weapons/legendary_infinity.png"
    },
    "legendary_voidbringer": {
        "name": "Legendary Voidbringer",
        "attack_bonus": 210,
        "defense_bonus": 45,
        "life_steal": 40,
        "soul_harvest": 30,
        "void_mastery": 100,
        "reality_tear": 90,
        "existence_drain": 80,
        "entropy_field": 85,
        "unlock_level": 60,
        "unlock_type": "gems",
        "cost": 6500,
        "rarity": "Legendary",
        "rank": "Legendary",
        "sprite_path": "weapons/legendary_voidbringer.png"
    },

    # Existing weapons for compatibility
    "rusty_sword": {
        "name": "Rusty Sword",
        "attack_bonus": 5,
        "defense_bonus": 0,
        "unlock_level": 1,
        "unlock_type": "default",
        "cost": 0,
        "rarity": "Common",
        "sprite_path": "weapons/rusty_sword.png"
    },
    "steel_sword": {
        "name": "Steel Sword",
        "attack_bonus": 15,
        "defense_bonus": 2,
        "unlock_level": 3,
        "unlock_type": "gold",
        "cost": 500,
        "rarity": "Common",
        "sprite_path": "weapons/steel_sword.png"
    },
    "enchanted_blade": {
        "name": "Enchanted Blade",
        "attack_bonus": 25,
        "defense_bonus": 5,
        "unlock_level": 8,
        "unlock_type": "gems",
        "cost": 1500,
        "rarity": "Rare",
        "sprite_path": "weapons/enchanted_blade.png"
    },
    "dragon_slayer": {
        "name": "Dragon Slayer",
        "attack_bonus": 35,
        "defense_bonus": 8,
        "unlock_level": 15,
        "unlock_type": "gems",
        "cost": 5000,
        "rarity": "Epic",
        "sprite_path": "weapons/dragon_slayer.png"
    },
    "shadow_dagger": {
        "name": "Shadow Dagger",
        "attack_bonus": 20,
        "defense_bonus": 0,
        "crit_chance": 25,
        "unlock_level": 12,
        "unlock_type": "gems",
        "cost": 3000,
        "rarity": "Rare",
        "sprite_path": "weapons/shadow_dagger.png"
    },
    # Merge premium weapons
    **PREMIUM_WEAPONS
}

# Enhanced Skins System with Premium Integration
SKINS = {
    # Existing skins
    "default": {
        "name": "Default",
        "unlock_type": "default",
        "cost": 0,
        "rarity": "Common",
        "sprite_path": "skins/default.png"
    },
    "golden_armor": {
        "name": "Golden Armor",
        "unlock_type": "gems",
        "cost": 2000,
        "rarity": "Rare",
        "bonus_stats": {"defense": 5},
        "sprite_path": "skins/golden_armor.png"
    },
    "shadow_cloak": {
        "name": "Shadow Cloak",
        "unlock_type": "gems",
        "cost": 3500,
        "rarity": "Epic",
        "bonus_stats": {"attack": 8, "crit_chance": 10},
        "sprite_path": "skins/shadow_cloak.png"
    },
    "phoenix_wings": {
        "name": "Phoenix Wings",
        "unlock_type": "gems",
        "cost": 8000,
        "rarity": "Epic",
        "bonus_stats": {"hp": 20, "attack": 10},
        "special_effect": "Fire Aura",
        "sprite_path": "skins/phoenix_wings.png"
    },
    # Merge premium skins
    **PREMIUM_SKINS
}

# === RARITY SETTINGS ===
RARITY_COLORS = {
    "Common": (169, 169, 169),      # Gray
    "Rare": (0, 123, 255),          # Blue
    "Epic": (138, 43, 226),         # Purple
    "Legendary": (255, 215, 0),     # Gold
    "Mythic": (255, 20, 147)        # Deep Pink
}

# === IN-APP PURCHASES ===
IAP_PACKAGES = {
    "starter_pack": {
        "name": "Starter Pack",
        "description": "Perfect for new adventurers",
        "price_usd": 0.99,
        "gems": 100,
        "gold": 5000,
        "items": ["silver_sword"]
    },
    "gem_small": {
        "name": "Small Gem Pack",
        "description": "A handful of precious gems",
        "price_usd": 1.99,
        "gems": 250,
        "gold": 0,
        "items": []
    },
    "gem_medium": {
        "name": "Medium Gem Pack",
        "description": "A pouch full of gems",
        "price_usd": 4.99,
        "gems": 650,
        "gold": 0,
        "items": []
    },
    "gem_large": {
        "name": "Large Gem Pack",
        "description": "A chest of brilliant gems",
        "price_usd": 9.99,
        "gems": 1400,
        "gold": 0,
        "items": []
    },
    "weekly_subscription": {
        "name": "Weekly VIP",
        "description": "7 days of VIP benefits",
        "price_usd": 2.99,
        "duration_days": 7,
        "daily_gems": 50,
        "daily_gold": 1000,
        "benefits": ["double_xp", "no_ads", "daily_rewards"]
    },
    "monthly_subscription": {
        "name": "Monthly VIP",
        "description": "30 days of VIP benefits",
        "price_usd": 9.99,
        "duration_days": 30,
        "daily_gems": 75,
        "daily_gold": 2000,
        "benefits": ["double_xp", "no_ads", "daily_rewards", "exclusive_content"]
    }
}

# === ENHANCED AD SYSTEM ===
AD_CONFIG = {
    "reward_ranges": {
        "gems": {"min": 5, "max": 15},
        "gold": {"min": 100, "max": 500}
    },
    "daily_limits": {
        "free_user": 10,
        "vip_user": 20
    },
    "cooldown_seconds": 30,
    "sources": [
        {"name": "AdMob", "priority": 1, "fill_rate": 0.95},
        {"name": "Unity Ads", "priority": 2, "fill_rate": 0.90},
        {"name": "IronSource", "priority": 3, "fill_rate": 0.85}
    ],
    "vip_bonus_multiplier": 1.5
}

# === ADMIN DASHBOARD ===
DASHBOARD_CONFIG = {
    "admin_email": "seiftouatilol@gmail.com",
    "admin_password": "seif0662",
    "session_timeout_hours": 24,
    "analytics_retention_days": 90
}

# === AUDIO SETTINGS ===
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.8
MAX_SOUND_CHANNELS = 8

# === MOBILE SETTINGS ===
MOBILE_BUTTON_SIZE = 80
TOUCH_SENSITIVITY = 5
GESTURE_THRESHOLD = 50

# === SAVE SETTINGS ===
SAVE_ENCRYPTION_KEY = b'kingdom_of_aldoria_save_key_2024_very_secure'
AUTO_SAVE_INTERVAL = 30
MAX_SAVE_BACKUPS = 5

# === LOCALIZATION ===
SUPPORTED_LANGUAGES = ["en", "ar", "fr"]
DEFAULT_LANGUAGE = "en"

# === PERFORMANCE SETTINGS ===
TEXTURE_ATLAS_SIZE = 2048
OBJECT_POOL_SIZE = 100
PRELOAD_WORLDS = 2

# === NETWORK SETTINGS ===
API_TIMEOUT = 10
RETRY_ATTEMPTS = 3
OFFLINE_MODE_ENABLED = True

# === FIREBASE CONFIG ===
FIREBASE_CONFIG = {
    "apiKey": "your-api-key",
    "authDomain": "kingdom-of-aldoria.firebaseapp.com",
    "projectId": "kingdom-of-aldoria",
    "storageBucket": "kingdom-of-aldoria.appspot.com",
    "messagingSenderId": "123456789",
    "appId": "your-app-id"
}

# === DATABASE CONFIG ===
SQLITE_DB_PATH = os.path.join(SAVES_DIR, "game_data.db")
SYNC_INTERVAL_MINUTES = 5
CONFLICT_RESOLUTION = "newest_timestamp"

# Additional Gem-Purchasable Heroes
GEM_HEROES = {
    "storm_caller": {
        "name": "Storm Caller",
        "description": "Master of lightning and thunder",
        "base_stats": {"hp": 120, "attack": 35, "defense": 20, "speed": 40},
        "special_abilities": ["Chain Lightning", "Thunder Shield"],
        "unlock_level": 15,
        "unlock_type": "gems",
        "cost": 500,
        "rarity": "Epic",
        "sprite_path": "heroes/storm_caller.png"
    },
    "flame_dancer": {
        "name": "Flame Dancer",
        "description": "Graceful warrior who dances with fire",
        "base_stats": {"hp": 100, "attack": 40, "defense": 15, "speed": 50},
        "special_abilities": ["Fire Whirl", "Burning Step"],
        "unlock_level": 20,
        "unlock_type": "gems", 
        "cost": 750,
        "rarity": "Epic",
        "sprite_path": "heroes/flame_dancer.png"
    },
    "ice_guardian": {
        "name": "Ice Guardian",
        "description": "Protector of the frozen realm",
        "base_stats": {"hp": 150, "attack": 25, "defense": 40, "speed": 25},
        "special_abilities": ["Ice Wall", "Frozen Armor"],
        "unlock_level": 25,
        "unlock_type": "gems",
        "cost": 1000,
        "rarity": "Epic", 
        "sprite_path": "heroes/ice_guardian.png"
    },
    "void_assassin": {
        "name": "Void Assassin",
        "description": "Strikes from the shadows of the void",
        "base_stats": {"hp": 80, "attack": 50, "defense": 10, "speed": 60},
        "special_abilities": ["Void Step", "Shadow Strike"],
        "unlock_level": 30,
        "unlock_type": "gems",
        "cost": 1250,
        "rarity": "Epic",
        "sprite_path": "heroes/void_assassin.png"
    }
}

# Additional Gem-Purchasable Weapons
GEM_WEAPONS = {
    "lightning_spear": {
        "name": "Lightning Spear",
        "type": "spear",
        "attack": 45,
        "special_effect": "Chain Lightning on crit",
        "unlock_level": 12,
        "unlock_type": "gems",
        "cost": 300,
        "rarity": "Rare",
        "sprite_path": "weapons/lightning_spear.png"
    },
    "frost_blade": {
        "name": "Frost Blade", 
        "type": "sword",
        "attack": 40,
        "special_effect": "Slows enemy on hit",
        "unlock_level": 15,
        "unlock_type": "gems",
        "cost": 400,
        "rarity": "Rare",
        "sprite_path": "weapons/frost_blade.png"
    },
    "shadow_dagger": {
        "name": "Shadow Dagger",
        "type": "dagger",
        "attack": 35,
        "special_effect": "Chance to ignore armor",
        "unlock_level": 18,
        "unlock_type": "gems", 
        "cost": 500,
        "rarity": "Rare",
        "sprite_path": "weapons/shadow_dagger.png"
    },
    "phoenix_bow": {
        "name": "Phoenix Bow",
        "type": "bow",
        "attack": 50,
        "special_effect": "Burning arrows",
        "unlock_level": 22,
        "unlock_type": "gems",
        "cost": 600,
        "rarity": "Epic",
        "sprite_path": "weapons/phoenix_bow.png"
    },
    "void_hammer": {
        "name": "Void Hammer",
        "type": "hammer", 
        "attack": 60,
        "special_effect": "Area damage on crit",
        "unlock_level": 25,
        "unlock_type": "gems",
        "cost": 750,
        "rarity": "Epic",
        "sprite_path": "weapons/void_hammer.png"
    }
}

# Additional Gem-Purchasable Skins
GEM_SKINS = {
    "elemental_knight": {
        "name": "Elemental Knight",
        "description": "Infused with elemental powers",
        "skill": "Elemental Strike",
        "skill_description": "Random elemental damage",
        "unlock_level": 10,
        "unlock_type": "gems",
        "cost": 200,
        "rarity": "Rare",
        "sprite_path": "skins/elemental_knight.png"
    },
    "shadow_warrior": {
        "name": "Shadow Warrior",
        "description": "Master of stealth and darkness",
        "skill": "Shadow Clone",
        "skill_description": "Creates temporary clone",
        "unlock_level": 15,
        "unlock_type": "gems",
        "cost": 350,
        "rarity": "Rare", 
        "sprite_path": "skins/shadow_warrior.png"
    },
    "crystal_guardian": {
        "name": "Crystal Guardian",
        "description": "Protected by magical crystals",
        "skill": "Crystal Shield",
        "skill_description": "Absorbs damage",
        "unlock_level": 20,
        "unlock_type": "gems",
        "cost": 500,
        "rarity": "Epic",
        "sprite_path": "skins/crystal_guardian.png"
    }
}

# Enhanced Heroes System - merge with premium content
HEROES.update(GEM_HEROES)
WEAPONS.update(GEM_WEAPONS) 
SKINS.update(GEM_SKINS)

# Enhanced storyline configuration
STORYLINE = {
    "session_1": {
        "title": "The Awakening",
        "worlds": [1, 2, 3, 4],
        "intro": "In the peaceful kingdom of Aldoria, darkness suddenly falls upon the land. Ancient evils stir from their slumber, corrupting the once-beautiful realms. Knight Arin, a young warrior blessed with divine light, must begin his quest to restore balance to the world.",
        "chapters": {
            1: {
                "title": "Shadows in the Forest",
                "description": "The Forest of Shadows was once a place of beauty and life. Now, twisted creatures roam its darkened paths. Arin must navigate through the corrupted woodland to reach the heart of the darkness.",
                "key_events": ["First encounter with shadow beasts", "Discovery of the cursed shrine", "Meeting the Forest Guardian"]
            },
            2: {
                "title": "Souls of the Desert",
                "description": "The Desert of Souls holds the spirits of ancient warriors who fell in a great battle long ago. These restless souls must be put to rest before they consume the living world.",
                "key_events": ["Battle with the Pharaoh's tomb guardians", "Solving the pyramid puzzles", "Freeing the trapped souls"]
            },
            3: {
                "title": "Ice and Fire",
                "description": "The Frozen Peaks hide ancient fire magic beneath their icy surface. Arin must master both elements to progress on his journey.",
                "key_events": ["Awakening the Ice Dragon", "Finding the Flame of Eternity", "Balancing opposing forces"]
            },
            4: {
                "title": "Heart of the Mountain",
                "description": "Deep within the Volcanic Caves lies the first source of corruption. Arin must face the Molten King to prevent the darkness from spreading further.",
                "key_events": ["Navigating lava rivers", "Confronting fire elementals", "Battle with the Molten King"]
            }
        }
    },
    "session_2": {
        "title": "The Forgotten Prophecy",
        "worlds": [5, 6, 7, 8],
        "intro": "With the first corruption cleansed, Arin discovers an ancient prophecy that speaks of a chosen one who will either save or doom Aldoria. As he delves deeper into the mystery, darker forces emerge, and allies become enemies.",
        "chapters": {
            5: {
                "title": "Whispers in the Swamp",
                "description": "The Mystic Swamp is home to powerful witches who hold fragments of the ancient prophecy. Arin must navigate their tests and riddles to learn the truth.",
                "key_events": ["Meeting the Swamp Witch", "The Trial of Elements", "Revelation of the prophecy"]
            },
            6: {
                "title": "Crystals of Truth",
                "description": "The Crystal Caverns contain memories of the past, showing visions of what was and what might be. Arin must face his own doubts and fears.",
                "key_events": ["Visions of the past", "Inner demons manifest", "Gaining crystal sight"]
            },
            7: {
                "title": "Among the Clouds",
                "description": "The Sky Citadel is where celestial beings dwell, but even they have been touched by corruption. Arin must prove his worth to gain their aid.",
                "key_events": ["Trials of the Sky Lords", "Earning celestial weapons", "The betrayal revealed"]
            },
            8: {
                "title": "Embracing Shadows",
                "description": "In the Shadow Realm, Arin must confront the darkness within himself. Only by accepting both light and shadow can he become truly powerful.",
                "key_events": ["Meeting his shadow self", "The dark knight's test", "Mastering shadow magic"]
            }
        }
    },
    "session_3": {
        "title": "The Final Convergence",
        "worlds": [9, 10, 11, 12, 13, 14, 15],
        "intro": "The prophecy is fulfilled, and Arin stands at the crossroads of destiny. The final battle approaches as all realms converge into one. Light and darkness, creation and destruction, all will be decided in the ultimate confrontation that will determine the fate of Aldoria forever.",
        "chapters": {
            9: {
                "title": "Divine Preparation",
                "description": "The Celestial Gardens serve as a sanctuary where Arin prepares for the final battle. Here, he gathers divine allies and receives the blessings of light.",
                "key_events": ["Blessing of the Divine", "Gathering celestial army", "Forging the Light Blade"]
            },
            10: {
                "title": "Descent to Darkness",
                "description": "The Abyssal Throne awaits. Arin must descend into the heart of evil to face the Dark Lord in his own domain.",
                "key_events": ["Breaking the dark seals", "Confronting fallen heroes", "The Dark Lord's challenge"]
            },
            11: {
                "title": "Cosmic Revelations",
                "description": "The Astral Observatory reveals the true nature of reality. Arin learns that his journey was guided by forces beyond mortal comprehension.",
                "key_events": ["Meeting the Star Sages", "Understanding cosmic truth", "Gaining astral powers"]
            },
            12: {
                "title": "Elemental Mastery",
                "description": "At the Elemental Nexus, Arin must prove mastery over all elemental forces to gain the power needed for the final confrontation.",
                "key_events": ["Trial of Five Elements", "Elemental fusion", "Becoming the Elemental Lord"]
            },
            13: {
                "title": "Temporal Paradox",
                "description": "The Time Spiral tests Arin's resolve across multiple timelines. He must ensure the correct future comes to pass.",
                "key_events": ["Navigating time streams", "Preventing dark futures", "Stabilizing the timeline"]
            },
            14: {
                "title": "Void Confrontation",
                "description": "In the Void Sanctum, Arin faces the source of all corruption - the Void itself. This battle will determine the nature of reality.",
                "key_events": ["Entering the Void", "Battle with Void entities", "Choosing creation over destruction"]
            },
            15: {
                "title": "Eternal Victory",
                "description": "The Eternal Realm is where legends are born. Arin's final test will echo through eternity, securing peace for all time.",
                "key_events": ["The ultimate trial", "Transcending mortality", "Becoming the Eternal Guardian"]
            }
        }
    }
}

# Enhanced Heroes System - merge with premium content
HEROES.update(PREMIUM_HEROES)

# Enhanced Weapons System - merge with premium content  
WEAPONS.update(PREMIUM_WEAPONS)

# Enhanced Skins System - merge with premium content
SKINS.update(PREMIUM_SKINS)

# Add premium bundles
BUNDLES = PREMIUM_BUNDLES

# Story Sessions
STORY_SESSIONS = {
    1: {
        "title": "The Awakening",
        "description": "The kingdom faces a growing darkness as ancient evils stir",
        "chapters": [
            {
                "title": "The Call to Adventure",
                "text": "In the peaceful Kingdom of Aldoria, young Knight Arin receives an urgent summons from the High Council. Dark creatures have begun emerging from the Whispering Woods, and strange magical disturbances plague the land. As the kingdom's newest knight, Arin must venture into these mystical realms to uncover the source of this growing threat.",
                "worlds": [1, 2, 3]
            }
        ]
    },
    2: {
        "title": "The Shadow War",
        "description": "The darkness spreads as an ancient enemy reveals itself",
        "chapters": [
            {
                "title": "Veil Between Worlds",
                "text": "Arin's journey leads deeper into realms where reality itself seems unstable. The Shadow Realm bleeds into the physical world, and crystal formations appear to be conduits for dark magic. Ancient texts speak of a Dark Lord who once ruled these lands, now stirring from his eternal slumber. The knight must gather allies and powerful artifacts to face this growing menace.",
                "worlds": [4, 5, 6, 7]
            }
        ]
    },
    3: {
        "title": "The Final Stand",
        "description": "The ultimate battle for Aldoria's future begins",
        "chapters": [
            {
                "title": "Beyond the Veil",
                "text": "The Dark Lord's influence reaches across dimensions, corrupting even the most sacred places. Arin must venture through mystical gardens where time itself is a weapon, into the void between stars, and finally to the Throne of Eternity. But even defeating the Dark Lord may not be enough, as new threats emerge from the depths of the ocean and the storm-torn peaks beyond.",
                "worlds": [8, 9, 10, 11, 12]
            }
        ]
    }
}