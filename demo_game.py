#!/usr/bin/env python3
"""
Kingdom of Aldoria - Demo Script
Demonstrates game structure and core functionality without requiring pygame
"""

import json
import time
from datetime import datetime

def demo_game_config():
    """Demonstrate game configuration"""
    print("🎮 Kingdom of Aldoria - Game Configuration Demo")
    print("=" * 60)
    
    # Import config without pygame dependencies
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))
    
    from game.core.config import GameConfig
    
    print(f"📱 Screen Resolution: {GameConfig.SCREEN_WIDTH}x{GameConfig.SCREEN_HEIGHT}")
    print(f"🌍 Total Worlds: {GameConfig.TOTAL_WORLDS}")
    print(f"🎯 Stages per World: {GameConfig.STAGES_PER_WORLD}")
    print(f"⚡ Total Stages: {GameConfig.TOTAL_WORLDS * GameConfig.STAGES_PER_WORLD}")
    print(f"🔋 Max Stamina: {GameConfig.MAX_STAMINA_DEFAULT}")
    print(f"⏰ Stamina Recharge: {GameConfig.STAMINA_RECHARGE_TIME // 60} minutes")
    
    print("\n🗺️ Available Worlds:")
    for world_id, world_data in GameConfig.WORLD_DATA.items():
        print(f"  {world_id}. {world_data['name']} - {world_data['description']}")
    
    print("\n👤 Character Skins:")
    for skin_id, skin_data in GameConfig.CHARACTER_SKINS.items():
        skill_text = f" (Skill: {skin_data['skill']})" if skin_data['skill'] else ""
        print(f"  • {skin_data['name']}{skill_text} - {skin_data['description']}")
    
    print("\n⚔️ Weapons:")
    for weapon_id, weapon_data in GameConfig.WEAPON_DATA.items():
        print(f"  • {weapon_data['name']} - Damage: {weapon_data['damage']} - {weapon_data['description']}")
    
    print("\n💰 Monetization:")
    print(f"  • Weekly Sub: ${GameConfig.WEEKLY_SUB_PRICE} - {GameConfig.WEEKLY_SUB_GEMS_DAILY} gems/day")
    print(f"  • Monthly Sub: ${GameConfig.MONTHLY_SUB_PRICE} - {GameConfig.MONTHLY_SUB_GEMS_DAILY} gems/day")
    print(f"  • Gems per Ad: {GameConfig.GEMS_PER_AD}")
    print(f"  • Max Ads/Day: {GameConfig.MAX_ADS_PER_DAY}")

def demo_balance_calculations():
    """Demonstrate game balance calculations"""
    print("\n⚖️ Game Balance Calculations")
    print("=" * 40)
    
    from game.core.config import GameConfig
    
    print("📈 Level Progression (XP Requirements):")
    for level in [1, 5, 10, 20, 50]:
        xp_req = GameConfig.get_xp_requirement(level)
        print(f"  Level {level}: {xp_req:,} XP required")
    
    print("\n🦹 Enemy Scaling Examples:")
    print("  Format: World-Stage (Player Level) -> HP | Damage")
    test_cases = [
        (1, 1, 1),   # Early game
        (1, 30, 10), # End of first world
        (5, 15, 25), # Mid game
        (10, 30, 50) # End game
    ]
    
    for world, stage, player_level in test_cases:
        enemy_hp = GameConfig.get_enemy_hp(world, stage, player_level)
        enemy_dmg = GameConfig.get_enemy_damage(world, stage, player_level)
        print(f"  {world}-{stage} (Lv{player_level}): {enemy_hp} HP | {enemy_dmg} DMG")
    
    print("\n💎 Reward Calculations:")
    for world in [1, 5, 10]:
        for stage in [1, 15, 30]:
            gold = GameConfig.get_stage_reward_gold(world, stage)
            xp = GameConfig.get_stage_reward_xp(world, stage)
            print(f"  World {world} Stage {stage}: {gold} Gold, {xp} XP")

def demo_save_system():
    """Demonstrate save/load system"""
    print("\n💾 Save System Demo")
    print("=" * 30)
    
    from game.core.save_manager import SaveManager
    
    # Create save manager
    save_manager = SaveManager()
    
    print("📋 Initial Player Data:")
    player_data = save_manager.get_player_data()
    print(f"  Name: {player_data['name']}")
    print(f"  Level: {player_data['level']}")
    print(f"  Gold: {player_data['gold']:,}")
    print(f"  Gems: {player_data['gems']:,}")
    print(f"  Stamina: {player_data['stamina']}/{player_data['max_stamina']}")
    
    print("\n💰 Testing Currency Operations:")
    print("  Adding 500 gold...")
    save_manager.add_gold(500)
    print(f"  New gold: {save_manager.get_player_data()['gold']:,}")
    
    print("  Spending 200 gold...")
    success = save_manager.spend_gold(200)
    print(f"  Success: {success}, Remaining: {save_manager.get_player_data()['gold']:,}")
    
    print("  Adding 100 gems...")
    save_manager.add_gems(100)
    print(f"  New gems: {save_manager.get_player_data()['gems']:,}")
    
    print("\n⭐ Testing Experience System:")
    print("  Adding 300 XP...")
    save_manager.add_experience(300)
    player_data = save_manager.get_player_data()
    print(f"  New level: {player_data['level']}")
    print(f"  Remaining XP: {player_data['experience']}")
    
    print("\n🏆 Testing Stage Completion:")
    rewards = {"gold": 50, "gems": 5, "experience": 75}
    save_manager.complete_stage(1, 5, rewards)
    progress_data = save_manager.get_progress_data()
    print(f"  Stages completed: {len(progress_data['stages_completed'])}")
    print(f"  Total stages: {progress_data['total_stages_completed']}")

def demo_mobile_features():
    """Demonstrate mobile-specific features"""
    print("\n📱 Mobile Features Demo")
    print("=" * 35)
    
    from game.utils.mobile_utils import MobileUtils, AdManager, NotificationManager
    
    mobile_utils = MobileUtils()
    print(f"🔍 Mobile Platform Detected: {mobile_utils.is_mobile}")
    print(f"🤖 Android Device: {mobile_utils.is_android}")
    print(f"📺 Screen Size: {mobile_utils.screen_size}")
    
    print("\n📺 Ad Manager Demo:")
    ad_manager = mobile_utils.ad_manager
    ad_manager.initialize_ads()
    
    print(f"  Can show rewarded ad: {ad_manager.can_show_rewarded_ad()}")
    print(f"  Can show interstitial: {ad_manager.can_show_interstitial_ad()}")
    print(f"  Ads watched today: {ad_manager.ads_watched_today}/{ad_manager.max_ads_per_day}")
    
    # Simulate watching an ad
    def mock_ad_reward(success):
        if success:
            print("  ✅ Ad watched! Rewarded 30 gems")
        else:
            print("  ❌ Ad failed or cancelled")
    
    if ad_manager.can_show_rewarded_ad():
        print("  🎬 Simulating rewarded ad...")
        ad_manager.show_rewarded_ad(mock_ad_reward)
    
    print("\n🔔 Notification Manager Demo:")
    notification_manager = mobile_utils.notification_manager
    
    print("  📅 Scheduling stamina notification...")
    notification_manager.schedule_stamina_notification(20)  # 20 minutes
    
    print("  🎁 Scheduling daily reward notification...")
    notification_manager.schedule_daily_reward_notification()
    
    print(f"  📋 Scheduled notifications: {len(notification_manager.scheduled_notifications)}")

def demo_player_progression():
    """Demonstrate player progression simulation"""
    print("\n⚔️ Player Progression Simulation")
    print("=" * 45)
    
    from game.core.save_manager import SaveManager
    
    save_manager = SaveManager()
    
    print("🎯 Simulating a gaming session...")
    print("Starting stats:")
    player_data = save_manager.get_player_data()
    print(f"  Level: {player_data['level']}")
    print(f"  HP: {player_data['stats']['hp']}/{player_data['stats']['max_hp']}")
    print(f"  Attack: {player_data['stats']['attack']}")
    print(f"  Defense: {player_data['stats']['defense']}")
    
    # Simulate completing several stages
    stages_to_complete = [
        (1, 1, {"gold": 15, "experience": 35}),
        (1, 2, {"gold": 17, "experience": 38}),
        (1, 3, {"gold": 19, "experience": 41}),
        (1, 4, {"gold": 21, "experience": 44}),
        (1, 5, {"gold": 25, "experience": 50, "gems": 5}),  # Boss stage
    ]
    
    for world, stage, rewards in stages_to_complete:
        save_manager.complete_stage(world, stage, rewards)
        print(f"✅ Completed World {world} Stage {stage}")
        for reward_type, amount in rewards.items():
            print(f"    +{amount} {reward_type}")
    
    print("\nFinal stats:")
    player_data = save_manager.get_player_data()
    print(f"  Level: {player_data['level']}")
    print(f"  Gold: {player_data['gold']:,}")
    print(f"  Gems: {player_data['gems']:,}")
    print(f"  XP: {player_data['experience']}")
    print(f"  HP: {player_data['stats']['hp']}/{player_data['stats']['max_hp']}")
    print(f"  Attack: {player_data['stats']['attack']}")

def demo_monetization_simulation():
    """Demonstrate monetization features"""
    print("\n💎 Monetization Simulation")
    print("=" * 35)
    
    from game.utils.mobile_utils import InAppPurchase
    
    iap = InAppPurchase()
    
    print("🛒 Available Products:")
    for product_id, product_info in iap.products.items():
        print(f"  • {product_info['name']} - {product_info['price']}")
        print(f"    {product_info['description']}")
    
    print("\n💳 Simulating Purchases:")
    
    def purchase_success(product_id):
        print(f"  ✅ Successfully purchased: {product_id}")
    
    # Simulate starter pack purchase
    print("  🛍️ Purchasing starter pack...")
    iap.purchase_product("starter_pack", purchase_success)
    
    print(f"  📦 Starter pack purchased: {iap.has_purchased('starter_pack')}")
    
    print("\n📊 Revenue Simulation (30 days):")
    daily_revenue = 0
    total_revenue = 0
    
    # Simulate different monetization sources
    daily_ad_revenue = 30 * 0.02  # 30 ads at $0.02 each
    weekly_subs = 5  # 5 weekly subscribers
    monthly_subs = 2  # 2 monthly subscribers
    
    weekly_sub_revenue = weekly_subs * 4.99 / 7  # Daily from weekly subs
    monthly_sub_revenue = monthly_subs * 15.99 / 30  # Daily from monthly subs
    
    daily_revenue = daily_ad_revenue + weekly_sub_revenue + monthly_sub_revenue
    total_revenue = daily_revenue * 30
    
    print(f"  📱 Daily Ad Revenue: ${daily_ad_revenue:.2f}")
    print(f"  📅 Weekly Sub Revenue/Day: ${weekly_sub_revenue:.2f}")
    print(f"  📆 Monthly Sub Revenue/Day: ${monthly_sub_revenue:.2f}")
    print(f"  💰 Total Daily Revenue: ${daily_revenue:.2f}")
    print(f"  🏆 30-Day Revenue: ${total_revenue:.2f}")

def main():
    """Run all demonstrations"""
    print("🏰 KINGDOM OF ALDORIA - Complete Game Demo")
    print("🎮 2D Mobile RPG for Android")
    print("⚔️ Built with Python & Pygame")
    print("\n" + "=" * 60)
    
    try:
        demo_game_config()
        demo_balance_calculations()
        demo_save_system()
        demo_mobile_features()
        demo_player_progression()
        demo_monetization_simulation()
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("\n📋 Game Features Summary:")
        print("✅ 10 fantasy worlds with 300 total stages")
        print("✅ Character progression with 5 unique skins")
        print("✅ Weapon system with 5 upgradeable weapons")
        print("✅ Stamina system with timed recharge")
        print("✅ Dual currency (Gold & Gems)")
        print("✅ Mobile-optimized with touch controls")
        print("✅ Monetization with ads and subscriptions")
        print("✅ Save/load system with encryption")
        print("✅ Balanced progression formulas")
        print("✅ Boss battles every 5 stages")
        
        print("\n🚀 Ready for Android deployment with Buildozer!")
        print("📱 Target: HD mobile devices (1280x720)")
        print("📦 Size: Under 2GB with asset optimization")
        print("💰 F2P with premium features")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()