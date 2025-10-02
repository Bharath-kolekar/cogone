"""
Gamification router for Voice-to-App SaaS Platform
Handles points, levels, achievements, referrals, and viral features
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import structlog
from datetime import datetime

from app.core.config import settings
from app.services.gamification_service import GamificationService
from app.services.referral_service import ReferralService
from app.routers.auth import AuthDependencies
from app.models.user import User
from app.models.gamification import (
    PointsAwardRequest,
    PointsAwardResponse,
    AchievementUnlockRequest,
    AchievementUnlockResponse,
    ReferralCreateRequest,
    ReferralCreateResponse,
    LeaderboardRequest,
    LeaderboardResponse,
)

logger = structlog.get_logger()
router = APIRouter()


class GamificationDependencies:
    """Gamification dependencies"""
    
    @staticmethod
    async def check_gamification_enabled() -> bool:
        """Check if gamification is enabled"""
        if not settings.ENABLE_GAMIFICATION:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gamification is disabled"
            )
        return True


@router.post("/points/award", response_model=PointsAwardResponse)
async def award_points(
    request: PointsAwardRequest,
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Award points to user for specific actions"""
    try:
        gamification_service = GamificationService()
        
        # Award points
        result = await gamification_service.award_points(
            user_id=current_user.id,
            points=request.points,
            reason=request.reason,
            metadata=request.metadata
        )
        
        logger.info(
            "Points awarded",
            user_id=current_user.id,
            points=request.points,
            reason=request.reason,
            new_total=result.new_total_points,
            new_level=result.new_level
        )
        
        return PointsAwardResponse(
            points_awarded=request.points,
            new_total_points=result.new_total_points,
            new_level=result.new_level,
            level_up=result.level_up,
            achievements_unlocked=result.achievements_unlocked
        )
        
    except Exception as e:
        logger.error("Points awarding failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/points/balance")
async def get_points_balance(
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Get user's current points balance and level"""
    try:
        gamification_service = GamificationService()
        balance = await gamification_service.get_user_points_balance(current_user.id)
        
        return {
            "points": balance.points,
            "level": balance.level,
            "points_to_next_level": balance.points_to_next_level,
            "level_progress_percentage": balance.level_progress_percentage,
            "total_points_earned": balance.total_points_earned
        }
        
    except Exception as e:
        logger.error("Failed to get points balance", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/achievements")
async def get_user_achievements(
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Get user's achievements"""
    try:
        gamification_service = GamificationService()
        achievements = await gamification_service.get_user_achievements(current_user.id)
        
        return {
            "achievements": achievements,
            "total_unlocked": len([a for a in achievements if a.unlocked]),
            "total_available": len(achievements)
        }
        
    except Exception as e:
        logger.error("Failed to get achievements", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/achievements/unlock", response_model=AchievementUnlockResponse)
async def unlock_achievement(
    request: AchievementUnlockRequest,
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Manually unlock achievement (admin only)"""
    try:
        gamification_service = GamificationService()
        
        # Check if user is admin
        if current_user.subscription_tier != "enterprise":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only enterprise users can manually unlock achievements"
            )
        
        result = await gamification_service.unlock_achievement(
            user_id=current_user.id,
            achievement_type=request.achievement_type,
            metadata=request.metadata
        )
        
        logger.info(
            "Achievement unlocked",
            user_id=current_user.id,
            achievement_type=request.achievement_type
        )
        
        return AchievementUnlockResponse(
            achievement_unlocked=result.achievement_unlocked,
            points_bonus=result.points_bonus,
            message=result.message
        )
        
    except Exception as e:
        logger.error("Achievement unlock failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/referrals/create", response_model=ReferralCreateResponse)
async def create_referral(
    request: ReferralCreateRequest,
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Create referral code for user"""
    try:
        if not settings.ENABLE_REFERRALS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Referrals are disabled"
            )
        
        referral_service = ReferralService()
        
        # Create referral code
        referral_code = await referral_service.create_referral_code(current_user.id)
        
        logger.info(
            "Referral code created",
            user_id=current_user.id,
            referral_code=referral_code
        )
        
        return ReferralCreateResponse(
            referral_code=referral_code,
            referral_url=f"{settings.NEXT_PUBLIC_APP_URL}/signup?ref={referral_code}",
            points_per_referral=settings.POINTS_PER_REFERRAL
        )
        
    except Exception as e:
        logger.error("Referral creation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/referrals/use")
async def use_referral_code(
    referral_code: str,
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Use referral code during signup"""
    try:
        if not settings.ENABLE_REFERRALS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Referrals are disabled"
            )
        
        referral_service = ReferralService()
        
        # Use referral code
        result = await referral_service.use_referral_code(
            referral_code=referral_code,
            referee_id=current_user.id
        )
        
        logger.info(
            "Referral code used",
            referral_code=referral_code,
            referrer_id=result.referrer_id,
            referee_id=current_user.id
        )
        
        return {
            "success": True,
            "referrer_id": result.referrer_id,
            "points_awarded": settings.POINTS_PER_REFERRAL,
            "message": "Referral code applied successfully"
        }
        
    except Exception as e:
        logger.error("Referral code usage failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/referrals/stats")
async def get_referral_stats(
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Get user's referral statistics"""
    try:
        if not settings.ENABLE_REFERRALS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Referrals are disabled"
            )
        
        referral_service = ReferralService()
        stats = await referral_service.get_referral_stats(current_user.id)
        
        return {
            "referral_code": stats.referral_code,
            "total_referrals": stats.total_referrals,
            "successful_referrals": stats.successful_referrals,
            "total_points_earned": stats.total_points_earned,
            "recent_referrals": stats.recent_referrals
        }
        
    except Exception as e:
        logger.error("Failed to get referral stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    request: LeaderboardRequest,
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Get leaderboard for different categories"""
    try:
        gamification_service = GamificationService()
        
        leaderboard = await gamification_service.get_leaderboard(
            category=request.category,
            time_period=request.time_period,
            limit=request.limit
        )
        
        return LeaderboardResponse(
            category=request.category,
            time_period=request.time_period,
            leaderboard=leaderboard,
            total_participants=len(leaderboard)
        )
        
    except Exception as e:
        logger.error("Failed to get leaderboard", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/streaks")
async def get_user_streaks(
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Get user's streaks and daily challenges"""
    try:
        gamification_service = GamificationService()
        streaks = await gamification_service.get_user_streaks(current_user.id)
        
        return {
            "current_streak": streaks.current_streak,
            "longest_streak": streaks.longest_streak,
            "streak_type": streaks.streak_type,
            "last_activity": streaks.last_activity,
            "daily_challenges": streaks.daily_challenges,
            "streak_rewards": streaks.streak_rewards
        }
        
    except Exception as e:
        logger.error("Failed to get streaks", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/share")
async def share_achievement(
    achievement_id: str,
    platform: str,
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Share achievement on social media and earn points"""
    try:
        gamification_service = GamificationService()
        
        # Award points for sharing
        result = await gamification_service.award_points(
            user_id=current_user.id,
            points=settings.POINTS_PER_SHARE,
            reason="social_share",
            metadata={"achievement_id": achievement_id, "platform": platform}
        )
        
        # Generate shareable content
        share_content = await gamification_service.generate_share_content(
            user_id=current_user.id,
            achievement_id=achievement_id,
            platform=platform
        )
        
        logger.info(
            "Achievement shared",
            user_id=current_user.id,
            achievement_id=achievement_id,
            platform=platform,
            points_awarded=settings.POINTS_PER_SHARE
        )
        
        return {
            "success": True,
            "points_awarded": settings.POINTS_PER_SHARE,
            "share_url": share_content.share_url,
            "share_text": share_content.share_text,
            "share_image": share_content.share_image
        }
        
    except Exception as e:
        logger.error("Achievement sharing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/rewards")
async def get_available_rewards(
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Get available rewards user can redeem with points"""
    try:
        gamification_service = GamificationService()
        rewards = await gamification_service.get_available_rewards(current_user.id)
        
        return {
            "rewards": rewards,
            "user_points": current_user.points,
            "total_rewards": len(rewards)
        }
        
    except Exception as e:
        logger.error("Failed to get rewards", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/rewards/redeem/{reward_id}")
async def redeem_reward(
    reward_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user),
    gamification_enabled: bool = Depends(GamificationDependencies.check_gamification_enabled)
):
    """Redeem reward with points"""
    try:
        gamification_service = GamificationService()
        
        result = await gamification_service.redeem_reward(
            user_id=current_user.id,
            reward_id=reward_id
        )
        
        logger.info(
            "Reward redeemed",
            user_id=current_user.id,
            reward_id=reward_id,
            points_spent=result.points_spent
        )
        
        return {
            "success": True,
            "reward": result.reward,
            "points_spent": result.points_spent,
            "remaining_points": result.remaining_points,
            "message": "Reward redeemed successfully"
        }
        
    except Exception as e:
        logger.error("Reward redemption failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )