"""
Kingdom of Aldoria - Main Menu State
The main menu with game title, buttons, and player info
"""

import pygame
import math
from .state_manager import GameState
from ..ui.button import Button
from ..ui.panel import Panel
from ..core.config import GameConfig

class MainMenuState(GameState):
    """Main menu state of the game"""
    
    def __init__(self):
        """Initialize the main menu"""
        super().__init__()
        
        # Get references to managers (will be set by main game)
        self.asset_manager = None
        self.audio_manager = None
        self.save_manager = None
        
        # UI elements
        self.buttons = {}
        self.panels = {}
        
        # Animation variables
        self.title_animation_time = 0
        self.background_scroll_x = 0
        self.background_scroll_speed = 20
        
        # Menu state
        self.menu_opened = False
        self.fade_alpha = 0
        self.fade_speed = 300
        
        # Player info display
        self.player_data = {}
        
    def enter(self):
        """Called when entering the main menu state"""
        print("Entering Main Menu")
        
        # Get manager references from the main game
        if hasattr(self.state_manager, 'asset_manager'):
            from main import KingdomOfAldoria
            # Access through the main game instance
            import main
            if hasattr(main, 'game_instance'):
                game = main.game_instance
                self.asset_manager = game.asset_manager
                self.audio_manager = game.audio_manager
                self.save_manager = game.save_manager
        
        # Initialize managers if not available (fallback)
        if not self.asset_manager:
            from ..core.asset_manager import AssetManager
            from ..core.audio_manager import AudioManager
            from ..core.save_manager import SaveManager
            
            self.asset_manager = AssetManager()
            self.audio_manager = AudioManager()
            self.save_manager = SaveManager()
        
        # Load player data
        self.player_data = self.save_manager.get_player_data()
        
        # Update stamina
        self.save_manager.update_stamina()
        
        # Check daily login
        if self.save_manager.update_daily_login():
            # Show daily reward popup later
            pass
        
        # Create UI elements
        self._create_ui_elements()
        
        # Start menu music
        self.audio_manager.play_music("main_menu", fade_in=2.0)
        
        # Start fade in animation
        self.fade_alpha = 255
        self.menu_opened = True
    
    def exit(self):
        """Called when exiting the main menu state"""
        print("Exiting Main Menu")
        
        # Stop menu music with fade out
        self.audio_manager.stop_music(fade_out=1.0)
    
    def _create_ui_elements(self):
        """Create all UI elements for the main menu"""
        screen_width = GameConfig.SCREEN_WIDTH
        screen_height = GameConfig.SCREEN_HEIGHT
        
        # Main buttons
        button_width = 250
        button_height = 60
        button_x = screen_width // 2 - button_width // 2
        button_spacing = 80
        start_y = screen_height // 2 - 50
        
        # Play button
        self.buttons["play"] = Button(
            x=button_x,
            y=start_y,
            width=button_width,
            height=button_height,
            text="PLAY",
            font_size=32,
            on_click=self._on_play_clicked
        )
        
        # Shop button
        self.buttons["shop"] = Button(
            x=button_x,
            y=start_y + button_spacing,
            width=button_width,
            height=button_height,
            text="SHOP",
            font_size=32,
            on_click=self._on_shop_clicked
        )
        
        # Settings button
        self.buttons["settings"] = Button(
            x=button_x,
            y=start_y + button_spacing * 2,
            width=button_width,
            height=button_height,
            text="SETTINGS",
            font_size=32,
            on_click=self._on_settings_clicked
        )
        
        # Player info panel (top left)
        self.panels["player_info"] = Panel(
            x=20,
            y=20,
            width=300,
            height=120,
            background_color=(30, 30, 50, 180)
        )
        
        # Currency panel (top right)
        self.panels["currency"] = Panel(
            x=screen_width - 220,
            y=20,
            width=200,
            height=80,
            background_color=(30, 30, 50, 180)
        )
        
        # Daily login button (bottom left)
        self.buttons["daily_login"] = Button(
            x=20,
            y=screen_height - 80,
            width=150,
            height=50,
            text="DAILY REWARD",
            font_size=16,
            on_click=self._on_daily_login_clicked
        )
        
        # Free gems button (bottom right) 
        self.buttons["free_gems"] = Button(
            x=screen_width - 170,
            y=screen_height - 80,
            width=150,
            height=50,
            text="FREE GEMS",
            font_size=16,
            on_click=self._on_free_gems_clicked
        )
    
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events"""
        # Handle button clicks
        for button in self.buttons.values():
            button.handle_event(event)
        
        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self._on_play_clicked()
            elif event.key == pygame.K_s:
                self._on_shop_clicked()
            elif event.key == pygame.K_ESCAPE:
                # Quit game
                self.state_manager.quit_game()
    
    def update(self, dt: float):
        """Update main menu logic"""
        # Update animations
        self.title_animation_time += dt
        self.background_scroll_x += self.background_scroll_speed * dt
        
        # Reset background scroll when it goes too far
        if self.background_scroll_x > GameConfig.SCREEN_WIDTH:
            self.background_scroll_x = 0
        
        # Update fade animation
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - self.fade_speed * dt)
        
        # Update UI elements
        for button in self.buttons.values():
            button.update(dt)
        
        # Update player data periodically
        self.player_data = self.save_manager.get_player_data()
    
    def render(self, screen: pygame.Surface):
        """Render the main menu"""
        # Clear screen with dark background
        screen.fill((10, 10, 20))
        
        # Draw animated background
        self._draw_background(screen)
        
        # Draw game title
        self._draw_title(screen)
        
        # Draw UI panels
        for panel in self.panels.values():
            panel.render(screen)
        
        # Draw player info
        self._draw_player_info(screen)
        
        # Draw currency info
        self._draw_currency_info(screen)
        
        # Draw buttons
        for button in self.buttons.values():
            button.render(screen)
        
        # Draw fade overlay
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            screen.blit(fade_surface, (0, 0))
    
    def _draw_background(self, screen: pygame.Surface):
        """Draw animated background"""
        # Try to load background image
        bg_image = self.asset_manager.load_image("worlds/forest_bg.png")
        
        if bg_image:
            # Scale background to screen size
            bg_scaled = pygame.transform.scale(bg_image, (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
            
            # Draw scrolling background
            screen.blit(bg_scaled, (-self.background_scroll_x // 2, 0))
            
            # Add overlay for darker effect
            overlay = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(120)
            screen.blit(overlay, (0, 0))
        else:
            # Fallback gradient background
            for y in range(GameConfig.SCREEN_HEIGHT):
                color_intensity = int(20 + (y / GameConfig.SCREEN_HEIGHT) * 30)
                color = (color_intensity // 3, color_intensity // 2, color_intensity)
                pygame.draw.line(screen, color, (0, y), (GameConfig.SCREEN_WIDTH, y))
    
    def _draw_title(self, screen: pygame.Surface):
        """Draw the game title with animation"""
        # Title text
        title_text = "KINGDOM OF ALDORIA"
        
        # Get font
        title_font = self.asset_manager.load_font("title", None, 56)
        
        # Create title surface with animation
        bounce_offset = math.sin(self.title_animation_time * 2) * 5
        
        # Draw title shadow
        shadow_surface = title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(GameConfig.SCREEN_WIDTH // 2 + 3, 100 + bounce_offset + 3))
        screen.blit(shadow_surface, shadow_rect)
        
        # Draw main title
        title_surface = title_font.render(title_text, True, (255, 215, 0))  # Gold color
        title_rect = title_surface.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 100 + bounce_offset))
        screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_text = "Epic Fantasy Adventure"
        subtitle_font = self.asset_manager.load_font("default", None, 24)
        subtitle_surface = subtitle_font.render(subtitle_text, True, (200, 200, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 150 + bounce_offset))
        screen.blit(subtitle_surface, subtitle_rect)
    
    def _draw_player_info(self, screen: pygame.Surface):
        """Draw player information panel"""
        panel = self.panels["player_info"]
        font = self.asset_manager.load_font("default", None, 20)
        small_font = self.asset_manager.load_font("small", None, 16)
        
        # Player name and level
        name = self.player_data.get("name", "Arin")
        level = self.player_data.get("level", 1)
        
        name_text = f"{name} - Level {level}"
        name_surface = font.render(name_text, True, (255, 255, 255))
        screen.blit(name_surface, (panel.x + 10, panel.y + 10))
        
        # Experience bar
        experience = self.player_data.get("experience", 0)
        xp_required = GameConfig.get_xp_requirement(level + 1)
        
        # XP bar background
        xp_bar_rect = pygame.Rect(panel.x + 10, panel.y + 40, 280, 15)
        pygame.draw.rect(screen, (50, 50, 50), xp_bar_rect)
        
        # XP bar fill
        if xp_required > 0:
            xp_progress = experience / xp_required
            xp_fill_width = int(280 * xp_progress)
            xp_fill_rect = pygame.Rect(panel.x + 10, panel.y + 40, xp_fill_width, 15)
            pygame.draw.rect(screen, (100, 150, 255), xp_fill_rect)
        
        # XP text
        xp_text = f"XP: {experience}/{xp_required}"
        xp_surface = small_font.render(xp_text, True, (255, 255, 255))
        screen.blit(xp_surface, (panel.x + 10, panel.y + 60))
        
        # Stamina info
        stamina = self.player_data.get("stamina", 0)
        max_stamina = self.player_data.get("max_stamina", 10)
        
        stamina_text = f"Stamina: {stamina}/{max_stamina}"
        stamina_surface = small_font.render(stamina_text, True, (100, 255, 100))
        screen.blit(stamina_surface, (panel.x + 10, panel.y + 85))
    
    def _draw_currency_info(self, screen: pygame.Surface):
        """Draw currency information"""
        panel = self.panels["currency"]
        font = self.asset_manager.load_font("default", None, 18)
        
        # Get currency amounts
        gold = self.player_data.get("gold", 0)
        gems = self.player_data.get("gems", 0)
        
        # Draw gold
        gold_text = f"Gold: {gold:,}"
        gold_surface = font.render(gold_text, True, (255, 215, 0))
        screen.blit(gold_surface, (panel.x + 10, panel.y + 10))
        
        # Draw gems
        gems_text = f"Gems: {gems:,}"
        gems_surface = font.render(gems_text, True, (255, 100, 255))
        screen.blit(gems_surface, (panel.x + 10, panel.y + 35))
    
    def _on_play_clicked(self):
        """Handle play button click"""
        self.audio_manager.play_ui_sound("click")
        
        # Check if player has stamina
        stamina = self.player_data.get("stamina", 0)
        if stamina > 0:
            # Go to world map
            from .world_map import WorldMapState
            self.set_next_state(WorldMapState)
        else:
            # Show no stamina popup
            from .popup_no_stamina import NoStaminaPopupState
            self.state_manager.push_state(NoStaminaPopupState())
    
    def _on_shop_clicked(self):
        """Handle shop button click"""
        self.audio_manager.play_ui_sound("click")
        
        # Go to shop
        from .shop import ShopState
        self.set_next_state(ShopState)
    
    def _on_settings_clicked(self):
        """Handle settings button click"""
        self.audio_manager.play_ui_sound("click")
        
        # Go to settings
        from .settings import SettingsState
        self.state_manager.push_state(SettingsState())
    
    def _on_daily_login_clicked(self):
        """Handle daily login button click"""
        self.audio_manager.play_ui_sound("click")
        
        # Show daily login popup
        from .daily_login import DailyLoginState
        self.state_manager.push_state(DailyLoginState())
    
    def _on_free_gems_clicked(self):
        """Handle free gems button click"""
        self.audio_manager.play_ui_sound("click")
        
        # Show rewarded ad for gems
        def on_ad_reward(success):
            if success:
                gems_reward = GameConfig.GEMS_PER_AD * 10  # 10 ads worth
                self.save_manager.add_gems(gems_reward)
                self.audio_manager.play_pickup_sound("gem")
        
        # Try to show rewarded ad
        from ..utils.mobile_utils import MobileUtils
        mobile_utils = MobileUtils()
        if mobile_utils.ad_manager.can_show_rewarded_ad():
            mobile_utils.ad_manager.show_rewarded_ad(on_ad_reward)
        else:
            # Show error popup
            print("No ads available")
    
    def handle_back_button(self):
        """Handle Android back button"""
        # Show quit confirmation
        self.state_manager.quit_game()