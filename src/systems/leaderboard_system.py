"""
Leaderboard System for Kingdom of Aldoria
Handles player rankings, seasonal competitions, and reward distribution
"""

import json
import time
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import math

class LeaderboardType(Enum):
    POWER_LEVEL = "power_level"           # Total player power (level + gear)
    STAGES_COMPLETED = "stages_completed" # Total stages cleared
    BOSS_KILLS = "boss_kills"            # Total boss defeats
    ARENA_WINS = "arena_wins"            # PvP victories
    WEEKLY_POINTS = "weekly_points"      # Weekly activity points
    MONTHLY_POINTS = "monthly_points"    # Monthly activity points

class RewardTier(Enum):
    LEGENDARY = "legendary"    # Rank 1
    DIAMOND = "diamond"       # Ranks 2-5
    PLATINUM = "platinum"     # Ranks 6-20
    GOLD = "gold"            # Ranks 21-50
    SILVER = "silver"        # Ranks 51-100

@dataclass
class LeaderboardEntry:
    user_id: str
    username: str
    rank: int
    score: int
    previous_rank: int
    change: int  # positive = moved up, negative = moved down
    avatar_url: str = ""
    level: int = 1
    title: str = ""
    last_updated: float = 0.0

@dataclass
class LeaderboardReward:
    reward_type: str  # gems, gold, weapon, skin, title
    item_id: Optional[str] = None
    amount: int = 0
    rarity: str = "common"
    description: str = ""

@dataclass
class SeasonInfo:
    season_id: str
    season_name: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    rewards_distributed: bool = False

class LeaderboardManager:
    def __init__(self, database_path: str = "database/leaderboards.db"):
        self.database_path = database_path
        self.logger = logging.getLogger(__name__)
        self.current_season = None
        self._init_database()
        self._load_current_season()
        
        # Reward configurations for different tiers
        self.tier_rewards = {
            RewardTier.LEGENDARY: {
                "gems": 5000,
                "gold": 100000,
                "exclusive_weapon": "legendary_crown_sword",
                "exclusive_skin": "champion_aura",
                "title": "Grand Champion",
                "vip_days": 30
            },
            RewardTier.DIAMOND: {
                "gems": 3000,
                "gold": 75000,
                "weapon": "diamond_victory_blade",
                "skin": "diamond_warrior",
                "title": "Diamond Warrior",
                "vip_days": 14
            },
            RewardTier.PLATINUM: {
                "gems": 1500,
                "gold": 50000,
                "weapon": "platinum_honor_sword",
                "skin": "platinum_guard",
                "title": "Platinum Guard"
            },
            RewardTier.GOLD: {
                "gems": 800,
                "gold": 25000,
                "weapon": "golden_achievement_blade",
                "title": "Golden Warrior"
            },
            RewardTier.SILVER: {
                "gems": 400,
                "gold": 15000,
                "title": "Silver Champion"
            }
        }
    
    def _init_database(self):
        """Initialize leaderboard database tables"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leaderboard_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    leaderboard_type TEXT NOT NULL,
                    season_id TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    rank_position INTEGER DEFAULT 0,
                    previous_rank INTEGER DEFAULT 0,
                    avatar_url TEXT DEFAULT '',
                    level INTEGER DEFAULT 1,
                    title TEXT DEFAULT '',
                    last_updated REAL DEFAULT 0,
                    created_at REAL DEFAULT (strftime('%s', 'now')),
                    UNIQUE(user_id, leaderboard_type, season_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seasons (
                    season_id TEXT PRIMARY KEY,
                    season_name TEXT NOT NULL,
                    start_date REAL NOT NULL,
                    end_date REAL NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    rewards_distributed INTEGER DEFAULT 0,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leaderboard_rewards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    season_id TEXT NOT NULL,
                    leaderboard_type TEXT NOT NULL,
                    rank_achieved INTEGER NOT NULL,
                    tier TEXT NOT NULL,
                    rewards TEXT NOT NULL,  -- JSON string
                    claimed INTEGER DEFAULT 0,
                    claim_date REAL,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS player_stats (
                    user_id TEXT PRIMARY KEY,
                    power_level INTEGER DEFAULT 0,
                    stages_completed INTEGER DEFAULT 0,
                    boss_kills INTEGER DEFAULT 0,
                    arena_wins INTEGER DEFAULT 0,
                    weekly_points INTEGER DEFAULT 0,
                    monthly_points INTEGER DEFAULT 0,
                    last_weekly_reset REAL DEFAULT 0,
                    last_monthly_reset REAL DEFAULT 0,
                    last_updated REAL DEFAULT (strftime('%s', 'now'))
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_leaderboard_score ON leaderboard_entries(leaderboard_type, season_id, score DESC)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_season ON leaderboard_entries(user_id, season_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_rewards_user ON leaderboard_rewards(user_id, claimed)')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize leaderboard database: {e}")
    
    def _load_current_season(self):
        """Load or create the current active season"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Check for active season
            cursor.execute('''
                SELECT season_id, season_name, start_date, end_date, is_active, rewards_distributed
                FROM seasons 
                WHERE is_active = 1 
                ORDER BY start_date DESC 
                LIMIT 1
            ''')
            
            result = cursor.fetchone()
            
            if result:
                season_id, name, start_date, end_date, is_active, rewards_distributed = result
                self.current_season = SeasonInfo(
                    season_id=season_id,
                    season_name=name,
                    start_date=datetime.fromtimestamp(start_date),
                    end_date=datetime.fromtimestamp(end_date),
                    is_active=bool(is_active),
                    rewards_distributed=bool(rewards_distributed)
                )
                
                # Check if season has ended
                if datetime.now() > self.current_season.end_date:
                    self._end_season()
            else:
                # Create new season
                self._create_new_season()
            
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to load current season: {e}")
            self._create_new_season()
    
    def _create_new_season(self):
        """Create a new leaderboard season"""
        try:
            season_id = f"season_{int(time.time())}"
            season_name = f"Season {datetime.now().strftime('%B %Y')}"
            start_date = datetime.now()
            end_date = start_date + timedelta(days=30)  # 30-day seasons
            
            self.current_season = SeasonInfo(
                season_id=season_id,
                season_name=season_name,
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )
            
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Deactivate old seasons
            cursor.execute('UPDATE seasons SET is_active = 0')
            
            # Create new season
            cursor.execute('''
                INSERT INTO seasons (season_id, season_name, start_date, end_date, is_active)
                VALUES (?, ?, ?, ?, 1)
            ''', (season_id, season_name, start_date.timestamp(), end_date.timestamp()))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Created new season: {season_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to create new season: {e}")
    
    def _end_season(self):
        """End the current season and distribute rewards"""
        if not self.current_season or self.current_season.rewards_distributed:
            return
        
        try:
            self.logger.info(f"Ending season: {self.current_season.season_name}")
            
            # Calculate and distribute rewards for all leaderboard types
            for leaderboard_type in LeaderboardType:
                self._distribute_season_rewards(leaderboard_type.value)
            
            # Mark season as ended and rewards distributed
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE seasons 
                SET is_active = 0, rewards_distributed = 1 
                WHERE season_id = ?
            ''', (self.current_season.season_id,))
            
            conn.commit()
            conn.close()
            
            # Create new season
            self._create_new_season()
            
        except Exception as e:
            self.logger.error(f"Failed to end season: {e}")
    
    def update_player_score(self, user_id: str, username: str, leaderboard_type: LeaderboardType, 
                           score_change: int, player_level: int = 1, avatar_url: str = ""):
        """Update a player's score on a specific leaderboard"""
        try:
            if not self.current_season:
                self._create_new_season()
            
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Get current entry
            cursor.execute('''
                SELECT score, rank_position FROM leaderboard_entries
                WHERE user_id = ? AND leaderboard_type = ? AND season_id = ?
            ''', (user_id, leaderboard_type.value, self.current_season.season_id))
            
            result = cursor.fetchone()
            current_score = result[0] if result else 0
            previous_rank = result[1] if result else 0
            
            new_score = max(0, current_score + score_change)
            
            # Update or insert entry
            cursor.execute('''
                INSERT OR REPLACE INTO leaderboard_entries 
                (user_id, username, leaderboard_type, season_id, score, previous_rank, 
                 avatar_url, level, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, leaderboard_type.value, self.current_season.season_id,
                  new_score, previous_rank, avatar_url, player_level, time.time()))
            
            conn.commit()
            
            # Recalculate rankings for this leaderboard
            self._recalculate_rankings(leaderboard_type.value)
            
            conn.close()
            
            self.logger.info(f"Updated {username} score on {leaderboard_type.value}: +{score_change}")
            
        except Exception as e:
            self.logger.error(f"Failed to update player score: {e}")
    
    def _recalculate_rankings(self, leaderboard_type: str):
        """Recalculate all rankings for a specific leaderboard"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Get all entries sorted by score
            cursor.execute('''
                SELECT user_id, score, rank_position FROM leaderboard_entries
                WHERE leaderboard_type = ? AND season_id = ?
                ORDER BY score DESC, last_updated ASC
            ''', (leaderboard_type, self.current_season.season_id))
            
            entries = cursor.fetchall()
            
            # Update rankings
            for rank, (user_id, score, old_rank) in enumerate(entries, 1):
                cursor.execute('''
                    UPDATE leaderboard_entries 
                    SET rank_position = ?, previous_rank = ?
                    WHERE user_id = ? AND leaderboard_type = ? AND season_id = ?
                ''', (rank, old_rank, user_id, leaderboard_type, self.current_season.season_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to recalculate rankings: {e}")
    
    def get_leaderboard(self, leaderboard_type: LeaderboardType, limit: int = 100) -> List[LeaderboardEntry]:
        """Get leaderboard entries for a specific type"""
        try:
            if not self.current_season:
                return []
            
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, username, rank_position, score, previous_rank, 
                       avatar_url, level, title, last_updated
                FROM leaderboard_entries
                WHERE leaderboard_type = ? AND season_id = ?
                ORDER BY rank_position ASC
                LIMIT ?
            ''', (leaderboard_type.value, self.current_season.season_id, limit))
            
            entries = []
            for row in cursor.fetchall():
                user_id, username, rank, score, prev_rank, avatar, level, title, updated = row
                
                # Calculate rank change
                change = prev_rank - rank if prev_rank > 0 else 0
                
                entry = LeaderboardEntry(
                    user_id=user_id,
                    username=username,
                    rank=rank,
                    score=score,
                    previous_rank=prev_rank,
                    change=change,
                    avatar_url=avatar,
                    level=level,
                    title=title,
                    last_updated=updated
                )
                entries.append(entry)
            
            conn.close()
            return entries
            
        except Exception as e:
            self.logger.error(f"Failed to get leaderboard: {e}")
            return []
    
    def get_player_ranking(self, user_id: str, leaderboard_type: LeaderboardType) -> Optional[LeaderboardEntry]:
        """Get a specific player's ranking on a leaderboard"""
        try:
            if not self.current_season:
                return None
            
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, username, rank_position, score, previous_rank, 
                       avatar_url, level, title, last_updated
                FROM leaderboard_entries
                WHERE user_id = ? AND leaderboard_type = ? AND season_id = ?
            ''', (user_id, leaderboard_type.value, self.current_season.season_id))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                user_id, username, rank, score, prev_rank, avatar, level, title, updated = result
                change = prev_rank - rank if prev_rank > 0 else 0
                
                return LeaderboardEntry(
                    user_id=user_id,
                    username=username,
                    rank=rank,
                    score=score,
                    previous_rank=prev_rank,
                    change=change,
                    avatar_url=avatar,
                    level=level,
                    title=title,
                    last_updated=updated
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get player ranking: {e}")
            return None
    
    def _get_reward_tier(self, rank: int) -> RewardTier:
        """Determine reward tier based on ranking"""
        if rank == 1:
            return RewardTier.LEGENDARY
        elif rank <= 5:
            return RewardTier.DIAMOND
        elif rank <= 20:
            return RewardTier.PLATINUM
        elif rank <= 50:
            return RewardTier.GOLD
        elif rank <= 100:
            return RewardTier.SILVER
        else:
            return None
    
    def _calculate_rewards(self, tier: RewardTier, rank: int) -> List[LeaderboardReward]:
        """Calculate rewards for a specific tier and rank"""
        rewards = []
        tier_config = self.tier_rewards[tier]
        
        # Base rewards for all tiers
        if "gems" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="gems",
                amount=tier_config["gems"],
                description=f"Season ranking reward for rank {rank}"
            ))
        
        if "gold" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="gold",
                amount=tier_config["gold"],
                description=f"Season ranking reward for rank {rank}"
            ))
        
        # Tier-specific rewards
        if "exclusive_weapon" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="weapon",
                item_id=tier_config["exclusive_weapon"],
                rarity="legendary",
                description="Exclusive weapon for Grand Champion"
            ))
        elif "weapon" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="weapon",
                item_id=tier_config["weapon"],
                rarity=tier.value,
                description=f"Season ranking weapon for {tier.value} tier"
            ))
        
        if "exclusive_skin" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="skin",
                item_id=tier_config["exclusive_skin"],
                rarity="legendary",
                description="Exclusive skin for Grand Champion"
            ))
        elif "skin" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="skin",
                item_id=tier_config["skin"],
                rarity=tier.value,
                description=f"Season ranking skin for {tier.value} tier"
            ))
        
        if "title" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="title",
                item_id=tier_config["title"],
                description=f"Honorary title for {tier.value} tier achievement"
            ))
        
        if "vip_days" in tier_config:
            rewards.append(LeaderboardReward(
                reward_type="vip_subscription",
                amount=tier_config["vip_days"],
                description=f"VIP subscription for {tier_config['vip_days']} days"
            ))
        
        return rewards
    
    def _distribute_season_rewards(self, leaderboard_type: str):
        """Distribute rewards for top 100 players in a leaderboard"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Get top 100 players
            cursor.execute('''
                SELECT user_id, username, rank_position, score
                FROM leaderboard_entries
                WHERE leaderboard_type = ? AND season_id = ? AND rank_position <= 100
                ORDER BY rank_position ASC
            ''', (leaderboard_type, self.current_season.season_id))
            
            top_players = cursor.fetchall()
            
            for user_id, username, rank, score in top_players:
                tier = self._get_reward_tier(rank)
                if not tier:
                    continue
                
                rewards = self._calculate_rewards(tier, rank)
                rewards_json = json.dumps([asdict(reward) for reward in rewards])
                
                # Store rewards
                cursor.execute('''
                    INSERT INTO leaderboard_rewards 
                    (user_id, season_id, leaderboard_type, rank_achieved, tier, rewards)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, self.current_season.season_id, leaderboard_type, 
                      rank, tier.value, rewards_json))
                
                self.logger.info(f"Distributed {tier.value} rewards to {username} (rank {rank})")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to distribute season rewards: {e}")
    
    def get_player_rewards(self, user_id: str, claimed: Optional[bool] = None) -> List[Dict]:
        """Get rewards for a specific player"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            query = '''
                SELECT id, season_id, leaderboard_type, rank_achieved, tier, rewards, 
                       claimed, claim_date, created_at
                FROM leaderboard_rewards
                WHERE user_id = ?
            '''
            params = [user_id]
            
            if claimed is not None:
                query += ' AND claimed = ?'
                params.append(int(claimed))
            
            query += ' ORDER BY created_at DESC'
            
            cursor.execute(query, params)
            
            rewards_list = []
            for row in cursor.fetchall():
                reward_id, season_id, lb_type, rank, tier, rewards_json, claimed_flag, claim_date, created_at = row
                
                rewards_list.append({
                    'id': reward_id,
                    'season_id': season_id,
                    'leaderboard_type': lb_type,
                    'rank_achieved': rank,
                    'tier': tier,
                    'rewards': json.loads(rewards_json),
                    'claimed': bool(claimed_flag),
                    'claim_date': claim_date,
                    'created_at': created_at
                })
            
            conn.close()
            return rewards_list
            
        except Exception as e:
            self.logger.error(f"Failed to get player rewards: {e}")
            return []
    
    def claim_rewards(self, user_id: str, reward_id: int) -> bool:
        """Claim rewards for a player"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Check if rewards exist and are unclaimed
            cursor.execute('''
                SELECT rewards, claimed FROM leaderboard_rewards
                WHERE id = ? AND user_id = ?
            ''', (reward_id, user_id))
            
            result = cursor.fetchone()
            if not result or result[1]:  # Doesn't exist or already claimed
                conn.close()
                return False
            
            # Mark as claimed
            cursor.execute('''
                UPDATE leaderboard_rewards 
                SET claimed = 1, claim_date = ?
                WHERE id = ? AND user_id = ?
            ''', (time.time(), reward_id, user_id))
            
            conn.commit()
            conn.close()
            
            # TODO: Apply rewards to player inventory/stats
            rewards = json.loads(result[0])
            self._apply_rewards_to_player(user_id, rewards)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to claim rewards: {e}")
            return False
    
    def _apply_rewards_to_player(self, user_id: str, rewards: List[Dict]):
        """Apply claimed rewards to player account"""
        # This would integrate with the main game's player system
        # For now, just log the rewards that should be applied
        for reward in rewards:
            self.logger.info(f"Applied reward to {user_id}: {reward}")
    
    def get_season_info(self) -> Optional[SeasonInfo]:
        """Get current season information"""
        return self.current_season
    
    def force_season_end(self) -> bool:
        """Force end current season (admin function)"""
        try:
            if self.current_season:
                self._end_season()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to force season end: {e}")
            return False
    
    def get_leaderboard_stats(self) -> Dict[str, Any]:
        """Get overall leaderboard statistics"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Get player counts per leaderboard
            for lb_type in LeaderboardType:
                cursor.execute('''
                    SELECT COUNT(*) FROM leaderboard_entries
                    WHERE leaderboard_type = ? AND season_id = ?
                ''', (lb_type.value, self.current_season.season_id if self.current_season else ""))
                
                count = cursor.fetchone()[0]
                stats[f"{lb_type.value}_players"] = count
            
            # Get total rewards distributed
            cursor.execute('SELECT COUNT(*) FROM leaderboard_rewards WHERE claimed = 1')
            stats['rewards_claimed'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM leaderboard_rewards WHERE claimed = 0')
            stats['rewards_pending'] = cursor.fetchone()[0]
            
            # Get season count
            cursor.execute('SELECT COUNT(*) FROM seasons')
            stats['total_seasons'] = cursor.fetchone()[0]
            
            conn.close()
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get leaderboard stats: {e}")
            return {}

# Example usage and testing
if __name__ == "__main__":
    # Initialize leaderboard manager
    lb_manager = LeaderboardManager()
    
    # Example: Update player scores
    lb_manager.update_player_score("player1", "TestPlayer1", LeaderboardType.POWER_LEVEL, 100, 15)
    lb_manager.update_player_score("player2", "TestPlayer2", LeaderboardType.POWER_LEVEL, 150, 12)
    lb_manager.update_player_score("player3", "TestPlayer3", LeaderboardType.POWER_LEVEL, 120, 18)
    
    # Get leaderboard
    leaderboard = lb_manager.get_leaderboard(LeaderboardType.POWER_LEVEL, 10)
    for entry in leaderboard:
        print(f"Rank {entry.rank}: {entry.username} - {entry.score} points (Change: {entry.change:+d})")
    
    # Get player ranking
    player_rank = lb_manager.get_player_ranking("player1", LeaderboardType.POWER_LEVEL)
    if player_rank:
        print(f"\nPlayer1 ranking: {player_rank.rank} with {player_rank.score} points")
    
    # Get season info
    season = lb_manager.get_season_info()
    if season:
        print(f"\nCurrent season: {season.season_name}")
        print(f"End date: {season.end_date}")
    
    # Get stats
    stats = lb_manager.get_leaderboard_stats()
    print(f"\nLeaderboard stats: {stats}")