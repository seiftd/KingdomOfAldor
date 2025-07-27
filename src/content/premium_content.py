"""
Kingdom of Aldoria - Premium Content
Contains all premium heroes, weapons, skins, and bundles
"""

from enum import Enum
from typing import Dict, List, Any, Optional

# === PREMIUM CONTENT TYPES ===

class PremiumType(Enum):
    """Premium content type enumeration"""
    HERO = "hero"
    WEAPON = "weapon"
    SKIN = "skin"
    BUNDLE = "bundle"

class PurchaseType(Enum):
    """Purchase type enumeration"""
    GEMS = "gems"
    MONEY = "money"
    VIP_EXCLUSIVE = "vip_exclusive"

# === PREMIUM HEROES ===

PREMIUM_HEROES = {
    "dragon_lord_arin": {
        "id": "dragon_lord_arin",
        "name": "Dragon Lord Arin",
        "description": "Arin wielding the power of dragons with fire immunity and devastating flame attacks",
        "class": "dragon_knight",
        "rarity": "legendary",
        "cost": 15000,  # gems
        "purchase_type": "gems",
        "payment_only": False,
        "stats": {
            "health": 1500,
            "attack": 200,
            "defense": 150,
            "speed": 80,
            "magic": 180
        },
        "abilities": [
            {
                "name": "Dragon's Breath",
                "description": "Unleashes a devastating fire breath that hits all enemies",
                "damage": 250,
                "type": "fire",
                "cooldown": 3,
                "mana_cost": 50
            },
            {
                "name": "Fire Immunity",
                "description": "Immune to all fire damage and heals from fire attacks",
                "type": "passive"
            },
            {
                "name": "Dragon Wings",
                "description": "Gains flight ability to avoid ground attacks for 2 turns",
                "type": "buff",
                "duration": 2,
                "cooldown": 5
            }
        ],
        "unlock_level": 30,
        "sprite_path": "heroes/dragon_lord_arin.png"
    },
    
    "cosmic_emperor_arin": {
        "id": "cosmic_emperor_arin",
        "name": "Cosmic Emperor Arin",
        "description": "Arin ascended to cosmic power with control over space and time",
        "class": "cosmic_mage",
        "rarity": "legendary",
        "cost": 20000,  # gems
        "purchase_type": "gems",
        "payment_only": False,
        "stats": {
            "health": 1200,
            "attack": 150,
            "defense": 100,
            "speed": 120,
            "magic": 300
        },
        "abilities": [
            {
                "name": "Cosmic Storm",
                "description": "Summons a storm of cosmic energy dealing massive damage",
                "damage": 400,
                "type": "cosmic",
                "cooldown": 4,
                "mana_cost": 80
            },
            {
                "name": "Time Manipulation",
                "description": "Can rewind time to undo damage or skip enemy turns",
                "type": "utility",
                "cooldown": 6
            },
            {
                "name": "Stellar Crown",
                "description": "Passive ability that regenerates mana faster and boosts all magic damage",
                "type": "passive",
                "mana_regen": 2.0,
                "magic_boost": 0.5
            }
        ],
        "unlock_level": 50,
        "sprite_path": "heroes/cosmic_emperor_arin.png"
    },
    
    "pyromancer_hero": {
        "id": "pyromancer_hero",
        "name": "Pyromancer Blaze",
        "description": "Master of fire magic with area burst abilities",
        "class": "pyromancer",
        "rarity": "epic",
        "cost": 8000,  # gems
        "purchase_type": "gems",
        "payment_only": False,
        "stats": {
            "health": 800,
            "attack": 120,
            "defense": 80,
            "speed": 90,
            "magic": 200
        },
        "abilities": [
            {
                "name": "Fire Burst",
                "description": "Area fireburst dealing damage over time",
                "damage": 150,
                "type": "fire",
                "area": True,
                "dot_damage": 25,
                "dot_duration": 3
            }
        ],
        "unlock_level": 20,
        "sprite_path": "heroes/pyromancer.png"
    },
    
    "void_assassin_hero": {
        "id": "void_assassin_hero",
        "name": "Void Assassin",
        "description": "Shadow warrior with teleportation and critical strike abilities",
        "class": "void_assassin",
        "rarity": "epic",
        "cost": 10000,  # gems
        "purchase_type": "gems",
        "payment_only": False,
        "stats": {
            "health": 600,
            "attack": 180,
            "defense": 60,
            "speed": 150,
            "magic": 100
        },
        "abilities": [
            {
                "name": "Void Strike",
                "description": "Teleport behind enemy for guaranteed critical hit",
                "damage": 200,
                "type": "physical",
                "crit_chance": 1.0,
                "teleport": True
            }
        ],
        "unlock_level": 25,
        "sprite_path": "heroes/void_assassin.png"
    },
    
    "ice_warden_hero": {
        "id": "ice_warden_hero",
        "name": "Ice Warden",
        "description": "Frost guardian with freeze and shield abilities",
        "class": "ice_warden",
        "rarity": "epic",
        "cost": 7500,  # gems
        "purchase_type": "gems",
        "payment_only": False,
        "stats": {
            "health": 1000,
            "attack": 100,
            "defense": 140,
            "speed": 70,
            "magic": 160
        },
        "abilities": [
            {
                "name": "Frost Prison",
                "description": "Freeze enemies for 3 seconds",
                "type": "ice",
                "freeze_duration": 3,
                "area": True
            }
        ],
        "unlock_level": 18,
        "sprite_path": "heroes/ice_warden.png"
    }
}

# === PREMIUM WEAPONS ===

PREMIUM_WEAPONS = {
    # Elite Tier Weapons
    "elite_cosmic_blade": {
        "id": "elite_cosmic_blade",
        "name": "Cosmic Blade",
        "description": "A sword forged from stardust with cosmic energy",
        "type": "sword",
        "rarity": "elite",
        "cost": 5000,  # gems
        "payment_only": False,
        "compatible_classes": ["knight", "dragon_knight"],
        "stats": {
            "attack": 180,
            "crit_chance": 0.25,
            "crit_damage": 2.0
        },
        "special_effect": "Cosmic Strike: 20% chance to deal double damage and blind enemy",
        "unlock_level": 40,
        "sprite_path": "weapons/elite/cosmic_blade.png"
    },
    
    "elite_void_crossbow": {
        "id": "elite_void_crossbow",
        "name": "Void Crossbow",
        "description": "Crossbow that shoots bolts through dimensional rifts",
        "type": "crossbow",
        "rarity": "elite",
        "cost": 4500,  # gems
        "payment_only": False,
        "compatible_classes": ["archer", "void_assassin"],
        "stats": {
            "attack": 160,
            "range": 5,
            "piercing": True
        },
        "special_effect": "Void Shot: Ignores enemy defense and has 15% chance to teleport behind target",
        "unlock_level": 38,
        "sprite_path": "weapons/elite/void_crossbow.png"
    },
    
    "elite_reality_orb": {
        "id": "elite_reality_orb",
        "name": "Reality Orb",
        "description": "Orb that bends reality to the wielder's will",
        "type": "orb",
        "rarity": "elite",
        "cost": 5500,  # gems
        "payment_only": False,
        "compatible_classes": ["mage", "cosmic_mage"],
        "stats": {
            "attack": 140,
            "magic": 200,
            "mana_regen": 1.5
        },
        "special_effect": "Reality Shift: 25% chance to negate enemy attack and reflect damage",
        "unlock_level": 42,
        "sprite_path": "weapons/elite/reality_orb.png"
    },
    
    # Hyper Tier Weapons
    "hyper_quantum_katana": {
        "id": "hyper_quantum_katana",
        "name": "Quantum Katana",
        "description": "Katana that exists in multiple dimensions simultaneously",
        "type": "katana",
        "rarity": "hyper",
        "cost": 10000,  # gems or $19.99
        "payment_only": False,
        "compatible_classes": ["assassin", "void_assassin"],
        "stats": {
            "attack": 220,
            "speed": 50,
            "crit_chance": 0.35
        },
        "special_effect": "Quantum Slash: Attacks hit all possible positions enemy could be in",
        "unlock_level": 60,
        "sprite_path": "weapons/hyper/quantum_katana.png"
    },
    
    "hyper_plasma_railgun": {
        "id": "hyper_plasma_railgun",
        "name": "Plasma Railgun",
        "description": "Advanced energy weapon from the far future",
        "type": "railgun",
        "rarity": "hyper",
        "cost": 12000,  # gems or $24.99
        "payment_only": False,
        "compatible_classes": ["archer"],
        "stats": {
            "attack": 250,
            "range": 8,
            "piercing": True,
            "energy_damage": True
        },
        "special_effect": "Plasma Burst: 30% chance to hit all enemies in a line",
        "unlock_level": 65,
        "sprite_path": "weapons/hyper/plasma_railgun.png"
    },
    
    "hyper_dimensional_nexus": {
        "id": "hyper_dimensional_nexus",
        "name": "Dimensional Nexus",
        "description": "Staff that channels power from multiple dimensions",
        "type": "nexus",
        "rarity": "hyper",
        "cost": 11000,  # gems or $22.99
        "payment_only": False,
        "compatible_classes": ["mage", "cosmic_mage"],
        "stats": {
            "attack": 180,
            "magic": 280,
            "mana_regen": 2.0,
            "spell_power": 1.5
        },
        "special_effect": "Dimensional Rift: Spells have 25% chance to cast twice",
        "unlock_level": 62,
        "sprite_path": "weapons/hyper/dimensional_nexus.png"
    },
    
    # Legendary Tier Weapons (Money Only)
    "legendary_godslayer_excalibur": {
        "id": "legendary_godslayer_excalibur",
        "name": "Godslayer Excalibur",
        "description": "The ultimate sword capable of slaying gods themselves",
        "type": "blade",
        "rarity": "legendary",
        "cost": 29.99,  # USD only
        "payment_only": True,
        "compatible_classes": ["knight", "dragon_knight", "paladin"],
        "stats": {
            "attack": 350,
            "crit_chance": 0.50,
            "crit_damage": 3.0,
            "divine_damage": True
        },
        "special_effect": "Divine Judgment: 40% chance to instantly defeat non-boss enemies, 25% chance to deal massive damage to bosses",
        "unlock_level": 80,
        "sprite_path": "weapons/legendary/godslayer_excalibur.png"
    },
    
    "legendary_worldender_bow": {
        "id": "legendary_worldender_bow",
        "name": "Worldender Bow",
        "description": "Bow of legends that can pierce through worlds",
        "type": "bow",
        "rarity": "legendary",
        "cost": 24.99,  # USD only
        "payment_only": True,
        "compatible_classes": ["archer", "ranger"],
        "stats": {
            "attack": 320,
            "range": 10,
            "piercing": True,
            "world_piercing": True
        },
        "special_effect": "Worldender Shot: Ignores all defenses and barriers, 35% chance to hit all enemies",
        "unlock_level": 75,
        "sprite_path": "weapons/legendary/worldender_bow.png"
    },
    
    "legendary_omniscience_staff": {
        "id": "legendary_omniscience_staff",
        "name": "Staff of Omniscience",
        "description": "Staff containing all knowledge of magic in the universe",
        "type": "staff",
        "rarity": "legendary",
        "cost": 27.99,  # USD only
        "payment_only": True,
        "compatible_classes": ["mage", "cosmic_mage", "wizard"],
        "stats": {
            "attack": 280,
            "magic": 400,
            "mana_regen": 3.0,
            "spell_power": 2.0,
            "knowledge": True
        },
        "special_effect": "Omniscience: Can cast any spell in the game, 30% chance spells cost no mana",
        "unlock_level": 85,
        "sprite_path": "weapons/legendary/omniscience_staff.png"
    },
    
    "legendary_void_reaper": {
        "id": "legendary_void_reaper",
        "name": "Void Reaper",
        "description": "Scythe that harvests souls from the void itself",
        "type": "reaper",
        "rarity": "legendary",
        "cost": 26.99,  # USD only
        "payment_only": True,
        "compatible_classes": ["assassin", "void_assassin", "death_knight"],
        "stats": {
            "attack": 330,
            "life_steal": 0.5,
            "void_damage": True,
            "soul_harvest": True
        },
        "special_effect": "Soul Harvest: Each kill permanently increases attack by 1, 20% chance to instantly kill damaged enemies",
        "unlock_level": 78,
        "sprite_path": "weapons/legendary/void_reaper.png"
    }
}

# === PREMIUM SKINS ===

PREMIUM_SKINS = {
    # VIP Exclusive Skins
    "dragon_lord_arin_vip": {
        "id": "dragon_lord_arin_vip",
        "name": "Dragon Lord Arin - Infernal Majesty",
        "description": "VIP exclusive skin with enhanced fire effects and stat bonuses",
        "hero_id": "dragon_lord_arin",
        "purchase_type": "vip_exclusive",
        "cost": 16.00,  # Monthly VIP subscription
        "stat_bonuses": {
            "attack": 20,
            "magic": 25,
            "fire_damage": 0.10  # +10% fire damage
        },
        "visual_effects": [
            "Flaming aura around character",
            "Enhanced fire breath animation",
            "Dragon wings glow with inner fire",
            "Footsteps leave burning trails"
        ],
        "enhanced_skills": {
            "dragons_breath": "+10% damage",
            "fire_immunity": "Also heals 50% more from fire"
        },
        "sprite_path": "skins/vip/dragon_lord_infernal.png"
    },
    
    "cosmic_emperor_arin_vip": {
        "id": "cosmic_emperor_arin_vip",
        "name": "Cosmic Emperor Arin - Stellar Divine",
        "description": "VIP exclusive skin with cosmic energy effects and enhanced abilities",
        "hero_id": "cosmic_emperor_arin",
        "purchase_type": "vip_exclusive", 
        "cost": 16.00,  # Monthly VIP subscription
        "stat_bonuses": {
            "magic": 30,
            "mana_regen": 1.0,
            "cosmic_damage": 0.15  # +15% cosmic damage
        },
        "visual_effects": [
            "Swirling galaxy aura",
            "Stellar crown with moving constellations",
            "Cosmic energy crackling around hands",
            "Space distortion effects when moving"
        ],
        "enhanced_skills": {
            "cosmic_storm": "+15% damage, larger area",
            "time_manipulation": "Reduced cooldown by 1 turn"
        },
        "sprite_path": "skins/vip/cosmic_emperor_stellar.png"
    },
    
    # Gem-Purchasable Skins (Cosmetic Only)
    "knight_arin_shadow": {
        "id": "knight_arin_shadow",
        "name": "Shadow Knight Arin",
        "description": "Dark themed variant with shadow effects",
        "hero_id": "knight_arin",
        "purchase_type": "gems",
        "cost": 2500,  # gems
        "stat_bonuses": {},  # Cosmetic only
        "visual_effects": [
            "Dark purple/black armor",
            "Shadow particles trailing behind",
            "Glowing purple eyes",
            "Dark energy weapon effects"
        ],
        "sprite_path": "skins/gems/knight_arin_shadow.png"
    },
    
    "knight_arin_golden": {
        "id": "knight_arin_golden",
        "name": "Golden Knight Arin",
        "description": "Majestic golden armor with royal effects",
        "hero_id": "knight_arin",
        "purchase_type": "gems",
        "cost": 3000,  # gems
        "stat_bonuses": {},  # Cosmetic only
        "visual_effects": [
            "Brilliant golden armor",
            "Golden light particles",
            "Royal cape with heraldic symbols",
            "Shimmering weapon effects"
        ],
        "sprite_path": "skins/gems/knight_arin_golden.png"
    },
    
    "mage_arin_arcane": {
        "id": "mage_arin_arcane",
        "name": "Arcane Scholar Arin",
        "description": "Mystical robes with floating tome and arcane symbols",
        "hero_id": "mage_arin",
        "purchase_type": "gems",
        "cost": 2800,  # gems
        "stat_bonuses": {},  # Cosmetic only
        "visual_effects": [
            "Flowing mystical robes",
            "Floating spell tome",
            "Arcane symbols orbiting around character",
            "Magical runes appearing during spells"
        ],
        "sprite_path": "skins/gems/mage_arin_arcane.png"
    },
    
    "archer_arin_forest": {
        "id": "archer_arin_forest",
        "name": "Forest Guardian Arin",
        "description": "Nature-themed skin with leaf and vine effects",
        "hero_id": "archer_arin",
        "purchase_type": "gems",
        "cost": 2200,  # gems
        "stat_bonuses": {},  # Cosmetic only
        "visual_effects": [
            "Green leather armor with leaf patterns",
            "Vine-wrapped bow",
            "Leaf particles when moving",
            "Nature magic arrow effects"
        ],
        "sprite_path": "skins/gems/archer_arin_forest.png"
    }
}

# === PREMIUM BUNDLES ===

PREMIUM_BUNDLES = {
    "ultimate_power_bundle": {
        "id": "ultimate_power_bundle",
        "name": "Ultimate Power Bundle",
        "description": "Complete legendary collection with maximum power",
        "cost": 79.99,  # USD
        "savings": 25.00,  # How much saved vs buying individually
        "contents": [
            {"type": "hero", "id": "dragon_lord_arin"},
            {"type": "hero", "id": "cosmic_emperor_arin"},
            {"type": "weapon", "id": "legendary_godslayer_excalibur"},
            {"type": "weapon", "id": "legendary_worldender_bow"},
            {"type": "weapon", "id": "legendary_omniscience_staff"},
            {"type": "skin", "id": "dragon_lord_arin_vip"},
            {"type": "skin", "id": "cosmic_emperor_arin_vip"},
            {"type": "currency", "amount": 10000, "currency": "gems"},
            {"type": "currency", "amount": 50000, "currency": "gold"}
        ],
        "bonus_items": [
            {"type": "title", "name": "Legendary Champion"},
            {"type": "achievement", "name": "Ultimate Power"}
        ],
        "sprite_path": "bundles/ultimate_power.png"
    },
    
    "starter_champion_bundle": {
        "id": "starter_champion_bundle",
        "name": "Champion Starter Bundle",
        "description": "Perfect for new players wanting to get ahead",
        "cost": 9.99,  # USD
        "contents": [
            {"type": "hero", "id": "pyromancer_hero"},
            {"type": "weapon", "id": "elite_cosmic_blade"},
            {"type": "skin", "id": "knight_arin_golden"},
            {"type": "currency", "amount": 5000, "currency": "gems"},
            {"type": "currency", "amount": 20000, "currency": "gold"}
        ],
        "sprite_path": "bundles/starter_champion.png"
    },
    
    "legendary_weapons_bundle": {
        "id": "legendary_weapons_bundle",
        "name": "Legendary Weapons Collection",
        "description": "All legendary weapons for the ultimate arsenal",
        "cost": 69.99,  # USD
        "savings": 18.96,  # Savings vs individual purchase
        "contents": [
            {"type": "weapon", "id": "legendary_godslayer_excalibur"},
            {"type": "weapon", "id": "legendary_worldender_bow"},
            {"type": "weapon", "id": "legendary_omniscience_staff"},
            {"type": "weapon", "id": "legendary_void_reaper"}
        ],
        "sprite_path": "bundles/legendary_weapons.png"
    }
}

# === UTILITY FUNCTIONS ===

def get_premium_content_by_type(content_type: str) -> Dict[str, Any]:
    """Get all premium content of a specific type"""
    content_map = {
        "hero": PREMIUM_HEROES,
        "weapon": PREMIUM_WEAPONS,
        "skin": PREMIUM_SKINS,
        "bundle": PREMIUM_BUNDLES
    }
    return content_map.get(content_type, {})

def get_premium_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific premium item by its ID"""
    all_content = {
        **PREMIUM_HEROES,
        **PREMIUM_WEAPONS,
        **PREMIUM_SKINS,
        **PREMIUM_BUNDLES
    }
    return all_content.get(item_id)

def get_vip_exclusive_items() -> List[Dict[str, Any]]:
    """Get all VIP exclusive items"""
    vip_items = []
    
    # Add VIP skins
    for skin in PREMIUM_SKINS.values():
        if skin.get("purchase_type") == "vip_exclusive":
            vip_items.append(skin)
    
    return vip_items

def get_money_only_items() -> List[Dict[str, Any]]:
    """Get all items that can only be purchased with real money"""
    money_items = []
    
    # Add payment-only weapons
    for weapon in PREMIUM_WEAPONS.values():
        if weapon.get("payment_only", False):
            money_items.append(weapon)
    
    # Add bundles (all require money)
    for bundle in PREMIUM_BUNDLES.values():
        money_items.append(bundle)
    
    return money_items

def get_gem_purchasable_items() -> List[Dict[str, Any]]:
    """Get all items that can be purchased with gems"""
    gem_items = []
    
    # Add gem heroes
    for hero in PREMIUM_HEROES.values():
        if hero.get("purchase_type") == "gems":
            gem_items.append(hero)
    
    # Add gem weapons
    for weapon in PREMIUM_WEAPONS.values():
        if not weapon.get("payment_only", False):
            gem_items.append(weapon)
    
    # Add gem skins
    for skin in PREMIUM_SKINS.values():
        if skin.get("purchase_type") == "gems":
            gem_items.append(skin)
    
    return gem_items

def calculate_bundle_savings(bundle_id: str) -> float:
    """Calculate how much money is saved by buying a bundle vs individual items"""
    bundle = PREMIUM_BUNDLES.get(bundle_id)
    if not bundle:
        return 0.0
    
    total_individual_cost = 0.0
    for item in bundle.get("contents", []):
        if item["type"] == "hero":
            hero = PREMIUM_HEROES.get(item["id"], {})
            if hero.get("payment_only", False):
                total_individual_cost += hero.get("cost", 0)
        elif item["type"] == "weapon":
            weapon = PREMIUM_WEAPONS.get(item["id"], {})
            if weapon.get("payment_only", False):
                total_individual_cost += weapon.get("cost", 0)
    
    bundle_cost = bundle.get("cost", 0)
    return max(0.0, total_individual_cost - bundle_cost)

# === PREMIUM CONTENT VALIDATION ===

def validate_premium_content():
    """Validate all premium content data for consistency"""
    errors = []
    
    # Check required fields for heroes
    for hero_id, hero in PREMIUM_HEROES.items():
        required_fields = ["id", "name", "description", "class", "rarity", "cost", "stats", "abilities"]
        for field in required_fields:
            if field not in hero:
                errors.append(f"Hero {hero_id} missing required field: {field}")
    
    # Check required fields for weapons
    for weapon_id, weapon in PREMIUM_WEAPONS.items():
        required_fields = ["id", "name", "description", "type", "rarity", "cost", "stats"]
        for field in required_fields:
            if field not in weapon:
                errors.append(f"Weapon {weapon_id} missing required field: {field}")
    
    # Check required fields for skins
    for skin_id, skin in PREMIUM_SKINS.items():
        required_fields = ["id", "name", "description", "hero_id", "purchase_type", "cost"]
        for field in required_fields:
            if field not in skin:
                errors.append(f"Skin {skin_id} missing required field: {field}")
    
    return errors

# Validate content on import
_validation_errors = validate_premium_content()
if _validation_errors:
    import logging
    logging.warning(f"Premium content validation errors: {_validation_errors}")