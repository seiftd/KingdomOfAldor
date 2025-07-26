"""
Kingdom of Aldoria - Enhanced Ad Manager
Handles ad display, rewards, and source management with analytics
"""

import logging
import time
import random
import json
from typing import Dict, List, Optional, Any
from ..core.config import Config

class AdManager:
    """Enhanced ad management system with multiple sources and analytics"""

    def __init__(self, game):
        """Initialize ad manager"""
        self.game = game
        self.logger = logging.getLogger(__name__)
        
        # Ad configuration
        self.ad_sources = Config.AD_SOURCES.copy()
        self.current_source = "AdMob"  # Default
        self.daily_limit = Config.AD_DAILY_LIMIT_DEFAULT
        
        # Ad tracking
        self.ads_watched_today = 0
        self.last_ad_time = 0
        self.total_ads_watched = 0
        self.last_reset_date = time.strftime("%Y-%m-%d")
        
        # Rewards tracking
        self.total_gems_earned = 0
        self.total_gold_earned = 0
        
        # Analytics data
        self.ad_analytics = {
            'daily_views': {},
            'source_performance': {},
            'reward_distribution': {},
            'conversion_rates': {}
        }
        
        # Load saved data
        self._load_ad_data()
        
        self.logger.info("Enhanced AdManager initialized")

    def _load_ad_data(self):
        """Load ad data from save manager"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        # Load ad statistics
        self.ads_watched_today = save_manager.get_player_data('ads.watched_today') or 0
        self.total_ads_watched = save_manager.get_player_data('ads.total_watched') or 0
        self.last_ad_time = save_manager.get_player_data('ads.last_ad_time') or 0
        self.last_reset_date = save_manager.get_player_data('ads.last_reset_date') or time.strftime("%Y-%m-%d")
        
        # Load rewards earned
        self.total_gems_earned = save_manager.get_player_data('ads.total_gems_earned') or 0
        self.total_gold_earned = save_manager.get_player_data('ads.total_gold_earned') or 0
        
        # Load analytics
        self.ad_analytics = save_manager.get_player_data('ads.analytics') or {
            'daily_views': {},
            'source_performance': {},
            'reward_distribution': {},
            'conversion_rates': {}
        }
        
        # Check if we need to reset daily counters
        current_date = time.strftime("%Y-%m-%d")
        if current_date != self.last_reset_date:
            self._reset_daily_counters()

    def _save_ad_data(self):
        """Save ad data to save manager"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        save_manager.set_player_data('ads.watched_today', self.ads_watched_today)
        save_manager.set_player_data('ads.total_watched', self.total_ads_watched)
        save_manager.set_player_data('ads.last_ad_time', self.last_ad_time)
        save_manager.set_player_data('ads.last_reset_date', self.last_reset_date)
        save_manager.set_player_data('ads.total_gems_earned', self.total_gems_earned)
        save_manager.set_player_data('ads.total_gold_earned', self.total_gold_earned)
        save_manager.set_player_data('ads.analytics', self.ad_analytics)

    def _reset_daily_counters(self):
        """Reset daily counters for new day"""
        # Save yesterday's data to analytics
        yesterday = self.last_reset_date
        self.ad_analytics['daily_views'][yesterday] = self.ads_watched_today
        
        # Reset counters
        self.ads_watched_today = 0
        self.last_reset_date = time.strftime("%Y-%m-%d")
        
        # Update daily limit based on VIP status
        save_manager = self.game.get_system('save_manager')
        if save_manager:
            is_vip = (save_manager.get_player_data('subscriptions.weekly.active') or 
                     save_manager.get_player_data('subscriptions.monthly.active'))
            self.daily_limit = Config.AD_DAILY_LIMIT_VIP if is_vip else Config.AD_DAILY_LIMIT_DEFAULT
        
        self.logger.info(f"Daily ad counters reset. New limit: {self.daily_limit}")

    def can_show_ad(self) -> Dict[str, Any]:
        """Check if an ad can be shown"""
        current_time = time.time()
        
        # Check daily limit
        if self.ads_watched_today >= self.daily_limit:
            return {
                'can_show': False,
                'reason': 'daily_limit_reached',
                'message': f'Daily ad limit reached ({self.daily_limit}). Try again tomorrow!'
            }
        
        # Check cooldown
        time_since_last = current_time - self.last_ad_time
        if time_since_last < Config.AD_COOLDOWN_SECONDS:
            remaining = int(Config.AD_COOLDOWN_SECONDS - time_since_last)
            return {
                'can_show': False,
                'reason': 'cooldown',
                'message': f'Please wait {remaining} seconds before watching another ad.'
            }
        
        return {
            'can_show': True,
            'reason': 'available',
            'message': 'Ad ready to watch!'
        }

    def show_rewarded_ad(self) -> Dict[str, Any]:
        """Show a rewarded ad and return reward info"""
        # Check if ad can be shown
        can_show = self.can_show_ad()
        if not can_show['can_show']:
            return can_show
        
        # Simulate ad display (in real implementation, this would call actual ad SDK)
        success = self._simulate_ad_display()
        
        if success:
            return self._process_ad_reward()
        else:
            return {
                'success': False,
                'reason': 'ad_failed',
                'message': 'Ad failed to load. Please try again.'
            }

    def _simulate_ad_display(self) -> bool:
        """Simulate ad display with realistic success rates"""
        # Different ad sources have different success rates
        source_success_rates = {
            'AdMob': 0.95,
            'Unity Ads': 0.90,
            'AppLovin': 0.88,
            'IronSource': 0.92,
            'Vungle': 0.85,
            'Facebook Audience Network': 0.87,
            'TikTok Ads': 0.83,
            'Chartboost': 0.86
        }
        
        success_rate = source_success_rates.get(self.current_source, 0.90)
        success = random.random() < success_rate
        
        # Update analytics
        source_data = self.ad_analytics['source_performance'].get(self.current_source, {
            'attempts': 0,
            'successes': 0,
            'failures': 0
        })
        
        source_data['attempts'] += 1
        if success:
            source_data['successes'] += 1
        else:
            source_data['failures'] += 1
        
        self.ad_analytics['source_performance'][self.current_source] = source_data
        
        return success

    def _process_ad_reward(self) -> Dict[str, Any]:
        """Process ad reward and update player currency"""
        current_time = time.time()
        
        # Calculate rewards
        gem_reward = random.randint(Config.AD_REWARD_GEMS_MIN, Config.AD_REWARD_GEMS_MAX)
        gold_reward = random.randint(Config.AD_REWARD_GOLD_MIN, Config.AD_REWARD_GOLD_MAX)
        
        # VIP bonus
        save_manager = self.game.get_system('save_manager')
        if save_manager:
            is_vip = (save_manager.get_player_data('subscriptions.weekly.active') or 
                     save_manager.get_player_data('subscriptions.monthly.active'))
            
            if is_vip:
                gem_reward = int(gem_reward * 1.5)  # 50% bonus for VIP
                gold_reward = int(gold_reward * 1.5)
        
        # Update player currency
        if save_manager:
            current_gems = save_manager.get_player_data('currency.gems') or 0
            current_gold = save_manager.get_player_data('currency.gold') or 0
            
            save_manager.set_player_data('currency.gems', current_gems + gem_reward)
            save_manager.set_player_data('currency.gold', current_gold + gold_reward)
        
        # Update counters
        self.ads_watched_today += 1
        self.total_ads_watched += 1
        self.last_ad_time = current_time
        self.total_gems_earned += gem_reward
        self.total_gold_earned += gold_reward
        
        # Update analytics
        today = time.strftime("%Y-%m-%d")
        if today not in self.ad_analytics['reward_distribution']:
            self.ad_analytics['reward_distribution'][today] = {
                'gems': 0,
                'gold': 0,
                'count': 0
            }
        
        self.ad_analytics['reward_distribution'][today]['gems'] += gem_reward
        self.ad_analytics['reward_distribution'][today]['gold'] += gold_reward
        self.ad_analytics['reward_distribution'][today]['count'] += 1
        
        # Save data
        self._save_ad_data()
        
        self.logger.info(f"Ad reward processed: {gem_reward} gems, {gold_reward} gold")
        
        return {
            'success': True,
            'rewards': {
                'gems': gem_reward,
                'gold': gold_reward
            },
            'remaining_ads': self.daily_limit - self.ads_watched_today,
            'source': self.current_source,
            'message': f'Congratulations! You earned {gem_reward} gems and {gold_reward} gold!'
        }

    def get_ad_status(self) -> Dict[str, Any]:
        """Get current ad status and statistics"""
        return {
            'ads_watched_today': self.ads_watched_today,
            'daily_limit': self.daily_limit,
            'remaining_ads': self.daily_limit - self.ads_watched_today,
            'total_ads_watched': self.total_ads_watched,
            'total_gems_earned': self.total_gems_earned,
            'total_gold_earned': self.total_gold_earned,
            'current_source': self.current_source,
            'available_sources': self.ad_sources,
            'can_show_ad': self.can_show_ad()
        }

    def set_ad_source(self, source: str) -> bool:
        """Set the current ad source"""
        if source in self.ad_sources:
            self.current_source = source
            self.logger.info(f"Ad source changed to: {source}")
            return True
        else:
            self.logger.warning(f"Invalid ad source: {source}")
            return False

    def get_analytics_data(self) -> Dict[str, Any]:
        """Get detailed analytics data for dashboard"""
        # Calculate conversion rates
        total_attempts = sum(
            data.get('attempts', 0) 
            for data in self.ad_analytics['source_performance'].values()
        )
        total_successes = sum(
            data.get('successes', 0) 
            for data in self.ad_analytics['source_performance'].values()
        )
        
        overall_conversion = (total_successes / total_attempts * 100) if total_attempts > 0 else 0
        
        # Source-specific conversion rates
        source_conversions = {}
        for source, data in self.ad_analytics['source_performance'].items():
            attempts = data.get('attempts', 0)
            successes = data.get('successes', 0)
            conversion = (successes / attempts * 100) if attempts > 0 else 0
            source_conversions[source] = {
                'attempts': attempts,
                'successes': successes,
                'conversion_rate': round(conversion, 2)
            }
        
        # Recent performance (last 7 days)
        recent_days = []
        for i in range(7):
            date = time.strftime("%Y-%m-%d", time.localtime(time.time() - i * 86400))
            views = self.ad_analytics['daily_views'].get(date, 0)
            rewards = self.ad_analytics['reward_distribution'].get(date, {})
            recent_days.append({
                'date': date,
                'views': views,
                'gems_earned': rewards.get('gems', 0),
                'gold_earned': rewards.get('gold', 0)
            })
        
        return {
            'overall_stats': {
                'total_ads_watched': self.total_ads_watched,
                'total_gems_earned': self.total_gems_earned,
                'total_gold_earned': self.total_gold_earned,
                'overall_conversion_rate': round(overall_conversion, 2)
            },
            'source_performance': source_conversions,
            'recent_performance': recent_days,
            'current_config': {
                'current_source': self.current_source,
                'daily_limit': self.daily_limit,
                'gem_reward_range': f"{Config.AD_REWARD_GEMS_MIN}-{Config.AD_REWARD_GEMS_MAX}",
                'gold_reward_range': f"{Config.AD_REWARD_GOLD_MIN}-{Config.AD_REWARD_GOLD_MAX}"
            }
        }

    def update_ad_limits(self, new_limit: int) -> bool:
        """Update daily ad limit (for admin use)"""
        if 1 <= new_limit <= 100:  # Reasonable limits
            self.daily_limit = new_limit
            self.logger.info(f"Daily ad limit updated to: {new_limit}")
            return True
        return False

    def add_ad_source(self, source: str) -> bool:
        """Add a new ad source"""
        if source not in self.ad_sources:
            self.ad_sources.append(source)
            self.logger.info(f"Added new ad source: {source}")
            return True
        return False

    def remove_ad_source(self, source: str) -> bool:
        """Remove an ad source"""
        if source in self.ad_sources and len(self.ad_sources) > 1:
            self.ad_sources.remove(source)
            if self.current_source == source:
                self.current_source = self.ad_sources[0]
            self.logger.info(f"Removed ad source: {source}")
            return True
        return False

    def force_ad_refresh(self):
        """Force refresh ad availability (admin function)"""
        self.last_ad_time = 0
        self.logger.info("Ad cooldown reset by admin")

    def grant_bonus_ad_views(self, count: int):
        """Grant bonus ad views (admin function)"""
        if count > 0:
            self.daily_limit += count
            self.logger.info(f"Granted {count} bonus ad views")

    def cleanup(self):
        """Cleanup ad manager"""
        self.logger.info("Cleaning up AdManager")
        self._save_ad_data()
        self.logger.info("AdManager cleanup complete")