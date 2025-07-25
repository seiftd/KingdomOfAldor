"""
Kingdom of Aldoria - Player Entity
The main character with stats, skills, and equipment
"""

import pygame
import math
from typing import Dict, Any, Optional, List
from ..core.config import GameConfig

class Player:
    """The player character in Kingdom of Aldoria"""
    
    def __init__(self, save_data: Dict[str, Any]):
        """Initialize the player from save data"""
        
        # Basic info
        self.name = save_data.get("name", "Arin")
        self.level = save_data.get("level", 1)
        self.experience = save_data.get("experience", 0)
        
        # Currency
        self.gold = save_data.get("gold", 100)
        self.gems = save_data.get("gems", 50)
        
        # Stamina system
        self.stamina = save_data.get("stamina", GameConfig.MAX_STAMINA_DEFAULT)
        self.max_stamina = save_data.get("max_stamina", GameConfig.MAX_STAMINA_DEFAULT)
        self.last_stamina_update = save_data.get("last_stamina_update", 0)
        
        # Equipment
        self.current_skin = save_data.get("current_skin", "default_knight")
        self.current_weapon = save_data.get("current_weapon", "bronze_sword")
        self.unlocked_skins = save_data.get("unlocked_skins", ["default_knight"])
        self.unlocked_weapons = save_data.get("unlocked_weapons", ["bronze_sword"])
        
        # Stats
        stats_data = save_data.get("stats", {})
        self.stats = {
            "hp": stats_data.get("hp", 100),
            "max_hp": stats_data.get("max_hp", 100),
            "attack": stats_data.get("attack", 50),
            "defense": stats_data.get("defense", 25),
            "speed": stats_data.get("speed", 100)
        }
        
        # Skills and cooldowns
        self.skill_cooldowns = save_data.get("skill_cooldowns", {})
        
        # Combat state
        self.in_combat = False
        self.target_enemy = None
        self.last_attack_time = 0
        self.attack_cooldown = 1.0  # seconds
        
        # Position and animation
        self.x = 0
        self.y = 0
        self.animation_time = 0
        self.current_animation = "idle"
        self.facing_right = True
        
        # Visual effects
        self.damage_numbers = []
        self.status_effects = {}
        
        # Skill system
        self.available_skills = self._get_available_skills()
        
        # Asset references
        self.sprite = None
        self.weapon_sprite = None
        
    def _get_available_skills(self) -> List[str]:
        """Get list of available skills based on equipment"""
        skills = []
        
        # Get skill from current skin
        skin_data = GameConfig.CHARACTER_SKINS.get(self.current_skin, {})
        skin_skill = skin_data.get("skill")
        if skin_skill:
            skills.append(skin_skill)
        
        return skills
    
    def update(self, dt: float):
        """Update player state"""
        # Update animation
        self.animation_time += dt
        
        # Update skill cooldowns
        for skill_name in list(self.skill_cooldowns.keys()):
            self.skill_cooldowns[skill_name] -= dt
            if self.skill_cooldowns[skill_name] <= 0:
                del self.skill_cooldowns[skill_name]
        
        # Update status effects
        for effect_name in list(self.status_effects.keys()):
            self.status_effects[effect_name]["duration"] -= dt
            if self.status_effects[effect_name]["duration"] <= 0:
                self._remove_status_effect(effect_name)
        
        # Update damage numbers
        for damage_number in self.damage_numbers[:]:
            damage_number["y"] -= 30 * dt  # Float upward
            damage_number["alpha"] -= 255 * dt  # Fade out
            damage_number["time"] += dt
            
            if damage_number["time"] > 1.0:  # Remove after 1 second
                self.damage_numbers.remove(damage_number)
        
        # Update combat cooldown
        if self.last_attack_time > 0:
            self.last_attack_time -= dt
    
    def render(self, screen: pygame.Surface, camera_offset: tuple = (0, 0)):
        """Render the player"""
        render_x = self.x - camera_offset[0]
        render_y = self.y - camera_offset[1]
        
        # Draw player sprite
        if self.sprite:
            # Apply animation transformations
            sprite_to_draw = self.sprite
            
            # Flip sprite if facing left
            if not self.facing_right:
                sprite_to_draw = pygame.transform.flip(self.sprite, True, False)
            
            # Apply idle animation bounce
            if self.current_animation == "idle":
                bounce_offset = math.sin(self.animation_time * 3) * 2
                render_y += bounce_offset
            
            # Draw shadow
            shadow_color = (0, 0, 0, 100)
            shadow_surface = pygame.Surface(self.sprite.get_size(), pygame.SRCALPHA)
            shadow_surface.fill(shadow_color)
            screen.blit(shadow_surface, (render_x + 2, render_y + self.sprite.get_height() - 5))
            
            # Draw main sprite
            screen.blit(sprite_to_draw, (render_x, render_y))
        else:
            # Fallback rectangle if no sprite
            player_rect = pygame.Rect(render_x, render_y, 32, 32)
            pygame.draw.rect(screen, (100, 150, 200), player_rect)
        
        # Draw weapon if equipped
        if self.weapon_sprite:
            weapon_x = render_x + (20 if self.facing_right else -10)
            weapon_y = render_y + 10
            
            weapon_to_draw = self.weapon_sprite
            if not self.facing_right:
                weapon_to_draw = pygame.transform.flip(self.weapon_sprite, True, False)
            
            screen.blit(weapon_to_draw, (weapon_x, weapon_y))
        
        # Draw health bar
        self._draw_health_bar(screen, render_x, render_y - 10)
        
        # Draw status effects
        self._draw_status_effects(screen, render_x, render_y - 20)
        
        # Draw damage numbers
        self._draw_damage_numbers(screen, camera_offset)
    
    def _draw_health_bar(self, screen: pygame.Surface, x: int, y: int):
        """Draw player health bar"""
        bar_width = 40
        bar_height = 6
        
        # Background
        bg_rect = pygame.Rect(x - bar_width // 2, y, bar_width, bar_height)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect)
        
        # Health fill
        health_ratio = self.stats["hp"] / max(1, self.stats["max_hp"])
        fill_width = int(bar_width * health_ratio)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(x - bar_width // 2, y, fill_width, bar_height)
            
            # Color based on health percentage
            if health_ratio > 0.6:
                color = (100, 200, 100)  # Green
            elif health_ratio > 0.3:
                color = (200, 200, 100)  # Yellow
            else:
                color = (200, 100, 100)  # Red
                
            pygame.draw.rect(screen, color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, (200, 200, 200), bg_rect, 1)
    
    def _draw_status_effects(self, screen: pygame.Surface, x: int, y: int):
        """Draw active status effects"""
        effect_x = x - 20
        for effect_name, effect_data in self.status_effects.items():
            # Draw effect icon (simplified as colored circle)
            effect_color = effect_data.get("color", (255, 255, 255))
            pygame.draw.circle(screen, effect_color, (effect_x, y), 6)
            pygame.draw.circle(screen, (0, 0, 0), (effect_x, y), 6, 1)
            effect_x += 15
    
    def _draw_damage_numbers(self, screen: pygame.Surface, camera_offset: tuple):
        """Draw floating damage numbers"""
        font = pygame.font.Font(None, 24)
        
        for damage_number in self.damage_numbers:
            if damage_number["alpha"] > 0:
                # Create text surface
                text = str(damage_number["damage"])
                color = (*damage_number["color"], int(damage_number["alpha"]))
                
                # Create surface with alpha
                text_surface = font.render(text, True, damage_number["color"])
                text_surface.set_alpha(int(damage_number["alpha"]))
                
                # Draw at floating position
                render_x = damage_number["x"] - camera_offset[0]
                render_y = damage_number["y"] - camera_offset[1]
                screen.blit(text_surface, (render_x, render_y))
    
    def attack(self, target) -> bool:
        """Perform an attack on target"""
        if self.last_attack_time > 0:
            return False  # Still on cooldown
        
        # Calculate damage
        base_damage = self.get_total_attack()
        
        # Add some randomness (80-120% of base damage)
        import random
        damage_multiplier = random.uniform(0.8, 1.2)
        final_damage = int(base_damage * damage_multiplier)
        
        # Apply attack to target
        target.take_damage(final_damage, self)
        
        # Set cooldown
        self.last_attack_time = self.attack_cooldown
        
        # Change animation
        self.current_animation = "attack"
        
        return True
    
    def use_skill(self, skill_name: str) -> bool:
        """Use a skill if available and not on cooldown"""
        if skill_name not in self.available_skills:
            return False
        
        if skill_name in self.skill_cooldowns:
            return False  # Still on cooldown
        
        # Execute skill effect
        success = self._execute_skill(skill_name)
        
        if success:
            # Set cooldown
            cooldown_time = GameConfig.SKILL_COOLDOWNS.get(skill_name, 30.0)
            self.skill_cooldowns[skill_name] = cooldown_time
        
        return success
    
    def _execute_skill(self, skill_name: str) -> bool:
        """Execute the effect of a skill"""
        if skill_name == "speed_boost":
            # Increase movement speed temporarily
            self.apply_status_effect("speed_boost", {
                "duration": GameConfig.SKILL_DURATIONS["speed_boost"],
                "effect": "speed_multiplier",
                "value": 1.5,
                "color": (100, 150, 255)
            })
            return True
            
        elif skill_name == "instant_heal":
            # Heal 30% of max HP
            heal_amount = int(self.stats["max_hp"] * 0.3)
            self.heal(heal_amount)
            return True
            
        elif skill_name == "damage_doubler":
            # Double damage for duration
            self.apply_status_effect("damage_doubler", {
                "duration": GameConfig.SKILL_DURATIONS["damage_doubler"],
                "effect": "damage_multiplier",
                "value": 2.0,
                "color": (255, 100, 100)
            })
            return True
            
        elif skill_name == "time_rewind":
            # Restore to previous state (simplified implementation)
            self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"] + 50)
            return True
        
        return False
    
    def apply_status_effect(self, effect_name: str, effect_data: Dict[str, Any]):
        """Apply a status effect"""
        self.status_effects[effect_name] = effect_data.copy()
    
    def _remove_status_effect(self, effect_name: str):
        """Remove a status effect"""
        if effect_name in self.status_effects:
            del self.status_effects[effect_name]
    
    def take_damage(self, damage: int, source=None) -> int:
        """Take damage and return actual damage taken"""
        # Apply defense
        defense_reduction = self.get_total_defense() * 0.5
        actual_damage = max(1, damage - defense_reduction)
        
        # Apply damage
        self.stats["hp"] = max(0, self.stats["hp"] - actual_damage)
        
        # Create damage number
        self.add_damage_number(actual_damage, (255, 100, 100))
        
        # Check for death
        if self.stats["hp"] <= 0:
            self.on_death()
        
        return int(actual_damage)
    
    def heal(self, amount: int) -> int:
        """Heal the player and return actual healing done"""
        old_hp = self.stats["hp"]
        self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"] + amount)
        actual_healing = self.stats["hp"] - old_hp
        
        if actual_healing > 0:
            # Create healing number
            self.add_damage_number(actual_healing, (100, 255, 100), "+")
        
        return actual_healing
    
    def add_damage_number(self, amount: int, color: tuple, prefix: str = ""):
        """Add a floating damage number"""
        self.damage_numbers.append({
            "damage": f"{prefix}{amount}",
            "x": self.x + 16,  # Center of sprite
            "y": self.y - 10,
            "color": color,
            "alpha": 255,
            "time": 0
        })
    
    def on_death(self):
        """Handle player death"""
        # Reset animation
        self.current_animation = "death"
        
        # Could trigger game over screen or revival options
        print(f"{self.name} has fallen!")
    
    def get_total_attack(self) -> int:
        """Get total attack including weapon and buffs"""
        base_attack = self.stats["attack"]
        
        # Add weapon damage
        weapon_data = GameConfig.WEAPON_DATA.get(self.current_weapon, {})
        weapon_damage = weapon_data.get("damage", 0)
        
        total_attack = base_attack + weapon_damage
        
        # Apply status effect multipliers
        if "damage_doubler" in self.status_effects:
            total_attack *= self.status_effects["damage_doubler"]["value"]
        
        return int(total_attack)
    
    def get_total_defense(self) -> int:
        """Get total defense including equipment and buffs"""
        base_defense = self.stats["defense"]
        
        # Could add armor bonuses here
        
        return base_defense
    
    def get_total_speed(self) -> int:
        """Get total speed including buffs"""
        base_speed = self.stats["speed"]
        
        # Apply status effect multipliers
        if "speed_boost" in self.status_effects:
            base_speed *= self.status_effects["speed_boost"]["value"]
        
        return int(base_speed)
    
    def can_use_skill(self, skill_name: str) -> bool:
        """Check if a skill can be used"""
        return (skill_name in self.available_skills and 
                skill_name not in self.skill_cooldowns)
    
    def get_skill_cooldown(self, skill_name: str) -> float:
        """Get remaining cooldown for a skill"""
        return self.skill_cooldowns.get(skill_name, 0.0)
    
    def is_alive(self) -> bool:
        """Check if player is alive"""
        return self.stats["hp"] > 0
    
    def set_position(self, x: int, y: int):
        """Set player position"""
        self.x = x
        self.y = y
    
    def move(self, dx: int, dy: int):
        """Move player by offset"""
        self.x += dx
        self.y += dy
        
        # Update facing direction
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False
    
    def load_sprites(self, asset_manager):
        """Load player sprites from asset manager"""
        # Load character sprite
        self.sprite = asset_manager.get_character_image(self.current_skin)
        
        # Load weapon sprite
        self.weapon_sprite = asset_manager.get_weapon_image(self.current_weapon)
    
    def change_skin(self, new_skin: str, asset_manager) -> bool:
        """Change player skin if unlocked"""
        if new_skin in self.unlocked_skins:
            self.current_skin = new_skin
            self.available_skills = self._get_available_skills()
            self.load_sprites(asset_manager)
            return True
        return False
    
    def change_weapon(self, new_weapon: str, asset_manager) -> bool:
        """Change player weapon if unlocked"""
        if new_weapon in self.unlocked_weapons:
            self.current_weapon = new_weapon
            self.load_sprites(asset_manager)
            return True
        return False
    
    def get_save_data(self) -> Dict[str, Any]:
        """Get data to save to file"""
        return {
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "gems": self.gems,
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
            "last_stamina_update": self.last_stamina_update,
            "current_skin": self.current_skin,
            "current_weapon": self.current_weapon,
            "unlocked_skins": self.unlocked_skins,
            "unlocked_weapons": self.unlocked_weapons,
            "skill_cooldowns": self.skill_cooldowns,
            "stats": self.stats
        }