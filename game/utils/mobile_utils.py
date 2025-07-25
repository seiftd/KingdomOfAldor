"""
Kingdom of Aldoria - Mobile Utilities
Android-specific optimizations and platform integration
"""

import pygame
import os
import platform
from typing import Dict, Any, Optional, Callable

class MobileUtils:
    """Utilities for mobile platform optimization and integration"""
    
    def __init__(self):
        """Initialize mobile utilities"""
        self.is_mobile = self._detect_mobile_platform()
        self.is_android = platform.system().lower() == "android"
        self.screen_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (1280, 720)
        
        # Touch input state
        self.touches = {}
        self.last_touch_time = 0
        self.touch_sensitivity = 1.0
        
        # Performance optimization
        self.frame_time_history = []
        self.max_frame_history = 60
        self.target_fps = 60
        
        # Android-specific
        self.back_button_callback: Optional[Callable] = None
        self.pause_callback: Optional[Callable] = None
        self.resume_callback: Optional[Callable] = None
        
        # Ad integration
        self.ad_manager = AdManager()
        
        # Notifications
        self.notification_manager = NotificationManager()
        
    def _detect_mobile_platform(self) -> bool:
        """Detect if running on mobile platform"""
        system = platform.system().lower()
        return system in ["android", "ios"]
    
    def optimize_for_mobile(self):
        """Apply mobile-specific optimizations"""
        if self.is_mobile:
            print("Applying mobile optimizations...")
            
            # Reduce particle density
            os.environ['PARTICLE_DENSITY'] = '0.5'
            
            # Set appropriate texture quality
            os.environ['TEXTURE_QUALITY'] = 'medium'
            
            # Enable touch input
            self._setup_touch_input()
            
            # Optimize memory usage
            self._optimize_memory()
            
            print("Mobile optimizations applied")
    
    def _setup_touch_input(self):
        """Setup touch input handling"""
        if self.is_mobile:
            # Enable multitouch
            os.environ['SDL_ANDROID_APK_EXPANSION_MAIN_FILE_VERSION'] = '1'
            os.environ['SDL_ANDROID_APK_EXPANSION_PATCH_FILE_VERSION'] = '1'
    
    def _optimize_memory(self):
        """Optimize memory usage for mobile devices"""
        # Suggest garbage collection more frequently
        import gc
        gc.set_threshold(700, 10, 10)  # More aggressive GC
    
    def handle_touch_event(self, event) -> Dict[str, Any]:
        """Handle touch events and convert to game input"""
        touch_data = {
            "type": "none",
            "position": (0, 0),
            "finger_id": 0,
            "pressure": 1.0
        }
        
        if event.type == pygame.FINGERDOWN:
            touch_data["type"] = "down"
            touch_data["position"] = self._normalize_touch_position(event.x, event.y)
            touch_data["finger_id"] = event.finger_id
            self.touches[event.finger_id] = touch_data
            
        elif event.type == pygame.FINGERUP:
            touch_data["type"] = "up"
            touch_data["position"] = self._normalize_touch_position(event.x, event.y)
            touch_data["finger_id"] = event.finger_id
            if event.finger_id in self.touches:
                del self.touches[event.finger_id]
                
        elif event.type == pygame.FINGERMOTION:
            touch_data["type"] = "move"
            touch_data["position"] = self._normalize_touch_position(event.x, event.y)
            touch_data["finger_id"] = event.finger_id
            self.touches[event.finger_id] = touch_data
        
        return touch_data
    
    def _normalize_touch_position(self, x: float, y: float) -> tuple:
        """Convert normalized touch coordinates to screen coordinates"""
        screen_x = int(x * self.screen_size[0])
        screen_y = int(y * self.screen_size[1])
        return (screen_x, screen_y)
    
    def is_touch_over_rect(self, touch_pos: tuple, rect: pygame.Rect) -> bool:
        """Check if touch position is over a rectangle"""
        return rect.collidepoint(touch_pos)
    
    def handle_back_button(self):
        """Handle Android back button press"""
        if self.back_button_callback:
            self.back_button_callback()
    
    def set_back_button_callback(self, callback: Callable):
        """Set callback for back button press"""
        self.back_button_callback = callback
    
    def on_pause(self):
        """Handle app pause (Android lifecycle)"""
        print("App paused")
        if self.pause_callback:
            self.pause_callback()
    
    def on_resume(self):
        """Handle app resume (Android lifecycle)"""
        print("App resumed")
        if self.resume_callback:
            self.resume_callback()
    
    def set_lifecycle_callbacks(self, pause_callback: Callable, resume_callback: Callable):
        """Set Android lifecycle callbacks"""
        self.pause_callback = pause_callback
        self.resume_callback = resume_callback
    
    def update_performance_metrics(self, frame_time: float):
        """Update performance metrics for optimization"""
        self.frame_time_history.append(frame_time)
        
        if len(self.frame_time_history) > self.max_frame_history:
            self.frame_time_history.pop(0)
    
    def get_average_fps(self) -> float:
        """Get average FPS over recent frames"""
        if not self.frame_time_history:
            return 60.0
        
        avg_frame_time = sum(self.frame_time_history) / len(self.frame_time_history)
        return 1.0 / max(avg_frame_time, 0.001)  # Avoid division by zero
    
    def should_reduce_quality(self) -> bool:
        """Check if quality should be reduced based on performance"""
        avg_fps = self.get_average_fps()
        return avg_fps < self.target_fps * 0.8  # Reduce if below 80% of target
    
    def get_safe_area_insets(self) -> Dict[str, int]:
        """Get safe area insets for devices with notches/rounded corners"""
        # Default safe area (can be overridden by platform-specific code)
        return {
            "top": 0,
            "bottom": 0,
            "left": 0,
            "right": 0
        }
    
    def vibrate(self, duration: int = 100):
        """Trigger device vibration"""
        if self.is_android:
            try:
                from plyer import vibrator
                vibrator.vibrate(duration / 1000.0)  # Convert to seconds
            except:
                print("Vibration not supported")
    
    def show_keyboard(self, text_input_rect: pygame.Rect):
        """Show on-screen keyboard for text input"""
        if self.is_mobile:
            # This would integrate with platform-specific keyboard
            print(f"Showing keyboard for input at {text_input_rect}")
    
    def hide_keyboard(self):
        """Hide on-screen keyboard"""
        if self.is_mobile:
            print("Hiding keyboard")

class AdManager:
    """Manages ad integration and rewards"""
    
    def __init__(self):
        """Initialize ad manager"""
        self.ads_watched_today = 0
        self.max_ads_per_day = 30
        self.rewarded_ad_cooldown = 0
        self.interstitial_ad_cooldown = 0
        
        # Mock ad networks (replace with real implementation)
        self.ad_networks = {
            "admob": {
                "initialized": False,
                "test_mode": True
            }
        }
        
        # Ad callbacks
        self.rewarded_ad_callback: Optional[Callable] = None
        self.interstitial_ad_callback: Optional[Callable] = None
    
    def initialize_ads(self):
        """Initialize ad networks"""
        print("Initializing ad networks...")
        
        # Mock initialization
        self.ad_networks["admob"]["initialized"] = True
        
        print("Ad networks initialized")
    
    def show_rewarded_ad(self, reward_callback: Callable):
        """Show rewarded ad"""
        if self.ads_watched_today >= self.max_ads_per_day:
            print("Daily ad limit reached")
            return False
        
        if self.rewarded_ad_cooldown > 0:
            print("Rewarded ad on cooldown")
            return False
        
        print("Showing rewarded ad...")
        
        # Mock ad display
        self.rewarded_ad_callback = reward_callback
        
        # Simulate ad completion after 5 seconds (in real implementation, this would be handled by ad callback)
        self._mock_ad_completion("rewarded")
        
        return True
    
    def show_interstitial_ad(self, completion_callback: Optional[Callable] = None):
        """Show interstitial ad"""
        if self.interstitial_ad_cooldown > 0:
            return False
        
        print("Showing interstitial ad...")
        
        self.interstitial_ad_callback = completion_callback
        
        # Mock ad display
        self._mock_ad_completion("interstitial")
        
        return True
    
    def _mock_ad_completion(self, ad_type: str):
        """Mock ad completion for testing"""
        if ad_type == "rewarded" and self.rewarded_ad_callback:
            # Grant reward
            self.ads_watched_today += 1
            self.rewarded_ad_cooldown = 30  # 30 second cooldown
            self.rewarded_ad_callback(True)  # Ad watched successfully
            
        elif ad_type == "interstitial" and self.interstitial_ad_callback:
            self.interstitial_ad_cooldown = 60  # 60 second cooldown
            self.interstitial_ad_callback()
    
    def update(self, dt: float):
        """Update ad manager cooldowns"""
        if self.rewarded_ad_cooldown > 0:
            self.rewarded_ad_cooldown = max(0, self.rewarded_ad_cooldown - dt)
        
        if self.interstitial_ad_cooldown > 0:
            self.interstitial_ad_cooldown = max(0, self.interstitial_ad_cooldown - dt)
    
    def reset_daily_ad_count(self):
        """Reset daily ad count (call once per day)"""
        self.ads_watched_today = 0
    
    def can_show_rewarded_ad(self) -> bool:
        """Check if rewarded ad can be shown"""
        return (self.ads_watched_today < self.max_ads_per_day and 
                self.rewarded_ad_cooldown <= 0 and
                self.ad_networks["admob"]["initialized"])
    
    def can_show_interstitial_ad(self) -> bool:
        """Check if interstitial ad can be shown"""
        return (self.interstitial_ad_cooldown <= 0 and
                self.ad_networks["admob"]["initialized"])

class NotificationManager:
    """Manages push notifications and local notifications"""
    
    def __init__(self):
        """Initialize notification manager"""
        self.notifications_enabled = True
        self.scheduled_notifications = []
    
    def schedule_stamina_notification(self, minutes_until_full: int):
        """Schedule notification for when stamina is full"""
        if not self.notifications_enabled:
            return
        
        print(f"Scheduling stamina notification in {minutes_until_full} minutes")
        
        # In real implementation, this would use platform-specific notification APIs
        notification = {
            "id": "stamina_full",
            "title": "Kingdom of Aldoria",
            "message": "Your stamina is full! Continue your adventure!",
            "delay": minutes_until_full * 60  # Convert to seconds
        }
        
        self.scheduled_notifications.append(notification)
    
    def schedule_daily_reward_notification(self):
        """Schedule daily reward notification"""
        if not self.notifications_enabled:
            return
        
        print("Scheduling daily reward notification")
        
        notification = {
            "id": "daily_reward",
            "title": "Kingdom of Aldoria",
            "message": "Don't forget to claim your daily reward!",
            "delay": 24 * 60 * 60  # 24 hours
        }
        
        self.scheduled_notifications.append(notification)
    
    def cancel_notification(self, notification_id: str):
        """Cancel a scheduled notification"""
        self.scheduled_notifications = [
            n for n in self.scheduled_notifications 
            if n.get("id") != notification_id
        ]
        
        print(f"Cancelled notification: {notification_id}")
    
    def set_notifications_enabled(self, enabled: bool):
        """Enable or disable notifications"""
        self.notifications_enabled = enabled
        
        if not enabled:
            # Cancel all scheduled notifications
            self.scheduled_notifications.clear()
            print("All notifications cancelled")

class InAppPurchase:
    """Handles in-app purchases"""
    
    def __init__(self):
        """Initialize IAP manager"""
        self.purchases = {}
        self.products = {
            "weekly_sub": {
                "price": "$4.99",
                "name": "Weekly Subscription",
                "description": "25 gems daily + max stamina 20"
            },
            "monthly_sub": {
                "price": "$15.99", 
                "name": "Monthly Subscription",
                "description": "40 gems daily + max stamina 25"
            },
            "starter_pack": {
                "price": "$0.99",
                "name": "Starter Pack",
                "description": "Special skin + weapon"
            },
            "legendary_pack": {
                "price": "$9.99",
                "name": "Legendary Pack",
                "description": "Legendary weapons and items"
            }
        }
    
    def purchase_product(self, product_id: str, success_callback: Callable):
        """Initiate purchase for a product"""
        if product_id not in self.products:
            print(f"Unknown product: {product_id}")
            return False
        
        print(f"Purchasing {product_id}...")
        
        # Mock purchase success
        self.purchases[product_id] = {
            "purchased": True,
            "timestamp": pygame.time.get_ticks()
        }
        
        success_callback(product_id)
        return True
    
    def restore_purchases(self):
        """Restore previous purchases"""
        print("Restoring purchases...")
        
        # Mock restore (in real implementation, query platform store)
        restored_count = len(self.purchases)
        print(f"Restored {restored_count} purchases")
        
        return restored_count
    
    def has_purchased(self, product_id: str) -> bool:
        """Check if product has been purchased"""
        return self.purchases.get(product_id, {}).get("purchased", False)