"""
Kingdom of Aldoria - Web Integration System
Handles communication between game and payment website
"""

import logging
import webbrowser
import json
import urllib.parse
from typing import Dict, Any, Optional
from ..core.config import Config

class WebIntegration:
    """Manages web integration for payments and external services"""

    def __init__(self, game):
        """Initialize web integration system"""
        self.game = game
        self.logger = logging.getLogger(__name__)
        
        # Website configuration
        self.website_url = "https://kingdomofaldoria.com"  # Replace with actual URL
        self.local_website_url = "file:///website/index.html"  # For local testing
        
        # Payment tracking
        self.pending_purchases = {}
        
        self.logger.info("WebIntegration system initialized")

    def open_store_website(self, package_type: str = None, auto_select: bool = False):
        """Open the payment website in browser
        
        Args:
            package_type: Specific package to preselect
            auto_select: Whether to auto-select the package
        """
        try:
            # Get player information
            save_manager = self.game.get_system('save_manager')
            player_data = save_manager.get_player_data() if save_manager else {}
            
            # Build URL parameters
            url_params = {
                'source': 'game',
                'player_id': self._get_player_id(player_data),
                'player_level': player_data.get('player', {}).get('level', 1),
                'current_gems': player_data.get('currency', {}).get('gems', 0),
                'current_gold': player_data.get('currency', {}).get('gold', 0)
            }
            
            # Add package preselection
            if package_type:
                url_params['package'] = package_type
                url_params['auto_select'] = 'true' if auto_select else 'false'
            
            # Build final URL
            base_url = self.website_url
            query_string = urllib.parse.urlencode(url_params)
            full_url = f"{base_url}#{query_string}"
            
            self.logger.info(f"Opening store website: {full_url}")
            
            # Open in browser
            webbrowser.open(full_url)
            
            # Track the purchase attempt
            if package_type:
                self._track_purchase_attempt(package_type, url_params)
                
        except Exception as e:
            self.logger.error(f"Failed to open store website: {e}")
            self._show_offline_store()

    def open_subscription_page(self, subscription_type: str):
        """Open subscription page with specific subscription preselected
        
        Args:
            subscription_type: 'weekly' or 'monthly'
        """
        package_map = {
            'weekly': 'weekly_premium',
            'monthly': 'monthly_premium'
        }
        
        package_type = package_map.get(subscription_type, 'weekly_premium')
        self.open_store_website(package_type, auto_select=True)

    def open_gem_store(self, suggested_amount: int = None):
        """Open gem purchase page
        
        Args:
            suggested_amount: Suggested gem amount to purchase
        """
        # Map suggested amounts to packages
        gem_packages = {
            100: 'gems_100',
            500: 'gems_500', 
            1200: 'gems_1200',
            3000: 'gems_3000'
        }
        
        # Find closest package
        package_type = 'gems_500'  # Default
        if suggested_amount:
            closest_amount = min(gem_packages.keys(), 
                                key=lambda x: abs(x - suggested_amount))
            package_type = gem_packages[closest_amount]
        
        self.open_store_website(package_type, auto_select=True)

    def open_starter_pack(self):
        """Open starter pack purchase page"""
        self.open_store_website('starter', auto_select=True)

    def open_premium_items(self, item_type: str = None):
        """Open premium items page
        
        Args:
            item_type: Specific item type to show
        """
        item_map = {
            'weapon': 'void_scythe',
            'skin': 'void_knight_skin',
            'sword': 'solar_sword'
        }
        
        package_type = item_map.get(item_type, 'void_scythe')
        self.open_store_website(package_type, auto_select=True)

    def _get_player_id(self, player_data: Dict[str, Any]) -> str:
        """Generate or retrieve player ID for web integration"""
        # Try to get existing ID from save data
        player_id = player_data.get('web_player_id')
        
        if not player_id:
            # Generate new player ID
            import time
            import hashlib
            
            # Create ID based on save creation time and some randomness
            created_time = player_data.get('created_time', time.time())
            random_component = str(time.time())
            
            id_string = f"KOA_{created_time}_{random_component}"
            player_id = hashlib.md5(id_string.encode()).hexdigest()[:12]
            
            # Save the ID for future use
            save_manager = self.game.get_system('save_manager')
            if save_manager:
                save_manager.set_player_data('web_player_id', player_id)
        
        return player_id

    def _track_purchase_attempt(self, package_type: str, params: Dict[str, Any]):
        """Track purchase attempt for analytics"""
        attempt_data = {
            'timestamp': time.time(),
            'package_type': package_type,
            'player_level': params.get('player_level', 1),
            'current_gems': params.get('current_gems', 0),
            'current_gold': params.get('current_gold', 0)
        }
        
        # Store in pending purchases
        player_id = params.get('player_id', 'unknown')
        self.pending_purchases[player_id] = attempt_data
        
        self.logger.info(f"Tracked purchase attempt: {package_type} for player {player_id}")

    def _show_offline_store(self):
        """Show offline store interface if web store is unavailable"""
        # This would show an in-game purchase interface
        # For now, just log the attempt
        self.logger.warning("Web store unavailable, showing offline store")
        
        # You could implement a basic in-game purchase flow here
        # or show a message to try again later

    def handle_purchase_result(self, result_data: Dict[str, Any]):
        """Handle purchase result from website
        
        Args:
            result_data: Purchase result data from website
        """
        try:
            transaction_id = result_data.get('transaction_id')
            package_type = result_data.get('package_type')
            success = result_data.get('success', False)
            
            if success:
                self._process_successful_purchase(package_type, transaction_id, result_data)
            else:
                self._process_failed_purchase(package_type, result_data)
                
        except Exception as e:
            self.logger.error(f"Error handling purchase result: {e}")

    def _process_successful_purchase(self, package_type: str, transaction_id: str, data: Dict[str, Any]):
        """Process successful purchase and grant rewards"""
        self.logger.info(f"Processing successful purchase: {package_type} - {transaction_id}")
        
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        # Grant rewards based on package type
        rewards = self._get_package_rewards(package_type)
        
        for reward_type, amount in rewards.items():
            if reward_type == 'gems':
                current_gems = save_manager.get_player_data('currency.gems') or 0
                save_manager.set_player_data('currency.gems', current_gems + amount)
                
            elif reward_type == 'gold':
                current_gold = save_manager.get_player_data('currency.gold') or 0
                save_manager.set_player_data('currency.gold', current_gold + amount)
                
            elif reward_type == 'subscription':
                self._grant_subscription(amount, save_manager)
                
            elif reward_type == 'item':
                self._grant_item(amount, save_manager)
        
        # Save transaction record
        self._save_transaction_record(transaction_id, package_type, data)
        
        # Show success message in game
        self._show_purchase_success(package_type, rewards)

    def _get_package_rewards(self, package_type: str) -> Dict[str, Any]:
        """Get rewards for a specific package type"""
        rewards = {
            # Gem packages
            'gems_100': {'gems': 100},
            'gems_500': {'gems': 550},  # 500 + 50 bonus
            'gems_1200': {'gems': 1400},  # 1200 + 200 bonus
            'gems_3000': {'gems': 3700},  # 3000 + 700 bonus
            
            # Subscriptions
            'weekly_premium': {'subscription': 'weekly'},
            'monthly_premium': {'subscription': 'monthly'},
            
            # Starter pack
            'starter': {
                'gems': 100,
                'gold': 1000,
                'item': 'forest_scout_skin'
            },
            
            # Premium items
            'void_scythe': {'item': 'void_scythe'},
            'solar_sword': {'item': 'solar_flare_sword'},
            'void_knight_skin': {'item': 'void_knight_skin'}
        }
        
        return rewards.get(package_type, {})

    def _grant_subscription(self, subscription_type: str, save_manager):
        """Grant subscription benefits"""
        import time
        
        current_time = time.time()
        
        if subscription_type == 'weekly':
            expires = current_time + (7 * 24 * 60 * 60)  # 7 days
            save_manager.set_player_data('subscriptions.weekly.active', True)
            save_manager.set_player_data('subscriptions.weekly.expires', expires)
            
            # Increase max stamina
            save_manager.set_player_data('stamina.max', Config.WEEKLY_SUB_MAX_STAMINA)
            
        elif subscription_type == 'monthly':
            expires = current_time + (30 * 24 * 60 * 60)  # 30 days
            save_manager.set_player_data('subscriptions.monthly.active', True)
            save_manager.set_player_data('subscriptions.monthly.expires', expires)
            
            # Increase max stamina
            save_manager.set_player_data('stamina.max', Config.MONTHLY_SUB_MAX_STAMINA)

    def _grant_item(self, item_id: str, save_manager):
        """Grant item to player inventory"""
        # Add to appropriate inventory category
        if 'skin' in item_id:
            skins = save_manager.get_player_data('inventory.skins') or []
            if item_id not in skins:
                skins.append(item_id)
                save_manager.set_player_data('inventory.skins', skins)
                
        elif 'sword' in item_id or 'scythe' in item_id:
            weapons = save_manager.get_player_data('inventory.weapons') or []
            if item_id not in weapons:
                weapons.append(item_id)
                save_manager.set_player_data('inventory.weapons', weapons)

    def _save_transaction_record(self, transaction_id: str, package_type: str, data: Dict[str, Any]):
        """Save transaction record for future reference"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        transactions = save_manager.get_player_data('transactions') or []
        
        transaction_record = {
            'id': transaction_id,
            'package': package_type,
            'timestamp': time.time(),
            'amount': data.get('amount', 0),
            'method': data.get('payment_method', 'unknown')
        }
        
        transactions.append(transaction_record)
        
        # Keep only last 50 transactions
        if len(transactions) > 50:
            transactions = transactions[-50:]
        
        save_manager.set_player_data('transactions', transactions)

    def _show_purchase_success(self, package_type: str, rewards: Dict[str, Any]):
        """Show purchase success message in game"""
        # This would trigger an in-game UI showing the purchase success
        self.logger.info(f"Purchase successful: {package_type} - Rewards: {rewards}")
        
        # You could implement a popup or notification system here
        # For now, just log the success

    def _process_failed_purchase(self, package_type: str, data: Dict[str, Any]):
        """Process failed purchase"""
        error_reason = data.get('error_reason', 'Unknown error')
        self.logger.warning(f"Purchase failed: {package_type} - Reason: {error_reason}")
        
        # Show error message to player
        # You could implement error handling UI here

    def check_subscription_status(self):
        """Check and update subscription status"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        import time
        current_time = time.time()
        
        # Check weekly subscription
        weekly_expires = save_manager.get_player_data('subscriptions.weekly.expires') or 0
        if weekly_expires < current_time:
            save_manager.set_player_data('subscriptions.weekly.active', False)
            # Reset stamina to default
            save_manager.set_player_data('stamina.max', Config.MAX_STAMINA_DEFAULT)
        
        # Check monthly subscription  
        monthly_expires = save_manager.get_player_data('subscriptions.monthly.expires') or 0
        if monthly_expires < current_time:
            save_manager.set_player_data('subscriptions.monthly.active', False)
            # Reset stamina if no other active subscription
            if not save_manager.get_player_data('subscriptions.weekly.active'):
                save_manager.set_player_data('stamina.max', Config.MAX_STAMINA_DEFAULT)

    def grant_daily_subscription_rewards(self):
        """Grant daily rewards for active subscriptions"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        import time
        current_time = time.time()
        last_daily_reward = save_manager.get_player_data('last_daily_reward') or 0
        
        # Check if 24 hours have passed
        if current_time - last_daily_reward < (24 * 60 * 60):
            return
        
        # Grant rewards for active subscriptions
        current_gems = save_manager.get_player_data('currency.gems') or 0
        gems_granted = 0
        
        if save_manager.get_player_data('subscriptions.weekly.active'):
            gems_granted += Config.WEEKLY_SUB_GEMS_PER_DAY
            
        if save_manager.get_player_data('subscriptions.monthly.active'):
            gems_granted += Config.MONTHLY_SUB_GEMS_PER_DAY
        
        if gems_granted > 0:
            save_manager.set_player_data('currency.gems', current_gems + gems_granted)
            save_manager.set_player_data('last_daily_reward', current_time)
            
            self.logger.info(f"Granted daily subscription rewards: {gems_granted} gems")

    def get_purchase_url_for_insufficient_gems(self, required_gems: int) -> str:
        """Get purchase URL when player doesn't have enough gems
        
        Args:
            required_gems: Number of gems needed
            
        Returns:
            URL to gem purchase page
        """
        # Suggest appropriate gem package
        if required_gems <= 100:
            package = 'gems_100'
        elif required_gems <= 550:
            package = 'gems_500'
        elif required_gems <= 1400:
            package = 'gems_1200'
        else:
            package = 'gems_3000'
        
        # Build URL
        params = urllib.parse.urlencode({
            'package': package,
            'auto_select': 'true',
            'required_gems': required_gems,
            'source': 'insufficient_gems'
        })
        
        return f"{self.website_url}#{params}"

    def cleanup(self):
        """Cleanup web integration system"""
        self.logger.info("Cleaning up WebIntegration")
        self.pending_purchases.clear()

# Integration with main game systems
def integrate_web_payments(game):
    """Integrate web payment system with game"""
    web_integration = WebIntegration(game)
    
    # Add to game systems
    game.web_integration = web_integration
    
    # Check subscription status on startup
    web_integration.check_subscription_status()
    
    return web_integration