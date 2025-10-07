"""
HierarchicalOrchestrationManager Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class HierarchicalOrchestrationManager:
    """
    Strategic Orchestration Manager that converts orchestrator redundancy into advantage
    through intelligent coordination, load balancing, and hierarchical processing
    """
    
    def __init__(self):
        # Initialize all orchestrators
        self.orchestrators = {
            OrchestrationLevel.STRATEGIC: UnifiedMetaAIOrchestrator(),
            OrchestrationLevel.TACTICAL: UnifiedAIComponentOrchestrator(),
            OrchestrationLevel.EXECUTION: SwarmAIOrchestrator("hierarchical_swarm", SwarmArchitecture.CONSENSUS),
            OrchestrationLevel.SMARTY: SmartCodingAIOptimized(),
            OrchestrationLevel.QUALITY: AIOrchestrationLayer(),
            OrchestrationLevel.OPERATIONS: AIComponentOrchestrator()
        }
        
        # Orchestrator metadata
        self.orchestrator_metadata = {
            "unified_meta_ai": {
                "level": OrchestrationLevel.STRATEGIC,
                "capabilities": ["governance", "policy", "strategic_planning", "escalation"],
                "specialties": ["high_level_decisions", "compliance", "governance_rules"]
            },
            "unified_ai_component": {
                "level": OrchestrationLevel.TACTICAL,
                "capabilities": ["service_coordination", "workflow", "resource_allocation", "task_routing"],
                "specialties": ["component_management", "workflow_orchestration", "service_integration"]
            },
            "swarm_ai": {
                "level": OrchestrationLevel.EXECUTION,
                "capabilities": ["consensus", "parallel_processing", "collective_intelligence", "multi_agent"],
                "specialties": ["consensus_building", "parallel_execution", "collective_decision_making"]
            },
            "smarty": {
                "level": OrchestrationLevel.SMARTY,
                "capabilities": ["code_completion", "code_generation", "codebase_memory", "pattern_recognition", "multi_language_support", "photographic_memory"],
                "specialties": ["in_line_completions", "context_aware_suggestions", "cross_session_memory", "intelligent_code_analysis", "real_time_validation"]
            },
            "ai_orchestration_layer": {
                "level": OrchestrationLevel.QUALITY,
                "capabilities": ["validation", "compliance", "quality_assurance", "code_analysis"],
                "specialties": ["factual_validation", "consistency_enforcement", "security_validation"]
            },
            "ai_component": {
                "level": OrchestrationLevel.OPERATIONS,
                "capabilities": ["basic_coordination", "monitoring", "lifecycle_management", "operations"],
                "specialties": ["operational_continuity", "basic_coordination", "component_monitoring"]
            }
        }
        
        # Performance tracking
        self.orchestrator_metrics: Dict[str, OrchestratorMetrics] = {}
        self.task_queue = queue.PriorityQueue()
        self.active_tasks: Dict[str, OrchestrationTask] = {}
        self.task_results: Dict[str, OrchestrationResult] = {}
        
        # Configuration
        self.load_balancing_config = LoadBalancingConfig()
        
        # Threading
        self.executor = ThreadPoolExecutor(max_workers=self.load_balancing_config.max_parallel_tasks)
        self.lock = threading.Lock()
        
        # Initialize metrics
        self._initialize_orchestrator_metrics()
        
        logger.info("Hierarchical Orchestration Manager initialized with 5 orchestrator levels")
    
    def _initialize_orchestrator_metrics(self):
        """Initialize performance metrics for all orchestrators"""
        for name, metadata in self.orchestrator_metadata.items():
            self.orchestrator_metrics[name] = OrchestratorMetrics(
                orchestrator_name=name,
                level=metadata["level"]
            )
    
    # ========================================================================
    # INTELLIGENT TASK ROUTING
    # ========================================================================
    
    async def route_task(self, task: OrchestrationTask) -> OrchestrationResult:
        """
        Intelligently route task to appropriate orchestrator(s) based on complexity,
        requirements, and current system load
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Routing task {task.task_id} with complexity {task.complexity}")
            
            # Determine orchestration strategy
            strategy = await self._determine_orchestration_strategy(task)
            
            # Execute based on strategy
            result = await self._execute_orchestration_strategy(task, strategy)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            
            # Update metrics
            await self._update_orchestrator_metrics(result)
            
            logger.info(f"Task {task.task_id} completed with strategy {strategy}")
            return result
            
        except Exception as e:
            logger.error(f"Task routing failed for {task.task_id}", error=str(e))
            return OrchestrationResult(
                task_id=task.task_id,
                success=False,
                error_message=str(e),
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def _determine_orchestration_strategy(self, task: OrchestrationTask) -> OrchestrationStrategy:
        """Determine the best orchestration strategy for a task"""
        
        # Check if consensus is required
        if task.complexity in [TaskComplexity.COMPLEX, TaskComplexity.CRITICAL, TaskComplexity.SUPREME]:
            if task.requirements.get("requires_consensus", False):
                return OrchestrationStrategy.CONSENSUS_VALIDATION
        
        # Check system load for parallel processing
        high_load_orchestrators = [
            name for name, metrics in self.orchestrator_metrics.items()
            if metrics.current_load > self.load_balancing_config.load_threshold
        ]
        
        if len(high_load_orchestrators) >= 2 and task.complexity == TaskComplexity.MODERATE:
            return OrchestrationStrategy.PARALLEL_PROCESSING
        
        # Check if hierarchical processing is beneficial
        if task.complexity in [TaskComplexity.COMPLEX, TaskComplexity.CRITICAL]:
            return OrchestrationStrategy.HIERARCHICAL_CASCADE
        
        # Default to adaptive routing if enabled
        if self.load_balancing_config.adaptive_routing_enabled:
            return OrchestrationStrategy.ADAPTIVE_ROUTING
        
        return OrchestrationStrategy.SINGLE_ORCHESTRATOR
    
    async def _execute_orchestration_strategy(self, task: OrchestrationTask, strategy: OrchestrationStrategy) -> OrchestrationResult:
        """Execute the determined orchestration strategy"""
        
        if strategy == OrchestrationStrategy.SINGLE_ORCHESTRATOR:
            return await self._execute_single_orchestrator(task)
        
        elif strategy == OrchestrationStrategy.PARALLEL_PROCESSING:
            return await self._execute_parallel_processing(task)
        
        elif strategy == OrchestrationStrategy.HIERARCHICAL_CASCADE:
            return await self._execute_hierarchical_cascade(task)
        
        elif strategy == OrchestrationStrategy.CONSENSUS_VALIDATION:
            return await self._execute_consensus_validation(task)
        
        elif strategy == OrchestrationStrategy.ADAPTIVE_ROUTING:
            return await self._execute_adaptive_routing(task)
        
        else:
            return await self._execute_single_orchestrator(task)
    
    # ========================================================================
    # ORCHESTRATION STRATEGY IMPLEMENTATIONS
    # ========================================================================
    
    async def _execute_single_orchestrator(self, task: OrchestrationTask) -> OrchestrationResult:
        """Execute task using single most appropriate orchestrator"""
        
        orchestrator_name, orchestrator = await self._select_best_orchestrator(task)
        
        try:
            # Route to appropriate orchestrator method
            if orchestrator_name == "unified_meta_ai":
                result_data = await orchestrator.start_meta_orchestration(task)
            elif orchestrator_name == "unified_ai_component":
                result_data = await orchestrator.coordinate_components(task)
            elif orchestrator_name == "swarm_ai":
                result_data = await orchestrator.execute_swarm_task(task)
            elif orchestrator_name == "ai_orchestration_layer":
                result_data = await orchestrator.orchestrate_validation(task.task_type, task.requirements)
            else:
                result_data = await orchestrator.orchestrate_task(task)
            
            return OrchestrationResult(
                task_id=task.task_id,
                orchestrator_used=orchestrator_name,
                orchestration_level=self.orchestrator_metadata[orchestrator_name]["level"],
                strategy_used=OrchestrationStrategy.SINGLE_ORCHESTRATOR,
                success=True,
                result_data=result_data,
                confidence_score=0.85
            )
            
        except Exception as e:
            return OrchestrationResult(
                task_id=task.task_id,
                orchestrator_used=orchestrator_name,
                success=False,
                error_message=str(e)
            )
    
    async def _execute_parallel_processing(self, task: OrchestrationTask) -> OrchestrationResult:
        """Execute task using multiple orchestrators in parallel"""
        
        # Select 2-3 orchestrators for parallel processing
        selected_orchestrators = await self._select_parallel_orchestrators(task)
        
        try:
            # Execute in parallel
            tasks = []
            for orchestrator_name, orchestrator in selected_orchestrators.items():
                task_future = asyncio.create_task(
                    self._execute_with_orchestrator(task, orchestrator_name, orchestrator)
                )
                tasks.append((orchestrator_name, task_future))
            
            # Wait for all to complete
            results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
            
            # Combine results
            combined_result = await self._combine_parallel_results(task, results, [t[0] for t in tasks])
            
            return OrchestrationResult(
                task_id=task.task_id,
                orchestrator_used="multiple_parallel",
                strategy_used=OrchestrationStrategy.PARALLEL_PROCESSING,
                success=combined_result["success"],
                result_data=combined_result["data"],
                confidence_score=combined_result["confidence"]
            )
            
        except Exception as e:
            return OrchestrationResult(
                task_id=task.task_id,
                strategy_used=OrchestrationStrategy.PARALLEL_PROCESSING,
                success=False,
                error_message=str(e)
            )
    
    async def _execute_hierarchical_cascade(self, task: OrchestrationTask) -> OrchestrationResult:
        """Execute task flowing through hierarchy levels"""
        
        hierarchy_order = [
            OrchestrationLevel.OPERATIONS,
            OrchestrationLevel.QUALITY,
            OrchestrationLevel.EXECUTION,
            OrchestrationLevel.TACTICAL,
            OrchestrationLevel.STRATEGIC
        ]
        
        try:
            current_result = None
            
            for level in hierarchy_order:
                if current_result and not current_result.get("continue_cascade", True):
                    break
                
                orchestrator_name = self._get_orchestrator_for_level(level)
                orchestrator = self.orchestrators[level]
                
                # Execute with current orchestrator
                level_result = await self._execute_with_orchestrator(task, orchestrator_name, orchestrator)
                
                # Pass result to next level
                if current_result:
                    task.requirements["previous_result"] = current_result
                
                current_result = level_result
                current_result["orchestration_level"] = level.value
            
            return OrchestrationResult(
                task_id=task.task_id,
                orchestrator_used="hierarchical_cascade",
                orchestration_level=OrchestrationLevel.STRATEGIC,
                strategy_used=OrchestrationStrategy.HIERARCHICAL_CASCADE,
                success=current_result.get("success", False),
                result_data=current_result.get("data", {}),
                confidence_score=current_result.get("confidence", 0.0)
            )
            
        except Exception as e:
            return OrchestrationResult(
                task_id=task.task_id,
                strategy_used=OrchestrationStrategy.HIERARCHICAL_CASCADE,
                success=False,
                error_message=str(e)
            )
    
    async def _execute_consensus_validation(self, task: OrchestrationTask) -> OrchestrationResult:
        """Execute task with consensus validation from multiple orchestrators"""
        
        # Select orchestrators for consensus
        consensus_orchestrators = await self._select_consensus_orchestrators(task)
        
        try:
            # Execute with each orchestrator
            results = []
            for orchestrator_name, orchestrator in consensus_orchestrators.items():
                result = await self._execute_with_orchestrator(task, orchestrator_name, orchestrator)
                results.append({
                    "orchestrator": orchestrator_name,
                    "result": result
                })
            
            # Build consensus
            consensus_result = await self._build_consensus(results, task)
            
            return OrchestrationResult(
                task_id=task.task_id,
                orchestrator_used="consensus_validation",
                strategy_used=OrchestrationStrategy.CONSENSUS_VALIDATION,
                success=consensus_result["success"],
                result_data=consensus_result["data"],
                confidence_score=consensus_result["confidence"],
                consensus_reached=consensus_result["consensus_reached"]
            )
            
        except Exception as e:
            return OrchestrationResult(
                task_id=task.task_id,
                strategy_used=OrchestrationStrategy.CONSENSUS_VALIDATION,
                success=False,
                error_message=str(e)
            )
    
    async def _execute_adaptive_routing(self, task: OrchestrationTask) -> OrchestrationResult:
        """Execute task with adaptive routing based on real-time performance"""
        
        # Analyze current system state
        system_state = await self._analyze_system_state()
        
        # Select orchestrator based on adaptive criteria
        orchestrator_name, orchestrator = await self._select_adaptive_orchestrator(task, system_state)
        
        # Execute with selected orchestrator
        return await self._execute_single_orchestrator(task)
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    async def _select_best_orchestrator(self, task: OrchestrationTask) -> Tuple[str, Any]:
        """Select the best orchestrator for a task based on complexity and capabilities"""
        
        # Check if this is a Smarty-specific task
        if await self._is_smarty_task(task):
            return "smarty", self.orchestrators[OrchestrationLevel.SMARTY]
        
        complexity_mapping = {
            TaskComplexity.SIMPLE: OrchestrationLevel.OPERATIONS,
            TaskComplexity.MODERATE: OrchestrationLevel.TACTICAL,
            TaskComplexity.COMPLEX: OrchestrationLevel.EXECUTION,
            TaskComplexity.CRITICAL: OrchestrationLevel.QUALITY,
            TaskComplexity.SUPREME: OrchestrationLevel.STRATEGIC
        }
        
        target_level = complexity_mapping.get(task.complexity, OrchestrationLevel.TACTICAL)
        
        # Find orchestrator with lowest load at target level
        best_orchestrator = None
        best_load = float('inf')
        
        for name, metadata in self.orchestrator_metadata.items():
            if metadata["level"] == target_level:
                metrics = self.orchestrator_metrics[name]
                if metrics.current_load < best_load:
                    best_load = metrics.current_load
                    best_orchestrator = name
        
        if not best_orchestrator:
            # Fallback to any available orchestrator
            best_orchestrator = list(self.orchestrator_metadata.keys())[0]
        
        return best_orchestrator, self.orchestrators[self.orchestrator_metadata[best_orchestrator]["level"]]
    
    async def _is_smarty_task(self, task: OrchestrationTask) -> bool:
        """Determine if this task should be handled by Smarty"""
        
        # Check task type for code-related activities
        smarty_task_types = [
            "code_completion", "code_generation", "code_analysis", "code_review",
            "smart_coding", "inline_completion", "code_suggestion", "pattern_recognition",
            "codebase_memory", "photographic_memory", "cross_session_context",
            "code_validation", "code_optimization", "refactoring", "debugging"
        ]
        
        if task.task_type.lower() in smarty_task_types:
            return True
        
        # Check requirements for code-related keywords
        if task.requirements:
            code_keywords = [
                "code", "programming", "development", "coding", "syntax", "function",
                "class", "method", "variable", "import", "module", "package",
                "api", "endpoint", "database", "schema", "migration", "test",
                "unit_test", "integration_test", "deployment", "build"
            ]
            
            requirements_text = str(task.requirements).lower()
            if any(keyword in requirements_text for keyword in code_keywords):
                return True
        
        # Check for language-specific requirements
        programming_languages = [
            "python", "javascript", "typescript", "java", "csharp", "cpp",
            "go", "rust", "php", "ruby", "swift", "kotlin", "html", "css",
            "sql", "yaml", "json", "markdown"
        ]
        
        if task.requirements:
            req_text = str(task.requirements).lower()
            if any(lang in req_text for lang in programming_languages):
                return True
        
        return False
    
    async def _select_parallel_orchestrators(self, task: OrchestrationTask) -> Dict[str, Any]:
        """Select orchestrators for parallel processing"""
        
        # Select 2-3 orchestrators with different specialties
        selected = {}
        
        # Always include execution orchestrator for consensus
        if OrchestrationLevel.EXECUTION in self.orchestrators:
            selected["swarm_ai"] = self.orchestrators[OrchestrationLevel.EXECUTION]
        
        # Add Smarty for code-related tasks
        if OrchestrationLevel.SMARTY in self.orchestrators and await self._is_smarty_task(task):
            selected["smarty"] = self.orchestrators[OrchestrationLevel.SMARTY]
        
        # Add quality orchestrator for validation
        if OrchestrationLevel.QUALITY in self.orchestrators:
            selected["ai_orchestration_layer"] = self.orchestrators[OrchestrationLevel.QUALITY]
        
        # Add tactical orchestrator for coordination (if not code-focused)
        if OrchestrationLevel.TACTICAL in self.orchestrators and not await self._is_smarty_task(task):
            selected["unified_ai_component"] = self.orchestrators[OrchestrationLevel.TACTICAL]
        
        return selected
    
    async def _execute_with_orchestrator(self, task: OrchestrationTask, orchestrator_name: str, orchestrator: Any) -> Dict[str, Any]:
        """Execute task with specific orchestrator"""
        
        try:
            # Route to appropriate method based on orchestrator
            if orchestrator_name == "unified_meta_ai":
                result = await orchestrator.start_meta_orchestration(task)
            elif orchestrator_name == "unified_ai_component":
                result = await orchestrator.coordinate_components(task)
            elif orchestrator_name == "swarm_ai":
                result = await orchestrator.execute_swarm_task(task)
            elif orchestrator_name == "smarty":
                result = await self._execute_smarty_task(task, orchestrator)
            elif orchestrator_name == "ai_orchestration_layer":
                result = await orchestrator.orchestrate_validation(task.task_type, task.requirements)
            else:
                result = await orchestrator.orchestrate_task(task)
            
            return {
                "success": True,
                "data": result,
                "confidence": 0.85,
                "orchestrator": orchestrator_name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "confidence": 0.0,
                "orchestrator": orchestrator_name
            }
    
    async def _execute_smarty_task(self, task: OrchestrationTask, smarty: SmartCodingAIOptimized) -> Dict[str, Any]:
        """Execute task using Smarty (Smart Coding AI)"""
        
        try:
            # Route to appropriate Smarty method based on task type
            if task.task_type == "code_completion":
                result = await smarty.get_completion(
                    code=task.requirements.get("code", ""),
                    language=task.requirements.get("language", "python"),
                    context=task.requirements.get("context", "")
                )
            elif task.task_type == "code_generation":
                result = await smarty.generate_code(
                    prompt=task.requirements.get("prompt", ""),
                    language=task.requirements.get("language", "python"),
                    context=task.requirements.get("context", {})
                )
            elif task.task_type == "code_analysis":
                result = await smarty.analyze_code(
                    code=task.requirements.get("code", ""),
                    analysis_type=task.requirements.get("analysis_type", "comprehensive")
                )
            elif task.task_type == "codebase_memory":
                result = await smarty.memory_system.analyze_project(
                    project_path=task.requirements.get("project_path", "."),
                    analysis_depth=task.requirements.get("analysis_depth", "comprehensive")
                )
            elif task.task_type == "pattern_recognition":
                result = await smarty.memory_system.recognize_patterns(
                    code=task.requirements.get("code", ""),
                    context=task.requirements.get("context", {})
                )
            elif task.task_type == "cross_session_context":
                result = await smarty.memory_system.get_session_context(
                    session_id=task.requirements.get("session_id", ""),
                    user_id=task.requirements.get("user_id", "")
                )
            else:
                # Generic Smarty task execution
                result = await smarty.process_smart_request(
                    request_type=task.task_type,
                    parameters=task.requirements
                )
            
            return {
                "success": True,
                "data": result,
                "smarty_features": {
                    "photographic_memory": True,
                    "cross_session_context": True,
                    "pattern_recognition": True,
                    "multi_language_support": True
                }
            }
            
        except Exception as e:
            logger.error("Smarty task execution failed", task_type=task.task_type, error=str(e))
            return {
                "success": False,
                "error": str(e),
                "smarty_features": {}
            }
    
    async def _combine_parallel_results(self, task: OrchestrationTask, results: List[Any], orchestrator_names: List[str]) -> Dict[str, Any]:
        """Combine results from parallel orchestrator execution"""
        
        successful_results = [r for r in results if isinstance(r, dict) and r.get("success", False)]
        
        if not successful_results:
            return {
                "success": False,
                "data": {},
                "confidence": 0.0,
                "error": "All parallel orchestrators failed"
            }
        
        # Calculate average confidence
        avg_confidence = sum(r.get("confidence", 0) for r in successful_results) / len(successful_results)
        
        # Combine data (simplified - in practice, you'd have more sophisticated merging)
        combined_data = {}
        for result in successful_results:
            combined_data.update(result.get("data", {}))
        
        return {
            "success": True,
            "data": combined_data,
            "confidence": avg_confidence,
            "orchestrators_used": len(successful_results)
        }
    
    async def _select_consensus_orchestrators(self, task: OrchestrationTask) -> Dict[str, Any]:
        """Select orchestrators for consensus validation"""
        
        # For consensus, we typically want diverse perspectives
        selected = {}
        
        # Include execution orchestrator (swarm intelligence)
        if OrchestrationLevel.EXECUTION in self.orchestrators:
            selected["swarm_ai"] = self.orchestrators[OrchestrationLevel.EXECUTION]
        
        # Include quality orchestrator (validation)
        if OrchestrationLevel.QUALITY in self.orchestrators:
            selected["ai_orchestration_layer"] = self.orchestrators[OrchestrationLevel.QUALITY]
        
        # Include tactical orchestrator (coordination)
        if OrchestrationLevel.TACTICAL in self.orchestrators:
            selected["unified_ai_component"] = self.orchestrators[OrchestrationLevel.TACTICAL]
        
        return selected
    
    async def _build_consensus(self, results: List[Dict[str, Any]], task: OrchestrationTask) -> Dict[str, Any]:
        """Build consensus from multiple orchestrator results"""
        
        successful_results = [r for r in results if r["result"].get("success", False)]
        
        if len(successful_results) < 2:
            return {
                "success": False,
                "consensus_reached": False,
                "data": {},
                "confidence": 0.0,
                "error": "Insufficient successful results for consensus"
            }
        
        # Calculate consensus metrics
        confidences = [r["result"].get("confidence", 0) for r in successful_results]
        avg_confidence = sum(confidences) / len(confidences)
        consensus_threshold = 0.75
        
        consensus_reached = avg_confidence >= consensus_threshold
        
        # Combine results (simplified consensus logic)
        combined_data = {}
        for result in successful_results:
            combined_data.update(result["result"].get("data", {}))
        
        return {
            "success": consensus_reached,
            "consensus_reached": consensus_reached,
            "data": combined_data,
            "confidence": avg_confidence,
            "participants": len(successful_results)
        }
    
    async def _analyze_system_state(self) -> Dict[str, Any]:
        """Analyze current system state for adaptive routing"""
        
        total_tasks = sum(metrics.total_tasks for metrics in self.orchestrator_metrics.values())
        total_success_rate = sum(metrics.success_rate for metrics in self.orchestrator_metrics.values()) / len(self.orchestrator_metrics)
        avg_load = sum(metrics.current_load for metrics in self.orchestrator_metrics.values()) / len(self.orchestrator_metrics)
        
        return {
            "total_tasks": total_tasks,
            "overall_success_rate": total_success_rate,
            "average_load": avg_load,
            "system_health": "good" if total_success_rate > 0.8 and avg_load < 0.8 else "degraded"
        }
    
    async def _select_adaptive_orchestrator(self, task: OrchestrationTask, system_state: Dict[str, Any]) -> Tuple[str, Any]:
        """Select orchestrator based on adaptive criteria"""
        
        # If system health is good, use complexity-based routing
        if system_state["system_health"] == "good":
            return await self._select_best_orchestrator(task)
        
        # If system is degraded, use orchestrator with best current performance
        best_orchestrator = None
        best_performance = 0.0
        
        for name, metrics in self.orchestrator_metrics.items():
            performance_score = metrics.success_rate * (1.0 - metrics.current_load)
            if performance_score > best_performance:
                best_performance = performance_score
                best_orchestrator = name
        
        if not best_orchestrator:
            best_orchestrator = list(self.orchestrator_metadata.keys())[0]
        
        return best_orchestrator, self.orchestrators[self.orchestrator_metadata[best_orchestrator]["level"]]
    
    def _get_orchestrator_for_level(self, level: OrchestrationLevel) -> str:
        """Get orchestrator name for a specific level"""
        
        for name, metadata in self.orchestrator_metadata.items():
            if metadata["level"] == level:
                return name
        
        return list(self.orchestrator_metadata.keys())[0]
    
    async def _update_orchestrator_metrics(self, result: OrchestrationResult):
        """Update performance metrics for orchestrators"""
        
        if result.orchestrator_used in self.orchestrator_metrics:
            metrics = self.orchestrator_metrics[result.orchestrator_used]
            
            metrics.total_tasks += 1
            if result.success:
                metrics.successful_tasks += 1
            else:
                metrics.failed_tasks += 1
            
            # Update running averages
            if metrics.total_tasks > 0:
                metrics.success_rate = metrics.successful_tasks / metrics.total_tasks
            
            # Update execution time average
            if metrics.total_tasks == 1:
                metrics.average_execution_time = result.execution_time
            else:
                metrics.average_execution_time = (
                    (metrics.average_execution_time * (metrics.total_tasks - 1) + result.execution_time) 
                    / metrics.total_tasks
                )
            
            # Update confidence average
            if metrics.total_tasks == 1:
                metrics.average_confidence = result.confidence_score
            else:
                metrics.average_confidence = (
                    (metrics.average_confidence * (metrics.total_tasks - 1) + result.confidence_score) 
                    / metrics.total_tasks
                )
            
            metrics.last_used = result.created_at
    
    # ========================================================================
    # PUBLIC API METHODS
    # ========================================================================
    
    async def submit_task(self, task_type: str, requirements: Dict[str, Any], 
                         complexity: TaskComplexity = TaskComplexity.MODERATE,
                         priority: int = 5, user_id: Optional[str] = None) -> str:
        """Submit a task for hierarchical orchestration"""
        
        task = OrchestrationTask(
            task_type=task_type,
            complexity=complexity,
            requirements=requirements,
            priority=priority,
            user_id=user_id
        )
        
        self.active_tasks[task.task_id] = task
        
        # Execute task asynchronously
        asyncio.create_task(self.route_task(task))
        
        logger.info(f"Task {task.task_id} submitted for hierarchical orchestration")
        return task.task_id
    
    async def get_task_result(self, task_id: str) -> Optional[OrchestrationResult]:
        """Get result for a completed task"""
        return self.task_results.get(task_id)
    
    async def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all orchestrators"""
        
        status = {
            "hierarchical_manager": {
                "active_tasks": len(self.active_tasks),
                "completed_tasks": len(self.task_results),
                "load_balancing_enabled": self.load_balancing_config.adaptive_routing_enabled
            },
            "orchestrators": {}
        }
        
        for name, metrics in self.orchestrator_metrics.items():
            status["orchestrators"][name] = {
                "level": metrics.level.value,
                "total_tasks": metrics.total_tasks,
                "success_rate": metrics.success_rate,
                "average_execution_time": metrics.average_execution_time,
                "average_confidence": metrics.average_confidence,
                "current_load": metrics.current_load,
                "last_used": metrics.last_used.isoformat() if metrics.last_used else None
            }
        
        return status
    
    async def optimize_orchestrator_performance(self) -> Dict[str, Any]:
        """Analyze and optimize orchestrator performance"""
        
        optimization_report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "recommendations": [],
            "performance_insights": {}
        }
        
        # Analyze performance patterns
        for name, metrics in self.orchestrator_metrics.items():
            if metrics.total_tasks > 10:  # Only analyze orchestrators with sufficient data
                
                # Performance insights
                optimization_report["performance_insights"][name] = {
                    "success_rate": metrics.success_rate,
                    "average_execution_time": metrics.average_execution_time,
                    "average_confidence": metrics.average_confidence,
                    "load_efficiency": 1.0 - metrics.current_load
                }
                
                # Generate recommendations
                if metrics.success_rate < 0.8:
                    optimization_report["recommendations"].append({
                        "orchestrator": name,
                        "type": "success_rate_improvement",
                        "description": f"{name} has low success rate ({metrics.success_rate:.2%})",
                        "suggestion": "Review error patterns and improve error handling"
                    })
                
                if metrics.average_execution_time > 5.0:  # More than 5 seconds
                    optimization_report["recommendations"].append({
                        "orchestrator": name,
                        "type": "performance_optimization",
                        "description": f"{name} has high execution time ({metrics.average_execution_time:.2f}s)",
                        "suggestion": "Optimize algorithms or implement caching"
                    })
                
                if metrics.current_load > 0.9:
                    optimization_report["recommendations"].append({
                        "orchestrator": name,
                        "type": "load_balancing",
                        "description": f"{name} is overloaded ({metrics.current_load:.2%})",
                        "suggestion": "Distribute load to other orchestrators or scale horizontally"
                    })
        
        return optimization_report
    
    async def emergency_failover(self, failed_orchestrator: str) -> Dict[str, Any]:
        """Handle emergency failover when an orchestrator fails"""
        
        failover_plan = {
            "failed_orchestrator": failed_orchestrator,
            "failover_timestamp": datetime.now().isoformat(),
            "actions_taken": [],
            "backup_orchestrators": []
        }
        
        # Find backup orchestrators at the same level
        failed_level = self.orchestrator_metadata[failed_orchestrator]["level"]
        
        for name, metadata in self.orchestrator_metadata.items():
            if name != failed_orchestrator and metadata["level"] == failed_level:
                failover_plan["backup_orchestrators"].append({
                    "orchestrator": name,
                    "capabilities": metadata["capabilities"],
                    "current_load": self.orchestrator_metrics[name].current_load
                })
        
        # Select best backup
        if failover_plan["backup_orchestrators"]:
            best_backup = min(
                failover_plan["backup_orchestrators"],
                key=lambda x: x["current_load"]
            )
            
            failover_plan["actions_taken"].append({
                "action": "backup_selection",
                "selected_backup": best_backup["orchestrator"],
                "reason": f"Lowest load ({best_backup['current_load']:.2%})"
            })
        
        # Redirect active tasks
        redirected_tasks = 0
        for task_id, task in self.active_tasks.items():
            if task.requirements.get("orchestrator") == failed_orchestrator:
                # Re-route task to backup orchestrator
                task.requirements["orchestrator"] = best_backup["orchestrator"]
                redirected_tasks += 1
        
        failover_plan["actions_taken"].append({
            "action": "task_redirection",
            "tasks_redirected": redirected_tasks
        })
        
        logger.warning(f"Emergency failover executed for {failed_orchestrator}", 
                      backup=best_backup["orchestrator"] if failover_plan["backup_orchestrators"] else "none",
                      tasks_redirected=redirected_tasks)
        
        return failover_plan
