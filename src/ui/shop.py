"""
Kingdom of Aldoria - Shop State
Monetization features: subscriptions, items, ads, currency management
"""

import pygame
import logging
from typing import Dict, List, Any, Optional

from ..core.state_manager import GameState
from ..core.config import Config, GameStates, CurrencyTypes

class ShopState(GameState):
    """Shop state for in-app purchases and monetization"""
    
    def __init__(self, game):
        """Initialize shop state"""
        super().__init__(game)
        
        # Shop categories
        self.categories = ["Subscriptions", "Items", "Skins", "Weapons", "Ads"]
        self.current_category = 0
        
        # UI elements
        self.category_buttons = []
        self.item_buttons = []
        self.currency_display_rect = None
        
        # Shop items data
        self.shop_items = {}
        
        self.logger.info("ShopState initialized")
    
    def enter(self, **kwargs):
        """Enter the shop state"""
        self.logger.info("Entering shop")
        
        # Load shop data
        self._load_shop_items()
        
        # Setup UI
        self._setup_ui()
        
        # Play shop music
        asset_manager = self.game.get_system('asset_manager')
        if asset_manager:
            asset_manager.play_music("shop_music", volume=0.4)
    
    def exit(self):
        """Exit the shop state"""
        self.logger.info("Exiting shop")
    
    def update(self, dt: float):
        """Update shop logic"""
        pass
    
    def render(self, screen: pygame.Surface):
        """Render the shop interface"""
        # Background
        self._render_background(screen)
        
        # Header
        self._render_header(screen)
        
        # Currency display
        self._render_currency_display(screen)
        
        # Category tabs
        self._render_category_tabs(screen)
        
        # Shop items
        self._render_shop_items(screen)
        
        # Back button
        self._render_back_button(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle shop events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state(GameStates.MAIN_MENU)
            elif event.key == pygame.K_LEFT:
                self._change_category(-1)
            elif event.key == pygame.K_RIGHT:
                self._change_category(1)
    
    def _load_shop_items(self):
        """Load shop items configuration"""
        self.shop_items = {
            "Subscriptions": [
                {
                    "id": "weekly_sub",
                    "name": "Weekly Pass",
                    "description": "25 gems daily + 20 max stamina",
                    "price": Config.WEEKLY_SUB_PRICE,
                    "currency": "USD",
                    "benefits": ["25 gems/day", "Max stamina 20", "No ads"],
                    "duration": "7 days"
                },
                {
                    "id": "monthly_sub", 
                    "name": "Monthly Pass",
                    "description": "40 gems daily + 25 max stamina",
                    "price": Config.MONTHLY_SUB_PRICE,
                    "currency": "USD",
                    "benefits": ["40 gems/day", "Max stamina 25", "No ads", "VIP badge"],
                    "duration": "30 days"
                }
            ],
            "Items": [
                {
                    "id": "stamina_refill",
                    "name": "Stamina Refill",
                    "description": "Instantly restore full stamina",
                    "price": 50,
                    "currency": "gems",
                    "icon": "stamina_potion"
                },
                {
                    "id": "gold_pack_small",
                    "name": "Gold Pack (S)",
                    "description": "1,000 gold coins",
                    "price": 25,
                    "currency": "gems",
                    "icon": "gold_bag"
                },
                {
                    "id": "gold_pack_large",
                    "name": "Gold Pack (L)", 
                    "description": "10,000 gold coins",
                    "price": 200,
                    "currency": "gems",
                    "icon": "gold_chest"
                }
            ],
            "Skins": [
                {
                    "id": "forest_scout",
                    "name": "Forest Scout",
                    "description": "Ranger skin with speed boost skill",
                    "price": 100,
                    "currency": "gems",
                    "skill": "speed_boost",
                    "rarity": "rare"
                },
                {
                    "id": "desert_nomad",
                    "name": "Desert Nomad",
                    "description": "Warrior skin with instant heal skill",
                    "price": 150,
                    "currency": "gems", 
                    "skill": "instant_heal",
                    "rarity": "epic"
                },
                {
                    "id": "void_knight",
                    "name": "Void Knight",
                    "description": "Dark armor with time rewind skill",
                    "price": 300,
                    "currency": "gems",
                    "skill": "time_rewind",
                    "rarity": "legendary"
                }
            ],
            "Weapons": [
                {
                    "id": "bronze_sword",
                    "name": "Bronze Sword",
                    "description": "Basic weapon (+10 attack)",
                    "price": 0,
                    "currency": "gold",
                    "attack_bonus": 10,
                    "rarity": "common"
                },
                {
                    "id": "void_scythe",
                    "name": "Void Scythe",
                    "description": "Cosmic weapon (+25 attack)",
                    "price": 500,
                    "currency": "gems",
                    "attack_bonus": 25,
                    "rarity": "epic"
                },
                {
                    "id": "solar_flare_sword",
                    "name": "Solar Flare Sword",
                    "description": "Fire weapon (+40 attack)",
                    "price": 1000,
                    "currency": "gems",
                    "attack_bonus": 40,
                    "rarity": "legendary"
                }
            ],
            "Ads": [
                {
                    "id": "watch_ad",
                    "name": "Watch Ad",
                    "description": "Get 3 gems for watching ad",
                    "price": 0,
                    "currency": "time",
                    "reward": "3 gems",
                    "cooldown": 300  # 5 minutes
                },
                {
                    "id": "ad_boost",
                    "name": "Ad Boost Package",
                    "description": "Watch 10 ads for bonus gems",
                    "price": 0,
                    "currency": "time",
                    "reward": "30 gems + bonus",
                    "limit": "daily"
                }
            ]
        }
    
    def _setup_ui(self):
        """Setup shop UI elements"""
        # Category tabs
        self.category_buttons = []
        tab_width = 150
        tab_height = 40
        tab_spacing = 10
        total_width = len(self.categories) * (tab_width + tab_spacing) - tab_spacing
        start_x = (Config.SCREEN_WIDTH - total_width) // 2
        
        for i, category in enumerate(self.categories):
            x = start_x + i * (tab_width + tab_spacing)
            y = 100
            
            self.category_buttons.append({
                'rect': pygame.Rect(x, y, tab_width, tab_height),
                'category': category,
                'index': i
            })
        
        # Currency display
        self.currency_display_rect = pygame.Rect(20, 20, 300, 60)
    
    def _render_background(self, screen: pygame.Surface):
        """Render shop background"""
        # Gradient background (purple to blue)
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            r = int(100 + ratio * 50)  # 100 to 150
            g = int(50 + ratio * 100)  # 50 to 150  
            b = int(150 + ratio * 50)  # 150 to 200
            
            color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(screen, color, (0, y), (Config.SCREEN_WIDTH, y))
    
    def _render_header(self, screen: pygame.Surface):
        """Render shop header"""
        # Shop title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("ROYAL SHOP", True, Config.GOLD)
        title_rect = title_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=20)
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 24)
        subtitle_text = subtitle_font.render("Enhance your adventure", True, Config.SILVER)
        subtitle_rect = subtitle_text.get_rect(centerx=Config.SCREEN_WIDTH // 2, y=65)
        screen.blit(subtitle_text, subtitle_rect)
    
    def _render_currency_display(self, screen: pygame.Surface):
        """Render player currency display"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        # Panel background
        pygame.draw.rect(screen, Config.UI_PANEL, self.currency_display_rect)
        pygame.draw.rect(screen, Config.GOLD, self.currency_display_rect, 3)
        
        # Get currency values
        gold = save_manager.get_player_data("currency.gold") or 0
        gems = save_manager.get_player_data("currency.gems") or 0
        
        # Display currencies
        font = pygame.font.Font(None, 28)
        
        # Gold
        gold_text = f"Gold: {gold:,}"
        gold_surface = font.render(gold_text, True, Config.GOLD)
        screen.blit(gold_surface, (self.currency_display_rect.x + 10, self.currency_display_rect.y + 5))
        
        # Gems  
        gems_text = f"Gems: {gems}"
        gems_surface = font.render(gems_text, True, Config.BLUE)
        screen.blit(gems_surface, (self.currency_display_rect.x + 10, self.currency_display_rect.y + 30))
    
    def _render_category_tabs(self, screen: pygame.Surface):
        """Render category selection tabs"""
        font = pygame.font.Font(None, 24)
        mouse_pos = pygame.mouse.get_pos()
        
        for button_data in self.category_buttons:
            rect = button_data['rect']
            category = button_data['category']
            index = button_data['index']
            
            # Tab appearance
            if index == self.current_category:
                bg_color = Config.UI_ACCENT
                text_color = Config.WHITE
                border_color = Config.GOLD
                border_width = 3
            elif rect.collidepoint(mouse_pos):
                bg_color = Config.UI_BUTTON_HOVER
                text_color = Config.GOLD
                border_color = Config.UI_ACCENT
                border_width = 2
            else:
                bg_color = Config.UI_BUTTON
                text_color = Config.UI_TEXT
                border_color = Config.UI_ACCENT
                border_width = 1
            
            # Draw tab
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, border_color, rect, border_width)
            
            # Tab text
            text_surface = font.render(category, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
    
    def _render_shop_items(self, screen: pygame.Surface):
        """Render items for current category"""
        current_category = self.categories[self.current_category]
        items = self.shop_items.get(current_category, [])
        
        if not items:
            # No items message
            font = pygame.font.Font(None, 36)
            no_items_text = font.render("Coming Soon!", True, Config.UI_TEXT_SECONDARY)
            text_rect = no_items_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
            screen.blit(no_items_text, text_rect)
            return
        
        # Item grid
        items_per_row = 3
        item_width = 250
        item_height = 200
        item_spacing = 20
        
        grid_width = items_per_row * (item_width + item_spacing) - item_spacing
        start_x = (Config.SCREEN_WIDTH - grid_width) // 2
        start_y = 170
        
        self.item_buttons = []
        
        for i, item in enumerate(items):
            row = i // items_per_row
            col = i % items_per_row
            
            x = start_x + col * (item_width + item_spacing)
            y = start_y + row * (item_height + item_spacing)
            
            item_rect = pygame.Rect(x, y, item_width, item_height)
            self.item_buttons.append({
                'rect': item_rect,
                'item': item
            })
            
            self._render_shop_item(screen, item, item_rect)
    
    def _render_shop_item(self, screen: pygame.Surface, item: Dict[str, Any], rect: pygame.Rect):
        """Render individual shop item"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Item card background
        if rect.collidepoint(mouse_pos):
            bg_color = Config.UI_BUTTON_HOVER
            border_color = Config.GOLD
            border_width = 3
        else:
            bg_color = Config.UI_PANEL
            border_color = Config.UI_ACCENT
            border_width = 2
        
        pygame.draw.rect(screen, bg_color, rect)
        pygame.draw.rect(screen, border_color, rect, border_width)
        
        # Rarity border for special items
        if item.get('rarity') == 'legendary':
            pygame.draw.rect(screen, Config.GOLD, rect, 5)
        elif item.get('rarity') == 'epic':
            pygame.draw.rect(screen, Config.PURPLE, rect, 4)
        elif item.get('rarity') == 'rare':
            pygame.draw.rect(screen, Config.BLUE, rect, 3)
        
        # Item content
        content_rect = rect.inflate(-20, -20)
        y_offset = content_rect.y + 10
        
        # Item name
        name_font = pygame.font.Font(None, 28)
        name_surface = name_font.render(item['name'], True, Config.WHITE)
        name_rect = name_surface.get_rect(centerx=content_rect.centerx, y=y_offset)
        screen.blit(name_surface, name_rect)
        y_offset += 35
        
        # Item description
        desc_font = pygame.font.Font(None, 18)
        desc_lines = self._wrap_text(item['description'], desc_font, content_rect.width - 10)
        for line in desc_lines:
            line_surface = desc_font.render(line, True, Config.UI_TEXT_SECONDARY)
            line_rect = line_surface.get_rect(centerx=content_rect.centerx, y=y_offset)
            screen.blit(line_surface, line_rect)
            y_offset += 20
        
        # Benefits (for subscriptions)
        if 'benefits' in item:
            y_offset += 10
            benefit_font = pygame.font.Font(None, 16)
            for benefit in item['benefits']:
                benefit_surface = benefit_font.render(f"• {benefit}", True, Config.GREEN)
                benefit_rect = benefit_surface.get_rect(centerx=content_rect.centerx, y=y_offset)
                screen.blit(benefit_surface, benefit_rect)
                y_offset += 18
        
        # Price button
        button_height = 35
        button_rect = pygame.Rect(
            content_rect.x + 10,
            content_rect.bottom - button_height - 10,
            content_rect.width - 20,
            button_height
        )
        
        # Check if item is owned or available
        can_purchase = self._can_purchase_item(item)
        is_owned = self._is_item_owned(item)
        
        if is_owned:
            button_color = Config.GREEN
            button_text = "OWNED"
            text_color = Config.WHITE
        elif can_purchase:
            button_color = Config.UI_ACCENT
            button_text = self._get_price_text(item)
            text_color = Config.WHITE
        else:
            button_color = Config.DARK_GRAY
            button_text = "INSUFFICIENT FUNDS"
            text_color = Config.UI_TEXT_SECONDARY
        
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, Config.WHITE, button_rect, 2)
        
        # Button text
        button_font = pygame.font.Font(None, 20)
        text_surface = button_font.render(button_text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _render_back_button(self, screen: pygame.Surface):
        """Render back button"""
        back_rect = pygame.Rect(20, Config.SCREEN_HEIGHT - 60, 100, 40)
        
        mouse_pos = pygame.mouse.get_pos()
        if back_rect.collidepoint(mouse_pos):
            bg_color = Config.UI_BUTTON_HOVER
            text_color = Config.GOLD
        else:
            bg_color = Config.UI_BUTTON
            text_color = Config.UI_TEXT
        
        pygame.draw.rect(screen, bg_color, back_rect)
        pygame.draw.rect(screen, Config.UI_ACCENT, back_rect, 2)
        
        font = pygame.font.Font(None, 24)
        text_surface = font.render("BACK", True, text_color)
        text_rect = text_surface.get_rect(center=back_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        # Category tabs
        for button_data in self.category_buttons:
            if button_data['rect'].collidepoint(pos):
                self.current_category = button_data['index']
                return
        
        # Shop items
        for button_data in self.item_buttons:
            if button_data['rect'].collidepoint(pos):
                item = button_data['item']
                if self._can_purchase_item(item) and not self._is_item_owned(item):
                    self._purchase_item(item)
                return
        
        # Back button
        back_rect = pygame.Rect(20, Config.SCREEN_HEIGHT - 60, 100, 40)
        if back_rect.collidepoint(pos):
            self.game.change_state(GameStates.MAIN_MENU)
            return
    
    def _change_category(self, direction: int):
        """Change category with keyboard"""
        self.current_category = (self.current_category + direction) % len(self.categories)
    
    def _can_purchase_item(self, item: Dict[str, Any]) -> bool:
        """Check if item can be purchased"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return False
        
        # Special handling for ads
        if item.get('currency') == 'time':
            return self._can_watch_ad(item)
        
        # Check currency
        if item['currency'] == 'gems':
            current_gems = save_manager.get_player_data("currency.gems") or 0
            return current_gems >= item['price']
        elif item['currency'] == 'gold':
            current_gold = save_manager.get_player_data("currency.gold") or 0
            return current_gold >= item['price']
        elif item['currency'] == 'USD':
            return True  # Assume real money purchases are always available
        
        return False
    
    def _is_item_owned(self, item: Dict[str, Any]) -> bool:
        """Check if item is already owned"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return False
        
        item_id = item['id']
        
        # Check subscriptions
        if item_id in ['weekly_sub', 'monthly_sub']:
            subscription_data = save_manager.get_player_data(f"subscriptions.{item_id.replace('_sub', '')}")
            return subscription_data and subscription_data.get('active', False)
        
        # Check inventory items
        if item_id in ['forest_scout', 'desert_nomad', 'void_knight']:
            skins = save_manager.get_player_data("inventory.skins") or []
            return item_id in skins
        
        if item_id in ['bronze_sword', 'void_scythe', 'solar_flare_sword']:
            weapons = save_manager.get_player_data("inventory.weapons") or []
            return item_id in weapons
        
        # Consumables are never "owned"
        return False
    
    def _can_watch_ad(self, item: Dict[str, Any]) -> bool:
        """Check if ad can be watched"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return False
        
        # Check daily ad limit
        ads_watched = save_manager.get_player_data("stats.ads_watched") or 0
        return ads_watched < Config.MAX_ADS_PER_DAY
    
    def _get_price_text(self, item: Dict[str, Any]) -> str:
        """Get formatted price text"""
        if item.get('currency') == 'time':
            return "WATCH AD"
        elif item['currency'] == 'USD':
            return f"${item['price']:.2f}"
        elif item['currency'] == 'gems':
            return f"{item['price']} 💎"
        elif item['currency'] == 'gold':
            return f"{item['price']:,} 🪙"
        else:
            return f"{item['price']}"
    
    def _purchase_item(self, item: Dict[str, Any]):
        """Purchase an item"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        item_id = item['id']
        self.logger.info(f"Purchasing item: {item_id}")
        
        # Handle different purchase types
        if item['currency'] == 'time':
            self._watch_ad(item)
        elif item['currency'] == 'USD':
            self._handle_real_money_purchase(item)
        else:
            self._handle_virtual_currency_purchase(item)
    
    def _handle_virtual_currency_purchase(self, item: Dict[str, Any]):
        """Handle purchases with virtual currency"""
        save_manager = self.game.get_system('save_manager')
        item_id = item['id']
        
        # Deduct currency
        if item['currency'] == 'gems':
            current_gems = save_manager.get_player_data("currency.gems") or 0
            save_manager.set_player_data("currency.gems", current_gems - item['price'])
        elif item['currency'] == 'gold':
            current_gold = save_manager.get_player_data("currency.gold") or 0
            save_manager.set_player_data("currency.gold", current_gold - item['price'])
        
        # Apply item effects
        if item_id == 'stamina_refill':
            max_stamina = save_manager.get_player_data("stamina.max") or Config.MAX_STAMINA_DEFAULT
            save_manager.set_player_data("stamina.current", max_stamina)
        
        elif item_id == 'gold_pack_small':
            current_gold = save_manager.get_player_data("currency.gold") or 0
            save_manager.set_player_data("currency.gold", current_gold + 1000)
        
        elif item_id == 'gold_pack_large':
            current_gold = save_manager.get_player_data("currency.gold") or 0
            save_manager.set_player_data("currency.gold", current_gold + 10000)
        
        elif item_id in ['forest_scout', 'desert_nomad', 'void_knight']:
            # Add skin to inventory
            skins = save_manager.get_player_data("inventory.skins") or []
            if item_id not in skins:
                skins.append(item_id)
                save_manager.set_player_data("inventory.skins", skins)
            
            # Unlock associated skill
            if 'skill' in item:
                skill_key = f"skills.{item['skill']}"
                save_manager.set_player_data(f"{skill_key}.unlocked", True)
                save_manager.set_player_data(f"{skill_key}.level", 1)
        
        elif item_id in ['bronze_sword', 'void_scythe', 'solar_flare_sword']:
            # Add weapon to inventory
            weapons = save_manager.get_player_data("inventory.weapons") or []
            if item_id not in weapons:
                weapons.append(item_id)
                save_manager.set_player_data("inventory.weapons", weapons)
        
        # Play purchase sound
        audio_manager = self.game.get_system('audio_manager')
        asset_manager = self.game.get_system('asset_manager')
        if audio_manager and asset_manager:
            purchase_sound = asset_manager.get_sound("ui/purchase_success")
            if purchase_sound:
                audio_manager.play_sound(purchase_sound, "purchase", volume=0.8)
    
    def _handle_real_money_purchase(self, item: Dict[str, Any]):
        """Handle real money purchases (subscriptions)"""
        save_manager = self.game.get_system('save_manager')
        item_id = item['id']
        
        # Mock subscription activation (in real app, this would go through app store)
        import time
        current_time = time.time()
        
        if item_id == 'weekly_sub':
            expires = current_time + (7 * 24 * 3600)  # 7 days
            save_manager.set_player_data("subscriptions.weekly.active", True)
            save_manager.set_player_data("subscriptions.weekly.expires", expires)
            
            # Increase max stamina
            save_manager.set_player_data("stamina.max", Config.WEEKLY_SUB_MAX_STAMINA)
        
        elif item_id == 'monthly_sub':
            expires = current_time + (30 * 24 * 3600)  # 30 days
            save_manager.set_player_data("subscriptions.monthly.active", True)
            save_manager.set_player_data("subscriptions.monthly.expires", expires)
            
            # Increase max stamina
            save_manager.set_player_data("stamina.max", Config.MONTHLY_SUB_MAX_STAMINA)
        
        self.logger.info(f"Activated subscription: {item_id}")
    
    def _watch_ad(self, item: Dict[str, Any]):
        """Simulate watching an ad"""
        save_manager = self.game.get_system('save_manager')
        
        # Mock ad watching (in real app, this would show actual ad)
        self.logger.info("Showing advertisement...")
        
        # Give reward
        if item['id'] == 'watch_ad':
            current_gems = save_manager.get_player_data("currency.gems") or 0
            save_manager.set_player_data("currency.gems", current_gems + Config.GEMS_PER_AD)
        
        elif item['id'] == 'ad_boost':
            current_gems = save_manager.get_player_data("currency.gems") or 0
            bonus_gems = Config.GEMS_PER_AD * 10 + 5  # Bonus gems
            save_manager.set_player_data("currency.gems", current_gems + bonus_gems)
        
        # Update ad stats
        ads_watched = save_manager.get_player_data("stats.ads_watched") or 0
        save_manager.set_player_data("stats.ads_watched", ads_watched + 1)
        
        # Play reward sound
        audio_manager = self.game.get_system('audio_manager')
        asset_manager = self.game.get_system('asset_manager')
        if audio_manager and asset_manager:
            reward_sound = asset_manager.get_sound("ui/reward_earned")
            if reward_sound:
                audio_manager.play_sound(reward_sound, "reward", volume=0.9)
    
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Wrap text to fit within max width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Single word too long
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines