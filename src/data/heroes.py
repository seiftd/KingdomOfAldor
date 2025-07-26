#!/usr/bin/env python3
"""
Kingdom of Aldoria - Heroes Database
Defines all available heroes with their stats and unlock requirements
"""

from ..core.config import ItemRarity, SkillType

class Hero:
    def __init__(self, id, name, description, base_stats, skills, unlock_cost, rarity, image_path):
        self.id = id
        self.name = name
        self.description = description
        self.base_stats = base_stats
        self.skills = skills
        self.unlock_cost = unlock_cost
        self.rarity = rarity
        self.image_path = image_path

# Base Hero (Free)
HEROES = {
    "knight_arin": Hero(
        id="knight_arin",
        name="Knight Arin",
        description="A brave knight from the Kingdom of Aldoria",
        base_stats={
            "health": 100,
            "attack": 25,
            "defense": 20,
            "speed": 15,
            "mana": 50
        },
        skills=[SkillType.SWORD_STRIKE],
        unlock_cost={"gold": 0, "gems": 0},
        rarity=ItemRarity.COMMON,
        image_path="assets/images/heroes/knight_arin.webp"
    ),
    
    # Legendary Heroes (Gems Only)
    "archmage_eldara": Hero(
        id="archmage_eldara",
        name="Archmage Eldara",
        description="Master of ancient magic, wielder of cosmic forces",
        base_stats={
            "health": 80,
            "attack": 45,
            "defense": 15,
            "speed": 25,
            "mana": 120
        },
        skills=[SkillType.FIREBALL, SkillType.FROST_SHIELD, SkillType.LIGHTNING_BOLT],
        unlock_cost={"gold": 0, "gems": 2500},
        rarity=ItemRarity.LEGENDARY,
        image_path="assets/images/heroes/archmage_eldara.webp"
    ),
    
    "shadow_assassin_kael": Hero(
        id="shadow_assassin_kael",
        name="Shadow Assassin Kael",
        description="Master of stealth and deadly precision strikes",
        base_stats={
            "health": 75,
            "attack": 50,
            "defense": 10,
            "speed": 40,
            "mana": 80
        },
        skills=[SkillType.SHADOW_STRIKE, SkillType.POISON_BLADE, SkillType.STEALTH],
        unlock_cost={"gold": 0, "gems": 3000},
        rarity=ItemRarity.LEGENDARY,
        image_path="assets/images/heroes/shadow_assassin_kael.webp"
    ),
    
    "dragon_lord_pyrion": Hero(
        id="dragon_lord_pyrion",
        name="Dragon Lord Pyrion",
        description="Ancient dragon in human form, master of fire magic",
        base_stats={
            "health": 150,
            "attack": 40,
            "defense": 35,
            "speed": 20,
            "mana": 100
        },
        skills=[SkillType.DRAGON_BREATH, SkillType.FIRE_AURA, SkillType.WING_STRIKE],
        unlock_cost={"gold": 0, "gems": 3500},
        rarity=ItemRarity.LEGENDARY,
        image_path="assets/images/heroes/dragon_lord_pyrion.webp"
    ),
    
    "celestial_guardian_luna": Hero(
        id="celestial_guardian_luna",
        name="Celestial Guardian Luna",
        description="Divine protector blessed by the moon goddess",
        base_stats={
            "health": 120,
            "attack": 35,
            "defense": 40,
            "speed": 30,
            "mana": 90
        },
        skills=[SkillType.DIVINE_SHIELD, SkillType.HEALING_LIGHT, SkillType.MOON_BEAM],
        unlock_cost={"gold": 0, "gems": 4000},
        rarity=ItemRarity.LEGENDARY,
        image_path="assets/images/heroes/celestial_guardian_luna.webp"
    ),
    
    "void_necromancer_malachar": Hero(
        id="void_necromancer_malachar",
        name="Void Necromancer Malachar",
        description="Master of death magic and dark arts",
        base_stats={
            "health": 90,
            "attack": 55,
            "defense": 20,
            "speed": 15,
            "mana": 130
        },
        skills=[SkillType.SOUL_DRAIN, SkillType.RAISE_UNDEAD, SkillType.DEATH_CURSE],
        unlock_cost={"gold": 0, "gems": 4500},
        rarity=ItemRarity.LEGENDARY,
        image_path="assets/images/heroes/void_necromancer_malachar.webp"
    ),
    
    "storm_berserker_thor": Hero(
        id="storm_berserker_thor",
        name="Storm Berserker Thor",
        description="Warrior blessed by the storm gods",
        base_stats={
            "health": 110,
            "attack": 60,
            "defense": 25,
            "speed": 35,
            "mana": 70
        },
        skills=[SkillType.LIGHTNING_STRIKE, SkillType.BERSERKER_RAGE, SkillType.THUNDER_CLAP],
        unlock_cost={"gold": 0, "gems": 3800},
        rarity=ItemRarity.LEGENDARY,
        image_path="assets/images/heroes/storm_berserker_thor.webp"
    )
}

def get_hero_by_id(hero_id):
    """Get hero data by ID"""
    return HEROES.get(hero_id)

def get_heroes_by_rarity(rarity):
    """Get all heroes of specific rarity"""
    return {k: v for k, v in HEROES.items() if v.rarity == rarity}

def get_purchasable_heroes():
    """Get heroes that require gems to unlock"""
    return {k: v for k, v in HEROES.items() if v.unlock_cost["gems"] > 0}

def get_unlocked_heroes(player_data):
    """Get list of heroes unlocked by player"""
    unlocked = player_data.get("unlocked_heroes", ["knight_arin"])
    return {k: v for k, v in HEROES.items() if k in unlocked}