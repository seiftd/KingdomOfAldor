"""
Kingdom of Aldoria - Main Game Class
Handles game loop, state management, and core system coordination
"""

import pygame
import logging
import time
from typing import Dict, Any

from .config import Config, GameStates
from .state_manager import StateManager
from ..systems.asset_manager import AssetManager
from ..systems.audio_manager import AudioManager
from ..systems.save_manager import SaveManager
from ..systems.input_manager import InputManager
from ..ui.main_menu import MainMenuState
from ..ui.world_map import WorldMapState
from ..ui.battle_ui import BattleState
from ..ui.shop import ShopState

class Game:
    """Main game class that manages the overall game loop and state"""
    
    def __init__(self):
        """Initialize the game"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Kingdom of Aldoria")
        
        # Initialize Pygame display
        self.screen = pygame.display.set_mode(
            (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT),
            pygame.FULLSCREEN if Config.FULLSCREEN else 0
        )
        pygame.display.set_caption(Config.GAME_TITLE)
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.running = True
        self.last_time = time.time()
        
        # Core systems
        self.asset_manager = AssetManager()
        self.audio_manager = AudioManager()
        self.save_manager = SaveManager()
        self.input_manager = InputManager()
        
        # State management
        self.state_manager = StateManager()
        self._setup_states()
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_timer = 0
        
        self.logger.info("Game initialization complete")
    
    def _setup_states(self):
        """Setup all game states"""
        # Register all game states
        self.state_manager.add_state(GameStates.MAIN_MENU, MainMenuState(self))
        self.state_manager.add_state(GameStates.WORLD_MAP, WorldMapState(self))
        self.state_manager.add_state(GameStates.BATTLE, BattleState(self))
        self.state_manager.add_state(GameStates.SHOP, ShopState(self))
        
        # Set initial state
        self.state_manager.change_state(GameStates.MAIN_MENU)
    
    def run(self):
        """Main game loop"""
        self.logger.info("Starting main game loop")
        
        try:
            while self.running:
                current_time = time.time()
                dt = current_time - self.last_time
                self.last_time = current_time
                
                # Handle events
                self._handle_events()
                
                # Update current state
                if self.state_manager.current_state:
                    self.state_manager.current_state.update(dt)
                
                # Render
                self._render()
                
                # Control FPS
                self.clock.tick(Config.FPS)
                
                # Update FPS counter
                self._update_fps_counter(dt)
                
        except Exception as e:
            self.logger.error(f"Error in main game loop: {e}", exc_info=True)
            raise
        
        finally:
            self._cleanup()
    
    def _handle_events(self):
        """Handle pygame events"""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state_manager.current_state_name == GameStates.MAIN_MENU:
                        self.quit_game()
                    else:
                        self.state_manager.change_state(GameStates.MAIN_MENU)
                elif event.key == pygame.K_F11:
                    self._toggle_fullscreen()
                elif Config.DEBUG and event.key == pygame.K_F12:
                    self._toggle_debug_mode()
            
            # Pass events to input manager
            self.input_manager.handle_event(event)
            
            # Pass events to current state
            if self.state_manager.current_state:
                self.state_manager.current_state.handle_event(event)
    
    def _render(self):
        """Render the current frame"""
        # Clear screen
        self.screen.fill(Config.BLACK)
        
        # Render current state
        if self.state_manager.current_state:
            self.state_manager.current_state.render(self.screen)
        
        # Debug information
        if Config.DEBUG:
            self._render_debug_info()
        
        # Update display
        pygame.display.flip()
    
    def _render_debug_info(self):
        """Render debug information"""
        font = pygame.font.Font(None, 24)
        
        # FPS
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, Config.WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        # Current state
        state_text = font.render(f"State: {self.state_manager.current_state_name}", True, Config.WHITE)
        self.screen.blit(state_text, (10, 35))
        
        # Memory usage (approximate)
        memory_text = font.render("Memory: OK", True, Config.GREEN)
        self.screen.blit(memory_text, (10, 60))
    
    def _update_fps_counter(self, dt):
        """Update FPS counter for performance monitoring"""
        self.fps_timer += dt
        self.fps_counter += 1
        
        if self.fps_timer >= 1.0:  # Log FPS every second
            avg_fps = self.fps_counter / self.fps_timer
            if avg_fps < Config.FPS * 0.8:  # Log if FPS drops below 80% target
                self.logger.warning(f"Low FPS detected: {avg_fps:.1f}")
            
            self.fps_counter = 0
            self.fps_timer = 0
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        Config.FULLSCREEN = not Config.FULLSCREEN
        
        if Config.FULLSCREEN:
            self.screen = pygame.display.set_mode(
                (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
            )
        
        self.logger.info(f"Fullscreen toggled: {Config.FULLSCREEN}")
    
    def _toggle_debug_mode(self):
        """Toggle debug mode"""
        Config.DEBUG = not Config.DEBUG
        self.logger.info(f"Debug mode toggled: {Config.DEBUG}")
    
    def _cleanup(self):
        """Cleanup resources before shutdown"""
        self.logger.info("Cleaning up game resources")
        
        # Save game data
        try:
            self.save_manager.save_game_data()
            self.logger.info("Game data saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save game data: {e}")
        
        # Cleanup systems
        if hasattr(self, 'audio_manager'):
            self.audio_manager.cleanup()
        
        if hasattr(self, 'asset_manager'):
            self.asset_manager.cleanup()
    
    def quit_game(self):
        """Gracefully quit the game"""
        self.logger.info("Game quit requested")
        self.running = False
    
    def change_state(self, new_state: str, **kwargs):
        """Change game state with optional parameters"""
        self.state_manager.change_state(new_state, **kwargs)
    
    def get_system(self, system_name: str) -> Any:
        """Get reference to a game system"""
        systems = {
            'asset_manager': self.asset_manager,
            'audio_manager': self.audio_manager,
            'save_manager': self.save_manager,
            'input_manager': self.input_manager,
        }
        return systems.get(system_name)
    
    @property
    def delta_time(self) -> float:
        """Get the time since last frame in seconds"""
        return self.clock.get_time() / 1000.0