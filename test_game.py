#!/usr/bin/env python3
"""
Kingdom of Aldoria - Test Script
Validates core game components without requiring display
"""

import os
import sys
import traceback

# Disable pygame display for testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

def test_imports():
    """Test all core imports"""
    print("Testing imports...")
    
    try:
        import pygame
        print("✓ Pygame imported successfully")
    except ImportError as e:
        print(f"✗ Pygame import failed: {e}")
        return False
    
    try:
        from game.core.config import GameConfig
        print("✓ GameConfig imported successfully")
    except ImportError as e:
        print(f"✗ GameConfig import failed: {e}")
        return False
    
    try:
        from game.core.asset_manager import AssetManager
        print("✓ AssetManager imported successfully")
    except ImportError as e:
        print(f"✗ AssetManager import failed: {e}")
        return False
    
    try:
        from game.core.audio_manager import AudioManager
        print("✓ AudioManager imported successfully")
    except ImportError as e:
        print(f"✗ AudioManager import failed: {e}")
        return False
    
    try:
        from game.core.save_manager import SaveManager
        print("✓ SaveManager imported successfully")
    except ImportError as e:
        print(f"✗ SaveManager import failed: {e}")
        return False
    
    try:
        from game.states.state_manager import StateManager, GameState
        print("✓ StateManager imported successfully")
    except ImportError as e:
        print(f"✗ StateManager import failed: {e}")
        return False
    
    try:
        from game.entities.player import Player
        print("✓ Player imported successfully")
    except ImportError as e:
        print(f"✗ Player import failed: {e}")
        return False
    
    try:
        from game.ui.button import Button
        print("✓ Button imported successfully")
    except ImportError as e:
        print(f"✗ Button import failed: {e}")
        return False
    
    try:
        from game.ui.panel import Panel
        print("✓ Panel imported successfully")
    except ImportError as e:
        print(f"✗ Panel import failed: {e}")
        return False
    
    try:
        from game.utils.mobile_utils import MobileUtils
        print("✓ MobileUtils imported successfully")
    except ImportError as e:
        print(f"✗ MobileUtils import failed: {e}")
        return False
    
    return True

def test_config():
    """Test game configuration"""
    print("\nTesting configuration...")
    
    try:
        from game.core.config import GameConfig
        
        # Test basic config values
        assert GameConfig.SCREEN_WIDTH == 1280
        assert GameConfig.SCREEN_HEIGHT == 720
        assert GameConfig.TOTAL_WORLDS == 10
        assert GameConfig.STAGES_PER_WORLD == 30
        
        print("✓ Basic config values correct")
        
        # Test world data
        assert len(GameConfig.WORLD_DATA) == 10
        assert 1 in GameConfig.WORLD_DATA
        assert GameConfig.WORLD_DATA[1]["name"] == "Forest of Shadows"
        
        print("✓ World data configuration correct")
        
        # Test character skins
        assert "default_knight" in GameConfig.CHARACTER_SKINS
        assert "forest_scout" in GameConfig.CHARACTER_SKINS
        
        print("✓ Character skin configuration correct")
        
        # Test weapons
        assert "bronze_sword" in GameConfig.WEAPON_DATA
        assert "solar_flare_sword" in GameConfig.WEAPON_DATA
        
        print("✓ Weapon configuration correct")
        
        # Test balance formulas
        xp_req = GameConfig.get_xp_requirement(5)
        assert xp_req > 100  # Should be scaled
        
        enemy_hp = GameConfig.get_enemy_hp(1, 1, 1)
        assert enemy_hp == 100  # Base values
        
        enemy_hp_scaled = GameConfig.get_enemy_hp(2, 5, 10)
        assert enemy_hp_scaled > enemy_hp  # Should be higher
        
        print("✓ Balance formulas working correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        traceback.print_exc()
        return False

def test_save_manager():
    """Test save manager functionality"""
    print("\nTesting save manager...")
    
    try:
        from game.core.save_manager import SaveManager
        
        # Create save manager
        save_manager = SaveManager()
        
        # Test default save data
        player_data = save_manager.get_player_data()
        assert player_data["name"] == "Arin"
        assert player_data["level"] == 1
        assert player_data["gold"] == 100
        
        print("✓ Default save data correct")
        
        # Test currency operations
        save_manager.add_gold(50)
        assert save_manager.get_player_data()["gold"] == 150
        
        success = save_manager.spend_gold(25)
        assert success == True
        assert save_manager.get_player_data()["gold"] == 125
        
        print("✓ Currency operations working")
        
        # Test experience and leveling
        save_manager.add_experience(200)
        player_data = save_manager.get_player_data()
        assert player_data["level"] > 1  # Should have leveled up
        
        print("✓ Experience and leveling working")
        
        return True
        
    except Exception as e:
        print(f"✗ Save manager test failed: {e}")
        traceback.print_exc()
        return False

def test_player():
    """Test player entity"""
    print("\nTesting player entity...")
    
    try:
        from game.entities.player import Player
        from game.core.save_manager import SaveManager
        
        # Create player from save data
        save_manager = SaveManager()
        player_data = save_manager.get_player_data()
        
        player = Player(player_data)
        
        # Test basic properties
        assert player.name == "Arin"
        assert player.level == 1
        assert player.is_alive() == True
        
        print("✓ Player initialization correct")
        
        # Test stats
        total_attack = player.get_total_attack()
        assert total_attack > 0
        
        total_defense = player.get_total_defense()
        assert total_defense > 0
        
        print("✓ Player stats calculation working")
        
        # Test skills
        available_skills = player.available_skills
        # Default knight has no skills
        assert len(available_skills) == 0
        
        print("✓ Player skills system working")
        
        return True
        
    except Exception as e:
        print(f"✗ Player test failed: {e}")
        traceback.print_exc()
        return False

def test_pygame_init():
    """Test pygame initialization"""
    print("\nTesting pygame initialization...")
    
    try:
        import pygame
        
        # Initialize pygame
        pygame.init()
        print("✓ Pygame initialized successfully")
        
        # Test mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✓ Pygame mixer initialized successfully")
        
        # Test display (dummy mode)
        screen = pygame.display.set_mode((1280, 720))
        print("✓ Pygame display initialized successfully")
        
        # Test font
        font = pygame.font.Font(None, 24)
        print("✓ Pygame font system working")
        
        pygame.quit()
        print("✓ Pygame cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Pygame test failed: {e}")
        traceback.print_exc()
        return False

def test_asset_manager():
    """Test asset manager"""
    print("\nTesting asset manager...")
    
    try:
        from game.core.asset_manager import AssetManager
        import pygame
        
        pygame.init()
        pygame.display.set_mode((1280, 720))
        
        asset_manager = AssetManager()
        asset_manager.load_essential_assets()
        
        print("✓ Asset manager initialized and essential assets loaded")
        
        # Test font loading
        font = asset_manager.load_font("test", None, 24)
        assert font is not None
        
        print("✓ Font loading working")
        
        # Test memory usage
        memory_usage = asset_manager.get_memory_usage()
        assert "images_loaded" in memory_usage
        
        print("✓ Memory usage tracking working")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ Asset manager test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Kingdom of Aldoria - Component Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_config),
        ("Save Manager Tests", test_save_manager),
        ("Player Entity Tests", test_player),
        ("Pygame Initialization Tests", test_pygame_init),
        ("Asset Manager Tests", test_asset_manager),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The game core is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())