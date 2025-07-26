"""
Kingdom of Aldoria - Enhanced Shop System
Displays heroes, weapons, skins with proper categorization and payment integration
"""

import pygame
import logging
from typing import Dict, List, Optional, Any
from ..core.config import Config
from ..core.state_manager import GameState

class ShopState(GameState):
    """Enhanced shop interface with multiple categories and payment integration"""

    def __init__(self, game):
        """Initialize shop state"""
        super().__init__(game)
        self.logger = logging.getLogger(__name__)
        
        # Shop state
        self.current_category = "heroes"
        self.selected_item = None
        self.scroll_offset = 0
        self.items_per_page = 6
        
        # UI elements
        self.buttons = {}
        self.category_buttons = {}
        self.item_cards = []
        
        # Colors
        self.bg_color = Config.UI_BACKGROUND
        self.panel_color = Config.UI_PANEL
        self.text_color = Config.UI_TEXT
        self.accent_color = Config.UI_ACCENT
        self.gold_color = Config.GOLD
        
        # Categories
        self.categories = {
            "heroes": {"name": "Heroes", "icon": "⚔️", "items": Config.HEROES},
            "weapons": {"name": "Weapons", "icon": "🗡️", "items": Config.WEAPONS},
            "skins": {"name": "Skins", "icon": "🎭", "items": Config.SKINS},
            "gems": {"name": "Gems", "icon": "💎", "items": self._get_gem_packages()}
        }
        
        self.logger.info("Enhanced Shop initialized")

    def _get_gem_packages(self) -> Dict[str, Any]:
        """Get available gem packages"""
        return {
            "small_gem_pack": {
                "name": "Small Gem Pack",
                "rarity": "common",
                "amount": 100,
                "bonus": 0,
                "unlock_type": "payment_only",
                "cost": 0.99,
                "description": "Perfect starter pack for new knights"
            },
            "medium_gem_pack": {
                "name": "Medium Gem Pack",
                "rarity": "uncommon",
                "amount": 500,
                "bonus": 50,
                "unlock_type": "payment_only",
                "cost": 4.99,
                "description": "Great value for dedicated players"
            },
            "large_gem_pack": {
                "name": "Large Gem Pack",
                "rarity": "rare",
                "amount": 1200,
                "bonus": 200,
                "unlock_type": "payment_only",
                "cost": 9.99,
                "description": "Best value gem package"
            },
            "legendary_gem_pack": {
                "name": "Legendary Gem Pack",
                "rarity": "legendary",
                "amount": 2500,
                "bonus": 750,
                "unlock_type": "payment_only",
                "cost": 19.99,
                "description": "Ultimate gem collection for true champions"
            }
        }

    def enter(self):
        """Called when entering shop state"""
        self.logger.info("Entering enhanced shop")
        self._setup_ui()
        self._load_player_data()

    def exit(self):
        """Called when exiting shop state"""
        self.logger.info("Exiting enhanced shop")

    def _setup_ui(self):
        """Setup shop UI elements"""
        screen_width = Config.SCREEN_WIDTH
        screen_height = Config.SCREEN_HEIGHT
        
        # Category buttons
        category_width = 120
        category_height = 60
        category_spacing = 10
        start_x = (screen_width - (len(self.categories) * (category_width + category_spacing))) // 2
        
        for i, (cat_id, cat_data) in enumerate(self.categories.items()):
            x = start_x + i * (category_width + category_spacing)
            y = 100
            self.category_buttons[cat_id] = {
                'rect': pygame.Rect(x, y, category_width, category_height),
                'name': cat_data['name'],
                'icon': cat_data['icon'],
                'active': cat_id == self.current_category
            }
        
        # Action buttons
        button_width = 150
        button_height = 50
        button_y = screen_height - 80
        
        self.buttons = {
            'back': {
                'rect': pygame.Rect(50, button_y, button_width, button_height),
                'text': 'Back',
                'color': Config.DARK_GRAY
            },
            'buy': {
                'rect': pygame.Rect(screen_width - 200, button_y, button_width, button_height),
                'text': 'Purchase',
                'color': Config.GREEN
            },
            'watch_ad': {
                'rect': pygame.Rect(screen_width - 360, button_y, button_width, button_height),
                'text': 'Watch Ad for Gems',
                'color': Config.PURPLE
            }
        }

    def _load_player_data(self):
        """Load player data from save manager"""
        save_manager = self.game.get_system('save_manager')
        if save_manager:
            self.player_gems = save_manager.get_player_data('currency.gems') or 0
            self.player_gold = save_manager.get_player_data('currency.gold') or 0
            self.owned_items = save_manager.get_player_data('inventory') or {}

    def handle_event(self, event):
        """Handle shop events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.pop_state()
                return True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check category buttons
                for cat_id, button in self.category_buttons.items():
                    if button['rect'].collidepoint(mouse_pos):
                        self._switch_category(cat_id)
                        return True
                
                # Check action buttons
                if self.buttons['back']['rect'].collidepoint(mouse_pos):
                    self.game.state_manager.pop_state()
                    return True
                
                elif self.buttons['buy']['rect'].collidepoint(mouse_pos):
                    if self.selected_item:
                        self._purchase_item()
                    return True
                
                elif self.buttons['watch_ad']['rect'].collidepoint(mouse_pos):
                    self._watch_ad_for_gems()
                    return True
                
                # Check item cards
                for card in self.item_cards:
                    if card['rect'].collidepoint(mouse_pos):
                        self.selected_item = card['item_id']
                        return True
        
        elif event.type == pygame.MOUSEWHEEL:
            # Handle scrolling
            if event.y > 0:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.y < 0:  # Scroll down
                max_items = len(self.categories[self.current_category]['items'])
                max_scroll = max(0, (max_items - self.items_per_page + 2) // 3)
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
            return True
        
        return False

    def _switch_category(self, category_id: str):
        """Switch to a different shop category"""
        self.current_category = category_id
        self.selected_item = None
        self.scroll_offset = 0
        
        # Update category button states
        for cat_id in self.category_buttons:
            self.category_buttons[cat_id]['active'] = (cat_id == category_id)
        
        self.logger.info(f"Switched to category: {category_id}")

    def _purchase_item(self):
        """Purchase the selected item"""
        if not self.selected_item:
            return
        
        items = self.categories[self.current_category]['items']
        item_data = items.get(self.selected_item)
        
        if not item_data:
            return
        
        unlock_type = item_data.get('unlock_type', 'default')
        cost = item_data.get('cost', 0)
        
        if unlock_type == 'default':
            # Already unlocked
            self._show_message("Item already owned!", Config.YELLOW)
            return
        
        elif unlock_type == 'gold':
            if self.player_gold >= cost:
                self._complete_purchase('gold', cost)
            else:
                self._show_message(f"Not enough gold! Need {cost}", Config.RED)
        
        elif unlock_type == 'gems':
            if self.player_gems >= cost:
                self._complete_purchase('gems', cost)
            else:
                self._show_message(f"Not enough gems! Need {cost}", Config.RED)
        
        elif unlock_type == 'payment_only':
            # Redirect to web payment
            self._redirect_to_payment(item_data)

    def _complete_purchase(self, currency_type: str, cost: int):
        """Complete a gem/gold purchase"""
        save_manager = self.game.get_system('save_manager')
        if not save_manager:
            return
        
        # Deduct currency
        if currency_type == 'gems':
            new_gems = self.player_gems - cost
            save_manager.set_player_data('currency.gems', new_gems)
            self.player_gems = new_gems
        else:  # gold
            new_gold = self.player_gold - cost
            save_manager.set_player_data('currency.gold', new_gold)
            self.player_gold = new_gold
        
        # Add item to inventory
        inventory_key = f"inventory.{self.current_category}.{self.selected_item}"
        save_manager.set_player_data(inventory_key, True)
        
        # Update owned items
        if self.current_category not in self.owned_items:
            self.owned_items[self.current_category] = {}
        self.owned_items[self.current_category][self.selected_item] = True
        
        item_name = self.categories[self.current_category]['items'][self.selected_item]['name']
        self._show_message(f"Purchased {item_name}!", Config.GREEN)
        
        self.logger.info(f"Purchased {self.selected_item} for {cost} {currency_type}")

    def _redirect_to_payment(self, item_data: Dict[str, Any]):
        """Redirect to web payment for premium items"""
        web_integration = self.game.get_system('web_integration')
        if web_integration:
            # Determine package type based on item
            package_type = None
            if self.current_category == "heroes":
                package_type = "hero_" + self.selected_item
            elif self.current_category == "weapons":
                package_type = "weapon_" + self.selected_item
            elif self.current_category == "skins":
                package_type = "skin_" + self.selected_item
            elif self.current_category == "gems":
                package_type = "gems_" + self.selected_item
            
            if package_type:
                web_integration.open_store_website(package_type, auto_select=True)
                self._show_message("Opening payment portal...", Config.BLUE)
        else:
            self._show_message("Payment system unavailable", Config.RED)

    def _watch_ad_for_gems(self):
        """Watch an ad to earn gems"""
        ad_manager = self.game.get_system('ad_manager')
        if ad_manager:
            result = ad_manager.show_rewarded_ad()
            
            if result.get('success'):
                rewards = result.get('rewards', {})
                gems_earned = rewards.get('gems', 0)
                gold_earned = rewards.get('gold', 0)
                
                # Update local currency
                self.player_gems += gems_earned
                self.player_gold += gold_earned
                
                message = f"Earned {gems_earned} gems"
                if gold_earned > 0:
                    message += f" and {gold_earned} gold"
                message += "!"
                
                self._show_message(message, Config.GREEN)
                self.logger.info(f"Ad reward: {gems_earned} gems, {gold_earned} gold")
            else:
                reason = result.get('reason', 'unknown')
                message = result.get('message', 'Ad failed to load')
                self._show_message(message, Config.RED)
        else:
            self._show_message("Ad system unavailable", Config.RED)

    def _show_message(self, message: str, color: tuple):
        """Show a temporary message to the player"""
        # For now, just log the message
        # In a full implementation, you'd show this on screen
        self.logger.info(f"Shop message: {message}")

    def update(self, dt):
        """Update shop state"""
        pass

    def render(self, screen):
        """Render shop interface"""
        # Clear screen
        screen.fill(self.bg_color)
        
        # Render title
        self._render_title(screen)
        
        # Render currency display
        self._render_currency(screen)
        
        # Render category buttons
        self._render_category_buttons(screen)
        
        # Render item grid
        self._render_item_grid(screen)
        
        # Render item details
        if self.selected_item:
            self._render_item_details(screen)
        
        # Render action buttons
        self._render_action_buttons(screen)

    def _render_title(self, screen):
        """Render shop title"""
        font = pygame.font.Font(None, 48)
        title_text = font.render("Royal Shop", True, self.gold_color)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

    def _render_currency(self, screen):
        """Render player currency"""
        font = pygame.font.Font(None, 32)
        
        # Gems
        gems_text = font.render(f"💎 {self.player_gems}", True, Config.BLUE)
        screen.blit(gems_text, (Config.SCREEN_WIDTH - 250, 20))
        
        # Gold
        gold_text = font.render(f"🪙 {self.player_gold}", True, self.gold_color)
        screen.blit(gold_text, (Config.SCREEN_WIDTH - 150, 20))

    def _render_category_buttons(self, screen):
        """Render category selection buttons"""
        font = pygame.font.Font(None, 24)
        
        for cat_id, button in self.category_buttons.items():
            # Button background
            color = self.accent_color if button['active'] else self.panel_color
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, self.gold_color, button['rect'], 2)
            
            # Icon and text
            icon_text = font.render(button['icon'], True, self.text_color)
            name_text = font.render(button['name'], True, self.text_color)
            
            icon_rect = icon_text.get_rect(center=(button['rect'].centerx, button['rect'].centery - 10))
            name_rect = name_text.get_rect(center=(button['rect'].centerx, button['rect'].centery + 10))
            
            screen.blit(icon_text, icon_rect)
            screen.blit(name_text, name_rect)

    def _render_item_grid(self, screen):
        """Render grid of items"""
        items = self.categories[self.current_category]['items']
        item_list = list(items.items())
        
        # Clear item cards
        self.item_cards = []
        
        # Calculate grid layout
        grid_start_y = 200
        grid_width = Config.SCREEN_WIDTH - 100
        grid_start_x = 50
        
        items_per_row = 3
        item_width = (grid_width - (items_per_row - 1) * 20) // items_per_row
        item_height = 180
        
        # Calculate visible items based on scroll
        start_index = self.scroll_offset * items_per_row
        visible_items = item_list[start_index:start_index + self.items_per_page]
        
        for i, (item_id, item_data) in enumerate(visible_items):
            row = i // items_per_row
            col = i % items_per_row
            
            x = grid_start_x + col * (item_width + 20)
            y = grid_start_y + row * (item_height + 20)
            
            item_rect = pygame.Rect(x, y, item_width, item_height)
            
            # Store card info for click detection
            self.item_cards.append({
                'rect': item_rect,
                'item_id': item_id,
                'item_data': item_data
            })
            
            # Render item card
            self._render_item_card(screen, item_rect, item_id, item_data)

    def _render_item_card(self, screen, rect, item_id, item_data):
        """Render individual item card"""
        # Card background
        is_selected = (item_id == self.selected_item)
        is_owned = self._is_item_owned(item_id)
        
        if is_selected:
            color = (100, 150, 255)
        elif is_owned:
            color = (100, 255, 100)
        else:
            color = self.panel_color
        
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, self.gold_color, rect, 2)
        
        # Item name
        font = pygame.font.Font(None, 24)
        name_text = font.render(item_data['name'], True, self.text_color)
        name_rect = name_text.get_rect(center=(rect.centerx, rect.y + 20))
        screen.blit(name_text, name_rect)
        
        # Rarity indicator
        rarity = item_data.get('rarity', 'common')
        rarity_colors = {
            'common': Config.WHITE,
            'uncommon': Config.GREEN,
            'rare': Config.BLUE,
            'epic': Config.PURPLE,
            'legendary': Config.ORANGE,
            'mythic': Config.RED
        }
        rarity_color = rarity_colors.get(rarity, Config.WHITE)
        
        rarity_text = pygame.font.Font(None, 18).render(rarity.upper(), True, rarity_color)
        rarity_rect = rarity_text.get_rect(center=(rect.centerx, rect.y + 45))
        screen.blit(rarity_text, rarity_rect)
        
        # Cost/Status
        unlock_type = item_data.get('unlock_type', 'default')
        cost = item_data.get('cost', 0)
        
        if is_owned:
            status_text = "OWNED"
            status_color = Config.GREEN
        elif unlock_type == 'default':
            status_text = "FREE"
            status_color = Config.GREEN
        elif unlock_type == 'gold':
            status_text = f"🪙 {cost}"
            status_color = self.gold_color
        elif unlock_type == 'gems':
            status_text = f"💎 {cost}"
            status_color = Config.BLUE
        elif unlock_type == 'payment_only':
            status_text = f"${cost}"
            status_color = Config.RED
        else:
            status_text = "N/A"
            status_color = Config.GRAY
        
        cost_font = pygame.font.Font(None, 20)
        cost_text = cost_font.render(status_text, True, status_color)
        cost_rect = cost_text.get_rect(center=(rect.centerx, rect.bottom - 20))
        screen.blit(cost_text, cost_rect)

    def _render_item_details(self, screen):
        """Render details of selected item"""
        if not self.selected_item:
            return
        
        items = self.categories[self.current_category]['items']
        item_data = items.get(self.selected_item)
        
        if not item_data:
            return
        
        # Details panel
        panel_width = 300
        panel_height = 200
        panel_x = Config.SCREEN_WIDTH - panel_width - 20
        panel_y = 200
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, self.panel_color, panel_rect)
        pygame.draw.rect(screen, self.gold_color, panel_rect, 2)
        
        # Item details
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
        y_offset = panel_y + 20
        
        # Name
        name_text = font.render(item_data['name'], True, self.text_color)
        screen.blit(name_text, (panel_x + 10, y_offset))
        y_offset += 30
        
        # Special attributes based on category
        if self.current_category == "heroes":
            self._render_hero_stats(screen, panel_x + 10, y_offset, item_data, small_font)
        elif self.current_category == "weapons":
            self._render_weapon_stats(screen, panel_x + 10, y_offset, item_data, small_font)
        elif self.current_category == "skins":
            self._render_skin_stats(screen, panel_x + 10, y_offset, item_data, small_font)
        elif self.current_category == "gems":
            self._render_gem_package_stats(screen, panel_x + 10, y_offset, item_data, small_font)

    def _render_hero_stats(self, screen, x, y, item_data, font):
        """Render hero-specific stats"""
        stats = [
            f"HP: {item_data.get('base_hp', 0)}",
            f"Attack: {item_data.get('base_attack', 0)}",
            f"Defense: {item_data.get('base_defense', 0)}",
            f"Skill: {item_data.get('skill', 'None')}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, self.text_color)
            screen.blit(text, (x, y + i * 20))

    def _render_weapon_stats(self, screen, x, y, item_data, font):
        """Render weapon-specific stats"""
        stats = [
            f"Attack: +{item_data.get('attack', 0)}",
            f"Special: {item_data.get('special', 'None')}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, self.text_color)
            screen.blit(text, (x, y + i * 20))

    def _render_skin_stats(self, screen, x, y, item_data, font):
        """Render skin-specific stats"""
        bonus = item_data.get('bonus', 'None')
        text = font.render(f"Bonus: {bonus}", True, self.text_color)
        screen.blit(text, (x, y))

    def _render_gem_package_stats(self, screen, x, y, item_data, font):
        """Render gem package details"""
        amount = item_data.get('amount', 0)
        bonus = item_data.get('bonus', 0)
        description = item_data.get('description', '')
        
        stats = [
            f"Gems: {amount}",
            f"Bonus: +{bonus}" if bonus > 0 else "No bonus",
            f"Total: {amount + bonus}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, self.text_color)
            screen.blit(text, (x, y + i * 20))

    def _render_action_buttons(self, screen):
        """Render action buttons"""
        font = pygame.font.Font(None, 32)
        
        for button_id, button in self.buttons.items():
            # Skip buy button if no item selected
            if button_id == 'buy' and not self.selected_item:
                continue
            
            # Button background
            pygame.draw.rect(screen, button['color'], button['rect'])
            pygame.draw.rect(screen, self.text_color, button['rect'], 2)
            
            # Button text
            text = font.render(button['text'], True, self.text_color)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)

    def _is_item_owned(self, item_id: str) -> bool:
        """Check if player owns the item"""
        return self.owned_items.get(self.current_category, {}).get(item_id, False)