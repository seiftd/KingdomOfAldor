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

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.game import Game
from core.config import Config

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
    
    logger.info("Starting Kingdom of Aldoria v1.0.0")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize Pygame
    try:
        pygame.init()
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        logger.info("Pygame initialized successfully")
        
        # Create and run game
        game = Game()
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