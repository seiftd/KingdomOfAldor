#!/usr/bin/env python3
"""
Kingdom of Aldoria - Game Runner
This script automatically sets up the proper display environment and runs the game.
"""

import os
import sys
import subprocess
import time

def run_game():
    """Run the game with proper display setup"""
    print("🏰 Kingdom of Aldoria - Game Runner")
    print("📺 Setting up display environment...")
    
    # Check if we have xvfb-run available
    try:
        subprocess.run(['which', 'xvfb-run'], check=True, capture_output=True)
        print("✅ Virtual display support found")
        
        # Run the game with xvfb-run
        print("🎮 Starting game with virtual display...")
        cmd = ['xvfb-run', '-a', '--server-args=-screen 0 1280x720x24', 'python3', 'main.py'] + sys.argv[1:]
        subprocess.run(cmd)
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  No virtual display support - trying direct mode...")
        
        # Try to run directly
        cmd = ['python3', 'main.py'] + sys.argv[1:]
        subprocess.run(cmd)
    
    print("👋 Game session ended")

if __name__ == "__main__":
    run_game()