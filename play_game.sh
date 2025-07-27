#!/bin/bash

# Kingdom of Aldoria - Play Game Script
# This script runs the game with a virtual display for compatibility

echo "🏰 Kingdom of Aldoria - Starting Game..."
echo "📺 Creating virtual display..."

# Run the game with virtual framebuffer
xvfb-run -a --server-args="-screen 0 1280x720x24" python3 main.py

echo "👋 Game session ended"