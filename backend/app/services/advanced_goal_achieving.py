"""
Advanced Goal Achieving System - Sophisticated goal tracking, progress monitoring,
and achievement prediction with intelligent recommendations
"""

import asyncio
import json
import logging
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from uuid import UUID
from dataclasses import dataclass
from enum import Enum
import numpy as np

from app.core.database import get_database
from app.core.redis import get_redis_client
from app.models.goal_integrity import GoalDefinition, GoalViolation
from app.services.goal_integrity_service import GoalIntegrityService

logger = logging.getLogger(__name__)


class GoalStatus(Enum):
    """Enhanced goal status tracking"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BEHIND_SCHEDULE = "behind_schedule"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class GoalPriority(Enum):
    """Goal priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProgressIndicator(Enum):
    """Progress indicators for goal tracking"""
    EXCELLENT = "excellent"      # 90-100%
    GOOD = "good"               # 70-89%
    FAIR = "fair"               # 50-69%
    POOR = "poor"               # 30-49%
    CRITICAL = "critical"       # 0-29%


@dataclass
class GoalProgress:
    """Comprehensive goal progress tracking"""
    goal_id: UUID
    current_progress: float  # 0.0 to 1.0
    target_progress: float   # Expected progress at this time
    progress_velocity: float # Rate of progress (progress per day)
    completion_estimate: Optional[datetime]
    confidence_level: float  # Confidence in completion estimate
    progress_indicator: ProgressIndicator
    milestones_completed: int
    total_milestones: int
    last_activity: datetime
    streak_days: int
    productivity_score: float
    efficiency_score: float
    quality_score: float


@dataclass
class GoalRecommendation:
    """Intelligent goal recommendations"""
    goal_id: UUID
    recommendation_type: str
    priority: GoalPriority
    description: str
    action_items: List[str]
    expected_impact: float  # 0.0 to 1.0
    implementation_difficulty: float  # 0.0 to 1.0
    estimated_time: int  # minutes
    success_probability: float  # 0.0 to 1.0
    related_goals: List[UUID]


@dataclass
class GoalAnalytics:
    """Comprehensive goal analytics"""
    goal_id: UUID
    success_probability: float
    risk_factors: List[str]
    success_factors: List[str]
    optimal_strategies: List[str]
    predicted_completion_date: Optional[datetime]
    confidence_interval: Tuple[datetime, datetime]
    performance_trends: Dict[str, Any]
    comparative_analysis: Dict[str, Any]


class GoalMilestoneTracker:
    """Advanced milestone tracking and management"""
    
    def __init__(self):
        self.milestone_templates = {
            "learning": [
                {"name": "Research Phase", "weight": 0.2, "estimated_days": 3},
                {"name": "Practice Phase", "weight": 0.3, "estimated_days": 7},
                {"name": "Application Phase", "weight": 0.3, "estimated_days": 10},
                {"name": "Mastery Phase", "weight": 0.2, "estimated_days": 5}
            ],
            "project": [
                {"name": "Planning", "weight": 0.15, "estimated_days": 2},
                {"name": "Development", "weight": 0.5, "estimated_days": 15},
                {"name": "Testing", "weight": 0.2, "estimated_days": 5},
                {"name": "Deployment", "weight": 0.15, "estimated_days": 3}
            ],
            "fitness": [
                {"name": "Foundation", "weight": 0.25, "estimated_days": 7},
                {"name": "Building", "weight": 0.35, "estimated_days": 14},
                {"name": "Maintenance", "weight": 0.25, "estimated_days": 7},
                {"name": "Optimization", "weight": 0.15, "estimated_days": 5}
            ]
        }
    
    async def create_milestones_for_goal(self, goal: GoalDefinition) -> List[Dict[str, Any]]:
        """Create appropriate milestones for a goal based on its type and duration"""
        try:
            goal_type = goal.category.lower() if goal.category else "general"
            duration_days = (goal.target_date - goal.created_at).days if goal.target_date else 30
            
            # Select appropriate template
            template = self.milestone_templates.get(goal_type, self.milestone_templates["learning"])
            
            milestones = []
            current_date = goal.created_at
            
            for i, milestone_template in enumerate(template):
                milestone_duration = int(milestone_template["estimated_days"] * (duration_days / 30))
                
                milestone = {
                    "id": f"{goal.id}_{i+1}",
                    "name": milestone_template["name"],
                    "weight": milestone_template["weight"],
                    "target_date": current_date + timedelta(days=milestone_duration),
                    "completed": False,
                    "completion_date": None,
                    "progress": 0.0
                }
                
                milestones.append(milestone)
                current_date += timedelta(days=milestone_duration)
            
            return milestones
            
        except Exception as e:
            logger.error(f"Error creating milestones: {e}")
            return []
    
    async def update_milestone_progress(self, goal_id: UUID, milestone_id: str, progress: float) -> bool:
        """Update progress for a specific milestone"""
        try:
            redis_client = await get_redis_client()
            if not redis_client:
                return False
            
            cache_key = f"goal_milestones:{goal_id}"
            milestones_data = await redis_client.get(cache_key)
            
            if milestones_data:
                milestones = json.loads(milestones_data)
                
                for milestone in milestones:
                    if milestone["id"] == milestone_id:
                        milestone["progress"] = min(1.0, max(0.0, progress))
                        if progress >= 1.0:
                            milestone["completed"] = True
                            milestone["completion_date"] = datetime.utcnow().isoformat()
                        
                        await redis_client.setex(cache_key, 86400, json.dumps(milestones))
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating milestone progress: {e}")
            return False


class GoalProgressAnalyzer:
    """Advanced goal progress analysis and prediction"""
    
    def __init__(self):
        self.analysis_weights = {
            "velocity": 0.3,
            "consistency": 0.25,
            "quality": 0.2,
            "efficiency": 0.15,
            "engagement": 0.1
        }
    
    async def analyze_goal_progress(self, goal_id: UUID) -> GoalProgress:
        """Comprehensive analysis of goal progress"""
        try:
            # Get goal data
            goal = await self._get_goal(goal_id)
            if not goal:
                raise ValueError(f"Goal {goal_id} not found")
            
            # Get progress history
            progress_history = await self._get_progress_history(goal_id)
            
            # Calculate current progress
            current_progress = await self._calculate_current_progress(goal_id, progress_history)
            
            # Calculate target progress
            target_progress = await self._calculate_target_progress(goal)
            
            # Calculate progress velocity
            progress_velocity = await self._calculate_progress_velocity(progress_history)
            
            # Estimate completion date
            completion_estimate = await self._estimate_completion_date(
                current_progress, progress_velocity, goal
            )
            
            # Calculate confidence level
            confidence_level = await self._calculate_confidence_level(
                progress_history, progress_velocity
            )
            
            # Determine progress indicator
            progress_indicator = self._determine_progress_indicator(current_progress, target_progress)
            
            # Get milestone information
            milestones_completed, total_milestones = await self._get_milestone_stats(goal_id)
            
            # Calculate performance scores
            productivity_score = await self._calculate_productivity_score(progress_history)
            efficiency_score = await self._calculate_efficiency_score(current_progress, target_progress)
            quality_score = await self._calculate_quality_score(goal_id)
            
            # Calculate streak
            streak_days = await self._calculate_streak_days(progress_history)
            
            return GoalProgress(
                goal_id=goal_id,
                current_progress=current_progress,
                target_progress=target_progress,
                progress_velocity=progress_velocity,
                completion_estimate=completion_estimate,
                confidence_level=confidence_level,
                progress_indicator=progress_indicator,
                milestones_completed=milestones_completed,
                total_milestones=total_milestones,
                last_activity=progress_history[-1]["timestamp"] if progress_history else goal.created_at,
                streak_days=streak_days,
                productivity_score=productivity_score,
                efficiency_score=efficiency_score,
                quality_score=quality_score
            )
            
        except Exception as e:
            logger.error(f"Error analyzing goal progress: {e}")
            raise
    
    async def _get_goal(self, goal_id: UUID) -> Optional[GoalDefinition]:
        """Get goal definition"""
        try:
            async with get_database() as db:
                from sqlalchemy import select
                query = select(GoalDefinition).where(GoalDefinition.id == goal_id)
                result = await db.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting goal: {e}")
            return None
    
    async def _get_progress_history(self, goal_id: UUID) -> List[Dict[str, Any]]:
        """Get progress history for the goal"""
        try:
            redis_client = await get_redis_client()
            if not redis_client:
                return []
            
            cache_key = f"goal_progress_history:{goal_id}"
            history_data = await redis_client.get(cache_key)
            
            if history_data:
                return json.loads(history_data)
            
            # If no cached data, return empty list
            return []
            
        except Exception as e:
            logger.error(f"Error getting progress history: {e}")
            return []
    
    async def _calculate_current_progress(self, goal_id: UUID, progress_history: List[Dict[str, Any]]) -> float:
        """Calculate current progress based on history"""
        try:
            if not progress_history:
                return 0.0
            
            # Get the latest progress entry
            latest_progress = progress_history[-1]
            return latest_progress.get("progress", 0.0)
            
        except Exception as e:
            logger.error(f"Error calculating current progress: {e}")
            return 0.0
    
    async def _calculate_target_progress(self, goal: GoalDefinition) -> float:
        """Calculate target progress based on time elapsed"""
        try:
            if not goal.target_date:
                return 0.0
            
            total_duration = (goal.target_date - goal.created_at).total_seconds()
            elapsed_time = (datetime.utcnow() - goal.created_at).total_seconds()
            
            if total_duration <= 0:
                return 1.0
            
            return min(1.0, elapsed_time / total_duration)
            
        except Exception as e:
            logger.error(f"Error calculating target progress: {e}")
            return 0.0
    
    async def _calculate_progress_velocity(self, progress_history: List[Dict[str, Any]]) -> float:
        """Calculate progress velocity (progress per day)"""
        try:
            if len(progress_history) < 2:
                return 0.0
            
            # Calculate velocity over the last 7 days
            recent_history = progress_history[-7:] if len(progress_history) >= 7 else progress_history
            
            if len(recent_history) < 2:
                return 0.0
            
            start_progress = recent_history[0]["progress"]
            end_progress = recent_history[-1]["progress"]
            
            start_time = datetime.fromisoformat(recent_history[0]["timestamp"])
            end_time = datetime.fromisoformat(recent_history[-1]["timestamp"])
            
            time_delta = (end_time - start_time).total_seconds() / 86400  # Convert to days
            
            if time_delta <= 0:
                return 0.0
            
            velocity = (end_progress - start_progress) / time_delta
            return max(0.0, velocity)  # Ensure non-negative velocity
            
        except Exception as e:
            logger.error(f"Error calculating progress velocity: {e}")
            return 0.0
    
    async def _estimate_completion_date(
        self, 
        current_progress: float, 
        progress_velocity: float, 
        goal: GoalDefinition
    ) -> Optional[datetime]:
        """Estimate completion date based on current progress and velocity"""
        try:
            if progress_velocity <= 0:
                return None
            
            remaining_progress = 1.0 - current_progress
            days_to_completion = remaining_progress / progress_velocity
            
            estimated_completion = datetime.utcnow() + timedelta(days=days_to_completion)
            
            return estimated_completion
            
        except Exception as e:
            logger.error(f"Error estimating completion date: {e}")
            return None
    
    async def _calculate_confidence_level(
        self, 
        progress_history: List[Dict[str, Any]], 
        progress_velocity: float
    ) -> float:
        """Calculate confidence level in completion estimate"""
        try:
            if not progress_history or progress_velocity <= 0:
                return 0.0
            
            # Calculate consistency of progress
            if len(progress_history) >= 3:
                progress_values = [entry["progress"] for entry in progress_history]
                progress_changes = [progress_values[i] - progress_values[i-1] for i in range(1, len(progress_values))]
                
                if progress_changes:
                    consistency = 1.0 - (np.std(progress_changes) / np.mean(progress_changes)) if np.mean(progress_changes) > 0 else 0.0
                    consistency = max(0.0, min(1.0, consistency))
                else:
                    consistency = 0.5
            else:
                consistency = 0.5
            
            # Calculate velocity stability
            velocity_stability = min(1.0, progress_velocity * 10)  # Scale velocity to 0-1
            
            # Combine consistency and velocity stability
            confidence = (consistency * 0.6 + velocity_stability * 0.4)
            
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            logger.error(f"Error calculating confidence level: {e}")
            return 0.0
    
    def _determine_progress_indicator(self, current_progress: float, target_progress: float) -> ProgressIndicator:
        """Determine progress indicator based on current vs target progress"""
        try:
            progress_ratio = current_progress / max(target_progress, 0.01)  # Avoid division by zero
            
            if progress_ratio >= 1.2:  # 20% ahead
                return ProgressIndicator.EXCELLENT
            elif progress_ratio >= 1.0:  # On track
                return ProgressIndicator.GOOD
            elif progress_ratio >= 0.8:  # 20% behind
                return ProgressIndicator.FAIR
            elif progress_ratio >= 0.5:  # 50% behind
                return ProgressIndicator.POOR
            else:  # More than 50% behind
                return ProgressIndicator.CRITICAL
                
        except Exception as e:
            logger.error(f"Error determining progress indicator: {e}")
            return ProgressIndicator.CRITICAL
    
    async def _get_milestone_stats(self, goal_id: UUID) -> Tuple[int, int]:
        """Get milestone completion statistics"""
        try:
            redis_client = await get_redis_client()
            if not redis_client:
                return 0, 0
            
            cache_key = f"goal_milestones:{goal_id}"
            milestones_data = await redis_client.get(cache_key)
            
            if milestones_data:
                milestones = json.loads(milestones_data)
                completed = sum(1 for milestone in milestones if milestone.get("completed", False))
                total = len(milestones)
                return completed, total
            
            return 0, 0
            
        except Exception as e:
            logger.error(f"Error getting milestone stats: {e}")
            return 0, 0
    
    async def _calculate_productivity_score(self, progress_history: List[Dict[str, Any]]) -> float:
        """Calculate productivity score based on progress consistency"""
        try:
            if len(progress_history) < 2:
                return 0.5
            
            # Calculate daily progress rates
            daily_progress = []
            for i in range(1, len(progress_history)):
                prev_progress = progress_history[i-1]["progress"]
                curr_progress = progress_history[i]["progress"]
                daily_progress.append(curr_progress - prev_progress)
            
            if not daily_progress:
                return 0.5
            
            # Calculate productivity as consistency of positive progress
            positive_days = sum(1 for progress in daily_progress if progress > 0)
            productivity = positive_days / len(daily_progress)
            
            return max(0.0, min(1.0, productivity))
            
        except Exception as e:
            logger.error(f"Error calculating productivity score: {e}")
            return 0.0
    
    async def _calculate_efficiency_score(self, current_progress: float, target_progress: float) -> float:
        """Calculate efficiency score based on progress vs target"""
        try:
            if target_progress <= 0:
                return 1.0 if current_progress > 0 else 0.0
            
            efficiency = current_progress / target_progress
            return max(0.0, min(1.0, efficiency))
            
        except Exception as e:
            logger.error(f"Error calculating efficiency score: {e}")
            return 0.0
    
    async def _calculate_quality_score(self, goal_id: UUID) -> float:
        """Calculate quality score based on goal violations and achievements"""
        try:
            # Get violations for this goal
            async with get_database() as db:
                from sqlalchemy import select
                query = select(GoalViolation).where(GoalViolation.goal_id == goal_id)
                result = await db.execute(query)
                violations = result.scalars().all()
            
            # Calculate quality based on violation frequency and severity
            if not violations:
                return 1.0
            
            total_violations = len(violations)
            severe_violations = sum(1 for v in violations if v.severity == "high")
            
            # Quality decreases with violations
            quality = max(0.0, 1.0 - (total_violations * 0.1) - (severe_violations * 0.2))
            
            return max(0.0, min(1.0, quality))
            
        except Exception as e:
            logger.error(f"Error calculating quality score: {e}")
            return 0.5
    
    async def _calculate_streak_days(self, progress_history: List[Dict[str, Any]]) -> int:
        """Calculate current streak of productive days"""
        try:
            if not progress_history:
                return 0
            
            streak = 0
            current_date = datetime.utcnow().date()
            
            # Check backwards from today
            for i in range(len(progress_history) - 1, -1, -1):
                entry_date = datetime.fromisoformat(progress_history[i]["timestamp"]).date()
                
                # If entry is not from today or yesterday, break
                if (current_date - entry_date).days > 1:
                    break
                
                # Check if there was progress
                if i > 0:
                    prev_progress = progress_history[i-1]["progress"]
                    curr_progress = progress_history[i]["progress"]
                    if curr_progress > prev_progress:
                        streak += 1
                        current_date = entry_date
                    else:
                        break
                else:
                    # First entry - if there's any progress, count it
                    if progress_history[i]["progress"] > 0:
                        streak += 1
                    break
            
            return streak
            
        except Exception as e:
            logger.error(f"Error calculating streak days: {e}")
            return 0


class GoalRecommendationEngine:
    """Intelligent goal recommendation engine"""
    
    def __init__(self):
        self.recommendation_templates = {
            "behind_schedule": {
                "priority": GoalPriority.HIGH,
                "recommendations": [
                    "Increase daily time allocation",
                    "Break down into smaller tasks",
                    "Remove non-essential activities",
                    "Seek additional resources or help"
                ]
            },
            "low_productivity": {
                "priority": GoalPriority.MEDIUM,
                "recommendations": [
                    "Improve time management",
                    "Eliminate distractions",
                    "Set specific daily targets",
                    "Use productivity techniques"
                ]
            },
            "quality_issues": {
                "priority": GoalPriority.HIGH,
                "recommendations": [
                    "Review and improve processes",
                    "Increase quality checkpoints",
                    "Get feedback from others",
                    "Invest in skill development"
                ]
            },
            "motivation_low": {
                "priority": GoalPriority.MEDIUM,
                "recommendations": [
                    "Reconnect with original motivation",
                    "Celebrate small wins",
                    "Find accountability partner",
                    "Adjust goal difficulty"
                ]
            }
        }
    
    async def generate_recommendations(self, goal_progress: GoalProgress) -> List[GoalRecommendation]:
        """Generate intelligent recommendations for goal improvement"""
        try:
            recommendations = []
            
            # Analyze goal status and generate recommendations
            if goal_progress.progress_indicator == ProgressIndicator.CRITICAL:
                recommendations.extend(await self._generate_critical_recommendations(goal_progress))
            elif goal_progress.progress_indicator == ProgressIndicator.POOR:
                recommendations.extend(await self._generate_poor_recommendations(goal_progress))
            elif goal_progress.productivity_score < 0.5:
                recommendations.extend(await self._generate_productivity_recommendations(goal_progress))
            elif goal_progress.quality_score < 0.7:
                recommendations.extend(await self._generate_quality_recommendations(goal_progress))
            else:
                recommendations.extend(await self._generate_optimization_recommendations(goal_progress))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
    
    async def _generate_critical_recommendations(self, goal_progress: GoalProgress) -> List[GoalRecommendation]:
        """Generate recommendations for critically behind goals"""
        return [
            GoalRecommendation(
                goal_id=goal_progress.goal_id,
                recommendation_type="emergency_intervention",
                priority=GoalPriority.CRITICAL,
                description="Goal is critically behind schedule and requires immediate intervention",
                action_items=[
                    "Dedicate 2x more time daily to this goal",
                    "Eliminate all non-essential activities",
                    "Break goal into hourly tasks",
                    "Get external help or resources",
                    "Consider adjusting target date"
                ],
                expected_impact=0.8,
                implementation_difficulty=0.7,
                estimated_time=120,
                success_probability=0.6,
                related_goals=[]
            )
        ]
    
    async def _generate_poor_recommendations(self, goal_progress: GoalProgress) -> List[GoalRecommendation]:
        """Generate recommendations for poor performing goals"""
        return [
            GoalRecommendation(
                goal_id=goal_progress.goal_id,
                recommendation_type="performance_improvement",
                priority=GoalPriority.HIGH,
                description="Goal performance is below expectations and needs improvement",
                action_items=[
                    "Increase daily time allocation by 50%",
                    "Set specific daily milestones",
                    "Remove time-wasting activities",
                    "Improve focus and concentration"
                ],
                expected_impact=0.6,
                implementation_difficulty=0.5,
                estimated_time=60,
                success_probability=0.7,
                related_goals=[]
            )
        ]
    
    async def _generate_productivity_recommendations(self, goal_progress: GoalProgress) -> List[GoalRecommendation]:
        """Generate recommendations for low productivity"""
        return [
            GoalRecommendation(
                goal_id=goal_progress.goal_id,
                recommendation_type="productivity_boost",
                priority=GoalPriority.MEDIUM,
                description="Low productivity detected - implementing productivity techniques",
                action_items=[
                    "Use Pomodoro technique for focused work",
                    "Eliminate digital distractions",
                    "Set clear daily priorities",
                    "Track time spent on goal activities"
                ],
                expected_impact=0.5,
                implementation_difficulty=0.3,
                estimated_time=30,
                success_probability=0.8,
                related_goals=[]
            )
        ]
    
    async def _generate_quality_recommendations(self, goal_progress: GoalProgress) -> List[GoalRecommendation]:
        """Generate recommendations for quality improvement"""
        return [
            GoalRecommendation(
                goal_id=goal_progress.goal_id,
                recommendation_type="quality_improvement",
                priority=GoalPriority.HIGH,
                description="Quality issues detected - focus on improvement processes",
                action_items=[
                    "Add quality checkpoints",
                    "Get feedback from experts",
                    "Review and improve processes",
                    "Invest in skill development"
                ],
                expected_impact=0.7,
                implementation_difficulty=0.4,
                estimated_time=45,
                success_probability=0.75,
                related_goals=[]
            )
        ]
    
    async def _generate_optimization_recommendations(self, goal_progress: GoalProgress) -> List[GoalRecommendation]:
        """Generate optimization recommendations for well-performing goals"""
        return [
            GoalRecommendation(
                goal_id=goal_progress.goal_id,
                recommendation_type="optimization",
                priority=GoalPriority.LOW,
                description="Goal is performing well - optimize for even better results",
                action_items=[
                    "Set stretch targets",
                    "Optimize current processes",
                    "Share knowledge with others",
                    "Consider advanced techniques"
                ],
                expected_impact=0.3,
                implementation_difficulty=0.2,
                estimated_time=20,
                success_probability=0.9,
                related_goals=[]
            )
        ]


class AdvancedGoalAchievingSystem:
    """Advanced goal achieving system with comprehensive tracking and recommendations"""
    
    def __init__(self):
        self.milestone_tracker = GoalMilestoneTracker()
        self.progress_analyzer = GoalProgressAnalyzer()
        self.recommendation_engine = GoalRecommendationEngine()
        self.goal_service = GoalIntegrityService()
    
    async def initialize(self):
        """Initialize the advanced goal achieving system"""
        try:
            await self.goal_service.initialize()
            logger.info("Advanced Goal Achieving System initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Advanced Goal Achieving System: {e}")
            raise
    
    async def track_goal_progress(
        self, 
        goal_id: UUID, 
        progress_update: float, 
        notes: str = ""
    ) -> Dict[str, Any]:
        """Track progress for a specific goal"""
        try:
            # Validate progress update
            if not 0.0 <= progress_update <= 1.0:
                raise ValueError("Progress update must be between 0.0 and 1.0")
            
            # Store progress update
            await self._store_progress_update(goal_id, progress_update, notes)
            
            # Update milestones if applicable
            await self._update_milestones_for_progress(goal_id, progress_update)
            
            # Analyze progress
            goal_progress = await self.progress_analyzer.analyze_goal_progress(goal_id)
            
            # Generate recommendations
            recommendations = await self.recommendation_engine.generate_recommendations(goal_progress)
            
            return {
                "goal_id": str(goal_id),
                "progress_updated": True,
                "current_progress": goal_progress.current_progress,
                "target_progress": goal_progress.target_progress,
                "progress_indicator": goal_progress.progress_indicator.value,
                "completion_estimate": goal_progress.completion_estimate.isoformat() if goal_progress.completion_estimate else None,
                "confidence_level": goal_progress.confidence_level,
                "recommendations": [
                    {
                        "type": rec.recommendation_type,
                        "priority": rec.priority.value,
                        "description": rec.description,
                        "action_items": rec.action_items,
                        "expected_impact": rec.expected_impact,
                        "success_probability": rec.success_probability
                    }
                    for rec in recommendations
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error tracking goal progress: {e}")
            raise
    
    async def _store_progress_update(self, goal_id: UUID, progress: float, notes: str):
        """Store progress update in cache"""
        try:
            redis_client = await get_redis_client()
            if not redis_client:
                return
            
            cache_key = f"goal_progress_history:{goal_id}"
            
            # Get existing history
            history_data = await redis_client.get(cache_key)
            history = json.loads(history_data) if history_data else []
            
            # Add new entry
            new_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "progress": progress,
                "notes": notes
            }
            
            history.append(new_entry)
            
            # Keep only last 30 entries
            if len(history) > 30:
                history = history[-30:]
            
            # Store updated history
            await redis_client.setex(cache_key, 86400 * 7, json.dumps(history))  # 7 days
            
        except Exception as e:
            logger.error(f"Error storing progress update: {e}")
    
    async def _update_milestones_for_progress(self, goal_id: UUID, progress: float):
        """Update milestone completion based on progress"""
        try:
            redis_client = await get_redis_client()
            if not redis_client:
                return
            
            cache_key = f"goal_milestones:{goal_id}"
            milestones_data = await redis_client.get(cache_key)
            
            if milestones_data:
                milestones = json.loads(milestones_data)
                
                # Update milestone progress based on overall progress
                cumulative_weight = 0.0
                for milestone in milestones:
                    if not milestone.get("completed", False):
                        milestone["progress"] = min(1.0, max(0.0, (progress - cumulative_weight) / milestone["weight"]))
                        
                        if milestone["progress"] >= 1.0:
                            milestone["completed"] = True
                            milestone["completion_date"] = datetime.utcnow().isoformat()
                        
                        cumulative_weight += milestone["weight"]
                        
                        if progress <= cumulative_weight:
                            break
                
                await redis_client.setex(cache_key, 86400 * 7, json.dumps(milestones))
            
        except Exception as e:
            logger.error(f"Error updating milestones: {e}")
    
    async def get_goal_analytics(self, goal_id: UUID) -> GoalAnalytics:
        """Get comprehensive analytics for a goal"""
        try:
            # Analyze progress
            goal_progress = await self.progress_analyzer.analyze_goal_progress(goal_id)
            
            # Calculate success probability
            success_probability = await self._calculate_success_probability(goal_progress)
            
            # Identify risk and success factors
            risk_factors = await self._identify_risk_factors(goal_progress)
            success_factors = await self._identify_success_factors(goal_progress)
            
            # Generate optimal strategies
            optimal_strategies = await self._generate_optimal_strategies(goal_progress)
            
            # Predict completion date with confidence interval
            predicted_completion, confidence_interval = await self._predict_completion_with_confidence(goal_progress)
            
            # Analyze performance trends
            performance_trends = await self._analyze_performance_trends(goal_id)
            
            # Comparative analysis
            comparative_analysis = await self._perform_comparative_analysis(goal_id)
            
            return GoalAnalytics(
                goal_id=goal_id,
                success_probability=success_probability,
                risk_factors=risk_factors,
                success_factors=success_factors,
                optimal_strategies=optimal_strategies,
                predicted_completion_date=predicted_completion,
                confidence_interval=confidence_interval,
                performance_trends=performance_trends,
                comparative_analysis=comparative_analysis
            )
            
        except Exception as e:
            logger.error(f"Error getting goal analytics: {e}")
            raise
    
    async def _calculate_success_probability(self, goal_progress: GoalProgress) -> float:
        """Calculate probability of goal success"""
        try:
            # Base probability from current progress
            base_probability = goal_progress.current_progress
            
            # Adjust based on velocity
            velocity_factor = min(1.0, goal_progress.progress_velocity * 10)
            
            # Adjust based on consistency (confidence level)
            consistency_factor = goal_progress.confidence_level
            
            # Adjust based on quality
            quality_factor = goal_progress.quality_score
            
            # Calculate weighted success probability
            success_probability = (
                base_probability * 0.4 +
                velocity_factor * 0.25 +
                consistency_factor * 0.2 +
                quality_factor * 0.15
            )
            
            return max(0.0, min(1.0, success_probability))
            
        except Exception as e:
            logger.error(f"Error calculating success probability: {e}")
            return 0.5
    
    async def _identify_risk_factors(self, goal_progress: GoalProgress) -> List[str]:
        """Identify risk factors for goal achievement"""
        risk_factors = []
        
        if goal_progress.progress_indicator in [ProgressIndicator.POOR, ProgressIndicator.CRITICAL]:
            risk_factors.append("Behind schedule")
        
        if goal_progress.productivity_score < 0.5:
            risk_factors.append("Low productivity")
        
        if goal_progress.quality_score < 0.7:
            risk_factors.append("Quality issues")
        
        if goal_progress.streak_days < 3:
            risk_factors.append("Inconsistent activity")
        
        if goal_progress.confidence_level < 0.6:
            risk_factors.append("Uncertain completion estimate")
        
        if goal_progress.progress_velocity < 0.01:
            risk_factors.append("Very slow progress")
        
        return risk_factors
    
    async def _identify_success_factors(self, goal_progress: GoalProgress) -> List[str]:
        """Identify success factors for goal achievement"""
        success_factors = []
        
        if goal_progress.progress_indicator in [ProgressIndicator.EXCELLENT, ProgressIndicator.GOOD]:
            success_factors.append("On track or ahead of schedule")
        
        if goal_progress.productivity_score >= 0.7:
            success_factors.append("High productivity")
        
        if goal_progress.quality_score >= 0.8:
            success_factors.append("High quality standards")
        
        if goal_progress.streak_days >= 7:
            success_factors.append("Consistent daily activity")
        
        if goal_progress.confidence_level >= 0.8:
            success_factors.append("Reliable progress pattern")
        
        if goal_progress.progress_velocity > 0.02:
            success_factors.append("Good progress velocity")
        
        return success_factors
    
    async def _generate_optimal_strategies(self, goal_progress: GoalProgress) -> List[str]:
        """Generate optimal strategies based on goal analysis"""
        strategies = []
        
        if goal_progress.progress_indicator == ProgressIndicator.CRITICAL:
            strategies.extend([
                "Implement emergency intervention plan",
                "Dedicate maximum available time",
                "Seek external help or resources",
                "Consider goal timeline adjustment"
            ])
        elif goal_progress.productivity_score < 0.6:
            strategies.extend([
                "Improve time management techniques",
                "Eliminate distractions and interruptions",
                "Use productivity tools and methods",
                "Set specific daily targets"
            ])
        elif goal_progress.quality_score < 0.7:
            strategies.extend([
                "Implement quality checkpoints",
                "Get regular feedback from experts",
                "Improve processes and workflows",
                "Invest in skill development"
            ])
        else:
            strategies.extend([
                "Maintain current momentum",
                "Optimize existing processes",
                "Set stretch targets",
                "Share knowledge and mentor others"
            ])
        
        return strategies
    
    async def _predict_completion_with_confidence(
        self, 
        goal_progress: GoalProgress
    ) -> Tuple[Optional[datetime], Tuple[datetime, datetime]]:
        """Predict completion date with confidence interval"""
        try:
            if not goal_progress.completion_estimate:
                return None, (datetime.utcnow(), datetime.utcnow())
            
            # Calculate confidence interval based on velocity consistency
            confidence_factor = goal_progress.confidence_level
            uncertainty_days = int(30 * (1.0 - confidence_factor))  # Up to 30 days uncertainty
            
            early_completion = goal_progress.completion_estimate - timedelta(days=uncertainty_days)
            late_completion = goal_progress.completion_estimate + timedelta(days=uncertainty_days)
            
            return goal_progress.completion_estimate, (early_completion, late_completion)
            
        except Exception as e:
            logger.error(f"Error predicting completion: {e}")
            return None, (datetime.utcnow(), datetime.utcnow())
    
    async def _analyze_performance_trends(self, goal_id: UUID) -> Dict[str, Any]:
        """Analyze performance trends for the goal"""
        try:
            progress_history = await self.progress_analyzer._get_progress_history(goal_id)
            
            if len(progress_history) < 3:
                return {"trend": "insufficient_data", "direction": "unknown"}
            
            # Calculate trend direction
            recent_progress = [entry["progress"] for entry in progress_history[-7:]]
            
            if len(recent_progress) >= 2:
                trend_slope = (recent_progress[-1] - recent_progress[0]) / len(recent_progress)
                
                if trend_slope > 0.01:
                    trend_direction = "improving"
                elif trend_slope < -0.01:
                    trend_direction = "declining"
                else:
                    trend_direction = "stable"
            else:
                trend_direction = "unknown"
            
            return {
                "trend": trend_direction,
                "recent_velocity": trend_slope if 'trend_slope' in locals() else 0.0,
                "data_points": len(progress_history),
                "trend_confidence": min(1.0, len(recent_progress) / 7.0)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing performance trends: {e}")
            return {"trend": "error", "error": str(e)}
    
    async def _perform_comparative_analysis(self, goal_id: UUID) -> Dict[str, Any]:
        """Perform comparative analysis against similar goals"""
        try:
            # This would typically compare against similar goals from other users
            # For now, we'll provide a simplified analysis
            
            goal_progress = await self.progress_analyzer.analyze_goal_progress(goal_id)
            
            # Simulate comparative metrics
            comparative_metrics = {
                "vs_average_progress": goal_progress.current_progress / 0.6,  # Assume 60% is average
                "vs_average_velocity": goal_progress.progress_velocity / 0.02,  # Assume 0.02 is average
                "vs_average_quality": goal_progress.quality_score / 0.7,  # Assume 0.7 is average
                "percentile_rank": min(100, max(0, goal_progress.current_progress * 100)),
                "performance_category": self._categorize_performance(goal_progress)
            }
            
            return comparative_metrics
            
        except Exception as e:
            logger.error(f"Error performing comparative analysis: {e}")
            return {"error": str(e)}
    
    def _categorize_performance(self, goal_progress: GoalProgress) -> str:
        """Categorize goal performance"""
        if goal_progress.progress_indicator == ProgressIndicator.EXCELLENT:
            return "Top Performer"
        elif goal_progress.progress_indicator == ProgressIndicator.GOOD:
            return "Above Average"
        elif goal_progress.progress_indicator == ProgressIndicator.FAIR:
            return "Average"
        elif goal_progress.progress_indicator == ProgressIndicator.POOR:
            return "Below Average"
        else:
            return "Needs Improvement"


# Global advanced goal achieving system instance
advanced_goal_achieving_system = AdvancedGoalAchievingSystem()
