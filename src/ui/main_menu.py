"""
Kingdom of Aldoria - Main Menu State
Beautiful fantasy-themed main menu with navigation options
"""

import pygame
import logging
from typing import Optional

from ..core.state_manager import GameState
from ..core.config import Config, GameStates

class MainMenuState(GameState):
    """Main menu state with fantasy UI"""
    
    def __init__(self, game):
        """Initialize main menu state"""
        super().__init__(game)
        
        # UI elements
        self.buttons = {}
        self.background_image = None
        self.title_font = None
        self.button_font = None
        
        # Animation
        self.title_glow = 0.0
        self.glow_direction = 1
        
        # Player stats display
        self.stats_panel_rect = None
        
        self.logger.info("MainMenuState initialized")
    
    def enter(self, **kwargs):
        """Enter the main menu state"""
        self.logger.info("Entering main menu")
        
        # Load assets
        self._load_assets()
        
        # Setup UI
        self._setup_ui()
        
        # Play menu music
        asset_manager = self.game.get_system('asset_manager')
        if asset_manager:
            asset_manager.play_music("menu_music", volume=0.6)
    
    def exit(self):
        """Exit the main menu state"""
        self.logger.info("Exiting main menu")
    
    def update(self, dt: float):
        """Update main menu logic"""
        # Animate title glow
        self.title_glow += self.glow_direction * dt * 2.0
        if self.title_glow >= 1.0:
            self.title_glow = 1.0
            self.glow_direction = -1
        elif self.title_glow <= 0.0:
            self.title_glow = 0.0
            self.glow_direction = 1
        
        # Auto-save check
        save_manager = self.game.get_system('save_manager')
        if save_manager:
            save_manager.auto_save_if_needed()
    
    def render(self, screen: pygame.Surface):
        """Render the main menu"""
        # Background
        self._render_background(screen)
        
        # Title
        self._render_title(screen)
        
        # Main buttons
        self._render_buttons(screen)
        
        # Player stats panel
        self._render_stats_panel(screen)
        
        # Version info
        self._render_version_info(screen)
        
        # Virtual buttons (for mobile)
        input_manager = self.game.get_system('input_manager')
        if input_manager:
            input_manager.render_virtual_buttons(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle main menu events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._start_game()
            elif event.key == pygame.K_s:
                self.game.change_state(GameStates.SHOP)
            elif event.key == pygame.K_ESCAPE:
                self.game.quit_game()
    
    def _load_assets(self):
        """Load menu assets"""
        asset_manager = self.game.get_system('asset_manager')
        if not asset_manager:
            return
        
        # Background
        self.background_image = asset_manager.get_image("ui/main_menu_bg")
        
        # Fonts
        self.title_font = asset_manager.get_font(None, 72)
        self.button_font = asset_manager.get_font(None, 36)
    
    def _setup_ui(self):
        """Setup UI elements"""
        # Screen center
        center_x = Config.SCREEN_WIDTH // 2
        center_y = Config.SCREEN_HEIGHT // 2
        
        # Button specifications
        button_width = 300
        button_height = 60
        button_spacing = 20
        
        # Main buttons
        buttons_data = [
            ("PLAY", self._start_game),
            ("SHOP", self._open_shop),
            ("SETTINGS", self._open_settings),
            ("QUIT", self._quit_game)
        ]
        
        start_y = center_y - (len(buttons_data) * (button_height + button_spacing)) // 2
        
        for i, (text, callback) in enumerate(buttons_data):
            y_pos = start_y + i * (button_height + button_spacing)
            
            self.buttons[text] = {
                'rect': pygame.Rect(
                    center_x - button_width // 2,
                    y_pos,
                    button_width,
                    button_height
                ),
                'text': text,
                'callback': callback,
                'hovered': False
            }
        
        # Stats panel
        self.stats_panel_rect = pygame.Rect(20, 20, 250, 150)
    
    def _render_background(self, screen: pygame.Surface):
        """Render menu background"""
        if self.background_image:
            # Scale background to screen size
            scaled_bg = pygame.transform.scale(
                self.background_image, 
                (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
            )
            screen.blit(scaled_bg, (0, 0))
        else:
            # Gradient background
            self._render_gradient_background(screen)
    
    def _render_gradient_background(self, screen: pygame.Surface):
        """Render gradient background if no image available"""
        # Create gradient from dark blue to purple
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            
            # Interpolate colors
            r = int(25 + ratio * 75)    # 25 to 100
            g = int(25 + ratio * 25)    # 25 to 50
            b = int(35 + ratio * 65)    # 35 to 100
            
            color = (r, g, b)
            pygame.draw.line(screen, color, (0, y), (Config.SCREEN_WIDTH, y))
    
    def _render_title(self, screen: pygame.Surface):
        """Render game title with glow effect"""
        if not self.title_font:
            return
        
        title_text = "Kingdom of Aldoria"
        
        # Main title
        title_surface = self.title_font.render(title_text, True, Config.GOLD)
        title_rect = title_surface.get_rect(
            centerx=Config.SCREEN_WIDTH // 2,
            y=50
        )
        
        # Glow effect
        glow_alpha = int(100 + self.title_glow * 155)
        glow_surface = self.title_font.render(title_text, True, (255, 255, 200))
        glow_surface.set_alpha(glow_alpha)
        
        # Render glow slightly offset
        for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            glow_rect = title_rect.copy()
            glow_rect.x += offset[0]
            glow_rect.y += offset[1]
            screen.blit(glow_surface, glow_rect)
        
        # Render main title
        screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 24)
        subtitle_text = "A Fantasy Mobile RPG Adventure"
        subtitle_surface = subtitle_font.render(subtitle_text, True, Config.SILVER)
        subtitle_rect = subtitle_surface.get_rect(
            centerx=Config.SCREEN_WIDTH // 2,
            y=title_rect.bottom + 10
        )
        screen.blit(subtitle_surface, subtitle_rect)
    
    def _render_buttons(self, screen: pygame.Surface):
        """Render menu buttons"""
        mouse_pos = pygame.mouse.get_pos()
        
        for button_data in self.buttons.values():
            rect = button_data['rect']
            text = button_data['text']
            
            # Check if mouse is over button
            button_data['hovered'] = rect.collidepoint(mouse_pos)
            
            # Button colors
            if button_data['hovered']:
                bg_color = Config.UI_BUTTON_HOVER
                text_color = Config.GOLD
                border_color = Config.GOLD
            else:
                bg_color = Config.UI_BUTTON
                text_color = Config.UI_TEXT
                border_color = Config.UI_ACCENT
            
            # Draw button background
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, border_color, rect, 3)
            
            # Add corner decorations for fantasy feel
            corner_size = 10
            # Top-left corner
            pygame.draw.polygon(screen, border_color, [
                (rect.left, rect.top + corner_size),
                (rect.left, rect.top),
                (rect.left + corner_size, rect.top)
            ])
            # Top-right corner
            pygame.draw.polygon(screen, border_color, [
                (rect.right - corner_size, rect.top),
                (rect.right, rect.top),
                (rect.right, rect.top + corner_size)
            ])
            # Bottom-left corner
            pygame.draw.polygon(screen, border_color, [
                (rect.left, rect.bottom - corner_size),
                (rect.left, rect.bottom),
                (rect.left + corner_size, rect.bottom)
            ])
            # Bottom-right corner
            pygame.draw.polygon(screen, border_color, [
                (rect.right - corner_size, rect.bottom),
                (rect.right, rect.bottom),
                (rect.right, rect.bottom - corner_size)
            ])
            
            # Button text
            if self.button_font:
                text_surface = self.button_font.render(text, True, text_color)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
    
    def _render_stats_panel(self, screen: pygame.Surface):
        """Render player stats panel"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        # Panel background
        pygame.draw.rect(screen, Config.UI_PANEL, self.stats_panel_rect)
        pygame.draw.rect(screen, Config.UI_ACCENT, self.stats_panel_rect, 2)
        
        # Panel title
        title_font = pygame.font.Font(None, 24)
        title_text = title_font.render("Knight Arin", True, Config.GOLD)
        screen.blit(title_text, (self.stats_panel_rect.x + 10, self.stats_panel_rect.y + 5))
        
        # Player stats
        stats_font = pygame.font.Font(None, 20)
        y_offset = 35
        
        # Get player data
        player_level = save_manager.get_player_data("player.level") or 1
        player_gold = save_manager.get_player_data("currency.gold") or 0
        player_gems = save_manager.get_player_data("currency.gems") or 0
        current_world = save_manager.get_player_data("progress.current_world") or 0
        current_stage = save_manager.get_player_data("progress.current_stage") or 1
        
        stats_data = [
            f"Level: {player_level}",
            f"Gold: {player_gold:,}",
            f"Gems: {player_gems}",
            f"World: {current_world + 1}-{current_stage}"
        ]
        
        for stat_text in stats_data:
            stat_surface = stats_font.render(stat_text, True, Config.UI_TEXT)
            screen.blit(stat_surface, (self.stats_panel_rect.x + 10, self.stats_panel_rect.y + y_offset))
            y_offset += 25
    
    def _render_version_info(self, screen: pygame.Surface):
        """Render version information"""
        version_font = pygame.font.Font(None, 18)
        version_text = f"v{Config.VERSION}"
        version_surface = version_font.render(version_text, True, Config.UI_TEXT_SECONDARY)
        
        version_rect = version_surface.get_rect(
            bottomright=(Config.SCREEN_WIDTH - 10, Config.SCREEN_HEIGHT - 10)
        )
        screen.blit(version_surface, version_rect)
    
    def _handle_mouse_click(self, pos):
        """Handle mouse click on buttons"""
        for button_data in self.buttons.values():
            if button_data['rect'].collidepoint(pos):
                # Play click sound
                audio_manager = self.game.get_system('audio_manager')
                asset_manager = self.game.get_system('asset_manager')
                if audio_manager and asset_manager:
                    click_sound = asset_manager.get_sound("ui/button_click")
                    if click_sound:
                        audio_manager.play_sound(click_sound, "button_click", volume=0.7)
                
                # Execute callback
                button_data['callback']()
                break
    
    def _start_game(self):
        """Start the game (go to world map)"""
        self.logger.info("Starting game")
        self.game.change_state(GameStates.WORLD_MAP)
    
    def _open_shop(self):
        """Open the shop"""
        self.logger.info("Opening shop")
        self.game.change_state(GameStates.SHOP)
    
    def _open_settings(self):
        """Open settings"""
        self.logger.info("Opening settings")
        # For now, just log - settings screen would be implemented later
        print("Settings screen not yet implemented")
    
    def _quit_game(self):
        """Quit the game"""
        self.logger.info("Quit requested from main menu")
        self.game.quit_game()