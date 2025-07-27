#!/usr/bin/env python3
"""
Kingdom of Aldoria - 2D Mobile RPG Game
Main entry point for the game

Author: Kingdom of Aldoria Team
Version: 1.0.0
"""

import sys
import os
import pygame
import logging
from pathlib import Path

# Add src directory to path and adjust Python path for relative imports
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)
sys.path.insert(0, os.path.dirname(__file__))

# Import the game modules
import src.core.game as game_module
from src.core.config import Config

Game = game_module.Game

def setup_logging():
    """Setup logging configuration"""
    log_level = logging.DEBUG if Config.DEBUG else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('kingdom_of_aldoria.log'),
            logging.StreamHandler()
        ]
    )
    
def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import pygame
        import PIL
        import numpy
        return True
    except ImportError as e:
        logging.error(f"Missing dependency: {e}")
        print(f"Error: Missing required dependency - {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def main():
    """Main entry point for Kingdom of Aldoria"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check for test mode
    test_mode = len(sys.argv) > 1 and '--test' in sys.argv
    if test_mode:
        logger.info("Starting Kingdom of Aldoria v1.0.0 in TEST MODE")
    else:
        logger.info("Starting Kingdom of Aldoria v1.0.0")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize Pygame
    try:
        # Set appropriate video driver based on environment
        if test_mode:
            # Use dummy driver for test mode only
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            logger.info("Using dummy video driver (test mode)")
        else:
            # Try to use default driver for window display
            logger.info("Attempting to create game window...")
        
        pygame.init()
        
        # Try to initialize audio, but don't fail if no audio device
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            logger.info("Pygame with audio initialized successfully")
        except pygame.error as audio_error:
            logger.warning(f"Audio initialization failed: {audio_error}")
            logger.info("Continuing without audio...")
            # Initialize pygame without audio
            pygame.mixer.quit()
        
        logger.info("Pygame initialized successfully")
        
        # Create and run game
        game = Game()
        
        if test_mode:
            logger.info("Test mode: Game initialized successfully!")
            logger.info("Game components:")
            logger.info(f"  - State Manager: {type(game.state_manager).__name__}")
            logger.info(f"  - Asset Manager: {type(game.asset_manager).__name__}")
            logger.info(f"  - Audio Manager: {type(game.audio_manager).__name__}")
            logger.info("Test completed successfully - game can start without black screen!")
        else:
            game.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Game crashed with error: {e}")
        sys.exit(1)
    
    finally:
        pygame.quit()
        logger.info("Game shutdown complete")

if __name__ == "__main__":
    main()