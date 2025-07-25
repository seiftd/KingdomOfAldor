"""
Kingdom of Aldoria - World Map State
World selection screen with stage progression and stamina system
"""

import pygame
import logging
import math
from typing import List, Dict, Tuple

from ..core.state_manager import GameState
from ..core.config import Config, GameStates

class WorldMapState(GameState):
    """World map state for world and stage selection"""
    
    def __init__(self, game):
        """Initialize world map state"""
        super().__init__(game)
        
        # World data
        self.worlds = []
        self.current_world = 0
        self.selected_stage = 1
        
        # UI elements
        self.world_buttons = []
        self.stage_buttons = []
        self.stamina_bar_rect = None
        self.play_button_rect = None
        
        # Animation
        self.scroll_offset = 0.0
        self.target_scroll = 0.0
        
        self.logger.info("WorldMapState initialized")
    
    def enter(self, **kwargs):
        """Enter the world map state"""
        self.logger.info("Entering world map")
        
        # Load world data
        self._load_world_data()
        
        # Setup UI
        self._setup_ui()
        
        # Get current progress
        save_manager = self.game.get_system('save_manager')
        if save_manager:
            self.current_world = save_manager.get_player_data("progress.current_world") or 0
            self.selected_stage = save_manager.get_player_data("progress.current_stage") or 1
        
        # Update stamina
        self._update_stamina()
        
        # Play world map music
        asset_manager = self.game.get_system('asset_manager')
        if asset_manager:
            asset_manager.play_music("world_map_music", volume=0.5)
    
    def exit(self):
        """Exit the world map state"""
        self.logger.info("Exiting world map")
    
    def update(self, dt: float):
        """Update world map logic"""
        # Smooth scrolling
        if abs(self.target_scroll - self.scroll_offset) > 1.0:
            self.scroll_offset += (self.target_scroll - self.scroll_offset) * dt * 5.0
        else:
            self.scroll_offset = self.target_scroll
        
        # Update stamina recharge
        self._update_stamina()
    
    def render(self, screen: pygame.Surface):
        """Render the world map"""
        # Background
        self._render_background(screen)
        
        # World selection
        self._render_world_selection(screen)
        
        # Stage selection for current world
        self._render_stage_selection(screen)
        
        # UI panels
        self._render_ui_panels(screen)
        
        # Stamina display
        self._render_stamina_display(screen)
        
        # Action buttons
        self._render_action_buttons(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle world map events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state(GameStates.MAIN_MENU)
            elif event.key == pygame.K_RETURN:
                self._start_battle()
            elif event.key == pygame.K_LEFT:
                self._change_world(-1)
            elif event.key == pygame.K_RIGHT:
                self._change_world(1)
    
    def _load_world_data(self):
        """Load world configuration data"""
        self.worlds = []
        
        for i, world_name in enumerate(Config.WORLD_NAMES):
            world_data = {
                'id': i,
                'name': world_name,
                'stages': Config.STAGES_PER_WORLD,
                'unlocked': self._is_world_unlocked(i),
                'background_color': self._get_world_color(i),
                'completed_stages': self._get_completed_stages(i)
            }
            self.worlds.append(world_data)
    
    def _setup_ui(self):
        """Setup UI elements"""
        # World buttons (horizontal scroll)
        self.world_buttons = []
        button_width = 200
        button_height = 60
        spacing = 20
        
        for i, world in enumerate(self.worlds):
            x = 50 + i * (button_width + spacing)
            y = 50
            
            self.world_buttons.append({
                'rect': pygame.Rect(x, y, button_width, button_height),
                'world_id': i,
                'world': world
            })
        
        # Stage grid
        self._setup_stage_grid()
        
        # UI rects
        self.stamina_bar_rect = pygame.Rect(20, Config.SCREEN_HEIGHT - 100, 300, 30)
        self.play_button_rect = pygame.Rect(
            Config.SCREEN_WIDTH - 150, 
            Config.SCREEN_HEIGHT - 80, 
            130, 60
        )
    
    def _setup_stage_grid(self):
        """Setup stage selection grid"""
        self.stage_buttons = []
        
        # Grid configuration
        cols = 6
        rows = 5
        button_size = 60
        spacing = 10
        grid_width = cols * (button_size + spacing) - spacing
        grid_height = rows * (button_size + spacing) - spacing
        
        start_x = (Config.SCREEN_WIDTH - grid_width) // 2
        start_y = 180
        
        for stage_num in range(1, Config.STAGES_PER_WORLD + 1):
            row = (stage_num - 1) // cols
            col = (stage_num - 1) % cols
            
            x = start_x + col * (button_size + spacing)
            y = start_y + row * (button_size + spacing)
            
            self.stage_buttons.append({
                'rect': pygame.Rect(x, y, button_size, button_size),
                'stage_num': stage_num,
                'unlocked': self._is_stage_unlocked(self.current_world, stage_num),
                'completed': self._is_stage_completed(self.current_world, stage_num),
                'is_boss': stage_num % Config.BOSS_STAGE_INTERVAL == 0
            })
    
    def _render_background(self, screen: pygame.Surface):
        """Render world map background"""
        # Get current world background color
        if self.current_world < len(self.worlds):
            bg_color = self.worlds[self.current_world]['background_color']
        else:
            bg_color = Config.UI_BACKGROUND
        
        # Gradient background based on world theme
        self._render_world_gradient(screen, bg_color)
        
        # Optional: Add world-specific background elements
        self._render_world_decorations(screen)
    
    def _render_world_gradient(self, screen: pygame.Surface, base_color: Tuple[int, int, int]):
        """Render gradient background for current world"""
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            
            # Create gradient effect
            r = int(base_color[0] * (0.3 + ratio * 0.7))
            g = int(base_color[1] * (0.3 + ratio * 0.7))
            b = int(base_color[2] * (0.3 + ratio * 0.7))
            
            color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(screen, color, (0, y), (Config.SCREEN_WIDTH, y))
    
    def _render_world_decorations(self, screen: pygame.Surface):
        """Render world-specific decorative elements"""
        # This could load world-specific background images
        # For now, we'll add some simple decorative elements
        pass
    
    def _render_world_selection(self, screen: pygame.Surface):
        """Render world selection tabs"""
        font = pygame.font.Font(None, 24)
        
        for button_data in self.world_buttons:
            rect = button_data['rect']
            world = button_data['world']
            world_id = button_data['world_id']
            
            # Adjust position based on scroll
            adjusted_rect = rect.copy()
            adjusted_rect.x += self.scroll_offset
            
            # Skip if not visible
            if adjusted_rect.right < 0 or adjusted_rect.left > Config.SCREEN_WIDTH:
                continue
            
            # Button appearance
            if world_id == self.current_world:
                bg_color = Config.UI_ACCENT
                text_color = Config.WHITE
                border_width = 3
            elif world['unlocked']:
                bg_color = Config.UI_BUTTON
                text_color = Config.UI_TEXT
                border_width = 2
            else:
                bg_color = Config.DARK_GRAY
                text_color = Config.UI_TEXT_SECONDARY
                border_width = 1
            
            # Draw button
            pygame.draw.rect(screen, bg_color, adjusted_rect)
            pygame.draw.rect(screen, Config.UI_ACCENT, adjusted_rect, border_width)
            
            # World name
            text_surface = font.render(world['name'], True, text_color)
            text_rect = text_surface.get_rect(center=adjusted_rect.center)
            screen.blit(text_surface, text_rect)
            
            # Progress indicator
            if world['unlocked']:
                progress = world['completed_stages'] / Config.STAGES_PER_WORLD
                progress_width = int(adjusted_rect.width * progress)
                if progress_width > 0:
                    progress_rect = pygame.Rect(
                        adjusted_rect.left, 
                        adjusted_rect.bottom - 5,
                        progress_width, 5
                    )
                    pygame.draw.rect(screen, Config.GREEN, progress_rect)
    
    def _render_stage_selection(self, screen: pygame.Surface):
        """Render stage selection grid"""
        # Update stage grid for current world
        self._setup_stage_grid()
        
        font = pygame.font.Font(None, 24)
        
        for button_data in self.stage_buttons:
            rect = button_data['rect']
            stage_num = button_data['stage_num']
            
            # Button appearance based on state
            if not button_data['unlocked']:
                bg_color = Config.DARK_GRAY
                text_color = Config.UI_TEXT_SECONDARY
                border_color = Config.DARK_GRAY
            elif button_data['completed']:
                bg_color = Config.GREEN
                text_color = Config.WHITE
                border_color = Config.GREEN
            elif stage_num == self.selected_stage:
                bg_color = Config.UI_ACCENT
                text_color = Config.WHITE
                border_color = Config.GOLD
            elif button_data['is_boss']:
                bg_color = Config.RED
                text_color = Config.WHITE
                border_color = Config.RED
            else:
                bg_color = Config.UI_BUTTON
                text_color = Config.UI_TEXT
                border_color = Config.UI_ACCENT
            
            # Draw stage button
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, border_color, rect, 2)
            
            # Special styling for boss stages
            if button_data['is_boss']:
                # Add crown icon or special border
                crown_points = [
                    (rect.centerx, rect.top + 5),
                    (rect.centerx - 8, rect.top + 15),
                    (rect.centerx + 8, rect.top + 15)
                ]
                pygame.draw.polygon(screen, Config.GOLD, crown_points)
            
            # Stage number
            text_surface = font.render(str(stage_num), True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            if button_data['is_boss']:
                text_rect.y += 8  # Offset for crown
            screen.blit(text_surface, text_rect)
            
            # Completion star
            if button_data['completed']:
                star_center = (rect.right - 10, rect.top + 10)
                self._draw_star(screen, star_center, 6, Config.GOLD)
    
    def _render_ui_panels(self, screen: pygame.Surface):
        """Render UI information panels"""
        # Current world info panel
        world_info_rect = pygame.Rect(20, 130, 300, 40)
        pygame.draw.rect(screen, Config.UI_PANEL, world_info_rect)
        pygame.draw.rect(screen, Config.UI_ACCENT, world_info_rect, 2)
        
        # World name and progress
        font = pygame.font.Font(None, 24)
        if self.current_world < len(self.worlds):
            world = self.worlds[self.current_world]
            world_text = f"{world['name']} ({world['completed_stages']}/{Config.STAGES_PER_WORLD})"
            text_surface = font.render(world_text, True, Config.UI_TEXT)
            screen.blit(text_surface, (world_info_rect.x + 10, world_info_rect.y + 10))
        
        # Stage info panel
        stage_info_rect = pygame.Rect(Config.SCREEN_WIDTH - 320, 130, 300, 40)
        pygame.draw.rect(screen, Config.UI_PANEL, stage_info_rect)
        pygame.draw.rect(screen, Config.UI_ACCENT, stage_info_rect, 2)
        
        # Stage info
        stage_text = f"Stage {self.selected_stage}"
        if self.selected_stage % Config.BOSS_STAGE_INTERVAL == 0:
            stage_text += " (BOSS)"
        
        text_surface = font.render(stage_text, True, Config.UI_TEXT)
        screen.blit(text_surface, (stage_info_rect.x + 10, stage_info_rect.y + 10))
    
    def _render_stamina_display(self, screen: pygame.Surface):
        """Render stamina bar and information"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        current_stamina = save_manager.get_player_data("stamina.current") or 0
        max_stamina = save_manager.get_player_data("stamina.max") or Config.MAX_STAMINA_DEFAULT
        
        # Stamina bar background
        pygame.draw.rect(screen, Config.DARK_GRAY, self.stamina_bar_rect)
        
        # Stamina bar fill
        if max_stamina > 0:
            fill_width = int(self.stamina_bar_rect.width * (current_stamina / max_stamina))
            fill_rect = pygame.Rect(
                self.stamina_bar_rect.x,
                self.stamina_bar_rect.y,
                fill_width,
                self.stamina_bar_rect.height
            )
            
            # Color based on stamina level
            if current_stamina >= Config.STAMINA_PER_STAGE:
                fill_color = Config.GREEN
            elif current_stamina > 0:
                fill_color = Config.YELLOW
            else:
                fill_color = Config.RED
            
            pygame.draw.rect(screen, fill_color, fill_rect)
        
        # Stamina bar border
        pygame.draw.rect(screen, Config.UI_ACCENT, self.stamina_bar_rect, 2)
        
        # Stamina text
        font = pygame.font.Font(None, 24)
        stamina_text = f"Stamina: {current_stamina}/{max_stamina}"
        text_surface = font.render(stamina_text, True, Config.UI_TEXT)
        screen.blit(text_surface, (self.stamina_bar_rect.x, self.stamina_bar_rect.y - 25))
        
        # Recharge timer
        if current_stamina < max_stamina:
            recharge_time = self._get_stamina_recharge_time()
            if recharge_time > 0:
                timer_text = f"Next: {recharge_time//60:02d}:{recharge_time%60:02d}"
                timer_surface = font.render(timer_text, True, Config.UI_TEXT_SECONDARY)
                screen.blit(timer_surface, (self.stamina_bar_rect.right - 100, self.stamina_bar_rect.y - 25))
    
    def _render_action_buttons(self, screen: pygame.Surface):
        """Render action buttons"""
        # Play button
        can_play = self._can_start_battle()
        
        if can_play:
            bg_color = Config.GREEN
            text_color = Config.WHITE
        else:
            bg_color = Config.DARK_GRAY
            text_color = Config.UI_TEXT_SECONDARY
        
        pygame.draw.rect(screen, bg_color, self.play_button_rect)
        pygame.draw.rect(screen, Config.UI_ACCENT, self.play_button_rect, 2)
        
        # Play button text
        font = pygame.font.Font(None, 32)
        play_text = "BATTLE!"
        text_surface = font.render(play_text, True, text_color)
        text_rect = text_surface.get_rect(center=self.play_button_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Back button
        back_button_rect = pygame.Rect(20, Config.SCREEN_HEIGHT - 60, 100, 40)
        pygame.draw.rect(screen, Config.UI_BUTTON, back_button_rect)
        pygame.draw.rect(screen, Config.UI_ACCENT, back_button_rect, 2)
        
        back_font = pygame.font.Font(None, 24)
        back_text = back_font.render("BACK", True, Config.UI_TEXT)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)
    
    def _handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        # World selection
        for button_data in self.world_buttons:
            adjusted_rect = button_data['rect'].copy()
            adjusted_rect.x += self.scroll_offset
            
            if adjusted_rect.collidepoint(pos) and button_data['world']['unlocked']:
                self._select_world(button_data['world_id'])
                return
        
        # Stage selection
        for button_data in self.stage_buttons:
            if button_data['rect'].collidepoint(pos) and button_data['unlocked']:
                self.selected_stage = button_data['stage_num']
                return
        
        # Play button
        if self.play_button_rect.collidepoint(pos) and self._can_start_battle():
            self._start_battle()
            return
        
        # Back button
        back_button_rect = pygame.Rect(20, Config.SCREEN_HEIGHT - 60, 100, 40)
        if back_button_rect.collidepoint(pos):
            self.game.change_state(GameStates.MAIN_MENU)
            return
    
    def _select_world(self, world_id: int):
        """Select a world"""
        if world_id != self.current_world:
            self.current_world = world_id
            self.selected_stage = 1  # Reset to first stage
            
            # Update scroll position
            button_x = self.world_buttons[world_id]['rect'].x
            self.target_scroll = -(button_x - Config.SCREEN_WIDTH // 2 + 100)
    
    def _change_world(self, direction: int):
        """Change world with keyboard"""
        new_world = self.current_world + direction
        if 0 <= new_world < len(self.worlds) and self.worlds[new_world]['unlocked']:
            self._select_world(new_world)
    
    def _start_battle(self):
        """Start battle for selected stage"""
        if not self._can_start_battle():
            return
        
        # Consume stamina
        save_manager = self.game.get_system('save_manager')
        if save_manager:
            current_stamina = save_manager.get_player_data("stamina.current") or 0
            save_manager.set_player_data("stamina.current", current_stamina - Config.STAMINA_PER_STAGE)
        
        # Go to battle state
        self.game.change_state(GameStates.BATTLE, 
                             world=self.current_world,
                             stage=self.selected_stage)
    
    def _can_start_battle(self) -> bool:
        """Check if battle can be started"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return False
        
        current_stamina = save_manager.get_player_data("stamina.current") or 0
        stage_unlocked = self._is_stage_unlocked(self.current_world, self.selected_stage)
        
        return current_stamina >= Config.STAMINA_PER_STAGE and stage_unlocked
    
    def _update_stamina(self):
        """Update stamina based on time"""
        import time
        
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        current_time = time.time()
        last_recharge = save_manager.get_player_data("stamina.last_recharge") or current_time
        current_stamina = save_manager.get_player_data("stamina.current") or 0
        max_stamina = save_manager.get_player_data("stamina.max") or Config.MAX_STAMINA_DEFAULT
        
        # Calculate stamina to add
        time_diff = current_time - last_recharge
        recharge_seconds = Config.STAMINA_RECHARGE_MINUTES * 60
        stamina_to_add = int(time_diff // recharge_seconds)
        
        if stamina_to_add > 0 and current_stamina < max_stamina:
            new_stamina = min(max_stamina, current_stamina + stamina_to_add)
            save_manager.set_player_data("stamina.current", new_stamina)
            save_manager.set_player_data("stamina.last_recharge", 
                                       last_recharge + stamina_to_add * recharge_seconds)
    
    def _get_stamina_recharge_time(self) -> int:
        """Get time until next stamina recharge in seconds"""
        import time
        
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return 0
        
        current_time = time.time()
        last_recharge = save_manager.get_player_data("stamina.last_recharge") or current_time
        recharge_seconds = Config.STAMINA_RECHARGE_MINUTES * 60
        
        time_since_recharge = current_time - last_recharge
        return max(0, int(recharge_seconds - (time_since_recharge % recharge_seconds)))
    
    def _is_world_unlocked(self, world_id: int) -> bool:
        """Check if world is unlocked"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return world_id == 0
        
        worlds_unlocked = save_manager.get_player_data("progress.worlds_unlocked") or 1
        return world_id < worlds_unlocked
    
    def _is_stage_unlocked(self, world_id: int, stage_num: int) -> bool:
        """Check if stage is unlocked"""
        if not self._is_world_unlocked(world_id):
            return False
        
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return stage_num == 1
        
        current_world = save_manager.get_player_data("progress.current_world") or 0
        current_stage = save_manager.get_player_data("progress.current_stage") or 1
        
        # If it's the current world, check current stage
        if world_id == current_world:
            return stage_num <= current_stage
        # If it's a previous world, all stages are unlocked
        elif world_id < current_world:
            return True
        # Future worlds are locked
        else:
            return False
    
    def _is_stage_completed(self, world_id: int, stage_num: int) -> bool:
        """Check if stage is completed"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return False
        
        current_world = save_manager.get_player_data("progress.current_world") or 0
        current_stage = save_manager.get_player_data("progress.current_stage") or 1
        
        # Stages in previous worlds are completed
        if world_id < current_world:
            return True
        # In current world, only stages before current are completed
        elif world_id == current_world:
            return stage_num < current_stage
        else:
            return False
    
    def _get_completed_stages(self, world_id: int) -> int:
        """Get number of completed stages in world"""
        count = 0
        for stage_num in range(1, Config.STAGES_PER_WORLD + 1):
            if self._is_stage_completed(world_id, stage_num):
                count += 1
        return count
    
    def _get_world_color(self, world_id: int) -> Tuple[int, int, int]:
        """Get theme color for world"""
        colors = [
            (34, 139, 34),   # Forest green
            (218, 165, 32),  # Desert gold
            (135, 206, 235), # Ice blue
            (75, 0, 130),    # Dark purple
            (255, 215, 0),   # Light gold
            (139, 69, 19),   # Mountain brown
            (0, 100, 148),   # Ocean blue
            (192, 192, 192), # Sky silver
            (101, 67, 33),   # Underground brown
            (178, 34, 34),   # Volcanic red
        ]
        return colors[world_id % len(colors)]
    
    def _draw_star(self, screen: pygame.Surface, center: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        """Draw a star shape"""
        import math
        
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.5
            
            x = center[0] + r * math.cos(angle - math.pi / 2)
            y = center[1] + r * math.sin(angle - math.pi / 2)
            points.append((x, y))
        
        pygame.draw.polygon(screen, color, points)