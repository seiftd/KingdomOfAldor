#!/usr/bin/env python3
"""
Kingdom of Aldoria - 2D Mobile RPG Game
Main entry point and game initialization
"""

import pygame
import sys
import os
from enum import Enum
import json
import time
from datetime import datetime, timedelta

# Add the game modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))

from game.states.state_manager import StateManager
from game.states.main_menu import MainMenuState
from game.core.config import GameConfig
from game.core.asset_manager import AssetManager
from game.core.audio_manager import AudioManager
from game.core.save_manager import SaveManager
from game.utils.mobile_utils import MobileUtils

class KingdomOfAldoria:
    """Main game class for Kingdom of Aldoria RPG"""
    
    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Set up display
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Kingdom of Aldoria")
        
        # Initialize core systems
        self.clock = pygame.time.Clock()
        self.running = True
        self.mobile_utils = MobileUtils()
        
        # Initialize managers
        self.asset_manager = AssetManager()
        self.audio_manager = AudioManager()
        self.save_manager = SaveManager()
        self.state_manager = StateManager()
        
        # Load game icon
        try:
            icon = pygame.image.load("assets/ui/game_icon.png")
            pygame.display.set_icon(icon)
        except:
            pass  # Icon not found, continue without it
        
        # Initialize first state
        self.state_manager.push_state(MainMenuState())
        
        # Mobile optimizations
        self.mobile_utils.optimize_for_mobile()
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Android back button handling
                    self.state_manager.handle_back_button()
            else:
                # Pass event to current state
                self.state_manager.handle_event(event)
    
    def update(self, dt):
        """Update game logic"""
        self.state_manager.update(dt)
        
        # Check if game should quit
        if self.state_manager.should_quit():
            self.running = False
    
    def render(self):
        """Render the game"""
        self.screen.fill((0, 0, 0))  # Clear screen
        self.state_manager.render(self.screen)
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting Kingdom of Aldoria...")
        
        # Load initial assets
        self.asset_manager.load_essential_assets()
        
        last_time = time.time()
        
        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Cap delta time to prevent large jumps
            dt = min(dt, 1.0 / 30.0)
            
            # Game loop
            self.handle_events()
            self.update(dt)
            self.render()
            
            # Control frame rate
            self.clock.tick(self.config.FPS)
        
        # Cleanup
        self.shutdown()
    
    def shutdown(self):
        """Clean shutdown of the game"""
        print("Shutting down Kingdom of Aldoria...")
        
        # Save game state
        self.save_manager.save_all()
        
        # Cleanup audio
        self.audio_manager.cleanup()
        
        # Quit pygame
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    try:
        game = KingdomOfAldoria()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()