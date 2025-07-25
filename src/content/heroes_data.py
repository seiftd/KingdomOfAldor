"""
Kingdom of Aldoria - Premium Content Data
Contains heroes, weapons, and skins available only through gem purchases
All items are Legendary rarity and payment-only
"""

from enum import Enum
from typing import Dict, List, Any
from ..core.config import ItemType, Rarity, CurrencyType

class HeroClass(Enum):
    KNIGHT = "knight"
    MAGE = "mage"
    ARCHER = "archer"
    ASSASSIN = "assassin"
    PALADIN = "paladin"
    NECROMANCER = "necromancer"
    BERSERKER = "berserker"
    MONK = "monk"

class WeaponType(Enum):
    SWORD = "sword"
    STAFF = "staff"
    BOW = "bow"
    DAGGER = "dagger"
    HAMMER = "hammer"
    SCYTHE = "scythe"
    FIST = "fist"
    SPEAR = "spear"

# Premium Heroes (Legendary Rarity, Gems Only)
PREMIUM_HEROES = {
    "shadow_assassin": {
        "id": "shadow_assassin",
        "name": "Shadow Assassin Kai",
        "description": "Master of stealth and shadow magic, strikes from the darkness",
        "class": HeroClass.ASSASSIN,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 2500},
        "payment_only": True,
        "base_stats": {
            "health": 850,
            "attack": 180,
            "defense": 65,
            "speed": 95,
            "critical_chance": 25,
            "critical_damage": 200
        },
        "special_abilities": [
            {
                "name": "Shadow Strike",
                "description": "Teleport behind enemy and deal 300% damage",
                "cooldown": 8,
                "damage_multiplier": 3.0
            },
            {
                "name": "Vanish",
                "description": "Become invisible for 3 turns, +50% critical chance",
                "cooldown": 12,
                "duration": 3
            }
        ],
        "passive": {
            "name": "Shadow Mastery",
            "description": "10% chance to dodge attacks and counter with 150% damage"
        },
        "unlock_level": 25,
        "sprite_path": "assets/images/heroes/shadow_assassin.webp"
    },
    
    "arcane_sorcerer": {
        "id": "arcane_sorcerer",
        "name": "Arcane Sorcerer Zara",
        "description": "Wielder of forbidden magic, commands the elements",
        "class": HeroClass.MAGE,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 2800},
        "payment_only": True,
        "base_stats": {
            "health": 700,
            "attack": 220,
            "defense": 45,
            "speed": 75,
            "critical_chance": 20,
            "critical_damage": 250
        },
        "special_abilities": [
            {
                "name": "Meteor Storm",
                "description": "Rain meteors on all enemies for 250% damage",
                "cooldown": 10,
                "damage_multiplier": 2.5,
                "targets": "all_enemies"
            },
            {
                "name": "Arcane Shield",
                "description": "Absorb next 3 attacks and reflect 100% damage",
                "cooldown": 15,
                "duration": 999,
                "charges": 3
            }
        ],
        "passive": {
            "name": "Mana Overflow",
            "description": "Each spell cast increases next spell damage by 20% (stacks 5 times)"
        },
        "unlock_level": 30,
        "sprite_path": "assets/images/heroes/arcane_sorcerer.webp"
    },
    
    "divine_paladin": {
        "id": "divine_paladin",
        "name": "Divine Paladin Theron",
        "description": "Blessed by the gods, protector of the innocent",
        "class": HeroClass.PALADIN,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 3000},
        "payment_only": True,
        "base_stats": {
            "health": 1200,
            "attack": 140,
            "defense": 120,
            "speed": 60,
            "critical_chance": 15,
            "critical_damage": 180
        },
        "special_abilities": [
            {
                "name": "Divine Intervention",
                "description": "Heal all allies to full HP and grant immunity for 2 turns",
                "cooldown": 20,
                "targets": "all_allies",
                "heal_percentage": 100
            },
            {
                "name": "Judgment Strike",
                "description": "Deal damage equal to missing health percentage x 5",
                "cooldown": 12,
                "special_calculation": "missing_health_multiplier"
            }
        ],
        "passive": {
            "name": "Divine Protection",
            "description": "All allies take 20% less damage while Paladin is alive"
        },
        "unlock_level": 35,
        "sprite_path": "assets/images/heroes/divine_paladin.webp"
    },
    
    "frost_archer": {
        "id": "frost_archer",
        "name": "Frost Archer Lyra",
        "description": "Ice-cold precision, never misses her target",
        "class": HeroClass.ARCHER,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 2400},
        "payment_only": True,
        "base_stats": {
            "health": 800,
            "attack": 190,
            "defense": 55,
            "speed": 85,
            "critical_chance": 30,
            "critical_damage": 220
        },
        "special_abilities": [
            {
                "name": "Frozen Arrow Barrage",
                "description": "Fire 5 arrows, each dealing 120% damage and freezing target",
                "cooldown": 9,
                "damage_multiplier": 1.2,
                "hits": 5,
                "effect": "freeze"
            },
            {
                "name": "Ice Prison",
                "description": "Trap enemy in ice for 3 turns, unable to act",
                "cooldown": 18,
                "duration": 3,
                "effect": "stun"
            }
        ],
        "passive": {
            "name": "Absolute Zero",
            "description": "Critical hits freeze enemies for 1 turn"
        },
        "unlock_level": 28,
        "sprite_path": "assets/images/heroes/frost_archer.webp"
    },
    
    "death_knight": {
        "id": "death_knight",
        "name": "Death Knight Morgrim",
        "description": "Undead warrior who commands the power of death itself",
        "class": HeroClass.NECROMANCER,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 3500},
        "payment_only": True,
        "base_stats": {
            "health": 1000,
            "attack": 160,
            "defense": 90,
            "speed": 70,
            "critical_chance": 18,
            "critical_damage": 200
        },
        "special_abilities": [
            {
                "name": "Soul Harvest",
                "description": "Deal damage and heal for 150% of damage dealt",
                "cooldown": 7,
                "damage_multiplier": 2.0,
                "heal_multiplier": 1.5
            },
            {
                "name": "Army of the Dead",
                "description": "Summon 3 skeleton warriors for 5 turns",
                "cooldown": 25,
                "summons": 3,
                "duration": 5
            }
        ],
        "passive": {
            "name": "Undead Resilience",
            "description": "Cannot be reduced below 1 HP for 1 turn after taking fatal damage"
        },
        "unlock_level": 40,
        "sprite_path": "assets/images/heroes/death_knight.webp"
    },
    
    "storm_berserker": {
        "id": "storm_berserker",
        "name": "Storm Berserker Ragnar",
        "description": "Wild warrior who channels lightning and thunder",
        "class": HeroClass.BERSERKER,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 2700},
        "payment_only": True,
        "base_stats": {
            "health": 950,
            "attack": 200,
            "defense": 70,
            "speed": 80,
            "critical_chance": 22,
            "critical_damage": 240
        },
        "special_abilities": [
            {
                "name": "Thunder Rage",
                "description": "Each attack this turn deals +50% damage (3 attacks)",
                "cooldown": 8,
                "damage_multiplier": 1.5,
                "attacks": 3
            },
            {
                "name": "Lightning Strike",
                "description": "Instant attack that chains to 3 enemies",
                "cooldown": 6,
                "damage_multiplier": 1.8,
                "chain_targets": 3
            }
        ],
        "passive": {
            "name": "Berserker's Fury",
            "description": "Attack increases by 10% each turn (max 100%)"
        },
        "unlock_level": 32,
        "sprite_path": "assets/images/heroes/storm_berserker.webp"
    },
    
    "celestial_monk": {
        "id": "celestial_monk",
        "name": "Celestial Monk Zen",
        "description": "Enlightened warrior who fights with inner peace and cosmic power",
        "class": HeroClass.MONK,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 2600},
        "payment_only": True,
        "base_stats": {
            "health": 900,
            "attack": 170,
            "defense": 80,
            "speed": 90,
            "critical_chance": 25,
            "critical_damage": 190
        },
        "special_abilities": [
            {
                "name": "Chi Explosion",
                "description": "Deal damage based on current Chi stacks (max 10 stacks)",
                "cooldown": 5,
                "special_calculation": "chi_stacks"
            },
            {
                "name": "Inner Peace",
                "description": "Become immune to debuffs and gain 2 Chi per turn for 4 turns",
                "cooldown": 16,
                "duration": 4,
                "chi_per_turn": 2
            }
        ],
        "passive": {
            "name": "Chi Master",
            "description": "Gain 1 Chi stack each turn. Each stack increases damage by 15%"
        },
        "unlock_level": 26,
        "sprite_path": "assets/images/heroes/celestial_monk.webp"
    }
}

# Premium Weapons (Legendary Rarity, Gems Only)
PREMIUM_WEAPONS = {
    "shadowfang_blade": {
        "id": "shadowfang_blade",
        "name": "Shadowfang Blade",
        "description": "Legendary dagger forged from shadow itself",
        "type": WeaponType.DAGGER,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1500},
        "payment_only": True,
        "compatible_classes": [HeroClass.ASSASSIN, HeroClass.ARCHER],
        "stats": {
            "attack": 85,
            "critical_chance": 20,
            "critical_damage": 50,
            "speed": 15
        },
        "special_effect": {
            "name": "Shadow Pierce",
            "description": "15% chance to ignore all defenses and deal pure damage"
        },
        "unlock_level": 20,
        "sprite_path": "assets/images/weapons/shadowfang_blade.webp"
    },
    
    "staff_of_eternities": {
        "id": "staff_of_eternities",
        "name": "Staff of Eternities",
        "description": "Ancient staff containing the power of time itself",
        "type": WeaponType.STAFF,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1800},
        "payment_only": True,
        "compatible_classes": [HeroClass.MAGE, HeroClass.NECROMANCER],
        "stats": {
            "attack": 95,
            "critical_chance": 12,
            "critical_damage": 80,
            "spell_power": 40
        },
        "special_effect": {
            "name": "Time Distortion",
            "description": "10% chance to reset all cooldowns after casting a spell"
        },
        "unlock_level": 25,
        "sprite_path": "assets/images/weapons/staff_of_eternities.webp"
    },
    
    "excalibur_divine": {
        "id": "excalibur_divine",
        "name": "Excalibur Divine",
        "description": "The legendary sword of kings, blessed by divine light",
        "type": WeaponType.SWORD,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 2000},
        "payment_only": True,
        "compatible_classes": [HeroClass.KNIGHT, HeroClass.PALADIN],
        "stats": {
            "attack": 110,
            "critical_chance": 15,
            "critical_damage": 60,
            "defense": 25
        },
        "special_effect": {
            "name": "Divine Blessing",
            "description": "Each attack has 20% chance to heal all allies for 10% of damage dealt"
        },
        "unlock_level": 30,
        "sprite_path": "assets/images/weapons/excalibur_divine.webp"
    },
    
    "frostbite_bow": {
        "id": "frostbite_bow",
        "name": "Frostbite Bow",
        "description": "Bow made from eternal ice, never melts",
        "type": WeaponType.BOW,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1600},
        "payment_only": True,
        "compatible_classes": [HeroClass.ARCHER],
        "stats": {
            "attack": 88,
            "critical_chance": 25,
            "critical_damage": 45,
            "range": 30
        },
        "special_effect": {
            "name": "Frost Shot",
            "description": "All attacks slow enemies by 30% for 2 turns"
        },
        "unlock_level": 22,
        "sprite_path": "assets/images/weapons/frostbite_bow.webp"
    },
    
    "doomhammer_apocalypse": {
        "id": "doomhammer_apocalypse",
        "name": "Doomhammer Apocalypse",
        "description": "Massive hammer that can shatter mountains",
        "type": WeaponType.HAMMER,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1900},
        "payment_only": True,
        "compatible_classes": [HeroClass.BERSERKER, HeroClass.PALADIN],
        "stats": {
            "attack": 120,
            "critical_chance": 10,
            "critical_damage": 100,
            "area_damage": 40
        },
        "special_effect": {
            "name": "Earthquake",
            "description": "Critical hits cause area damage to all enemies equal to 50% of damage"
        },
        "unlock_level": 28,
        "sprite_path": "assets/images/weapons/doomhammer_apocalypse.webp"
    },
    
    "soul_reaper_scythe": {
        "id": "soul_reaper_scythe",
        "name": "Soul Reaper Scythe",
        "description": "Scythe of death itself, harvests souls of the fallen",
        "type": WeaponType.SCYTHE,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 2200},
        "payment_only": True,
        "compatible_classes": [HeroClass.NECROMANCER],
        "stats": {
            "attack": 105,
            "critical_chance": 18,
            "critical_damage": 75,
            "life_steal": 25
        },
        "special_effect": {
            "name": "Soul Harvest",
            "description": "Killing an enemy permanently increases attack by 2 (max +50)"
        },
        "unlock_level": 35,
        "sprite_path": "assets/images/weapons/soul_reaper_scythe.webp"
    },
    
    "dragon_fists": {
        "id": "dragon_fists",
        "name": "Gauntlets of the Dragon",
        "description": "Mystical gauntlets infused with dragon essence",
        "type": WeaponType.FIST,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1700},
        "payment_only": True,
        "compatible_classes": [HeroClass.MONK, HeroClass.BERSERKER],
        "stats": {
            "attack": 92,
            "critical_chance": 22,
            "critical_damage": 55,
            "combo_damage": 35
        },
        "special_effect": {
            "name": "Dragon Combo",
            "description": "Each consecutive hit increases damage by 25% (max 5 hits)"
        },
        "unlock_level": 24,
        "sprite_path": "assets/images/weapons/dragon_fists.webp"
    },
    
    "lightning_spear": {
        "id": "lightning_spear",
        "name": "Lightning Spear of Zeus",
        "description": "Spear crackling with divine lightning",
        "type": WeaponType.SPEAR,
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1650},
        "payment_only": True,
        "compatible_classes": [HeroClass.KNIGHT, HeroClass.BERSERKER],
        "stats": {
            "attack": 98,
            "critical_chance": 16,
            "critical_damage": 65,
            "lightning_damage": 30
        },
        "special_effect": {
            "name": "Chain Lightning",
            "description": "Attacks jump to 2 nearby enemies for 60% damage"
        },
        "unlock_level": 26,
        "sprite_path": "assets/images/weapons/lightning_spear.webp"
    }
}

# Premium Skins (Legendary Rarity, Gems Only)
PREMIUM_SKINS = {
    "shadow_lord_skin": {
        "id": "shadow_lord_skin",
        "name": "Shadow Lord",
        "description": "Embrace the darkness with this intimidating shadow-themed skin",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 800},
        "payment_only": True,
        "compatible_heroes": ["shadow_assassin", "death_knight"],
        "stat_bonuses": {
            "attack": 15,
            "critical_chance": 8,
            "speed": 10
        },
        "special_ability": {
            "name": "Shadow Form",
            "description": "Become untargetable for 1 turn (once per battle)",
            "cooldown": 999,  # Once per battle
            "uses": 1
        },
        "visual_effects": {
            "aura": "dark_shadow",
            "particle_effects": ["shadow_wisps", "dark_energy"],
            "animation_set": "shadow_lord"
        },
        "unlock_level": 25,
        "sprite_path": "assets/images/skins/shadow_lord.webp"
    },
    
    "arcane_master_skin": {
        "id": "arcane_master_skin",
        "name": "Arcane Master",
        "description": "Channel pure magical energy with this mystical skin",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 900},
        "payment_only": True,
        "compatible_heroes": ["arcane_sorcerer"],
        "stat_bonuses": {
            "attack": 20,
            "spell_power": 25,
            "critical_damage": 15
        },
        "special_ability": {
            "name": "Arcane Overload",
            "description": "Next 3 spells cost no mana and deal +100% damage",
            "cooldown": 15,
            "duration": 3
        },
        "visual_effects": {
            "aura": "arcane_energy",
            "particle_effects": ["floating_runes", "magical_sparkles"],
            "animation_set": "arcane_master"
        },
        "unlock_level": 30,
        "sprite_path": "assets/images/skins/arcane_master.webp"
    },
    
    "golden_champion_skin": {
        "id": "golden_champion_skin",
        "name": "Golden Champion",
        "description": "Shine like gold with this prestigious champion skin",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1200},
        "payment_only": True,
        "compatible_heroes": ["divine_paladin"],
        "stat_bonuses": {
            "health": 100,
            "defense": 30,
            "all_stats": 10
        },
        "special_ability": {
            "name": "Golden Aura",
            "description": "All allies gain +20% stats while champion is alive",
            "passive": True,
            "aura_range": "all_allies"
        },
        "visual_effects": {
            "aura": "golden_light",
            "particle_effects": ["golden_sparkles", "divine_rays"],
            "animation_set": "golden_champion"
        },
        "unlock_level": 35,
        "sprite_path": "assets/images/skins/golden_champion.webp"
    },
    
    "ice_queen_skin": {
        "id": "ice_queen_skin",
        "name": "Ice Queen",
        "description": "Rule the frozen realm with this majestic ice skin",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 850},
        "payment_only": True,
        "compatible_heroes": ["frost_archer"],
        "stat_bonuses": {
            "critical_chance": 12,
            "critical_damage": 20,
            "ice_damage": 30
        },
        "special_ability": {
            "name": "Absolute Zero",
            "description": "Freeze all enemies for 2 turns",
            "cooldown": 20,
            "targets": "all_enemies",
            "duration": 2
        },
        "visual_effects": {
            "aura": "frost_aura",
            "particle_effects": ["ice_crystals", "snow_storm"],
            "animation_set": "ice_queen"
        },
        "unlock_level": 28,
        "sprite_path": "assets/images/skins/ice_queen.webp"
    },
    
    "death_emperor_skin": {
        "id": "death_emperor_skin",
        "name": "Death Emperor",
        "description": "Command the undead legions with this terrifying skin",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1000},
        "payment_only": True,
        "compatible_heroes": ["death_knight"],
        "stat_bonuses": {
            "health": 150,
            "life_steal": 20,
            "necromancy_power": 40
        },
        "special_ability": {
            "name": "Undead Legion",
            "description": "Summon 5 undead minions for the entire battle",
            "cooldown": 999,  # Once per battle
            "summons": 5,
            "duration": 999
        },
        "visual_effects": {
            "aura": "death_energy",
            "particle_effects": ["floating_skulls", "dark_mist"],
            "animation_set": "death_emperor"
        },
        "unlock_level": 40,
        "sprite_path": "assets/images/skins/death_emperor.webp"
    },
    
    "storm_god_skin": {
        "id": "storm_god_skin",
        "name": "Storm God",
        "description": "Harness the power of thunder and lightning",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 950},
        "payment_only": True,
        "compatible_heroes": ["storm_berserker"],
        "stat_bonuses": {
            "attack": 25,
            "speed": 15,
            "lightning_damage": 35
        },
        "special_ability": {
            "name": "Thunder Strike",
            "description": "Deal massive lightning damage to all enemies",
            "cooldown": 12,
            "damage_multiplier": 3.0,
            "targets": "all_enemies"
        },
        "visual_effects": {
            "aura": "electric_storm",
            "particle_effects": ["lightning_bolts", "thunder_clouds"],
            "animation_set": "storm_god"
        },
        "unlock_level": 32,
        "sprite_path": "assets/images/skins/storm_god.webp"
    },
    
    "enlightened_master_skin": {
        "id": "enlightened_master_skin",
        "name": "Enlightened Master",
        "description": "Achieve perfect balance with this serene martial arts skin",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 750},
        "payment_only": True,
        "compatible_heroes": ["celestial_monk"],
        "stat_bonuses": {
            "chi_generation": 50,
            "balance": 25,
            "inner_peace": 30
        },
        "special_ability": {
            "name": "Perfect Balance",
            "description": "Immune to all debuffs and gain maximum Chi stacks",
            "cooldown": 18,
            "duration": 5,
            "chi_stacks": 10
        },
        "visual_effects": {
            "aura": "peaceful_energy",
            "particle_effects": ["floating_lotus", "energy_waves"],
            "animation_set": "enlightened_master"
        },
        "unlock_level": 26,
        "sprite_path": "assets/images/skins/enlightened_master.webp"
    },
    
    "cosmic_warrior_skin": {
        "id": "cosmic_warrior_skin",
        "name": "Cosmic Warrior",
        "description": "Wield the power of stars and galaxies",
        "rarity": Rarity.LEGENDARY,
        "cost": {"currency": CurrencyType.GEMS, "amount": 1100},
        "payment_only": True,
        "compatible_heroes": ["all"],  # Universal skin
        "stat_bonuses": {
            "all_stats": 15,
            "cosmic_power": 50,
            "stellar_energy": 25
        },
        "special_ability": {
            "name": "Cosmic Nova",
            "description": "Explode with cosmic energy, dealing % max HP damage to all enemies",
            "cooldown": 25,
            "damage_calculation": "percentage_max_hp",
            "percentage": 30,
            "targets": "all_enemies"
        },
        "visual_effects": {
            "aura": "cosmic_energy",
            "particle_effects": ["stars", "galaxy_swirl", "cosmic_dust"],
            "animation_set": "cosmic_warrior"
        },
        "unlock_level": 50,
        "sprite_path": "assets/images/skins/cosmic_warrior.webp"
    }
}

# Bundle Packages for Premium Content
PREMIUM_BUNDLES = {
    "assassin_pack": {
        "id": "assassin_pack",
        "name": "Shadow Assassin Pack",
        "description": "Complete assassin package with hero, weapon, and skin",
        "contents": [
            {"type": "hero", "id": "shadow_assassin"},
            {"type": "weapon", "id": "shadowfang_blade"},
            {"type": "skin", "id": "shadow_lord_skin"}
        ],
        "original_price": 4800,  # Sum of individual prices
        "bundle_price": 3500,    # 27% discount
        "savings": 1300,
        "payment_only": True,
        "rarity": Rarity.LEGENDARY
    },
    
    "mage_master_pack": {
        "id": "mage_master_pack",
        "name": "Arcane Sorcerer Pack",
        "description": "Ultimate mage package with enhanced magical abilities",
        "contents": [
            {"type": "hero", "id": "arcane_sorcerer"},
            {"type": "weapon", "id": "staff_of_eternities"},
            {"type": "skin", "id": "arcane_master_skin"}
        ],
        "original_price": 5500,
        "bundle_price": 4200,
        "savings": 1300,
        "payment_only": True,
        "rarity": Rarity.LEGENDARY
    },
    
    "divine_champion_pack": {
        "id": "divine_champion_pack",
        "name": "Divine Champion Pack",
        "description": "Righteous paladin with divine blessings",
        "contents": [
            {"type": "hero", "id": "divine_paladin"},
            {"type": "weapon", "id": "excalibur_divine"},
            {"type": "skin", "id": "golden_champion_skin"}
        ],
        "original_price": 6200,
        "bundle_price": 4800,
        "savings": 1400,
        "payment_only": True,
        "rarity": Rarity.LEGENDARY
    },
    
    "ultimate_legends_pack": {
        "id": "ultimate_legends_pack",
        "name": "Ultimate Legends Pack",
        "description": "All premium heroes, weapons, and exclusive cosmic skin",
        "contents": [
            {"type": "all_heroes", "id": "premium_heroes"},
            {"type": "all_weapons", "id": "premium_weapons"},
            {"type": "skin", "id": "cosmic_warrior_skin"},
            {"type": "bonus_gems", "amount": 5000}
        ],
        "original_price": 25000,
        "bundle_price": 15000,
        "savings": 10000,
        "payment_only": True,
        "rarity": Rarity.LEGENDARY,
        "limited_time": True,
        "exclusive": True
    }
}

def get_premium_content_by_type(content_type: str) -> Dict[str, Any]:
    """Get all premium content of a specific type"""
    if content_type == "heroes":
        return PREMIUM_HEROES
    elif content_type == "weapons":
        return PREMIUM_WEAPONS
    elif content_type == "skins":
        return PREMIUM_SKINS
    elif content_type == "bundles":
        return PREMIUM_BUNDLES
    else:
        return {}

def get_premium_item_by_id(item_id: str) -> Dict[str, Any]:
    """Get a specific premium item by ID"""
    all_content = {**PREMIUM_HEROES, **PREMIUM_WEAPONS, **PREMIUM_SKINS, **PREMIUM_BUNDLES}
    return all_content.get(item_id, None)

def get_compatible_items(hero_id: str) -> Dict[str, List[str]]:
    """Get all compatible weapons and skins for a hero"""
    hero = PREMIUM_HEROES.get(hero_id)
    if not hero:
        return {"weapons": [], "skins": []}
    
    hero_class = hero["class"]
    compatible_weapons = []
    compatible_skins = []
    
    # Find compatible weapons
    for weapon_id, weapon in PREMIUM_WEAPONS.items():
        if hero_class in weapon["compatible_classes"]:
            compatible_weapons.append(weapon_id)
    
    # Find compatible skins
    for skin_id, skin in PREMIUM_SKINS.items():
        if (hero_id in skin["compatible_heroes"] or 
            "all" in skin["compatible_heroes"]):
            compatible_skins.append(skin_id)
    
    return {
        "weapons": compatible_weapons,
        "skins": compatible_skins
    }

def calculate_bundle_savings(bundle_id: str) -> int:
    """Calculate savings for a bundle"""
    bundle = PREMIUM_BUNDLES.get(bundle_id)
    if not bundle:
        return 0
    
    return bundle["original_price"] - bundle["bundle_price"]