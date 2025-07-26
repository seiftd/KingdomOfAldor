"""
Ad Competition System
Handles daily, weekly, and monthly ad competitions with separate tracking from regular ads
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class CompetitionType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

@dataclass
class CompetitionEntry:
    user_id: str
    ads_watched: int
    last_ad_timestamp: float
    weight_multiplier: float  # Based on consistency and frequency

@dataclass
class CompetitionReward:
    type: str  # "weapon", "gems", "vip_subscription"
    item_id: Optional[str] = None
    amount: Optional[int] = None
    level: Optional[int] = None
    duration_days: Optional[int] = None

class AdCompetitionManager:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.competitions = {
            CompetitionType.DAILY: {
                "ads_required": 10,
                "reset_hours": 24,
                "winners": 1,
                "rewards": [
                    CompetitionReward("weapon", "silver_sword"),
                    CompetitionReward("weapon", "silver_bow"), 
                    CompetitionReward("weapon", "silver_staff")
                ]
            },
            CompetitionType.WEEKLY: {
                "ads_required": 30,
                "reset_hours": 168,  # 7 days
                "winners": 3,
                "rewards": [
                    CompetitionReward("weapon", "golden_sword"),
                    CompetitionReward("weapon", "golden_bow"),
                    CompetitionReward("weapon", "golden_staff"),
                    CompetitionReward("weapon", "golden_hammer")
                ]
            },
            CompetitionType.MONTHLY: {
                "ads_required": 100,
                "reset_hours": 720,  # 30 days
                "winners": 5,
                "rewards": {
                    1: [  # 1st place
                        CompetitionReward("vip_subscription", duration_days=30),
                        CompetitionReward("gems", amount=3000)
                    ],
                    2: [  # 2nd-5th place
                        CompetitionReward("weapon", "golden_sword", level=60),
                        CompetitionReward("gems", amount=2000)
                    ]
                }
            }
        }
        
    def log_competition_ad_view(self, user_id: str) -> Dict:
        """Log an ad view for competitions (separate from regular ads)"""
        current_time = time.time()
        competition_data = self.save_manager.get_player_data('competitions') or {}
        
        # Initialize if needed
        if user_id not in competition_data:
            competition_data[user_id] = {
                "daily": {"ads_watched": 0, "last_reset": current_time, "entries": []},
                "weekly": {"ads_watched": 0, "last_reset": current_time, "entries": []}, 
                "monthly": {"ads_watched": 0, "last_reset": current_time, "entries": []}
            }
        
        user_data = competition_data[user_id]
        results = {}
        
        # Update each competition type
        for comp_type in CompetitionType:
            comp_key = comp_type.value
            comp_config = self.competitions[comp_type]
            
            # Check if reset is needed
            if self._should_reset_competition(user_data[comp_key]["last_reset"], comp_config["reset_hours"]):
                user_data[comp_key] = {
                    "ads_watched": 0,
                    "last_reset": current_time,
                    "entries": []
                }
            
            # Increment ad count
            user_data[comp_key]["ads_watched"] += 1
            user_data[comp_key]["entries"].append(current_time)
            
            # Calculate weight multiplier based on consistency
            weight = self._calculate_weight_multiplier(user_data[comp_key]["entries"], comp_config["reset_hours"])
            
            # Check if eligible for competition
            ads_watched = user_data[comp_key]["ads_watched"]
            if ads_watched >= comp_config["ads_required"]:
                results[comp_key] = {
                    "eligible": True,
                    "ads_watched": ads_watched,
                    "weight": weight,
                    "requirement": comp_config["ads_required"]
                }
            else:
                results[comp_key] = {
                    "eligible": False,
                    "ads_watched": ads_watched,
                    "remaining": comp_config["ads_required"] - ads_watched,
                    "requirement": comp_config["ads_required"]
                }
        
        # Save updated data
        self.save_manager.set_player_data('competitions', competition_data)
        
        return {
            "success": True,
            "timestamp": current_time,
            "competitions": results
        }
    
    def _should_reset_competition(self, last_reset: float, reset_hours: int) -> bool:
        """Check if competition period has ended"""
        return time.time() - last_reset >= (reset_hours * 3600)
    
    def _calculate_weight_multiplier(self, entries: List[float], period_hours: int) -> float:
        """Calculate weight multiplier based on ad watching consistency"""
        if not entries:
            return 1.0
        
        current_time = time.time()
        period_seconds = period_hours * 3600
        
        # Filter entries within current period
        recent_entries = [e for e in entries if current_time - e <= period_seconds]
        
        if len(recent_entries) < 2:
            return 1.0
        
        # Calculate consistency score based on distribution
        time_gaps = []
        for i in range(1, len(recent_entries)):
            gap = recent_entries[i] - recent_entries[i-1]
            time_gaps.append(gap)
        
        # Reward consistent watching (smaller gaps = higher weight)
        avg_gap = sum(time_gaps) / len(time_gaps)
        ideal_gap = period_seconds / len(recent_entries)
        
        # Weight formula: more consistent = higher weight (max 2.0x)
        consistency_ratio = min(ideal_gap / avg_gap, 2.0) if avg_gap > 0 else 1.0
        
        # Frequency bonus: more ads = slight weight increase
        frequency_bonus = min(len(recent_entries) / 50.0, 0.5)  # Max 0.5 bonus
        
        return min(1.0 + frequency_bonus + (consistency_ratio - 1.0) * 0.5, 2.0)
    
    def conduct_competition_drawing(self, competition_type: CompetitionType) -> Dict:
        """Conduct drawing for specified competition type"""
        comp_config = self.competitions[competition_type]
        competition_data = self.save_manager.get_player_data('competitions') or {}
        
        # Get all eligible participants
        eligible_participants = []
        comp_key = competition_type.value
        
        for user_id, user_data in competition_data.items():
            if comp_key in user_data:
                comp_data = user_data[comp_key]
                if comp_data["ads_watched"] >= comp_config["ads_required"]:
                    weight = self._calculate_weight_multiplier(
                        comp_data["entries"], 
                        comp_config["reset_hours"]
                    )
                    eligible_participants.append(
                        CompetitionEntry(user_id, comp_data["ads_watched"], 
                                      comp_data.get("last_ad_timestamp", 0), weight)
                    )
        
        if not eligible_participants:
            return {"success": False, "message": "No eligible participants"}
        
        # Weighted random selection
        winners = self._select_winners(eligible_participants, comp_config["winners"])
        
        # Distribute rewards
        reward_results = []
        for i, winner in enumerate(winners):
            if competition_type == CompetitionType.MONTHLY:
                # Special monthly rewards
                place = i + 1
                if place == 1:
                    rewards = comp_config["rewards"][1]
                else:
                    rewards = comp_config["rewards"][2]
            else:
                # Daily/Weekly rewards
                rewards = [random.choice(comp_config["rewards"])]
            
            # Apply rewards to winner
            for reward in rewards:
                self._apply_reward(winner.user_id, reward)
                reward_results.append({
                    "user_id": winner.user_id,
                    "place": i + 1,
                    "reward": reward.__dict__
                })
        
        # Reset competition for all participants
        self._reset_competition(competition_type)
        
        # Send notifications
        self._send_competition_notifications(competition_type, reward_results)
        
        return {
            "success": True,
            "competition_type": competition_type.value,
            "total_participants": len(eligible_participants),
            "winners": reward_results
        }
    
    def _select_winners(self, participants: List[CompetitionEntry], num_winners: int) -> List[CompetitionEntry]:
        """Select winners using weighted random selection"""
        if len(participants) <= num_winners:
            return participants
        
        # Create weighted list
        weighted_choices = []
        for participant in participants:
            # Weight includes base ads watched + consistency multiplier
            weight = participant.ads_watched * participant.weight_multiplier
            weighted_choices.extend([participant] * int(weight * 10))  # Scale for selection
        
        # Select unique winners
        winners = []
        remaining_choices = weighted_choices.copy()
        
        for _ in range(num_winners):
            if not remaining_choices:
                break
                
            winner = random.choice(remaining_choices)
            if winner not in winners:
                winners.append(winner)
                # Remove all instances of this winner
                remaining_choices = [p for p in remaining_choices if p.user_id != winner.user_id]
        
        return winners
    
    def _apply_reward(self, user_id: str, reward: CompetitionReward):
        """Apply reward to user account"""
        if reward.type == "weapon":
            weapons = self.save_manager.get_player_data('inventory.weapons') or []
            if reward.item_id not in weapons:
                weapons.append(reward.item_id)
                self.save_manager.set_player_data('inventory.weapons', weapons)
            
            # If weapon has a level specified, set it
            if reward.level:
                weapon_levels = self.save_manager.get_player_data('weapon_levels') or {}
                weapon_levels[reward.item_id] = reward.level
                self.save_manager.set_player_data('weapon_levels', weapon_levels)
        
        elif reward.type == "gems":
            current_gems = self.save_manager.get_player_data('currency.gems') or 0
            self.save_manager.set_player_data('currency.gems', current_gems + reward.amount)
        
        elif reward.type == "vip_subscription":
            vip_data = self.save_manager.get_player_data('vip') or {}
            current_time = time.time()
            expiry = vip_data.get('expiry', current_time)
            
            # Extend VIP subscription
            new_expiry = max(expiry, current_time) + (reward.duration_days * 24 * 3600)
            vip_data.update({
                'active': True,
                'expiry': new_expiry,
                'tier': 'premium'
            })
            self.save_manager.set_player_data('vip', vip_data)
    
    def _reset_competition(self, competition_type: CompetitionType):
        """Reset competition data for all users"""
        competition_data = self.save_manager.get_player_data('competitions') or {}
        comp_key = competition_type.value
        current_time = time.time()
        
        for user_id in competition_data:
            if comp_key in competition_data[user_id]:
                competition_data[user_id][comp_key] = {
                    "ads_watched": 0,
                    "last_reset": current_time,
                    "entries": []
                }
        
        self.save_manager.set_player_data('competitions', competition_data)
    
    def _send_competition_notifications(self, competition_type: CompetitionType, results: List[Dict]):
        """Send in-game email notifications to winners"""
        for result in results:
            notification = {
                "id": f"comp_{competition_type.value}_{int(time.time())}_{result['user_id']}",
                "type": "competition_reward",
                "title": f"{competition_type.value.title()} Competition Winner!",
                "message": f"Congratulations! You placed #{result['place']} in the {competition_type.value} ad competition!",
                "rewards": [result['reward']],
                "timestamp": time.time(),
                "read": False
            }
            
            # Add to user's inbox
            user_notifications = self.save_manager.get_player_data(f'notifications.{result["user_id"]}') or []
            user_notifications.append(notification)
            self.save_manager.set_player_data(f'notifications.{result["user_id"]}', user_notifications)
    
    def get_competition_status(self, user_id: str) -> Dict:
        """Get current competition status for user"""
        competition_data = self.save_manager.get_player_data('competitions') or {}
        user_data = competition_data.get(user_id, {})
        
        status = {}
        current_time = time.time()
        
        for comp_type in CompetitionType:
            comp_key = comp_type.value
            comp_config = self.competitions[comp_type]
            
            if comp_key in user_data:
                comp_data = user_data[comp_key]
                time_since_reset = current_time - comp_data["last_reset"]
                time_remaining = (comp_config["reset_hours"] * 3600) - time_since_reset
                
                status[comp_key] = {
                    "ads_watched": comp_data["ads_watched"],
                    "ads_required": comp_config["ads_required"],
                    "eligible": comp_data["ads_watched"] >= comp_config["ads_required"],
                    "time_remaining": max(0, time_remaining),
                    "weight_multiplier": self._calculate_weight_multiplier(
                        comp_data["entries"], comp_config["reset_hours"]
                    )
                }
            else:
                status[comp_key] = {
                    "ads_watched": 0,
                    "ads_required": comp_config["ads_required"],
                    "eligible": False,
                    "time_remaining": comp_config["reset_hours"] * 3600,
                    "weight_multiplier": 1.0
                }
        
        return status
    
    def schedule_competition_drawings(self):
        """Schedule automatic competition drawings (called by game scheduler)"""
        current_time = datetime.now()
        
        # Daily: Run at 23:59
        if current_time.hour == 23 and current_time.minute == 59:
            self.conduct_competition_drawing(CompetitionType.DAILY)
        
        # Weekly: Run Sunday at 23:59
        if current_time.weekday() == 6 and current_time.hour == 23 and current_time.minute == 59:
            self.conduct_competition_drawing(CompetitionType.WEEKLY)
        
        # Monthly: Run last day of month at 23:59
        next_month = current_time.replace(day=28) + timedelta(days=4)
        last_day = (next_month - timedelta(days=next_month.day)).day
        if current_time.day == last_day and current_time.hour == 23 and current_time.minute == 59:
            self.conduct_competition_drawing(CompetitionType.MONTHLY)