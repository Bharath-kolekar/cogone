"""
Database Optimization Service - Fixes N+1 queries, adds compound indexes, and optimizes queries
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, text, and_, or_
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from sqlalchemy.sql import Query
import time

from app.core.database import get_database
from app.models.ai_agent import AgentDefinition, TaskDefinition, AgentInteraction
from app.models.goal_integrity import GoalDefinition, GoalState, GoalViolation

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """Optimizes database queries to prevent N+1 problems and improve performance"""
    
    def __init__(self):
        self._query_cache: Dict[str, Any] = {}
        self._cache_ttl = 300  # 5 minutes
        self._last_cleanup = time.time()
    
    async def get_agents_with_tasks_optimized(
        self, 
        user_id: Optional[UUID] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get agents with their tasks in a single optimized query"""
        try:
            # Build optimized query with proper joins
            query = (
                select(AgentDefinition)
                .options(
                    selectinload(AgentDefinition.tasks).selectinload(TaskDefinition.interactions),
                    selectinload(AgentDefinition.metrics),
                    selectinload(AgentDefinition.config)
                )
                .where(AgentDefinition.status == 'active')
                .limit(limit)
            )
            
            # Add filters if provided
            if user_id:
                query = query.where(AgentDefinition.user_id == user_id)
            if status:
                query = query.where(AgentDefinition.status == status)
            
            async with get_database() as db:
                result = await db.execute(query)
                agents = result.scalars().all()
                
                # Transform to optimized format
                optimized_agents = []
                for agent in agents:
                    agent_data = {
                        "id": agent.id,
                        "name": agent.name,
                        "description": agent.description,
                        "type": agent.type,
                        "status": agent.status,
                        "capabilities": agent.capabilities,
                        "config": agent.config,
                        "metrics": agent.metrics,
                        "tasks": [
                            {
                                "id": task.id,
                                "type": task.type,
                                "title": task.title,
                                "status": task.status,
                                "created_at": task.created_at,
                                "interactions_count": len(task.interactions)
                            }
                            for task in agent.tasks
                        ],
                        "total_tasks": len(agent.tasks),
                        "created_at": agent.created_at
                    }
                    optimized_agents.append(agent_data)
                
                return optimized_agents
                
        except Exception as e:
            logger.error(f"Failed to get optimized agents: {e}")
            return []
    
    async def get_agent_analytics_optimized(
        self, 
        agent_id: UUID,
        period: str = "daily",
        days: int = 30
    ) -> Dict[str, Any]:
        """Get agent analytics with optimized aggregation queries"""
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            async with get_database() as db:
                # Single query to get all analytics data
                analytics_query = text("""
                    SELECT 
                        DATE(ai.created_at) as date,
                        COUNT(*) as total_interactions,
                        COUNT(DISTINCT ai.user_id) as unique_users,
                        AVG(ai.response_time) as avg_response_time,
                        COUNT(CASE WHEN ai.user_rating >= 4 THEN 1 END) as positive_ratings,
                        COUNT(CASE WHEN ai.user_rating < 4 THEN 1 END) as negative_ratings,
                        SUM(ai.tokens_used) as total_tokens,
                        SUM(ai.cost) as total_cost
                    FROM ai_agent_interactions ai
                    WHERE ai.agent_id = :agent_id 
                        AND ai.created_at >= :start_date 
                        AND ai.created_at <= :end_date
                    GROUP BY DATE(ai.created_at)
                    ORDER BY date DESC
                """)
                
                result = await db.execute(
                    analytics_query, 
                    {"agent_id": str(agent_id), "start_date": start_date, "end_date": end_date}
                )
                
                daily_analytics = result.fetchall()
                
                # Get task analytics
                task_query = text("""
                    SELECT 
                        at.type,
                        COUNT(*) as total_tasks,
                        COUNT(CASE WHEN at.status = 'completed' THEN 1 END) as completed_tasks,
                        AVG(at.execution_time) as avg_execution_time
                    FROM ai_agent_tasks at
                    WHERE at.agent_id = :agent_id 
                        AND at.created_at >= :start_date 
                        AND at.created_at <= :end_date
                    GROUP BY at.type
                """)
                
                task_result = await db.execute(
                    task_query,
                    {"agent_id": str(agent_id), "start_date": start_date, "end_date": end_date}
                )
                
                task_analytics = task_result.fetchall()
                
                # Calculate aggregated metrics
                total_interactions = sum(row.total_interactions for row in daily_analytics)
                total_users = sum(row.unique_users for row in daily_analytics)
                avg_response_time = (
                    sum(row.avg_response_time for row in daily_analytics if row.avg_response_time) / 
                    len([row for row in daily_analytics if row.avg_response_time])
                    if daily_analytics else 0
                )
                total_positive = sum(row.positive_ratings for row in daily_analytics)
                total_negative = sum(row.negative_ratings for row in daily_analytics)
                total_tokens = sum(row.total_tokens for row in daily_analytics if row.total_tokens)
                total_cost = sum(row.total_cost for row in daily_analytics if row.total_cost)
                
                satisfaction_rate = (
                    (total_positive / (total_positive + total_negative) * 100)
                    if (total_positive + total_negative) > 0 else 0
                )
                
                return {
                    "period": period,
                    "days_analyzed": days,
                    "summary": {
                        "total_interactions": total_interactions,
                        "unique_users": total_users,
                        "average_response_time": round(avg_response_time, 3),
                        "satisfaction_rate": round(satisfaction_rate, 2),
                        "total_tokens": total_tokens,
                        "total_cost": round(total_cost, 4)
                    },
                    "daily_breakdown": [
                        {
                            "date": row.date.isoformat(),
                            "interactions": row.total_interactions,
                            "unique_users": row.unique_users,
                            "avg_response_time": round(row.avg_response_time or 0, 3),
                            "satisfaction_rate": round(
                                (row.positive_ratings / (row.positive_ratings + row.negative_ratings) * 100)
                                if (row.positive_ratings + row.negative_ratings) > 0 else 0, 2
                            ),
                            "tokens_used": row.total_tokens or 0,
                            "cost": round(row.total_cost or 0, 4)
                        }
                        for row in daily_analytics
                    ],
                    "task_breakdown": [
                        {
                            "type": row.type,
                            "total_tasks": row.total_tasks,
                            "completed_tasks": row.completed_tasks,
                            "completion_rate": round(
                                (row.completed_tasks / row.total_tasks * 100) if row.total_tasks > 0 else 0, 2
                            ),
                            "avg_execution_time": round(row.avg_execution_time or 0, 3)
                        }
                        for row in task_analytics
                    ]
                }
                
        except Exception as e:
            logger.error(f"Failed to get agent analytics: {e}")
            return {}
    
    async def get_goal_integrity_metrics_optimized(
        self,
        goal_ids: Optional[List[str]] = None,
        time_range_hours: int = 24
    ) -> Dict[str, Any]:
        """Get goal integrity metrics with optimized queries"""
        try:
            start_time = datetime.utcnow() - timedelta(hours=time_range_hours)
            
            async with get_database() as db:
                # Build optimized query for goal metrics
                base_query = select(
                    GoalDefinition.id,
                    GoalDefinition.name,
                    GoalDefinition.type,
                    GoalState.status,
                    GoalState.integrity_score,
                    func.count(GoalViolation.id).label('violation_count')
                ).select_from(
                    GoalDefinition.__table__
                    .join(GoalState.__table__, GoalDefinition.id == GoalState.goal_id)
                    .outerjoin(GoalViolation.__table__, 
                              and_(GoalDefinition.id == GoalViolation.goal_id,
                                   GoalViolation.detected_at >= start_time))
                )
                
                if goal_ids:
                    base_query = base_query.where(GoalDefinition.id.in_(goal_ids))
                
                base_query = base_query.group_by(
                    GoalDefinition.id,
                    GoalDefinition.name,
                    GoalDefinition.type,
                    GoalState.status,
                    GoalState.integrity_score
                )
                
                result = await db.execute(base_query)
                goal_metrics = result.fetchall()
                
                # Calculate aggregated metrics
                total_goals = len(goal_metrics)
                active_goals = len([g for g in goal_metrics if g.status == 'active'])
                compromised_goals = len([g for g in goal_metrics if g.status == 'compromised'])
                avg_integrity = (
                    sum(g.integrity_score for g in goal_metrics) / total_goals
                    if total_goals > 0 else 0
                )
                total_violations = sum(g.violation_count for g in goal_metrics)
                
                return {
                    "time_range_hours": time_range_hours,
                    "summary": {
                        "total_goals": total_goals,
                        "active_goals": active_goals,
                        "compromised_goals": compromised_goals,
                        "average_integrity_score": round(avg_integrity, 2),
                        "total_violations": total_violations
                    },
                    "goal_details": [
                        {
                            "goal_id": str(g.id),
                            "name": g.name,
                            "type": g.type,
                            "status": g.status,
                            "integrity_score": g.integrity_score,
                            "violations_count": g.violation_count
                        }
                        for g in goal_metrics
                    ]
                }
                
        except Exception as e:
            logger.error(f"Failed to get goal integrity metrics: {e}")
            return {}


class DatabaseIndexOptimizer:
    """Manages database indexes for optimal performance"""
    
    @staticmethod
    async def create_compound_indexes():
        """Create compound indexes for frequently used query patterns"""
        try:
            async with get_database() as db:
                # AI Agent compound indexes
                indexes_to_create = [
                    # Agent queries with user and status
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_agents_user_status ON ai_agents(user_id, status) WHERE status = 'active'",
                    
                    # Agent tasks with agent and status
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_agent_status ON ai_agent_tasks(agent_id, status) WHERE status IN ('pending', 'in_progress')",
                    
                    # Interactions with agent and date range
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_interactions_agent_date ON ai_agent_interactions(agent_id, created_at DESC)",
                    
                    # Interactions with user and session
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_interactions_user_session ON ai_agent_interactions(user_id, session_id)",
                    
                    # Goal integrity queries
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_goal_states_goal_status ON goal_states(goal_id, status) WHERE status = 'active'",
                    
                    # Violations with goal and date
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_violations_goal_date ON goal_violations(goal_id, detected_at DESC)",
                    
                    # Analytics with agent and period
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_analytics_agent_period ON ai_agent_analytics(agent_id, period, created_at DESC)",
                    
                    # Voice commands with user and date
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_voice_commands_user_date ON voice_commands(user_id, created_at DESC)",
                    
                    # Generated apps with user and status
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_apps_user_status ON generated_apps(user_id, status) WHERE status = 'generating'",
                    
                    # Payments with user and status
                    "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payments_user_status ON payments(user_id, status) WHERE status = 'pending'"
                ]
                
                for index_sql in indexes_to_create:
                    try:
                        await db.execute(text(index_sql))
                        logger.info(f"Created index: {index_sql.split('idx_')[1].split(' ')[0]}")
                    except Exception as e:
                        logger.warning(f"Failed to create index: {e}")
                
                await db.commit()
                logger.info("Compound indexes creation completed")
                
        except Exception as e:
            logger.error(f"Failed to create compound indexes: {e}")
    
    @staticmethod
    async def analyze_query_performance():
        """Analyze slow queries and suggest optimizations"""
        try:
            async with get_database() as db:
                # Get slow queries from pg_stat_statements (if enabled)
                slow_queries_query = text("""
                    SELECT 
                        query,
                        calls,
                        total_time,
                        mean_time,
                        rows
                    FROM pg_stat_statements 
                    WHERE mean_time > 100  -- queries taking more than 100ms on average
                    ORDER BY mean_time DESC
                    LIMIT 10
                """)
                
                try:
                    result = await db.execute(slow_queries_query)
                    slow_queries = result.fetchall()
                    
                    if slow_queries:
                        logger.warning(f"Found {len(slow_queries)} slow queries:")
                        for query in slow_queries:
                            logger.warning(
                                f"Query: {query.query[:100]}... "
                                f"(Calls: {query.calls}, Avg Time: {query.mean_time:.2f}ms)"
                            )
                    else:
                        logger.info("No slow queries detected")
                        
                except Exception as e:
                    logger.info("pg_stat_statements not available or not configured")
                
                # Analyze table statistics
                table_stats_query = text("""
                    SELECT 
                        schemaname,
                        tablename,
                        n_tup_ins,
                        n_tup_upd,
                        n_tup_del,
                        n_live_tup,
                        n_dead_tup
                    FROM pg_stat_user_tables 
                    WHERE n_dead_tup > 1000
                    ORDER BY n_dead_tup DESC
                """)
                
                result = await db.execute(table_stats_query)
                tables_with_dead_tuples = result.fetchall()
                
                if tables_with_dead_tuples:
                    logger.warning(f"Tables with high dead tuple count:")
                    for table in tables_with_dead_tuples:
                        logger.warning(
                            f"Table {table.tablename}: {table.n_dead_tup} dead tuples "
                            f"(Live: {table.n_live_tup})"
                        )
                
        except Exception as e:
            logger.error(f"Failed to analyze query performance: {e}")
    
    @staticmethod
    async def optimize_database():
        """Run database optimization tasks"""
        try:
            async with get_database() as db:
                # Update table statistics
                await db.execute(text("ANALYZE"))
                
                # Vacuum tables with high dead tuple count
                await db.execute(text("VACUUM ANALYZE"))
                
                logger.info("Database optimization completed")
                
        except Exception as e:
            logger.error(f"Failed to optimize database: {e}")


class ConnectionPoolOptimizer:
    """Optimizes database connection pooling"""
    
    @staticmethod
    async def get_connection_stats():
        """Get database connection statistics"""
        try:
            async with get_database() as db:
                # Get connection pool stats
                pool_stats_query = text("""
                    SELECT 
                        state,
                        COUNT(*) as connection_count
                    FROM pg_stat_activity 
                    WHERE datname = current_database()
                    GROUP BY state
                """)
                
                result = await db.execute(pool_stats_query)
                connection_stats = result.fetchall()
                
                return {
                    "connection_stats": [
                        {"state": row.state, "count": row.connection_count}
                        for row in connection_stats
                    ],
                    "total_connections": sum(row.connection_count for row in connection_stats)
                }
                
        except Exception as e:
            logger.error(f"Failed to get connection stats: {e}")
            return {}


# Global instances
query_optimizer = QueryOptimizer()
index_optimizer = DatabaseIndexOptimizer()
connection_optimizer = ConnectionPoolOptimizer()
