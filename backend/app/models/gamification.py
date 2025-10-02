"""
Gamification models for Voice-to-App SaaS Platform
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class PointsAwardRequest(BaseModel):
    points: int
    reason: str
    metadata: Optional[Dict[str, Any]] = None


class PointsAwardResponse(BaseModel):
    points_awarded: int
    new_total_points: int
    new_level: int
    level_up: bool
    achievements_unlocked: List[str]


class AchievementUnlockRequest(BaseModel):
    achievement_type: str
    metadata: Optional[Dict[str, Any]] = None


class AchievementUnlockResponse(BaseModel):
    achievement_unlocked: bool
    points_bonus: int
    message: str


class ReferralCreateRequest(BaseModel):
    pass  # No additional data needed


class ReferralCreateResponse(BaseModel):
    referral_code: str
    referral_url: str
    points_per_referral: int


class LeaderboardRequest(BaseModel):
    category: str = "points"  # "points", "apps", "referrals"
    time_period: str = "all"  # "daily", "weekly", "monthly", "all"
    limit: int = 10


class LeaderboardEntry(BaseModel):
    user_id: str
    username: str
    avatar_url: Optional[str] = None
    score: int
    rank: int


class LeaderboardResponse(BaseModel):
    category: str
    time_period: str
    leaderboard: List[LeaderboardEntry]
    total_participants: int


class UserPoints(BaseModel):
    id: str
    user_id: str
    points: int
    reason: str
    metadata: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class UserAchievement(BaseModel):
    id: str
    user_id: str
    achievement_type: str
    achievement_data: Dict[str, Any]
    unlocked_at: datetime

    class Config:
        from_attributes = True


class Referral(BaseModel):
    id: str
    referrer_id: str
    referee_id: str
    referral_code: str
    status: str
    points_awarded: int
    created_at: datetime

    class Config:
        from_attributes = True


class StreakData(BaseModel):
    current_streak: int
    longest_streak: int
    streak_type: str
    last_activity: Optional[datetime] = None
    daily_challenges: List[Dict[str, Any]]
    streak_rewards: List[Dict[str, Any]]


class ShareContent(BaseModel):
    share_url: str
    share_text: str
    share_image: Optional[str] = None


class Reward(BaseModel):
    id: str
    name: str
    description: str
    points_cost: int
    category: str
    is_available: bool
    metadata: Dict[str, Any]


class RewardRedemption(BaseModel):
    reward: Reward
    points_spent: int
    remaining_points: int