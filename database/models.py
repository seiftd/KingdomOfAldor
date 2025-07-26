"""
Database Models for Kingdom of Aldoria
Supports both online (SQLite/PostgreSQL) and offline (JSON) storage
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, 
    ForeignKey, Table, JSON, BigInteger
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional, Any

Base = declarative_base()

# Association tables for many-to-many relationships
user_weapons = Table(
    'user_weapons',
    Base.metadata,
    Column('user_id', String(50), ForeignKey('users.id')),
    Column('weapon_id', String(50), ForeignKey('weapons.id')),
    Column('level', Integer, default=1),
    Column('acquired_date', DateTime, default=datetime.utcnow)
)

user_heroes = Table(
    'user_heroes',
    Base.metadata,
    Column('user_id', String(50), ForeignKey('users.id')),
    Column('hero_id', String(50), ForeignKey('heroes.id')),
    Column('level', Integer, default=1),
    Column('acquired_date', DateTime, default=datetime.utcnow)
)

user_skins = Table(
    'user_skins',
    Base.metadata,
    Column('user_id', String(50), ForeignKey('users.id')),
    Column('skin_id', String(50), ForeignKey('skins.id')),
    Column('acquired_date', DateTime, default=datetime.utcnow)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(50), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Game stats
    level = Column(Integer, default=1)
    experience = Column(BigInteger, default=0)
    gold = Column(BigInteger, default=100)
    gems = Column(Integer, default=10)
    
    # Player stats
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)
    speed = Column(Integer, default=8)
    
    # Progress
    current_world = Column(Integer, default=0)
    current_stage = Column(Integer, default=1)
    worlds_unlocked = Column(Integer, default=1)
    stages_completed = Column(Integer, default=0)
    bosses_defeated = Column(Integer, default=0)
    
    # Current equipment
    current_weapon_id = Column(String(50), ForeignKey('weapons.id'))
    current_hero_id = Column(String(50), ForeignKey('heroes.id'))
    current_skin_id = Column(String(50), ForeignKey('skins.id'))
    
    # Stamina
    current_stamina = Column(Integer, default=100)
    max_stamina = Column(Integer, default=100)
    last_stamina_recharge = Column(DateTime, default=datetime.utcnow)
    
    # VIP status
    vip_active = Column(Boolean, default=False)
    vip_tier = Column(String(20), default='none')
    vip_expiry = Column(DateTime, nullable=True)
    
    # Ad tracking
    total_ads_watched = Column(Integer, default=0)
    last_ad_timestamp = Column(DateTime, nullable=True)
    
    # Session tracking
    last_login = Column(DateTime, default=datetime.utcnow)
    session_start = Column(DateTime, nullable=True)
    total_playtime = Column(Integer, default=0)  # in seconds
    
    # Account details
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    weapons = relationship("Weapon", secondary=user_weapons, back_populates="owners")
    heroes = relationship("Hero", secondary=user_heroes, back_populates="owners")
    skins = relationship("Skin", secondary=user_skins, back_populates="owners")
    
    current_weapon = relationship("Weapon", foreign_keys=[current_weapon_id])
    current_hero = relationship("Hero", foreign_keys=[current_hero_id])
    current_skin = relationship("Skin", foreign_keys=[current_skin_id])
    
    competitions = relationship("CompetitionEntry", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class Weapon(Base):
    __tablename__ = 'weapons'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    weapon_type = Column(String(20), nullable=False)  # sword, bow, staff, etc.
    
    # Base stats
    attack_bonus = Column(Integer, default=0)
    defense_bonus = Column(Integer, default=0)
    crit_chance = Column(Float, default=0.0)
    crit_damage = Column(Float, default=0.0)
    
    # Special attributes (stored as JSON)
    special_attributes = Column(JSON)
    
    # Acquisition
    acquisition_method = Column(String(50), nullable=False)  # store, event, money, etc.
    unlock_level = Column(Integer, default=1)
    cost = Column(Float, default=0)
    currency_type = Column(String(20), default='gold')  # gold, gems, usd
    
    # Metadata
    rarity = Column(String(20), default='Common')
    rank = Column(String(20), default='Wood')
    max_level = Column(Integer, default=120)
    sprite_path = Column(String(200))
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    owners = relationship("User", secondary=user_weapons, back_populates="weapons")

class Hero(Base):
    __tablename__ = 'heroes'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    hero_class = Column(String(20), nullable=False)  # knight, mage, archer, etc.
    
    # Base stats
    base_attack = Column(Integer, default=10)
    base_defense = Column(Integer, default=5)
    base_speed = Column(Integer, default=8)
    base_health = Column(Integer, default=100)
    base_mana = Column(Integer, default=50)
    
    # Special abilities (stored as JSON)
    abilities = Column(JSON)
    
    # Acquisition
    acquisition_method = Column(String(50), nullable=False)
    cost = Column(Float, default=0)
    currency_type = Column(String(20), default='gems')
    
    # Metadata
    rarity = Column(String(20), default='Common')
    unlock_level = Column(Integer, default=1)
    sprite_path = Column(String(200))
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    owners = relationship("User", secondary=user_heroes, back_populates="heroes")
    compatible_skins = relationship("Skin", back_populates="hero")

class Skin(Base):
    __tablename__ = 'skins'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Associated hero
    hero_id = Column(String(50), ForeignKey('heroes.id'))
    
    # Effects
    stat_bonuses = Column(JSON)  # Additional stats
    visual_effects = Column(JSON)  # Visual enhancements
    
    # Acquisition
    acquisition_method = Column(String(50), nullable=False)  # vip, gems, event
    cost = Column(Float, default=0)
    currency_type = Column(String(20), default='gems')
    vip_required = Column(Boolean, default=False)
    
    # Metadata
    rarity = Column(String(20), default='Common')
    sprite_path = Column(String(200))
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    hero = relationship("Hero", back_populates="compatible_skins")
    owners = relationship("User", secondary=user_skins, back_populates="skins")

class CompetitionEntry(Base):
    __tablename__ = 'competition_entries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    competition_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    
    # Progress tracking
    ads_watched = Column(Integer, default=0)
    entries = Column(JSON)  # List of timestamps
    weight_multiplier = Column(Float, default=1.0)
    
    # Period tracking
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    is_eligible = Column(Boolean, default=False)
    
    # Results
    is_winner = Column(Boolean, default=False)
    placement = Column(Integer, nullable=True)
    rewards_claimed = Column(Boolean, default=False)
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="competitions")

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    event_type = Column(String(50), nullable=False)  # competition, special, seasonal
    
    # Timing
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Requirements and rewards
    requirements = Column(JSON)  # What players need to do
    rewards = Column(JSON)  # What they can win
    
    # Configuration
    max_participants = Column(Integer, nullable=True)
    current_participants = Column(Integer, default=0)
    
    # System
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(50))  # Admin who created it

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    
    # Content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # reward, competition, system
    
    # Rewards (if applicable)
    rewards = Column(JSON)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_claimed = Column(Boolean, default=False)
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    
    # Transaction details
    transaction_type = Column(String(50), nullable=False)  # purchase, reward, refund
    item_type = Column(String(50), nullable=False)  # weapon, hero, skin, gems, vip
    item_id = Column(String(50), nullable=True)
    
    # Payment
    amount = Column(Float, nullable=False)
    currency = Column(String(20), nullable=False)  # usd, gems, gold
    payment_method = Column(String(50), nullable=True)  # stripe, paypal, etc.
    
    # Status
    status = Column(String(20), default='pending')  # pending, completed, failed, refunded
    external_transaction_id = Column(String(100), nullable=True)
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")

class AdminLog(Base):
    __tablename__ = 'admin_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    target_type = Column(String(50), nullable=True)  # user, weapon, event, etc.
    target_id = Column(String(50), nullable=True)
    
    # Details
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    reason = Column(Text, nullable=True)
    
    # System
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)

class GameStats(Base):
    __tablename__ = 'game_stats'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Daily aggregates
    date = Column(DateTime, nullable=False)
    active_users = Column(Integer, default=0)
    new_registrations = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    total_playtime = Column(Integer, default=0)  # in seconds
    
    # Revenue
    total_revenue = Column(Float, default=0.0)
    gem_purchases = Column(Integer, default=0)
    vip_subscriptions = Column(Integer, default=0)
    
    # Engagement
    ads_watched = Column(Integer, default=0)
    competitions_entered = Column(Integer, default=0)
    weapons_acquired = Column(Integer, default=0)
    heroes_acquired = Column(Integer, default=0)

# Database Manager Class
class DatabaseManager:
    def __init__(self, db_url: str = None, offline_mode: bool = False):
        self.offline_mode = offline_mode
        self.offline_data_path = "database/offline_data"
        
        if offline_mode:
            self._init_offline_storage()
        else:
            self.db_url = db_url or "sqlite:///database/game.db"
            self.engine = create_engine(self.db_url)
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
    
    def _init_offline_storage(self):
        """Initialize offline JSON storage"""
        os.makedirs(self.offline_data_path, exist_ok=True)
        
        # Create default JSON files
        default_files = {
            'users.json': {},
            'weapons.json': {},
            'heroes.json': {},
            'skins.json': {},
            'competitions.json': {},
            'events.json': {},
            'notifications.json': {},
            'transactions.json': {},
            'admin_logs.json': [],
            'game_stats.json': {}
        }
        
        for filename, default_content in default_files.items():
            filepath = os.path.join(self.offline_data_path, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    json.dump(default_content, f, indent=2)
    
    def _load_offline_data(self, table_name: str) -> Dict:
        """Load data from offline JSON file"""
        filepath = os.path.join(self.offline_data_path, f"{table_name}.json")
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_offline_data(self, table_name: str, data: Dict):
        """Save data to offline JSON file"""
        filepath = os.path.join(self.offline_data_path, f"{table_name}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        if self.offline_mode:
            users = self._load_offline_data('users')
            return users.get(user_id)
        else:
            user = self.session.query(User).filter_by(id=user_id).first()
            return user.__dict__ if user else None
    
    def create_user(self, user_data: Dict) -> bool:
        """Create new user"""
        try:
            if self.offline_mode:
                users = self._load_offline_data('users')
                users[user_data['id']] = user_data
                self._save_offline_data('users', users)
            else:
                user = User(**user_data)
                self.session.add(user)
                self.session.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def update_user(self, user_id: str, updates: Dict) -> bool:
        """Update user data"""
        try:
            if self.offline_mode:
                users = self._load_offline_data('users')
                if user_id in users:
                    users[user_id].update(updates)
                    users[user_id]['updated_at'] = datetime.utcnow().isoformat()
                    self._save_offline_data('users', users)
                    return True
                return False
            else:
                user = self.session.query(User).filter_by(id=user_id).first()
                if user:
                    for key, value in updates.items():
                        setattr(user, key, value)
                    self.session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def sync_to_online(self) -> bool:
        """Sync offline data to online database"""
        if not self.offline_mode:
            return False
        
        try:
            # Load all offline data
            users = self._load_offline_data('users')
            
            # Create online connection
            online_db = DatabaseManager(offline_mode=False)
            
            # Sync users
            for user_id, user_data in users.items():
                existing_user = online_db.get_user(user_id)
                if existing_user:
                    online_db.update_user(user_id, user_data)
                else:
                    online_db.create_user(user_data)
            
            return True
        except Exception as e:
            print(f"Error syncing to online: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if not self.offline_mode and hasattr(self, 'session'):
            self.session.close()