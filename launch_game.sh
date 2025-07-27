#!/bin/bash

# Kingdom of Aldoria Game Launcher
# This script sets up a virtual display for the game to run properly

echo "🏰 Starting Kingdom of Aldoria..."
echo "📺 Setting up virtual display..."

# Kill any existing Xvfb processes on display :99
pkill -f "Xvfb :99" 2>/dev/null || true

# Start Xvfb virtual display
Xvfb :99 -screen 0 1280x720x24 &
XVFB_PID=$!

# Set display environment
export DISPLAY=:99

# Wait for Xvfb to start
sleep 2

echo "✅ Virtual display ready on $DISPLAY"
echo "🎮 Starting game..."

# Run the game
python3 main.py

# Cleanup
echo "🧹 Cleaning up..."
kill $XVFB_PID 2>/dev/null || true

echo "👋 Game session ended"