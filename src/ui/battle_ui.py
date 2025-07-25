"""
Kingdom of Aldoria - Battle State
Turn-based combat with skills, animations, and RPG mechanics
"""

import pygame
import logging
import random
import time
from typing import Optional, Dict, Any, Tuple

from ..core.state_manager import GameState
from ..core.config import Config, GameStates, SkillTypes

class BattleState(GameState):
    """Battle state for turn-based combat"""
    
    def __init__(self, game):
        """Initialize battle state"""
        super().__init__(game)
        
        # Battle data
        self.world_id = 0
        self.stage_num = 1
        self.is_boss_battle = False
        
        # Combat participants
        self.player = None
        self.enemy = None
        
        # Battle state
        self.battle_phase = "start"  # start, player_turn, enemy_turn, victory, defeat
        self.turn_timer = 0.0
        self.action_selected = None
        
        # UI elements
        self.action_buttons = {}
        self.skill_buttons = {}
        
        # Animation
        self.damage_numbers = []
        self.effect_particles = []
        
        # Battle results
        self.victory_rewards = {}
        
        self.logger.info("BattleState initialized")
    
    def enter(self, **kwargs):
        """Enter the battle state"""
        self.world_id = kwargs.get('world', 0)
        self.stage_num = kwargs.get('stage', 1)
        self.is_boss_battle = (self.stage_num % Config.BOSS_STAGE_INTERVAL) == 0
        
        self.logger.info(f"Starting battle: World {self.world_id + 1}, Stage {self.stage_num}")
        
        # Initialize battle
        self._setup_battle()
        
        # Setup UI
        self._setup_ui()
        
        # Play battle music
        asset_manager = self.game.get_system('asset_manager')
        if asset_manager:
            if self.is_boss_battle:
                asset_manager.play_music("boss_battle_music", volume=0.7)
            else:
                asset_manager.play_music("battle_music", volume=0.6)
    
    def exit(self):
        """Exit the battle state"""
        self.logger.info("Exiting battle")
    
    def update(self, dt: float):
        """Update battle logic"""
        # Update turn timer
        self.turn_timer += dt
        
        # Update battle phase
        if self.battle_phase == "start":
            self._update_battle_start(dt)
        elif self.battle_phase == "player_turn":
            self._update_player_turn(dt)
        elif self.battle_phase == "enemy_turn":
            self._update_enemy_turn(dt)
        elif self.battle_phase == "victory":
            self._update_victory_phase(dt)
        elif self.battle_phase == "defeat":
            self._update_defeat_phase(dt)
        
        # Update animations
        self._update_damage_numbers(dt)
        self._update_particles(dt)
    
    def render(self, screen: pygame.Surface):
        """Render the battle scene"""
        # Background
        self._render_background(screen)
        
        # Battle participants
        self._render_combatants(screen)
        
        # Health bars
        self._render_health_bars(screen)
        
        # Action UI
        if self.battle_phase in ["player_turn"]:
            self._render_action_ui(screen)
        
        # Battle info
        self._render_battle_info(screen)
        
        # Animations
        self._render_damage_numbers(screen)
        self._render_particles(screen)
        
        # Turn indicator
        self._render_turn_indicator(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle battle events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.battle_phase == "player_turn":
                self._handle_action_selection(event.pos)
            elif self.battle_phase in ["victory", "defeat"]:
                self._handle_result_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.battle_phase in ["victory", "defeat"]:
                    self._return_to_world_map()
            elif self.battle_phase == "player_turn":
                self._handle_keyboard_action(event.key)
    
    def _setup_battle(self):
        """Initialize battle participants and data"""
        # Setup player
        save_manager = self.game.get_system('save_manager')
        self.player = self._create_player_combatant(save_manager)
        
        # Setup enemy
        self.enemy = self._create_enemy_combatant()
        
        # Initialize battle state
        self.battle_phase = "start"
        self.turn_timer = 0.0
        self.damage_numbers = []
        self.effect_particles = []
    
    def _create_player_combatant(self, save_manager) -> Dict[str, Any]:
        """Create player combatant data"""
        if not save_manager:
            # Default stats if no save manager
            return {
                'name': 'Arin',
                'level': 1,
                'max_hp': 100,
                'current_hp': 100,
                'attack': 10,
                'defense': 5,
                'speed': 8,
                'skills': ['speed_boost'],
                'position': (200, 400),
                'sprite': None
            }
        
        # Load from save data
        level = save_manager.get_player_data("player.level") or 1
        base_hp = save_manager.get_player_data("player.max_hp") or Config.PLAYER_START_HP
        base_attack = save_manager.get_player_data("player.attack") or Config.PLAYER_START_ATTACK
        base_defense = save_manager.get_player_data("player.defense") or Config.PLAYER_START_DEFENSE
        base_speed = save_manager.get_player_data("player.speed") or Config.PLAYER_START_SPEED
        
        # Apply level scaling
        level_multiplier = 1 + (level - 1) * Config.STAT_INCREASE_PER_LEVEL
        
        return {
            'name': save_manager.get_player_data("player.name") or 'Arin',
            'level': level,
            'max_hp': int(base_hp * level_multiplier),
            'current_hp': int(base_hp * level_multiplier),
            'attack': int(base_attack * level_multiplier),
            'defense': int(base_defense * level_multiplier),
            'speed': int(base_speed * level_multiplier),
            'skills': self._get_available_skills(save_manager),
            'position': (200, 400),
            'sprite': None,
            'effects': {}  # Active effects like speed boost
        }
    
    def _create_enemy_combatant(self) -> Dict[str, Any]:
        """Create enemy combatant based on world and stage"""
        # Base enemy stats
        base_hp = 80
        base_attack = 8
        base_defense = 3
        base_speed = 6
        
        # Scale based on stage and world
        stage_multiplier = (Config.ENEMY_POWER_SCALE_PER_STAGE ** (self.stage_num - 1))
        world_multiplier = 1 + (self.world_id * 0.2)
        
        total_multiplier = stage_multiplier * world_multiplier
        
        # Boss multiplier
        if self.is_boss_battle:
            total_multiplier *= Config.BOSS_POWER_MULTIPLIER
        
        # Get enemy type based on world
        enemy_data = self._get_enemy_data()
        
        return {
            'name': enemy_data['name'],
            'type': enemy_data['type'],
            'max_hp': int(base_hp * total_multiplier),
            'current_hp': int(base_hp * total_multiplier),
            'attack': int(base_attack * total_multiplier),
            'defense': int(base_defense * total_multiplier),
            'speed': int(base_speed * total_multiplier),
            'position': (Config.SCREEN_WIDTH - 300, 350),
            'sprite': None,
            'skills': enemy_data.get('skills', []),
            'effects': {}
        }
    
    def _get_enemy_data(self) -> Dict[str, Any]:
        """Get enemy data based on world and stage"""
        # World-specific enemies
        world_enemies = [
            # Forest of Shadows
            [
                {'name': 'Shadow Wolf', 'type': 'normal', 'skills': ['howl']},
                {'name': 'Dark Sprite', 'type': 'normal', 'skills': ['dark_bolt']},
                {'name': 'Forest Guardian', 'type': 'boss', 'skills': ['nature_wrath', 'healing_roots']}
            ],
            # Desert of Souls
            [
                {'name': 'Sand Scorpion', 'type': 'normal', 'skills': ['poison_sting']},
                {'name': 'Desert Nomad', 'type': 'normal', 'skills': ['sand_storm']},
                {'name': 'Sand Pharaoh', 'type': 'boss', 'skills': ['mummy_curse', 'golden_strike']}
            ],
            # Ice Peaks
            [
                {'name': 'Ice Wolf', 'type': 'normal', 'skills': ['frost_bite']},
                {'name': 'Frost Giant', 'type': 'normal', 'skills': ['ice_throw']},
                {'name': 'Ice Yeti', 'type': 'boss', 'skills': ['blizzard', 'ice_armor']}
            ]
        ]
        
        # Extend pattern for other worlds
        while len(world_enemies) <= self.world_id:
            world_enemies.append([
                {'name': f'World {len(world_enemies)} Enemy', 'type': 'normal', 'skills': ['basic_attack']},
                {'name': f'World {len(world_enemies)} Elite', 'type': 'normal', 'skills': ['power_strike']},
                {'name': f'World {len(world_enemies)} Boss', 'type': 'boss', 'skills': ['ultimate_attack']}
            ])
        
        enemies = world_enemies[self.world_id]
        
        if self.is_boss_battle:
            return enemies[2]  # Boss enemy
        else:
            return random.choice(enemies[:2])  # Normal enemies
    
    def _get_available_skills(self, save_manager) -> list:
        """Get player's available skills"""
        skills = []
        
        # Check each skill
        for skill_type in [SkillTypes.SPEED_BOOST, SkillTypes.INSTANT_HEAL, 
                          SkillTypes.TIME_REWIND, SkillTypes.DAMAGE_DOUBLER]:
            skill_data = save_manager.get_player_data(f"skills.{skill_type}")
            if skill_data and skill_data.get('unlocked', False):
                skills.append(skill_type)
        
        return skills
    
    def _setup_ui(self):
        """Setup battle UI elements"""
        # Action buttons
        button_width = 120
        button_height = 50
        button_spacing = 10
        
        actions = ['Attack', 'Skill', 'Defend']
        start_x = (Config.SCREEN_WIDTH - (len(actions) * (button_width + button_spacing) - button_spacing)) // 2
        start_y = Config.SCREEN_HEIGHT - 80
        
        for i, action in enumerate(actions):
            x = start_x + i * (button_width + button_spacing)
            self.action_buttons[action] = pygame.Rect(x, start_y, button_width, button_height)
        
        # Skill buttons (shown when skill is selected)
        self.skill_buttons = {}
        skills = self.player.get('skills', [])
        for i, skill in enumerate(skills):
            x = start_x + i * (button_width + button_spacing)
            y = start_y - 60
            self.skill_buttons[skill] = pygame.Rect(x, y, button_width, button_height)
    
    def _update_battle_start(self, dt: float):
        """Update battle start phase"""
        if self.turn_timer > 1.0:  # 1 second intro
            # Determine who goes first based on speed
            if self.player['speed'] >= self.enemy['speed']:
                self.battle_phase = "player_turn"
            else:
                self.battle_phase = "enemy_turn"
            self.turn_timer = 0.0
    
    def _update_player_turn(self, dt: float):
        """Update player turn"""
        # Wait for player action or timeout
        if self.turn_timer > 30.0:  # 30 second timeout
            self._execute_action('Attack')  # Default to attack
    
    def _update_enemy_turn(self, dt: float):
        """Update enemy turn"""
        if self.turn_timer > 2.0:  # 2 second AI think time
            self._execute_enemy_action()
    
    def _update_victory_phase(self, dt: float):
        """Update victory phase"""
        # Auto-advance after 3 seconds if no input
        if self.turn_timer > 3.0:
            self._apply_victory_rewards()
            self._return_to_world_map()
    
    def _update_defeat_phase(self, dt: float):
        """Update defeat phase"""
        # Auto-advance after 3 seconds if no input
        if self.turn_timer > 3.0:
            self._handle_defeat()
    
    def _render_background(self, screen: pygame.Surface):
        """Render battle background"""
        # World-specific background
        world_colors = [
            (34, 100, 34),   # Forest
            (139, 111, 78),  # Desert
            (135, 175, 235), # Ice
            (50, 25, 80),    # Dark
            (200, 180, 100), # Light
        ]
        
        if self.world_id < len(world_colors):
            bg_color = world_colors[self.world_id]
        else:
            bg_color = Config.UI_BACKGROUND
        
        # Gradient background
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            r = int(bg_color[0] * (0.5 + ratio * 0.5))
            g = int(bg_color[1] * (0.5 + ratio * 0.5))
            b = int(bg_color[2] * (0.5 + ratio * 0.5))
            
            color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(screen, color, (0, y), (Config.SCREEN_WIDTH, y))
    
    def _render_combatants(self, screen: pygame.Surface):
        """Render player and enemy sprites"""
        # Player
        player_pos = self.player['position']
        player_rect = pygame.Rect(player_pos[0] - 50, player_pos[1] - 50, 100, 100)
        
        # Player placeholder (blue rectangle with sword)
        pygame.draw.rect(screen, Config.BLUE, player_rect)
        pygame.draw.rect(screen, Config.WHITE, player_rect, 3)
        
        # Simple sword representation
        sword_points = [
            (player_pos[0] + 20, player_pos[1] - 30),
            (player_pos[0] + 30, player_pos[1] - 20),
            (player_pos[0] + 40, player_pos[1] + 10)
        ]
        pygame.draw.lines(screen, Config.SILVER, False, sword_points, 3)
        
        # Enemy
        enemy_pos = self.enemy['position']
        enemy_rect = pygame.Rect(enemy_pos[0] - 60, enemy_pos[1] - 60, 120, 120)
        
        # Enemy color based on type
        if self.is_boss_battle:
            enemy_color = Config.RED
        else:
            enemy_color = Config.PURPLE
        
        pygame.draw.rect(screen, enemy_color, enemy_rect)
        pygame.draw.rect(screen, Config.WHITE, enemy_rect, 3)
        
        # Enemy name
        font = pygame.font.Font(None, 24)
        name_text = font.render(self.enemy['name'], True, Config.WHITE)
        name_rect = name_text.get_rect(centerx=enemy_pos[0], y=enemy_pos[1] + 70)
        screen.blit(name_text, name_rect)
    
    def _render_health_bars(self, screen: pygame.Surface):
        """Render health bars for player and enemy"""
        # Player health bar
        player_hp_ratio = self.player['current_hp'] / self.player['max_hp']
        player_bar_rect = pygame.Rect(50, 50, 200, 20)
        
        pygame.draw.rect(screen, Config.DARK_GRAY, player_bar_rect)
        
        hp_fill_rect = pygame.Rect(
            player_bar_rect.x, player_bar_rect.y,
            int(player_bar_rect.width * player_hp_ratio), player_bar_rect.height
        )
        
        # Health bar color based on HP percentage
        if player_hp_ratio > 0.6:
            hp_color = Config.GREEN
        elif player_hp_ratio > 0.3:
            hp_color = Config.YELLOW
        else:
            hp_color = Config.RED
        
        pygame.draw.rect(screen, hp_color, hp_fill_rect)
        pygame.draw.rect(screen, Config.WHITE, player_bar_rect, 2)
        
        # Player HP text
        font = pygame.font.Font(None, 20)
        hp_text = f"{self.player['current_hp']}/{self.player['max_hp']}"
        hp_surface = font.render(hp_text, True, Config.WHITE)
        screen.blit(hp_surface, (player_bar_rect.x, player_bar_rect.y - 25))
        
        # Player name
        name_surface = font.render(f"Lv.{self.player['level']} {self.player['name']}", True, Config.GOLD)
        screen.blit(name_surface, (player_bar_rect.x, player_bar_rect.y - 45))
        
        # Enemy health bar
        enemy_hp_ratio = self.enemy['current_hp'] / self.enemy['max_hp']
        enemy_bar_rect = pygame.Rect(Config.SCREEN_WIDTH - 250, 50, 200, 20)
        
        pygame.draw.rect(screen, Config.DARK_GRAY, enemy_bar_rect)
        
        enemy_hp_fill = pygame.Rect(
            enemy_bar_rect.x, enemy_bar_rect.y,
            int(enemy_bar_rect.width * enemy_hp_ratio), enemy_bar_rect.height
        )
        pygame.draw.rect(screen, Config.RED, enemy_hp_fill)
        pygame.draw.rect(screen, Config.WHITE, enemy_bar_rect, 2)
        
        # Enemy HP text
        enemy_hp_text = f"{self.enemy['current_hp']}/{self.enemy['max_hp']}"
        enemy_hp_surface = font.render(enemy_hp_text, True, Config.WHITE)
        enemy_text_rect = enemy_hp_surface.get_rect(right=enemy_bar_rect.right, y=enemy_bar_rect.y - 25)
        screen.blit(enemy_hp_surface, enemy_text_rect)
    
    def _render_action_ui(self, screen: pygame.Surface):
        """Render action selection UI"""
        font = pygame.font.Font(None, 24)
        mouse_pos = pygame.mouse.get_pos()
        
        # Action buttons
        for action, rect in self.action_buttons.items():
            # Button appearance
            if rect.collidepoint(mouse_pos):
                bg_color = Config.UI_BUTTON_HOVER
                text_color = Config.GOLD
            else:
                bg_color = Config.UI_BUTTON
                text_color = Config.UI_TEXT
            
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, Config.UI_ACCENT, rect, 2)
            
            # Button text
            text_surface = font.render(action, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
        
        # Skill buttons (if skill action selected)
        if self.action_selected == 'Skill':
            for skill, rect in self.skill_buttons.items():
                if rect.collidepoint(mouse_pos):
                    bg_color = Config.UI_BUTTON_HOVER
                    text_color = Config.GOLD
                else:
                    bg_color = Config.PURPLE
                    text_color = Config.UI_TEXT
                
                pygame.draw.rect(screen, bg_color, rect)
                pygame.draw.rect(screen, Config.UI_ACCENT, rect, 2)
                
                # Skill name
                skill_name = skill.replace('_', ' ').title()
                text_surface = font.render(skill_name, True, text_color)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
    
    def _render_battle_info(self, screen: pygame.Surface):
        """Render battle information"""
        # Stage info
        font = pygame.font.Font(None, 32)
        stage_text = f"World {self.world_id + 1} - Stage {self.stage_num}"
        if self.is_boss_battle:
            stage_text += " (BOSS)"
        
        stage_surface = font.render(stage_text, True, Config.GOLD)
        stage_rect = stage_surface.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=10)
        screen.blit(stage_surface, stage_rect)
    
    def _render_turn_indicator(self, screen: pygame.Surface):
        """Render current turn indicator"""
        font = pygame.font.Font(None, 28)
        
        if self.battle_phase == "player_turn":
            turn_text = "Your Turn"
            text_color = Config.GREEN
        elif self.battle_phase == "enemy_turn":
            turn_text = "Enemy Turn"
            text_color = Config.RED
        elif self.battle_phase == "victory":
            turn_text = "VICTORY!"
            text_color = Config.GOLD
        elif self.battle_phase == "defeat":
            turn_text = "DEFEAT"
            text_color = Config.RED
        else:
            return
        
        text_surface = font.render(turn_text, True, text_color)
        text_rect = text_surface.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=Config.SCREEN_HEIGHT // 2 - 100)
        
        # Background for text
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(screen, Config.UI_PANEL, bg_rect)
        pygame.draw.rect(screen, text_color, bg_rect, 2)
        
        screen.blit(text_surface, text_rect)
    
    def _render_damage_numbers(self, screen: pygame.Surface):
        """Render floating damage numbers"""
        font = pygame.font.Font(None, 36)
        
        for damage_data in self.damage_numbers:
            alpha = int(255 * (damage_data['life'] / damage_data['max_life']))
            color = (*damage_data['color'], alpha)
            
            text_surface = font.render(str(damage_data['value']), True, damage_data['color'])
            text_surface.set_alpha(alpha)
            
            screen.blit(text_surface, damage_data['position'])
    
    def _render_particles(self, screen: pygame.Surface):
        """Render effect particles"""
        for particle in self.effect_particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (*particle['color'][:3], alpha)
            
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))
    
    def _update_damage_numbers(self, dt: float):
        """Update floating damage numbers"""
        for damage_data in self.damage_numbers[:]:
            damage_data['life'] -= dt
            damage_data['position'] = (
                damage_data['position'][0],
                damage_data['position'][1] - 50 * dt
            )
            
            if damage_data['life'] <= 0:
                self.damage_numbers.remove(damage_data)
    
    def _update_particles(self, dt: float):
        """Update effect particles"""
        for particle in self.effect_particles[:]:
            particle['life'] -= dt
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            particle['size'] *= 0.98  # Shrink over time
            
            if particle['life'] <= 0 or particle['size'] < 1:
                self.effect_particles.remove(particle)
    
    def _handle_action_selection(self, pos: Tuple[int, int]):
        """Handle action button clicks"""
        # Check action buttons
        for action, rect in self.action_buttons.items():
            if rect.collidepoint(pos):
                if action == 'Skill':
                    self.action_selected = 'Skill'
                else:
                    self._execute_action(action)
                return
        
        # Check skill buttons
        if self.action_selected == 'Skill':
            for skill, rect in self.skill_buttons.items():
                if rect.collidepoint(pos):
                    self._execute_skill(skill)
                    return
    
    def _handle_keyboard_action(self, key: int):
        """Handle keyboard shortcuts for actions"""
        if key == pygame.K_a:
            self._execute_action('Attack')
        elif key == pygame.K_s:
            self.action_selected = 'Skill'
        elif key == pygame.K_d:
            self._execute_action('Defend')
    
    def _execute_action(self, action: str):
        """Execute player action"""
        if action == 'Attack':
            self._player_attack()
        elif action == 'Defend':
            self._player_defend()
        
        self.action_selected = None
        self._end_player_turn()
    
    def _execute_skill(self, skill: str):
        """Execute player skill"""
        if skill == SkillTypes.SPEED_BOOST:
            self._use_speed_boost()
        elif skill == SkillTypes.INSTANT_HEAL:
            self._use_instant_heal()
        elif skill == SkillTypes.TIME_REWIND:
            self._use_time_rewind()
        elif skill == SkillTypes.DAMAGE_DOUBLER:
            self._use_damage_doubler()
        
        self.action_selected = None
        self._end_player_turn()
    
    def _player_attack(self):
        """Execute player attack"""
        # Calculate damage
        base_damage = self.player['attack']
        
        # Apply damage multiplier if active
        if 'damage_doubler' in self.player['effects']:
            base_damage *= 2
            del self.player['effects']['damage_doubler']
        
        # Random damage variance
        damage = int(base_damage * random.uniform(0.8, 1.2))
        
        # Apply enemy defense
        defense_reduction = self.enemy['defense'] * 0.1
        final_damage = max(1, damage - int(defense_reduction))
        
        # Critical hit chance
        if random.random() < Config.CRITICAL_HIT_CHANCE:
            final_damage = int(final_damage * Config.CRITICAL_HIT_MULTIPLIER)
            self._add_damage_number(final_damage, self.enemy['position'], Config.GOLD, "CRIT!")
        else:
            self._add_damage_number(final_damage, self.enemy['position'], Config.WHITE)
        
        # Apply damage
        self.enemy['current_hp'] = max(0, self.enemy['current_hp'] - final_damage)
        
        # Check for victory
        if self.enemy['current_hp'] <= 0:
            self.battle_phase = "victory"
            self.turn_timer = 0.0
            self._calculate_victory_rewards()
    
    def _player_defend(self):
        """Execute player defend action"""
        # Reduce incoming damage for this turn
        self.player['effects']['defending'] = True
        
        # Small heal
        heal_amount = int(self.player['max_hp'] * 0.1)
        self.player['current_hp'] = min(self.player['max_hp'], 
                                       self.player['current_hp'] + heal_amount)
        
        self._add_damage_number(heal_amount, self.player['position'], Config.GREEN, "+")
    
    def _use_speed_boost(self):
        """Use speed boost skill"""
        self.player['effects']['speed_boost'] = {
            'duration': Config.SKILL_SPEED_BOOST_DURATION,
            'remaining': Config.SKILL_SPEED_BOOST_DURATION
        }
        self._add_particles(self.player['position'], Config.BLUE, 10)
    
    def _use_instant_heal(self):
        """Use instant heal skill"""
        heal_amount = int(self.player['max_hp'] * Config.SKILL_HEAL_PERCENTAGE)
        self.player['current_hp'] = min(self.player['max_hp'], 
                                       self.player['current_hp'] + heal_amount)
        self._add_damage_number(heal_amount, self.player['position'], Config.GREEN, "+")
        self._add_particles(self.player['position'], Config.GREEN, 15)
    
    def _use_time_rewind(self):
        """Use time rewind skill"""
        # Restore HP to previous turn (simplified)
        restore_amount = int(self.player['max_hp'] * 0.2)
        self.player['current_hp'] = min(self.player['max_hp'], 
                                       self.player['current_hp'] + restore_amount)
        self._add_damage_number(restore_amount, self.player['position'], Config.PURPLE, "REWIND")
        self._add_particles(self.player['position'], Config.PURPLE, 20)
    
    def _use_damage_doubler(self):
        """Use damage doubler skill"""
        self.player['effects']['damage_doubler'] = {
            'duration': Config.SKILL_DAMAGE_DOUBLE_DURATION,
            'remaining': Config.SKILL_DAMAGE_DOUBLE_DURATION
        }
        self._add_particles(self.player['position'], Config.RED, 12)
    
    def _execute_enemy_action(self):
        """Execute enemy action (AI)"""
        # Simple AI: attack most of the time, occasionally use skills
        action_choice = random.choices(['attack', 'skill'], weights=[70, 30])[0]
        
        if action_choice == 'attack' or not self.enemy['skills']:
            self._enemy_attack()
        else:
            skill = random.choice(self.enemy['skills'])
            self._enemy_use_skill(skill)
        
        self._end_enemy_turn()
    
    def _enemy_attack(self):
        """Execute enemy attack"""
        base_damage = self.enemy['attack']
        damage = int(base_damage * random.uniform(0.8, 1.2))
        
        # Apply player defense
        if 'defending' in self.player['effects']:
            damage = int(damage * 0.5)  # Half damage when defending
            del self.player['effects']['defending']
        
        defense_reduction = self.player['defense'] * 0.1
        final_damage = max(1, damage - int(defense_reduction))
        
        self._add_damage_number(final_damage, self.player['position'], Config.RED)
        
        # Apply damage
        self.player['current_hp'] = max(0, self.player['current_hp'] - final_damage)
        
        # Check for defeat
        if self.player['current_hp'] <= 0:
            self.battle_phase = "defeat"
            self.turn_timer = 0.0
    
    def _enemy_use_skill(self, skill: str):
        """Enemy uses a skill"""
        # Simplified enemy skills
        if skill == 'howl':
            # Intimidate - reduce player attack temporarily
            pass
        elif skill == 'poison_sting':
            # Poison damage over time
            pass
        else:
            # Default to enhanced attack
            base_damage = int(self.enemy['attack'] * 1.5)
            damage = int(base_damage * random.uniform(0.9, 1.1))
            
            self._add_damage_number(damage, self.player['position'], Config.PURPLE, skill.upper())
            self.player['current_hp'] = max(0, self.player['current_hp'] - damage)
    
    def _end_player_turn(self):
        """End player turn and switch to enemy"""
        # Update effect durations
        self._update_effect_durations()
        
        if self.enemy['current_hp'] > 0:
            self.battle_phase = "enemy_turn"
            self.turn_timer = 0.0
    
    def _end_enemy_turn(self):
        """End enemy turn and switch to player"""
        if self.player['current_hp'] > 0:
            self.battle_phase = "player_turn"
            self.turn_timer = 0.0
    
    def _update_effect_durations(self):
        """Update active effect durations"""
        for effect_name in list(self.player['effects'].keys()):
            effect = self.player['effects'][effect_name]
            if isinstance(effect, dict) and 'remaining' in effect:
                effect['remaining'] -= Config.TURN_DURATION
                if effect['remaining'] <= 0:
                    del self.player['effects'][effect_name]
    
    def _add_damage_number(self, value: int, position: Tuple[int, int], color: Tuple[int, int, int], prefix: str = ""):
        """Add floating damage number"""
        display_text = f"{prefix}{value}" if prefix else str(value)
        
        self.damage_numbers.append({
            'value': display_text,
            'position': list(position),
            'color': color,
            'life': 2.0,
            'max_life': 2.0
        })
    
    def _add_particles(self, position: Tuple[int, int], color: Tuple[int, int, int], count: int):
        """Add effect particles"""
        for _ in range(count):
            self.effect_particles.append({
                'x': position[0] + random.randint(-30, 30),
                'y': position[1] + random.randint(-30, 30),
                'vel_x': random.uniform(-50, 50),
                'vel_y': random.uniform(-100, -20),
                'size': random.uniform(3, 8),
                'color': color,
                'life': random.uniform(1.0, 2.0),
                'max_life': 2.0
            })
    
    def _calculate_victory_rewards(self):
        """Calculate rewards for victory"""
        # Base rewards
        base_gold = 50 + (self.world_id * 20) + (self.stage_num * 5)
        base_xp = 25 + (self.world_id * 10) + (self.stage_num * 3)
        
        # Boss bonus
        if self.is_boss_battle:
            base_gold *= 3
            base_xp *= 2
        
        self.victory_rewards = {
            'gold': base_gold,
            'xp': base_xp,
            'gems': 1 if self.is_boss_battle else 0
        }
    
    def _apply_victory_rewards(self):
        """Apply victory rewards to player"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        # Add rewards
        current_gold = save_manager.get_player_data("currency.gold") or 0
        current_gems = save_manager.get_player_data("currency.gems") or 0
        current_xp = save_manager.get_player_data("player.xp") or 0
        
        save_manager.set_player_data("currency.gold", current_gold + self.victory_rewards['gold'])
        save_manager.set_player_data("currency.gems", current_gems + self.victory_rewards['gems'])
        save_manager.set_player_data("player.xp", current_xp + self.victory_rewards['xp'])
        
        # Check for level up
        self._check_level_up(save_manager)
        
        # Update progress
        self._update_progress(save_manager)
        
        # Update stats
        battles_won = save_manager.get_player_data("stats.battles_won") or 0
        save_manager.set_player_data("stats.battles_won", battles_won + 1)
    
    def _check_level_up(self, save_manager):
        """Check and handle level up"""
        current_level = save_manager.get_player_data("player.level") or 1
        current_xp = save_manager.get_player_data("player.xp") or 0
        
        xp_needed = current_level * Config.XP_PER_LEVEL
        
        if current_xp >= xp_needed:
            # Level up!
            new_level = current_level + 1
            remaining_xp = current_xp - xp_needed
            
            save_manager.set_player_data("player.level", new_level)
            save_manager.set_player_data("player.xp", remaining_xp)
            
            # Increase stats
            level_multiplier = 1 + new_level * Config.STAT_INCREASE_PER_LEVEL
            
            base_hp = Config.PLAYER_START_HP
            base_attack = Config.PLAYER_START_ATTACK
            base_defense = Config.PLAYER_START_DEFENSE
            base_speed = Config.PLAYER_START_SPEED
            
            save_manager.set_player_data("player.max_hp", int(base_hp * level_multiplier))
            save_manager.set_player_data("player.attack", int(base_attack * level_multiplier))
            save_manager.set_player_data("player.defense", int(base_defense * level_multiplier))
            save_manager.set_player_data("player.speed", int(base_speed * level_multiplier))
            
            self.logger.info(f"Player leveled up to {new_level}!")
    
    def _update_progress(self, save_manager):
        """Update game progress"""
        current_world = save_manager.get_player_data("progress.current_world") or 0
        current_stage = save_manager.get_player_data("progress.current_stage") or 1
        
        # If this is the current stage, advance
        if self.world_id == current_world and self.stage_num == current_stage:
            next_stage = current_stage + 1
            
            if next_stage > Config.STAGES_PER_WORLD:
                # Move to next world
                next_world = current_world + 1
                if next_world < Config.WORLDS_COUNT:
                    save_manager.set_player_data("progress.current_world", next_world)
                    save_manager.set_player_data("progress.current_stage", 1)
                    
                    # Unlock next world
                    worlds_unlocked = save_manager.get_player_data("progress.worlds_unlocked") or 1
                    save_manager.set_player_data("progress.worlds_unlocked", max(worlds_unlocked, next_world + 1))
            else:
                save_manager.set_player_data("progress.current_stage", next_stage)
        
        # Update completion stats
        stages_completed = save_manager.get_player_data("progress.stages_completed") or 0
        save_manager.set_player_data("progress.stages_completed", stages_completed + 1)
        
        if self.is_boss_battle:
            bosses_defeated = save_manager.get_player_data("progress.bosses_defeated") or 0
            save_manager.set_player_data("progress.bosses_defeated", bosses_defeated + 1)
    
    def _handle_defeat(self):
        """Handle player defeat"""
        save_manager = self.game.get_system('save_manager')
        if save_manager:
            battles_lost = save_manager.get_player_data("stats.battles_lost") or 0
            save_manager.set_player_data("stats.battles_lost", battles_lost + 1)
        
        # Return to world map
        self._return_to_world_map()
    
    def _handle_result_click(self, pos: Tuple[int, int]):
        """Handle clicks during victory/defeat screen"""
        self._return_to_world_map()
    
    def _return_to_world_map(self):
        """Return to world map"""
        self.game.change_state(GameStates.WORLD_MAP)