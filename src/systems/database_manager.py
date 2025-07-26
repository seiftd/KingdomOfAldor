"""
Kingdom of Aldoria - Database Manager
Handles both offline (SQLite) and online (Firebase) data storage with sync
"""

import sqlite3
import json
import time
import logging
import hashlib
import threading
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime, timedelta

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Firebase not available - running in offline mode only")

from ..core.config import Config

class DatabaseManager:
    """Unified database manager for offline and online data"""
    
    def __init__(self, game):
        self.game = game
        self.logger = logging.getLogger(__name__)
        
        # Database connections
        self.sqlite_conn = None
        self.firestore_db = None
        
        # User state
        self.current_user_id = None
        self.is_online = False
        self.last_sync_time = 0
        
        # Sync settings
        self.auto_sync_enabled = True
        self.sync_interval = 300  # 5 minutes
        self.sync_lock = threading.Lock()
        
        # Initialize databases
        self._init_sqlite()
        self._init_firebase()
        
        self.logger.info("DatabaseManager initialized")

    def _init_sqlite(self):
        """Initialize SQLite database for offline storage"""
        try:
            db_path = Config.SAVE_DIR / "kingdom_of_aldoria.db"
            Config.SAVE_DIR.mkdir(exist_ok=True)
            
            self.sqlite_conn = sqlite3.connect(str(db_path), check_same_thread=False)
            self.sqlite_conn.row_factory = sqlite3.Row
            
            # Create tables
            self._create_sqlite_tables()
            
            self.logger.info("SQLite database initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize SQLite: {e}")
            raise

    def _create_sqlite_tables(self):
        """Create SQLite tables for offline storage"""
        cursor = self.sqlite_conn.cursor()
        
        # Player data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_data (
                id INTEGER PRIMARY KEY,
                user_id TEXT UNIQUE,
                level INTEGER DEFAULT 1,
                hp INTEGER DEFAULT 100,
                attack INTEGER DEFAULT 10,
                defense INTEGER DEFAULT 5,
                gold INTEGER DEFAULT 0,
                gems INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                current_world INTEGER DEFAULT 1,
                current_stage INTEGER DEFAULT 1,
                stamina_current INTEGER DEFAULT 10,
                stamina_max INTEGER DEFAULT 10,
                stamina_last_update INTEGER DEFAULT 0,
                created_at INTEGER DEFAULT 0,
                updated_at INTEGER DEFAULT 0
            )
        ''')
        
        # Inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                item_type TEXT,
                item_id TEXT,
                quantity INTEGER DEFAULT 1,
                equipped BOOLEAN DEFAULT FALSE,
                acquired_at INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES player_data (user_id)
            )
        ''')
        
        # Stage progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stage_progress (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                world_id INTEGER,
                stage_id INTEGER,
                completed BOOLEAN DEFAULT FALSE,
                stars INTEGER DEFAULT 0,
                best_time REAL DEFAULT 0,
                completed_at INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES player_data (user_id)
            )
        ''')
        
        # Login streaks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_streaks (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_login_date TEXT,
                total_logins INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES player_data (user_id)
            )
        ''')
        
        # Subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                subscription_type TEXT,
                active BOOLEAN DEFAULT FALSE,
                start_date INTEGER DEFAULT 0,
                end_date INTEGER DEFAULT 0,
                auto_renew BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES player_data (user_id)
            )
        ''')
        
        # Sync metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_metadata (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                table_name TEXT,
                last_sync INTEGER DEFAULT 0,
                sync_hash TEXT,
                conflict_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES player_data (user_id)
            )
        ''')
        
        self.sqlite_conn.commit()

    def _init_firebase(self):
        """Initialize Firebase connection"""
        if not FIREBASE_AVAILABLE:
            self.logger.warning("Firebase SDK not available")
            return
        
        try:
            # Initialize Firebase (in production, use service account key)
            if not firebase_admin._apps:
                # Mock Firebase config for development
                firebase_config = {
                    "type": "service_account",
                    "project_id": "kingdom-of-aldoria",
                    "private_key_id": "mock_key_id",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMOCK_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
                    "client_email": "firebase-adminsdk@kingdom-of-aldoria.iam.gserviceaccount.com",
                    "client_id": "mock_client_id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
                
                # In development mode, we'll simulate Firebase
                self.firestore_db = MockFirestore()
                self.logger.info("Mock Firebase initialized for development")
            else:
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
                self.firestore_db = firestore.client()
                self.logger.info("Firebase Firestore initialized")
                
        except Exception as e:
            self.logger.warning(f"Firebase initialization failed: {e}")
            self.firestore_db = MockFirestore()

    def create_user(self, user_id: str) -> bool:
        """Create new user in both databases"""
        try:
            current_time = int(time.time())
            
            # Create in SQLite
            cursor = self.sqlite_conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO player_data 
                (user_id, created_at, updated_at, stamina_last_update)
                VALUES (?, ?, ?, ?)
            ''', (user_id, current_time, current_time, current_time))
            
            # Initialize login streak
            cursor.execute('''
                INSERT OR REPLACE INTO login_streaks 
                (user_id, last_login_date, total_logins)
                VALUES (?, ?, ?)
            ''', (user_id, datetime.now().strftime('%Y-%m-%d'), 1))
            
            self.sqlite_conn.commit()
            
            # Create in Firebase if online
            if self.is_online and self.firestore_db:
                player_data = {
                    'user_id': user_id,
                    'level': 1,
                    'hp': 100,
                    'attack': 10,
                    'defense': 5,
                    'gold': 0,
                    'gems': 0,
                    'xp': 0,
                    'current_world': 1,
                    'current_stage': 1,
                    'stamina_current': 10,
                    'stamina_max': 10,
                    'stamina_last_update': current_time,
                    'created_at': current_time,
                    'updated_at': current_time
                }
                
                self.firestore_db.collection('players').document(user_id).set(player_data)
                
                # Initialize login streak in Firebase
                streak_data = {
                    'current_streak': 1,
                    'longest_streak': 1,
                    'last_login_date': datetime.now().strftime('%Y-%m-%d'),
                    'total_logins': 1
                }
                self.firestore_db.collection('login_streaks').document(user_id).set(streak_data)
            
            self.current_user_id = user_id
            self.logger.info(f"Created user: {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create user {user_id}: {e}")
            return False

    def login_user(self, user_id: str) -> bool:
        """Login user and sync data"""
        try:
            self.current_user_id = user_id
            
            # Update stamina based on offline time
            self._update_stamina(user_id)
            
            # Handle daily login
            self._handle_daily_login(user_id)
            
            # Attempt online sync
            if self.firestore_db:
                self._attempt_online_sync(user_id)
            
            self.logger.info(f"User logged in: {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Login failed for {user_id}: {e}")
            return False

    def _update_stamina(self, user_id: str):
        """Update stamina based on offline time"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('''
                SELECT stamina_current, stamina_max, stamina_last_update
                FROM player_data WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if not result:
                return
            
            current_stamina, max_stamina, last_update = result
            current_time = int(time.time())
            
            # Calculate stamina regeneration
            time_diff = current_time - last_update
            stamina_regen_time = Config.STAMINA_RECHARGE_MINUTES * 60  # Convert to seconds
            
            if time_diff >= stamina_regen_time:
                stamina_gained = min(time_diff // stamina_regen_time, max_stamina - current_stamina)
                new_stamina = min(current_stamina + stamina_gained, max_stamina)
                
                cursor.execute('''
                    UPDATE player_data 
                    SET stamina_current = ?, stamina_last_update = ?
                    WHERE user_id = ?
                ''', (new_stamina, current_time, user_id))
                
                self.sqlite_conn.commit()
                
                if stamina_gained > 0:
                    self.logger.info(f"Stamina regenerated: +{stamina_gained} (Total: {new_stamina})")
                    
        except Exception as e:
            self.logger.error(f"Failed to update stamina: {e}")

    def _handle_daily_login(self, user_id: str):
        """Handle daily login streaks and rewards"""
        try:
            cursor = self.sqlite_conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT current_streak, longest_streak, last_login_date, total_logins
                FROM login_streaks WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if not result:
                # First login
                cursor.execute('''
                    INSERT INTO login_streaks 
                    (user_id, current_streak, longest_streak, last_login_date, total_logins)
                    VALUES (?, 1, 1, ?, 1)
                ''', (user_id, today))
            else:
                current_streak, longest_streak, last_login, total_logins = result
                
                if last_login == today:
                    # Already logged in today
                    return
                
                yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                
                if last_login == yesterday:
                    # Consecutive login
                    current_streak += 1
                else:
                    # Streak broken
                    current_streak = 1
                
                longest_streak = max(longest_streak, current_streak)
                total_logins += 1
                
                cursor.execute('''
                    UPDATE login_streaks 
                    SET current_streak = ?, longest_streak = ?, 
                        last_login_date = ?, total_logins = ?
                    WHERE user_id = ?
                ''', (current_streak, longest_streak, today, total_logins, user_id))
                
                # Grant daily login rewards
                self._grant_daily_rewards(user_id, current_streak)
            
            self.sqlite_conn.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to handle daily login: {e}")

    def _grant_daily_rewards(self, user_id: str, streak_day: int):
        """Grant daily login rewards based on streak"""
        try:
            # Daily login rewards (gems)
            base_gems = 5
            streak_bonus = min(streak_day - 1, 10)  # Max 10 bonus gems
            total_gems = base_gems + streak_bonus
            
            # Weekly milestone rewards
            if streak_day % 7 == 0:
                total_gems += 50  # Weekly bonus
            
            # Add gems to player
            self.add_currency(user_id, 'gems', total_gems)
            
            self.logger.info(f"Daily login reward: {total_gems} gems (Day {streak_day})")
            
        except Exception as e:
            self.logger.error(f"Failed to grant daily rewards: {e}")

    def get_player_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get player data from SQLite"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('SELECT * FROM player_data WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get player data: {e}")
            return None

    def update_player_data(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Update player data in SQLite"""
        try:
            current_time = int(time.time())
            data['updated_at'] = current_time
            
            # Build dynamic UPDATE query
            fields = list(data.keys())
            placeholders = ', '.join([f"{field} = ?" for field in fields])
            values = list(data.values()) + [user_id]
            
            cursor = self.sqlite_conn.cursor()
            cursor.execute(f'''
                UPDATE player_data SET {placeholders}
                WHERE user_id = ?
            ''', values)
            
            self.sqlite_conn.commit()
            
            # Queue for online sync if available
            if self.is_online:
                self._queue_sync('player_data', user_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update player data: {e}")
            return False

    def add_currency(self, user_id: str, currency_type: str, amount: int) -> bool:
        """Add currency to player account"""
        try:
            cursor = self.sqlite_conn.cursor()
            
            if currency_type == 'gold':
                cursor.execute('''
                    UPDATE player_data SET gold = gold + ?, updated_at = ?
                    WHERE user_id = ?
                ''', (amount, int(time.time()), user_id))
            elif currency_type == 'gems':
                cursor.execute('''
                    UPDATE player_data SET gems = gems + ?, updated_at = ?
                    WHERE user_id = ?
                ''', (amount, int(time.time()), user_id))
            else:
                return False
            
            self.sqlite_conn.commit()
            
            if self.is_online:
                self._queue_sync('player_data', user_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add currency: {e}")
            return False

    def add_inventory_item(self, user_id: str, item_type: str, item_id: str, quantity: int = 1) -> bool:
        """Add item to player inventory"""
        try:
            cursor = self.sqlite_conn.cursor()
            current_time = int(time.time())
            
            # Check if item already exists
            cursor.execute('''
                SELECT quantity FROM inventory 
                WHERE user_id = ? AND item_type = ? AND item_id = ?
            ''', (user_id, item_type, item_id))
            
            result = cursor.fetchone()
            
            if result:
                # Update existing item
                cursor.execute('''
                    UPDATE inventory SET quantity = quantity + ?
                    WHERE user_id = ? AND item_type = ? AND item_id = ?
                ''', (quantity, user_id, item_type, item_id))
            else:
                # Insert new item
                cursor.execute('''
                    INSERT INTO inventory 
                    (user_id, item_type, item_id, quantity, acquired_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, item_type, item_id, quantity, current_time))
            
            self.sqlite_conn.commit()
            
            if self.is_online:
                self._queue_sync('inventory', user_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add inventory item: {e}")
            return False

    def get_inventory(self, user_id: str) -> List[Dict[str, Any]]:
        """Get player inventory"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('''
                SELECT * FROM inventory WHERE user_id = ?
                ORDER BY item_type, item_id
            ''', (user_id,))
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Failed to get inventory: {e}")
            return []

    def update_stage_progress(self, user_id: str, world_id: int, stage_id: int, 
                            completed: bool = True, stars: int = 0, time_taken: float = 0) -> bool:
        """Update stage completion progress"""
        try:
            cursor = self.sqlite_conn.cursor()
            current_time = int(time.time())
            
            cursor.execute('''
                INSERT OR REPLACE INTO stage_progress 
                (user_id, world_id, stage_id, completed, stars, best_time, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, world_id, stage_id, completed, stars, time_taken, current_time))
            
            self.sqlite_conn.commit()
            
            if self.is_online:
                self._queue_sync('stage_progress', user_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update stage progress: {e}")
            return False

    def get_stage_progress(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all stage progress for user"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('''
                SELECT * FROM stage_progress WHERE user_id = ?
                ORDER BY world_id, stage_id
            ''', (user_id,))
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Failed to get stage progress: {e}")
            return []

    def _attempt_online_sync(self, user_id: str):
        """Attempt to sync with Firebase"""
        if not self.firestore_db:
            return
        
        try:
            # Check network connectivity (simplified)
            self.is_online = True  # In production, implement actual connectivity check
            
            if self.is_online:
                # Perform bidirectional sync
                self._sync_player_data(user_id)
                self._sync_inventory(user_id)
                self._sync_stage_progress(user_id)
                
                self.last_sync_time = int(time.time())
                self.logger.info("Online sync completed")
                
        except Exception as e:
            self.logger.error(f"Online sync failed: {e}")
            self.is_online = False

    def _sync_player_data(self, user_id: str):
        """Sync player data between SQLite and Firebase"""
        try:
            # Get local data
            local_data = self.get_player_data(user_id)
            if not local_data:
                return
            
            # Get remote data
            remote_doc = self.firestore_db.collection('players').document(user_id).get()
            
            if remote_doc.exists:
                remote_data = remote_doc.to_dict()
                
                # Conflict resolution: use newest timestamp
                local_timestamp = local_data.get('updated_at', 0)
                remote_timestamp = remote_data.get('updated_at', 0)
                
                if remote_timestamp > local_timestamp:
                    # Remote is newer, update local
                    self.update_player_data(user_id, remote_data)
                    self.logger.info("Updated local data from remote")
                elif local_timestamp > remote_timestamp:
                    # Local is newer, update remote
                    self.firestore_db.collection('players').document(user_id).set(local_data)
                    self.logger.info("Updated remote data from local")
            else:
                # No remote data, push local to remote
                self.firestore_db.collection('players').document(user_id).set(local_data)
                self.logger.info("Pushed local data to remote")
                
        except Exception as e:
            self.logger.error(f"Failed to sync player data: {e}")

    def _sync_inventory(self, user_id: str):
        """Sync inventory between SQLite and Firebase"""
        try:
            # Get local inventory
            local_inventory = self.get_inventory(user_id)
            
            # Get remote inventory
            remote_ref = self.firestore_db.collection('inventory').where('user_id', '==', user_id)
            remote_docs = remote_ref.get()
            
            remote_inventory = [doc.to_dict() for doc in remote_docs]
            
            # Simple merge: combine both inventories
            # In production, implement proper conflict resolution
            all_items = {}
            
            # Add local items
            for item in local_inventory:
                key = f"{item['item_type']}_{item['item_id']}"
                all_items[key] = item
            
            # Merge remote items
            for item in remote_inventory:
                key = f"{item['item_type']}_{item['item_id']}"
                if key not in all_items:
                    all_items[key] = item
                    # Add to local database
                    self.add_inventory_item(
                        user_id, item['item_type'], 
                        item['item_id'], item['quantity']
                    )
            
            # Update remote with local changes
            for item in local_inventory:
                doc_id = f"{user_id}_{item['item_type']}_{item['item_id']}"
                self.firestore_db.collection('inventory').document(doc_id).set(item)
                
        except Exception as e:
            self.logger.error(f"Failed to sync inventory: {e}")

    def _sync_stage_progress(self, user_id: str):
        """Sync stage progress between SQLite and Firebase"""
        try:
            # Get local progress
            local_progress = self.get_stage_progress(user_id)
            
            # Update remote with local progress
            for progress in local_progress:
                doc_id = f"{user_id}_{progress['world_id']}_{progress['stage_id']}"
                self.firestore_db.collection('stage_progress').document(doc_id).set(progress)
                
        except Exception as e:
            self.logger.error(f"Failed to sync stage progress: {e}")

    def _queue_sync(self, table_name: str, user_id: str):
        """Queue data for sync when online"""
        try:
            cursor = self.sqlite_conn.cursor()
            current_time = int(time.time())
            
            cursor.execute('''
                INSERT OR REPLACE INTO sync_metadata 
                (user_id, table_name, last_sync)
                VALUES (?, ?, ?)
            ''', (user_id, table_name, current_time))
            
            self.sqlite_conn.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to queue sync: {e}")

    def force_sync(self, user_id: str) -> bool:
        """Force immediate sync with Firebase"""
        if not self.is_online or not self.firestore_db:
            return False
        
        try:
            with self.sync_lock:
                self._sync_player_data(user_id)
                self._sync_inventory(user_id)
                self._sync_stage_progress(user_id)
                
                self.last_sync_time = int(time.time())
                self.logger.info("Force sync completed")
                return True
                
        except Exception as e:
            self.logger.error(f"Force sync failed: {e}")
            return False

    def get_sync_status(self, user_id: str) -> Dict[str, Any]:
        """Get sync status information"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('''
                SELECT table_name, last_sync FROM sync_metadata 
                WHERE user_id = ?
            ''', (user_id,))
            
            results = cursor.fetchall()
            sync_status = {row['table_name']: row['last_sync'] for row in results}
            
            return {
                'is_online': self.is_online,
                'last_sync_time': self.last_sync_time,
                'table_sync_times': sync_status,
                'pending_syncs': len([t for t in sync_status.values() if t > self.last_sync_time])
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get sync status: {e}")
            return {}

    def cleanup(self):
        """Cleanup database connections"""
        try:
            if self.sqlite_conn:
                self.sqlite_conn.close()
                
            self.logger.info("DatabaseManager cleaned up")
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


class MockFirestore:
    """Mock Firestore for development/testing"""
    
    def __init__(self):
        self.data = {}
        
    def collection(self, collection_name):
        return MockCollection(self.data, collection_name)


class MockCollection:
    """Mock Firestore collection"""
    
    def __init__(self, data, collection_name):
        self.data = data
        self.collection_name = collection_name
        
        if collection_name not in self.data:
            self.data[collection_name] = {}
    
    def document(self, doc_id):
        return MockDocument(self.data[self.collection_name], doc_id)
    
    def where(self, field, operator, value):
        return MockQuery(self.data[self.collection_name], field, operator, value)


class MockDocument:
    """Mock Firestore document"""
    
    def __init__(self, collection_data, doc_id):
        self.collection_data = collection_data
        self.doc_id = doc_id
    
    def get(self):
        return MockDocumentSnapshot(self.collection_data, self.doc_id)
    
    def set(self, data):
        self.collection_data[self.doc_id] = data


class MockDocumentSnapshot:
    """Mock Firestore document snapshot"""
    
    def __init__(self, collection_data, doc_id):
        self.collection_data = collection_data
        self.doc_id = doc_id
    
    @property
    def exists(self):
        return self.doc_id in self.collection_data
    
    def to_dict(self):
        return self.collection_data.get(self.doc_id, {})


class MockQuery:
    """Mock Firestore query"""
    
    def __init__(self, collection_data, field, operator, value):
        self.collection_data = collection_data
        self.field = field
        self.operator = operator
        self.value = value
    
    def get(self):
        results = []
        for doc_id, doc_data in self.collection_data.items():
            if self.field in doc_data and doc_data[self.field] == self.value:
                results.append(MockDocumentSnapshot({doc_id: doc_data}, doc_id))
        return results