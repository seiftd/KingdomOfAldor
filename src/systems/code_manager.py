"""
Kingdom of Aldoria - Code Redemption Manager
Handles promo codes with admin management and tracking
"""

import logging
import time
import hashlib
import json
import sqlite3
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from ..core.config import Config

class CodeManager:
    """Manages promo codes and redemption system"""
    
    def __init__(self, game):
        self.game = game
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.sqlite_conn = None
        
        # Code types and rewards
        self.code_types = {
            'welcome': {'gems': 100, 'gold': 1000},
            'daily': {'gems': 25, 'gold': 500},
            'weekly': {'gems': 100, 'gold': 2000},
            'event': {'gems': 500, 'gold': 5000},
            'premium': {'gems': 1000, 'gold': 10000},
            'vip': {'gems': 2500, 'gold': 25000}
        }
        
        # Initialize database
        self._init_database()
        
        self.logger.info("CodeManager initialized")

    def _init_database(self):
        """Initialize SQLite database for code management"""
        try:
            db_path = Config.SAVE_DIR / "codes.db"
            Config.SAVE_DIR.mkdir(exist_ok=True)
            
            self.sqlite_conn = sqlite3.connect(str(db_path), check_same_thread=False)
            self.sqlite_conn.row_factory = sqlite3.Row
            
            # Create tables
            self._create_tables()
            
            # Insert default codes
            self._create_default_codes()
            
            self.logger.info("Code database initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize code database: {e}")
            raise

    def _create_tables(self):
        """Create code management tables"""
        cursor = self.sqlite_conn.cursor()
        
        # Promo codes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promo_codes (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                code_type TEXT DEFAULT 'custom',
                reward_gems INTEGER DEFAULT 0,
                reward_gold INTEGER DEFAULT 0,
                reward_items TEXT,
                usage_limit INTEGER DEFAULT 1,
                current_usage INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT TRUE,
                start_date INTEGER DEFAULT 0,
                end_date INTEGER DEFAULT 0,
                created_by TEXT DEFAULT 'system',
                created_at INTEGER DEFAULT 0,
                updated_at INTEGER DEFAULT 0
            )
        ''')
        
        # Code redemptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS code_redemptions (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                code TEXT NOT NULL,
                redeemed_at INTEGER DEFAULT 0,
                reward_claimed TEXT,
                ip_address TEXT,
                FOREIGN KEY (code) REFERENCES promo_codes (code)
            )
        ''')
        
        # Code analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS code_analytics (
                id INTEGER PRIMARY KEY,
                code TEXT NOT NULL,
                date TEXT NOT NULL,
                redemptions INTEGER DEFAULT 0,
                unique_users INTEGER DEFAULT 0,
                total_gems_given INTEGER DEFAULT 0,
                total_gold_given INTEGER DEFAULT 0,
                FOREIGN KEY (code) REFERENCES promo_codes (code)
            )
        ''')
        
        self.sqlite_conn.commit()

    def _create_default_codes(self):
        """Create some default promotional codes"""
        default_codes = [
            {
                'code': 'WELCOME2024',
                'name': 'Welcome to Kingdom of Aldoria',
                'description': 'New player welcome gift',
                'code_type': 'welcome',
                'reward_gems': 100,
                'reward_gold': 1000,
                'usage_limit': 1000,
                'end_date': int(time.time()) + (365 * 24 * 3600),  # 1 year
                'created_by': 'system'
            },
            {
                'code': 'LAUNCH50',
                'name': 'Game Launch Celebration',
                'description': 'Limited time launch bonus',
                'code_type': 'event',
                'reward_gems': 500,
                'reward_gold': 5000,
                'usage_limit': 500,
                'end_date': int(time.time()) + (30 * 24 * 3600),  # 30 days
                'created_by': 'system'
            },
            {
                'code': 'SEIFVIP',
                'name': 'Creator Special',
                'description': 'Special code from the creator',
                'code_type': 'vip',
                'reward_gems': 2500,
                'reward_gold': 25000,
                'usage_limit': 100,
                'end_date': int(time.time()) + (90 * 24 * 3600),  # 90 days
                'created_by': 'seiftouatilol@gmail.com'
            }
        ]
        
        cursor = self.sqlite_conn.cursor()
        current_time = int(time.time())
        
        for code_data in default_codes:
            cursor.execute('''
                INSERT OR IGNORE INTO promo_codes 
                (code, name, description, code_type, reward_gems, reward_gold, 
                 usage_limit, end_date, created_by, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                code_data['code'], code_data['name'], code_data['description'],
                code_data['code_type'], code_data['reward_gems'], code_data['reward_gold'],
                code_data['usage_limit'], code_data['end_date'], code_data['created_by'],
                current_time, current_time
            ))
        
        self.sqlite_conn.commit()

    def create_code(self, code: str, name: str, description: str = "", 
                   code_type: str = "custom", reward_gems: int = 0, 
                   reward_gold: int = 0, reward_items: Optional[Dict] = None,
                   usage_limit: int = 1, duration_days: int = 30,
                   created_by: str = "admin") -> Dict[str, Any]:
        """Create a new promo code"""
        try:
            cursor = self.sqlite_conn.cursor()
            current_time = int(time.time())
            end_date = current_time + (duration_days * 24 * 3600)
            
            # Validate code format
            if not self._is_valid_code_format(code):
                return {
                    'success': False,
                    'message': 'Invalid code format. Use uppercase letters and numbers only.'
                }
            
            # Check if code already exists
            cursor.execute('SELECT code FROM promo_codes WHERE code = ?', (code,))
            if cursor.fetchone():
                return {
                    'success': False,
                    'message': 'Code already exists.'
                }
            
            # Prepare reward items JSON
            reward_items_json = json.dumps(reward_items) if reward_items else None
            
            # Insert new code
            cursor.execute('''
                INSERT INTO promo_codes 
                (code, name, description, code_type, reward_gems, reward_gold, 
                 reward_items, usage_limit, start_date, end_date, created_by, 
                 created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                code, name, description, code_type, reward_gems, reward_gold,
                reward_items_json, usage_limit, current_time, end_date, created_by,
                current_time, current_time
            ))
            
            self.sqlite_conn.commit()
            
            self.logger.info(f"Created promo code: {code} by {created_by}")
            
            return {
                'success': True,
                'message': f'Code {code} created successfully!',
                'code_data': {
                    'code': code,
                    'name': name,
                    'description': description,
                    'reward_gems': reward_gems,
                    'reward_gold': reward_gold,
                    'usage_limit': usage_limit,
                    'expires': datetime.fromtimestamp(end_date).strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create code {code}: {e}")
            return {
                'success': False,
                'message': f'Failed to create code: {str(e)}'
            }

    def redeem_code(self, user_id: str, code: str, ip_address: str = "unknown") -> Dict[str, Any]:
        """Redeem a promo code for a user"""
        try:
            cursor = self.sqlite_conn.cursor()
            current_time = int(time.time())
            
            # Get code information
            cursor.execute('''
                SELECT * FROM promo_codes WHERE code = ? AND active = TRUE
            ''', (code.upper(),))
            
            code_data = cursor.fetchone()
            if not code_data:
                return {
                    'success': False,
                    'message': 'Invalid or inactive code.'
                }
            
            code_dict = dict(code_data)
            
            # Check if code is expired
            if code_dict['end_date'] > 0 and current_time > code_dict['end_date']:
                return {
                    'success': False,
                    'message': 'Code has expired.'
                }
            
            # Check if code hasn't started yet
            if code_dict['start_date'] > 0 and current_time < code_dict['start_date']:
                return {
                    'success': False,
                    'message': 'Code is not yet active.'
                }
            
            # Check usage limit
            if code_dict['current_usage'] >= code_dict['usage_limit']:
                return {
                    'success': False,
                    'message': 'Code usage limit reached.'
                }
            
            # Check if user already redeemed this code
            cursor.execute('''
                SELECT id FROM code_redemptions 
                WHERE user_id = ? AND code = ?
            ''', (user_id, code.upper()))
            
            if cursor.fetchone():
                return {
                    'success': False,
                    'message': 'You have already redeemed this code.'
                }
            
            # Process redemption
            rewards_granted = {}
            
            # Grant gems
            if code_dict['reward_gems'] > 0:
                db_manager = self.game.get_system('database_manager')
                if db_manager:
                    db_manager.add_currency(user_id, 'gems', code_dict['reward_gems'])
                    rewards_granted['gems'] = code_dict['reward_gems']
            
            # Grant gold
            if code_dict['reward_gold'] > 0:
                db_manager = self.game.get_system('database_manager')
                if db_manager:
                    db_manager.add_currency(user_id, 'gold', code_dict['reward_gold'])
                    rewards_granted['gold'] = code_dict['reward_gold']
            
            # Grant items
            if code_dict['reward_items']:
                try:
                    items = json.loads(code_dict['reward_items'])
                    db_manager = self.game.get_system('database_manager')
                    if db_manager and items:
                        for item_type, item_list in items.items():
                            for item_id, quantity in item_list.items():
                                db_manager.add_inventory_item(user_id, item_type, item_id, quantity)
                        rewards_granted['items'] = items
                except json.JSONDecodeError:
                    pass
            
            # Record redemption
            cursor.execute('''
                INSERT INTO code_redemptions 
                (user_id, code, redeemed_at, reward_claimed, ip_address)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, code.upper(), current_time, json.dumps(rewards_granted), ip_address))
            
            # Update code usage
            cursor.execute('''
                UPDATE promo_codes 
                SET current_usage = current_usage + 1, updated_at = ?
                WHERE code = ?
            ''', (current_time, code.upper()))
            
            # Update analytics
            self._update_code_analytics(code.upper(), code_dict['reward_gems'], code_dict['reward_gold'])
            
            self.sqlite_conn.commit()
            
            self.logger.info(f"Code {code} redeemed by {user_id}")
            
            return {
                'success': True,
                'message': 'Code redeemed successfully!',
                'rewards': rewards_granted,
                'code_name': code_dict['name']
            }
            
        except Exception as e:
            self.logger.error(f"Failed to redeem code {code}: {e}")
            return {
                'success': False,
                'message': f'Failed to redeem code: {str(e)}'
            }

    def get_code_info(self, code: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific code"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('SELECT * FROM promo_codes WHERE code = ?', (code.upper(),))
            
            result = cursor.fetchone()
            if result:
                code_data = dict(result)
                
                # Parse reward items if present
                if code_data['reward_items']:
                    try:
                        code_data['reward_items'] = json.loads(code_data['reward_items'])
                    except json.JSONDecodeError:
                        code_data['reward_items'] = {}
                
                # Format dates
                if code_data['start_date']:
                    code_data['start_date_formatted'] = datetime.fromtimestamp(
                        code_data['start_date']).strftime('%Y-%m-%d %H:%M:%S')
                
                if code_data['end_date']:
                    code_data['end_date_formatted'] = datetime.fromtimestamp(
                        code_data['end_date']).strftime('%Y-%m-%d %H:%M:%S')
                
                # Calculate remaining uses
                code_data['remaining_uses'] = max(0, code_data['usage_limit'] - code_data['current_usage'])
                
                return code_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get code info for {code}: {e}")
            return None

    def get_all_codes(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Get all promo codes"""
        try:
            cursor = self.sqlite_conn.cursor()
            
            if active_only:
                cursor.execute('''
                    SELECT * FROM promo_codes 
                    WHERE active = TRUE 
                    ORDER BY created_at DESC
                ''')
            else:
                cursor.execute('''
                    SELECT * FROM promo_codes 
                    ORDER BY created_at DESC
                ''')
            
            results = cursor.fetchall()
            codes = []
            
            for row in results:
                code_data = dict(row)
                
                # Parse reward items
                if code_data['reward_items']:
                    try:
                        code_data['reward_items'] = json.loads(code_data['reward_items'])
                    except json.JSONDecodeError:
                        code_data['reward_items'] = {}
                
                # Format dates
                if code_data['start_date']:
                    code_data['start_date_formatted'] = datetime.fromtimestamp(
                        code_data['start_date']).strftime('%Y-%m-%d %H:%M:%S')
                
                if code_data['end_date']:
                    code_data['end_date_formatted'] = datetime.fromtimestamp(
                        code_data['end_date']).strftime('%Y-%m-%d %H:%M:%S')
                
                # Calculate status
                current_time = int(time.time())
                if not code_data['active']:
                    code_data['status'] = 'inactive'
                elif code_data['end_date'] > 0 and current_time > code_data['end_date']:
                    code_data['status'] = 'expired'
                elif code_data['current_usage'] >= code_data['usage_limit']:
                    code_data['status'] = 'exhausted'
                else:
                    code_data['status'] = 'active'
                
                codes.append(code_data)
            
            return codes
            
        except Exception as e:
            self.logger.error(f"Failed to get all codes: {e}")
            return []

    def update_code(self, code: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing promo code"""
        try:
            cursor = self.sqlite_conn.cursor()
            current_time = int(time.time())
            
            # Check if code exists
            cursor.execute('SELECT id FROM promo_codes WHERE code = ?', (code.upper(),))
            if not cursor.fetchone():
                return {
                    'success': False,
                    'message': 'Code not found.'
                }
            
            # Build update query
            allowed_fields = [
                'name', 'description', 'reward_gems', 'reward_gold', 
                'reward_items', 'usage_limit', 'active', 'end_date'
            ]
            
            update_fields = []
            values = []
            
            for field, value in updates.items():
                if field in allowed_fields:
                    update_fields.append(f"{field} = ?")
                    if field == 'reward_items' and isinstance(value, dict):
                        values.append(json.dumps(value))
                    else:
                        values.append(value)
            
            if not update_fields:
                return {
                    'success': False,
                    'message': 'No valid fields to update.'
                }
            
            # Add updated timestamp
            update_fields.append("updated_at = ?")
            values.append(current_time)
            values.append(code.upper())
            
            # Execute update
            cursor.execute(f'''
                UPDATE promo_codes 
                SET {', '.join(update_fields)}
                WHERE code = ?
            ''', values)
            
            self.sqlite_conn.commit()
            
            self.logger.info(f"Updated code: {code}")
            
            return {
                'success': True,
                'message': f'Code {code} updated successfully!'
            }
            
        except Exception as e:
            self.logger.error(f"Failed to update code {code}: {e}")
            return {
                'success': False,
                'message': f'Failed to update code: {str(e)}'
            }

    def delete_code(self, code: str) -> Dict[str, Any]:
        """Delete a promo code"""
        try:
            cursor = self.sqlite_conn.cursor()
            
            # Check if code exists
            cursor.execute('SELECT id FROM promo_codes WHERE code = ?', (code.upper(),))
            if not cursor.fetchone():
                return {
                    'success': False,
                    'message': 'Code not found.'
                }
            
            # Delete redemptions first (foreign key constraint)
            cursor.execute('DELETE FROM code_redemptions WHERE code = ?', (code.upper(),))
            
            # Delete analytics
            cursor.execute('DELETE FROM code_analytics WHERE code = ?', (code.upper(),))
            
            # Delete code
            cursor.execute('DELETE FROM promo_codes WHERE code = ?', (code.upper(),))
            
            self.sqlite_conn.commit()
            
            self.logger.info(f"Deleted code: {code}")
            
            return {
                'success': True,
                'message': f'Code {code} deleted successfully!'
            }
            
        except Exception as e:
            self.logger.error(f"Failed to delete code {code}: {e}")
            return {
                'success': False,
                'message': f'Failed to delete code: {str(e)}'
            }

    def get_code_analytics(self, code: str = None) -> Dict[str, Any]:
        """Get analytics data for codes"""
        try:
            cursor = self.sqlite_conn.cursor()
            
            if code:
                # Analytics for specific code
                cursor.execute('''
                    SELECT * FROM code_analytics 
                    WHERE code = ? 
                    ORDER BY date DESC
                ''', (code.upper(),))
                
                analytics = [dict(row) for row in cursor.fetchall()]
                
                # Get redemption details
                cursor.execute('''
                    SELECT user_id, redeemed_at, reward_claimed 
                    FROM code_redemptions 
                    WHERE code = ? 
                    ORDER BY redeemed_at DESC
                ''', (code.upper(),))
                
                redemptions = [dict(row) for row in cursor.fetchall()]
                
                return {
                    'code': code.upper(),
                    'analytics': analytics,
                    'redemptions': redemptions
                }
            else:
                # Overall analytics
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_codes,
                        COUNT(CASE WHEN active = TRUE THEN 1 END) as active_codes,
                        SUM(current_usage) as total_redemptions,
                        SUM(reward_gems * current_usage) as total_gems_given,
                        SUM(reward_gold * current_usage) as total_gold_given
                    FROM promo_codes
                ''')
                
                overall_stats = dict(cursor.fetchone())
                
                # Top codes by usage
                cursor.execute('''
                    SELECT code, name, current_usage, usage_limit
                    FROM promo_codes 
                    ORDER BY current_usage DESC 
                    LIMIT 10
                ''')
                
                top_codes = [dict(row) for row in cursor.fetchall()]
                
                return {
                    'overall_stats': overall_stats,
                    'top_codes': top_codes
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get analytics: {e}")
            return {}

    def get_user_redemptions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all codes redeemed by a user"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('''
                SELECT cr.*, pc.name, pc.description
                FROM code_redemptions cr
                JOIN promo_codes pc ON cr.code = pc.code
                WHERE cr.user_id = ?
                ORDER BY cr.redeemed_at DESC
            ''', (user_id,))
            
            redemptions = []
            for row in cursor.fetchall():
                redemption = dict(row)
                
                # Parse reward data
                if redemption['reward_claimed']:
                    try:
                        redemption['reward_claimed'] = json.loads(redemption['reward_claimed'])
                    except json.JSONDecodeError:
                        redemption['reward_claimed'] = {}
                
                # Format date
                redemption['redeemed_at_formatted'] = datetime.fromtimestamp(
                    redemption['redeemed_at']).strftime('%Y-%m-%d %H:%M:%S')
                
                redemptions.append(redemption)
            
            return redemptions
            
        except Exception as e:
            self.logger.error(f"Failed to get user redemptions for {user_id}: {e}")
            return []

    def _update_code_analytics(self, code: str, gems_given: int, gold_given: int):
        """Update daily analytics for a code"""
        try:
            cursor = self.sqlite_conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Check if entry exists for today
            cursor.execute('''
                SELECT id FROM code_analytics 
                WHERE code = ? AND date = ?
            ''', (code, today))
            
            if cursor.fetchone():
                # Update existing entry
                cursor.execute('''
                    UPDATE code_analytics 
                    SET redemptions = redemptions + 1,
                        unique_users = unique_users + 1,
                        total_gems_given = total_gems_given + ?,
                        total_gold_given = total_gold_given + ?
                    WHERE code = ? AND date = ?
                ''', (gems_given, gold_given, code, today))
            else:
                # Create new entry
                cursor.execute('''
                    INSERT INTO code_analytics 
                    (code, date, redemptions, unique_users, total_gems_given, total_gold_given)
                    VALUES (?, ?, 1, 1, ?, ?)
                ''', (code, today, gems_given, gold_given))
            
            self.sqlite_conn.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to update analytics for {code}: {e}")

    def _is_valid_code_format(self, code: str) -> bool:
        """Validate code format"""
        if not code:
            return False
        
        # Must be 3-20 characters, uppercase letters and numbers only
        if len(code) < 3 or len(code) > 20:
            return False
        
        return code.replace('_', '').replace('-', '').isalnum() and code.isupper()

    def cleanup(self):
        """Cleanup database connections"""
        try:
            if self.sqlite_conn:
                self.sqlite_conn.close()
                
            self.logger.info("CodeManager cleaned up")
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")