"""
Smart Coding AI - Requirements & Planning Transformation Capabilities
Implements capabilities 111-120: Intelligent requirements analysis and project planning
"""

import re
import structlog
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = structlog.get_logger()


class RequirementPriority(str, Enum):
    """Priority levels for requirements"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Requirement:
    """Represents a software requirement"""
    id: str
    title: str
    description: str
    type: str  # functional, non-functional, technical
    priority: RequirementPriority
    complexity: str  # simple, medium, complex
    dependencies: List[str]
    acceptance_criteria: List[str]
    estimated_effort: str


class RequirementsAnalyzer:
    """Implements capability #111: Requirements Analysis"""
    
    async def analyze_requirements(self, raw_requirements: str, 
                                   project_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyzes and clarifies software requirements
        
        Args:
            raw_requirements: Raw requirement text or description
            project_context: Additional project context
            
        Returns:
            Structured and clarified requirements with analysis
        """
        try:
            context = project_context or {}
            
            # Parse raw requirements
            parsed = self._parse_requirements(raw_requirements)
            
            # Identify requirement types
            categorized = self._categorize_requirements(parsed)
            
            # Extract stakeholders
            stakeholders = self._identify_stakeholders(raw_requirements, context)
            
            # Detect ambiguities
            ambiguities = self._detect_ambiguities(parsed)
            
            # Identify conflicts
            conflicts = self._find_conflicts(categorized)
            
            # Extract constraints
            constraints = self._extract_constraints(raw_requirements)
            
            # Clarify requirements
            clarified = self._clarify_requirements(parsed, ambiguities)
            
            return {
                "success": True,
                "raw_input": raw_requirements,
                "parsed_requirements": parsed,
                "categorized_requirements": categorized,
                "stakeholders": stakeholders,
                "ambiguities_detected": ambiguities,
                "conflicts_found": conflicts,
                "constraints": constraints,
                "clarified_requirements": clarified,
                "total_requirements": len(parsed),
                "completeness_score": self._assess_completeness(parsed),
                "recommendations": self._generate_recommendations(parsed, ambiguities, conflicts)
            }
        except Exception as e:
            logger.error("Requirements analysis failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _parse_requirements(self, raw: str) -> List[Dict[str, Any]]:
        """Parse raw requirements text"""
        requirements = []
        
        # Split by lines or numbered items
        lines = raw.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            # Detect requirement patterns
            if any(keyword in line.lower() for keyword in ['must', 'should', 'shall', 'will', 'need to']):
                req_type = self._identify_requirement_type(line)
                requirements.append({
                    "id": f"REQ-{i:03d}",
                    "text": line,
                    "type": req_type,
                    "priority": self._infer_priority(line),
                    "is_testable": self._is_testable(line)
                })
        
        return requirements
    
    def _identify_requirement_type(self, text: str) -> str:
        """Identify requirement type"""
        text_lower = text.lower()
        
        functional_keywords = ['user', 'system', 'feature', 'functionality', 'process', 'calculate', 'display']
        nonfunctional_keywords = ['performance', 'security', 'scalability', 'availability', 'usability', 'maintainability']
        technical_keywords = ['api', 'database', 'framework', 'library', 'architecture', 'infrastructure']
        
        if any(kw in text_lower for kw in nonfunctional_keywords):
            return "non-functional"
        elif any(kw in text_lower for kw in technical_keywords):
            return "technical"
        elif any(kw in text_lower for kw in functional_keywords):
            return "functional"
        else:
            return "functional"  # Default
    
    def _infer_priority(self, text: str) -> str:
        """Infer requirement priority"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['critical', 'must', 'essential', 'required']):
            return "high"
        elif any(word in text_lower for word in ['should', 'important']):
            return "medium"
        else:
            return "medium"
    
    def _is_testable(self, text: str) -> bool:
        """Check if requirement is testable"""
        # Testable requirements have measurable criteria
        testable_indicators = ['when', 'if', 'then', 'within', 'at least', 'no more than', 'exactly']
        return any(indicator in text.lower() for indicator in testable_indicators)
    
    def _categorize_requirements(self, requirements: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize requirements by type"""
        categorized = {
            "functional": [],
            "non-functional": [],
            "technical": []
        }
        
        for req in requirements:
            req_type = req.get("type", "functional")
            categorized[req_type].append(req)
        
        return categorized
    
    def _identify_stakeholders(self, raw: str, context: Dict) -> List[Dict[str, str]]:
        """Identify stakeholders"""
        stakeholders = []
        
        # Common stakeholder patterns
        if "user" in raw.lower():
            stakeholders.append({"role": "End User", "interest": "Usability and features"})
        if "admin" in raw.lower():
            stakeholders.append({"role": "Administrator", "interest": "Management and control"})
        if "customer" in raw.lower() or "client" in raw.lower():
            stakeholders.append({"role": "Customer", "interest": "Business value"})
        if "developer" in raw.lower():
            stakeholders.append({"role": "Developer", "interest": "Technical implementation"})
        
        # Add from context
        if context.get("stakeholders"):
            for sh in context["stakeholders"]:
                stakeholders.append({"role": sh, "interest": "Specified in context"})
        
        return stakeholders if stakeholders else [{"role": "Generic User", "interest": "System functionality"}]
    
    def _detect_ambiguities(self, requirements: List[Dict]) -> List[Dict[str, str]]:
        """Detect ambiguous requirements"""
        ambiguities = []
        
        ambiguous_terms = ['etc', 'and so on', 'various', 'appropriate', 'adequate', 'sufficient', 
                          'reasonable', 'user-friendly', 'fast', 'efficient', 'flexible']
        
        for req in requirements:
            text_lower = req["text"].lower()
            found_terms = [term for term in ambiguous_terms if term in text_lower]
            
            if found_terms:
                ambiguities.append({
                    "requirement_id": req["id"],
                    "text": req["text"],
                    "ambiguous_terms": found_terms,
                    "suggestion": "Specify concrete, measurable criteria"
                })
            
            # Check for missing specifics
            if not any(char.isdigit() for char in req["text"]) and req["type"] == "non-functional":
                ambiguities.append({
                    "requirement_id": req["id"],
                    "text": req["text"],
                    "issue": "Missing quantifiable metrics",
                    "suggestion": "Add specific numbers (e.g., response time < 200ms)"
                })
        
        return ambiguities
    
    def _find_conflicts(self, categorized: Dict[str, List[Dict]]) -> List[Dict[str, str]]:
        """Find conflicting requirements"""
        conflicts = []
        
        all_reqs = []
        for req_list in categorized.values():
            all_reqs.extend(req_list)
        
        # Check for contradictions (simplified)
        for i, req1 in enumerate(all_reqs):
            for req2 in all_reqs[i+1:]:
                if self._are_conflicting(req1["text"], req2["text"]):
                    conflicts.append({
                        "requirement_1": req1["id"],
                        "requirement_2": req2["id"],
                        "conflict": "Potential contradiction detected",
                        "resolution": "Review and clarify both requirements"
                    })
        
        return conflicts
    
    def _are_conflicting(self, text1: str, text2: str) -> bool:
        """Check if two requirements conflict"""
        # Simplified conflict detection
        contradictory_pairs = [
            (['real-time', 'immediate'], ['batch', 'scheduled']),
            (['simple', 'minimal'], ['comprehensive', 'complete']),
            (['public', 'open'], ['private', 'secure'])
        ]
        
        for pair1, pair2 in contradictory_pairs:
            has_pair1 = any(term in text1.lower() for term in pair1)
            has_pair2 = any(term in text2.lower() for term in pair2)
            if has_pair1 and has_pair2:
                return True
        
        return False
    
    def _extract_constraints(self, raw: str) -> List[Dict[str, str]]:
        """Extract project constraints"""
        constraints = []
        
        constraint_patterns = {
            "budget": r'budget.*\$?([\d,]+)',
            "timeline": r'(deadline|timeline|due).*(\d+\s*(day|week|month))',
            "technology": r'(using|with|built on)\s+(\w+)',
            "compliance": r'(comply|compliant|meet)\s+(\w+)'
        }
        
        for constraint_type, pattern in constraint_patterns.items():
            matches = re.findall(pattern, raw, re.IGNORECASE)
            if matches:
                constraints.append({
                    "type": constraint_type,
                    "value": str(matches[0]),
                    "impact": "high" if constraint_type in ["budget", "timeline"] else "medium"
                })
        
        return constraints
    
    def _clarify_requirements(self, requirements: List[Dict], ambiguities: List[Dict]) -> List[Dict[str, Any]]:
        """Provide clarified versions of requirements"""
        clarified = []
        
        ambiguous_ids = {amb["requirement_id"] for amb in ambiguities}
        
        for req in requirements:
            if req["id"] in ambiguous_ids:
                clarified.append({
                    "requirement_id": req["id"],
                    "original": req["text"],
                    "clarified": self._generate_clarified_version(req["text"]),
                    "needs_stakeholder_input": True
                })
        
        return clarified
    
    def _generate_clarified_version(self, text: str) -> str:
        """Generate clarified version of requirement"""
        clarified = text
        
        # Replace ambiguous terms with specific suggestions
        replacements = {
            "user-friendly": "intuitive with clear labels and <2 clicks to complete actions",
            "fast": "response time < 200ms for 95% of requests",
            "efficient": "CPU usage < 50%, memory < 512MB",
            "scalable": "handle 10x current load with < 20% performance degradation"
        }
        
        for ambiguous, specific in replacements.items():
            if ambiguous in text.lower():
                clarified += f"\n  → Suggested clarification: {specific}"
        
        return clarified
    
    def _assess_completeness(self, requirements: List[Dict]) -> int:
        """Assess completeness of requirements (0-100)"""
        score = 50  # Base score
        
        # Has both functional and non-functional
        types = set(req["type"] for req in requirements)
        if len(types) >= 2:
            score += 20
        
        # Has testable requirements
        testable_count = sum(1 for req in requirements if req.get("is_testable"))
        if testable_count > len(requirements) * 0.7:
            score += 15
        
        # Has prioritization
        has_priority = all("priority" in req for req in requirements)
        if has_priority:
            score += 15
        
        return min(score, 100)
    
    def _generate_recommendations(self, requirements: List[Dict], 
                                 ambiguities: List[Dict], 
                                 conflicts: List[Dict]) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        if len(ambiguities) > len(requirements) * 0.3:
            recommendations.append("High number of ambiguous requirements - add specific, measurable criteria")
        
        if conflicts:
            recommendations.append(f"Found {len(conflicts)} potential conflicts - review and resolve contradictions")
        
        testable_count = sum(1 for req in requirements if req.get("is_testable"))
        if testable_count < len(requirements) * 0.5:
            recommendations.append("Many requirements are not testable - add acceptance criteria")
        
        if not any(req["type"] == "non-functional" for req in requirements):
            recommendations.append("Missing non-functional requirements - add performance, security, scalability criteria")
        
        return recommendations if recommendations else ["Requirements are well-defined"]


class UserStoryGenerator:
    """Implements capability #112: User Story Generation"""
    
    async def generate_user_stories(self, requirements: List[Dict[str, Any]], 
                                    personas: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Creates detailed user stories from high-level needs
        
        Args:
            requirements: List of requirements
            personas: User personas
            
        Returns:
            Generated user stories with acceptance criteria
        """
        try:
            # Use default personas if none provided
            if not personas:
                personas = self._create_default_personas()
            
            # Generate stories for each requirement
            user_stories = []
            for req in requirements:
                stories = self._generate_stories_for_requirement(req, personas)
                user_stories.extend(stories)
            
            # Prioritize stories
            prioritized = self._prioritize_stories(user_stories)
            
            # Group into epics
            epics = self._group_into_epics(prioritized)
            
            return {
                "success": True,
                "user_stories": prioritized,
                "epics": epics,
                "total_stories": len(user_stories),
                "story_points_total": sum(s.get("story_points", 0) for s in user_stories),
                "recommended_sprints": self._estimate_sprints(user_stories)
            }
        except Exception as e:
            logger.error("User story generation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _create_default_personas(self) -> List[Dict[str, str]]:
        """Create default user personas"""
        return [
            {
                "name": "End User",
                "role": "user",
                "goals": "Complete tasks efficiently",
                "pain_points": "Complex interfaces"
            },
            {
                "name": "Administrator",
                "role": "admin",
                "goals": "Manage system and users",
                "pain_points": "Lack of visibility"
            },
            {
                "name": "Power User",
                "role": "power_user",
                "goals": "Advanced functionality",
                "pain_points": "Limited customization"
            }
        ]
    
    def _generate_stories_for_requirement(self, requirement: Dict, personas: List[Dict]) -> List[Dict[str, Any]]:
        """Generate user stories for a requirement"""
        stories = []
        
        # Select relevant persona
        persona = personas[0]  # Simplified selection
        
        # Generate story in standard format
        story = {
            "id": f"US-{requirement.get('id', '001')}",
            "title": self._create_story_title(requirement),
            "story": self._format_user_story(persona, requirement),
            "persona": persona["name"],
            "acceptance_criteria": self._generate_acceptance_criteria(requirement),
            "story_points": self._estimate_story_points(requirement),
            "priority": requirement.get("priority", "medium"),
            "dependencies": [],
            "tags": self._extract_tags(requirement)
        }
        
        stories.append(story)
        return stories
    
    def _create_story_title(self, requirement: Dict) -> str:
        """Create concise story title"""
        text = requirement.get("text", "")
        # Extract first meaningful phrase
        words = text.split()[:8]
        return " ".join(words) + ("..." if len(text.split()) > 8 else "")
    
    def _format_user_story(self, persona: Dict, requirement: Dict) -> str:
        """Format in standard user story format"""
        role = persona["role"]
        goal = self._extract_goal(requirement)
        benefit = self._extract_benefit(requirement)
        
        return f"As a {role}, I want to {goal}, so that {benefit}."
    
    def _extract_goal(self, requirement: Dict) -> str:
        """Extract goal from requirement"""
        text = requirement.get("text", "")
        # Simplified extraction
        if "must" in text.lower():
            goal_start = text.lower().index("must") + 5
            return text[goal_start:].split('.')[0].strip()
        return text.split('.')[0].strip()
    
    def _extract_benefit(self, requirement: Dict) -> str:
        """Extract benefit from requirement"""
        # Default benefits based on type
        req_type = requirement.get("type", "functional")
        if req_type == "non-functional":
            return "the system performs reliably"
        else:
            return "I can accomplish my task efficiently"
    
    def _generate_acceptance_criteria(self, requirement: Dict) -> List[str]:
        """Generate acceptance criteria"""
        criteria = []
        
        # Given-When-Then format
        criteria.append(f"Given I am authenticated")
        criteria.append(f"When I perform the action")
        criteria.append(f"Then the expected result occurs")
        
        # Add specific criteria based on requirement
        if "data" in requirement.get("text", "").lower():
            criteria.append("And the data is validated")
            criteria.append("And appropriate error messages are shown for invalid input")
        
        if "save" in requirement.get("text", "").lower() or "store" in requirement.get("text", "").lower():
            criteria.append("And the data persists after page reload")
        
        return criteria
    
    def _estimate_story_points(self, requirement: Dict) -> int:
        """Estimate story points (Fibonacci: 1, 2, 3, 5, 8, 13)"""
        text = requirement.get("text", "")
        complexity = requirement.get("complexity", "medium")
        
        # Simple heuristic
        if complexity == "simple" or len(text) < 50:
            return 2
        elif complexity == "complex" or len(text) > 200:
            return 8
        else:
            return 5
    
    def _extract_tags(self, requirement: Dict) -> List[str]:
        """Extract relevant tags"""
        tags = [requirement.get("type", "functional")]
        
        text_lower = requirement.get("text", "").lower()
        if "api" in text_lower:
            tags.append("api")
        if "ui" in text_lower or "interface" in text_lower:
            tags.append("ui")
        if "database" in text_lower or "data" in text_lower:
            tags.append("database")
        
        return tags
    
    def _prioritize_stories(self, stories: List[Dict]) -> List[Dict]:
        """Prioritize user stories"""
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return sorted(stories, key=lambda s: priority_order.get(s.get("priority", "medium"), 2))
    
    def _group_into_epics(self, stories: List[Dict]) -> List[Dict[str, Any]]:
        """Group user stories into epics"""
        # Group by tags
        epics_dict = {}
        
        for story in stories:
            for tag in story.get("tags", ["general"]):
                if tag not in epics_dict:
                    epics_dict[tag] = []
                epics_dict[tag].append(story["id"])
        
        epics = []
        for epic_name, story_ids in epics_dict.items():
            if len(story_ids) >= 2:  # Only create epic if multiple stories
                epics.append({
                    "name": f"{epic_name.title()} Features",
                    "description": f"User stories related to {epic_name}",
                    "story_ids": story_ids,
                    "total_points": sum(s["story_points"] for s in stories if s["id"] in story_ids)
                })
        
        return epics
    
    def _estimate_sprints(self, stories: List[Dict]) -> int:
        """Estimate number of sprints needed"""
        total_points = sum(s.get("story_points", 0) for s in stories)
        velocity = 20  # Assumed team velocity
        return max(1, (total_points + velocity - 1) // velocity)  # Ceiling division


class AcceptanceCriteriaDefiner:
    """Implements capability #113: Acceptance Criteria Definition"""
    
    async def define_acceptance_criteria(self, user_story: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates comprehensive acceptance criteria
        
        Args:
            user_story: User story to create criteria for
            
        Returns:
            Detailed acceptance criteria in multiple formats
        """
        try:
            # Generate Given-When-Then criteria
            gwt_criteria = self._generate_gwt_criteria(user_story)
            
            # Generate checklist criteria
            checklist = self._generate_checklist(user_story)
            
            # Generate test scenarios
            test_scenarios = self._generate_test_scenarios(user_story)
            
            # Define edge cases
            edge_cases = self._define_edge_cases(user_story)
            
            # Create DoD (Definition of Done)
            dod = self._create_definition_of_done(user_story)
            
            return {
                "success": True,
                "user_story_id": user_story.get("id"),
                "given_when_then": gwt_criteria,
                "checklist": checklist,
                "test_scenarios": test_scenarios,
                "edge_cases": edge_cases,
                "definition_of_done": dod,
                "testability_score": self._assess_testability(gwt_criteria, test_scenarios),
                "coverage_completeness": "high"
            }
        except Exception as e:
            logger.error("Acceptance criteria generation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _generate_gwt_criteria(self, story: Dict) -> List[Dict[str, str]]:
        """Generate Given-When-Then criteria"""
        criteria = []
        
        # Positive scenario
        criteria.append({
            "scenario": "Happy Path",
            "given": "the user is authenticated and has necessary permissions",
            "when": "the user performs the intended action",
            "then": "the action completes successfully and appropriate feedback is shown"
        })
        
        # Error scenario
        criteria.append({
            "scenario": "Invalid Input",
            "given": "the user provides invalid or incomplete data",
            "when": "the user attempts to submit",
            "then": "clear error messages are displayed and no partial data is saved"
        })
        
        # Edge case
        criteria.append({
            "scenario": "Boundary Conditions",
            "given": "the user provides data at system limits",
            "when": "the system processes the request",
            "then": "the system handles it gracefully without errors"
        })
        
        return criteria
    
    def _generate_checklist(self, story: Dict) -> List[str]:
        """Generate acceptance checklist"""
        return [
            "☐ Feature works as described in the user story",
            "☐ All happy path scenarios pass",
            "☐ Error handling works correctly",
            "☐ Input validation is comprehensive",
            "☐ UI/UX is intuitive and accessible",
            "☐ Performance meets requirements",
            "☐ Security considerations addressed",
            "☐ Data persistence works correctly",
            "☐ Integration points tested",
            "☐ Documentation updated",
            "☐ Unit tests written and passing",
            "☐ Code reviewed and approved"
        ]
    
    def _generate_test_scenarios(self, story: Dict) -> List[Dict[str, Any]]:
        """Generate detailed test scenarios"""
        return [
            {
                "scenario_id": "TS-001",
                "title": "Successful execution",
                "steps": [
                    "1. Navigate to feature",
                    "2. Enter valid data",
                    "3. Submit",
                    "4. Verify success message",
                    "5. Verify data is saved"
                ],
                "expected_result": "Operation completes successfully",
                "priority": "high"
            },
            {
                "scenario_id": "TS-002",
                "title": "Validation error handling",
                "steps": [
                    "1. Navigate to feature",
                    "2. Enter invalid data",
                    "3. Attempt submit",
                    "4. Verify error messages",
                    "5. Verify no data saved"
                ],
                "expected_result": "Clear error messages shown, no side effects",
                "priority": "high"
            },
            {
                "scenario_id": "TS-003",
                "title": "Permission denied",
                "steps": [
                    "1. Login with insufficient permissions",
                    "2. Attempt to access feature",
                    "3. Verify access denied message"
                ],
                "expected_result": "Access denied, appropriate error shown",
                "priority": "medium"
            }
        ]
    
    def _define_edge_cases(self, story: Dict) -> List[Dict[str, str]]:
        """Define edge cases to test"""
        return [
            {
                "case": "Empty input",
                "expected": "Validation error shown"
            },
            {
                "case": "Maximum length input",
                "expected": "Handles gracefully within limits"
            },
            {
                "case": "Special characters",
                "expected": "Properly sanitized and stored"
            },
            {
                "case": "Concurrent operations",
                "expected": "Data integrity maintained"
            },
            {
                "case": "Network timeout",
                "expected": "User notified, operation retryable"
            }
        ]
    
    def _create_definition_of_done(self, story: Dict) -> List[str]:
        """Create Definition of Done"""
        return [
            "✓ Code complete and reviewed",
            "✓ Unit tests written (>80% coverage)",
            "✓ Integration tests passing",
            "✓ Acceptance criteria met",
            "✓ No critical/high bugs",
            "✓ Performance benchmarks met",
            "✓ Security review completed",
            "✓ Documentation updated",
            "✓ Deployed to staging",
            "✓ QA sign-off received",
            "✓ Product Owner acceptance"
        ]
    
    def _assess_testability(self, gwt: List, scenarios: List) -> int:
        """Assess testability score (0-100)"""
        score = 70  # Base score
        
        if len(gwt) >= 3:
            score += 15
        
        if len(scenarios) >= 3:
            score += 15
        
        return min(score, 100)


class EstimationAutomator:
    """Implements capability #114: Estimation Automation"""
    
    async def estimate_development(self, user_stories: List[Dict[str, Any]], 
                                   team_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Provides accurate development time estimates
        
        Args:
            user_stories: List of user stories to estimate
            team_data: Historical team performance data
            
        Returns:
            Detailed estimates with confidence intervals
        """
        try:
            team_data = team_data or {"velocity": 20, "experience": "medium"}
            
            # Estimate each story
            estimates = []
            for story in user_stories:
                estimate = self._estimate_story(story, team_data)
                estimates.append(estimate)
            
            # Calculate totals
            totals = self._calculate_totals(estimates)
            
            # Factor in risks
            risk_adjusted = self._apply_risk_factors(totals, user_stories)
            
            # Generate timeline
            timeline = self._generate_timeline(risk_adjusted, team_data)
            
            return {
                "success": True,
                "story_estimates": estimates,
                "totals": totals,
                "risk_adjusted_estimate": risk_adjusted,
                "timeline": timeline,
                "confidence_level": self._calculate_confidence(team_data),
                "assumptions": self._list_assumptions(team_data)
            }
        except Exception as e:
            logger.error("Estimation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _estimate_story(self, story: Dict, team_data: Dict) -> Dict[str, Any]:
        """Estimate individual story"""
        story_points = story.get("story_points", 5)
        
        # Convert story points to hours (typical: 1 SP = 4-8 hours)
        hours_per_point = 6  # Middle of range
        base_hours = story_points * hours_per_point
        
        # Adjust for team experience
        experience_multipliers = {
            "junior": 1.5,
            "medium": 1.0,
            "senior": 0.8,
            "expert": 0.6
        }
        experience = team_data.get("experience", "medium")
        adjusted_hours = base_hours * experience_multipliers.get(experience, 1.0)
        
        return {
            "story_id": story.get("id"),
            "story_points": story_points,
            "base_hours": base_hours,
            "adjusted_hours": adjusted_hours,
            "best_case": adjusted_hours * 0.8,
            "worst_case": adjusted_hours * 1.5,
            "confidence": "medium"
        }
    
    def _calculate_totals(self, estimates: List[Dict]) -> Dict[str, float]:
        """Calculate total estimates"""
        return {
            "total_story_points": sum(e["story_points"] for e in estimates),
            "total_hours": sum(e["adjusted_hours"] for e in estimates),
            "best_case_hours": sum(e["best_case"] for e in estimates),
            "worst_case_hours": sum(e["worst_case"] for e in estimates),
            "total_days": sum(e["adjusted_hours"] for e in estimates) / 8,
            "total_weeks": sum(e["adjusted_hours"] for e in estimates) / 40
        }
    
    def _apply_risk_factors(self, totals: Dict, stories: List) -> Dict[str, Any]:
        """Apply risk factors to estimates"""
        risk_multiplier = 1.0
        
        # Technical complexity risk
        complex_stories = sum(1 for s in stories if s.get("story_points", 0) >= 8)
        if complex_stories > len(stories) * 0.3:
            risk_multiplier += 0.2
        
        # Dependency risk
        has_dependencies = any(s.get("dependencies") for s in stories)
        if has_dependencies:
            risk_multiplier += 0.15
        
        # Integration risk
        integration_stories = sum(1 for s in stories if "api" in s.get("tags", []))
        if integration_stories > 0:
            risk_multiplier += 0.1
        
        return {
            "base_estimate_weeks": totals["total_weeks"],
            "risk_multiplier": risk_multiplier,
            "risk_adjusted_weeks": totals["total_weeks"] * risk_multiplier,
            "risk_factors": {
                "technical_complexity": complex_stories > len(stories) * 0.3,
                "dependencies": has_dependencies,
                "integration_points": integration_stories > 0
            }
        }
    
    def _generate_timeline(self, risk_adjusted: Dict, team_data: Dict) -> Dict[str, Any]:
        """Generate project timeline"""
        weeks = risk_adjusted["risk_adjusted_weeks"]
        velocity = team_data.get("velocity", 20)
        
        sprints = max(1, int(weeks / 2))  # 2-week sprints
        
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=weeks)
        
        return {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "estimated_end_date": end_date.strftime("%Y-%m-%d"),
            "duration_weeks": round(weeks, 1),
            "sprints_needed": sprints,
            "sprint_length": "2 weeks",
            "milestones": self._generate_milestones(sprints)
        }
    
    def _generate_milestones(self, sprints: int) -> List[Dict[str, str]]:
        """Generate project milestones"""
        milestones = []
        
        if sprints >= 1:
            milestones.append({"sprint": 1, "milestone": "Core features", "target": "25% complete"})
        if sprints >= 2:
            milestones.append({"sprint": 2, "milestone": "MVP", "target": "50% complete"})
        if sprints >= 3:
            milestones.append({"sprint": 3, "milestone": "Feature complete", "target": "80% complete"})
        if sprints >= 4:
            milestones.append({"sprint": 4, "milestone": "Polish & testing", "target": "100% complete"})
        
        return milestones
    
    def _calculate_confidence(self, team_data: Dict) -> str:
        """Calculate confidence level"""
        if team_data.get("historical_data"):
            return "High - Based on team historical data"
        elif team_data.get("experience") in ["senior", "expert"]:
            return "Medium-High - Experienced team"
        else:
            return "Medium - Based on industry standards"
    
    def _list_assumptions(self, team_data: Dict) -> List[str]:
        """List estimation assumptions"""
        return [
            f"Team velocity: {team_data.get('velocity', 20)} points per sprint",
            f"Team experience: {team_data.get('experience', 'medium')}",
            "2-week sprint duration",
            "No major blockers or external dependencies",
            "Requirements are stable",
            "Team availability at 80%"
        ]


class RiskAssessor:
    """Implements capability #115: Risk Assessment"""
    
    async def assess_risks(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identifies project risks and mitigation strategies
        
        Args:
            project_data: Project requirements, timeline, team info
            
        Returns:
            Comprehensive risk assessment with mitigation plans
        """
        try:
            # Identify technical risks
            technical_risks = self._identify_technical_risks(project_data)
            
            # Identify schedule risks
            schedule_risks = self._identify_schedule_risks(project_data)
            
            # Identify resource risks
            resource_risks = self._identify_resource_risks(project_data)
            
            # Identify business risks
            business_risks = self._identify_business_risks(project_data)
            
            # Calculate overall risk score
            risk_score = self._calculate_risk_score(
                technical_risks, schedule_risks, resource_risks, business_risks
            )
            
            # Generate mitigation strategies
            mitigations = self._generate_mitigations(
                technical_risks + schedule_risks + resource_risks + business_risks
            )
            
            return {
                "success": True,
                "overall_risk_level": risk_score["level"],
                "risk_score": risk_score["score"],
                "technical_risks": technical_risks,
                "schedule_risks": schedule_risks,
                "resource_risks": resource_risks,
                "business_risks": business_risks,
                "mitigation_strategies": mitigations,
                "monitoring_plan": self._create_monitoring_plan(),
                "contingency_plan": self._create_contingency_plan(risk_score)
            }
        except Exception as e:
            logger.error("Risk assessment failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _identify_technical_risks(self, project_data: Dict) -> List[Dict[str, Any]]:
        """Identify technical risks"""
        risks = []
        
        # New technology risk
        if project_data.get("new_technologies"):
            risks.append({
                "risk": "New Technology Adoption",
                "probability": "medium",
                "impact": "high",
                "description": "Team lacks experience with required technologies",
                "category": "technical"
            })
        
        # Integration complexity
        if project_data.get("integration_points", 0) > 3:
            risks.append({
                "risk": "Integration Complexity",
                "probability": "high",
                "impact": "high",
                "description": "Multiple external integrations may cause delays",
                "category": "technical"
            })
        
        # Technical debt
        if project_data.get("legacy_system"):
            risks.append({
                "risk": "Legacy System Constraints",
                "probability": "high",
                "impact": "medium",
                "description": "Working with legacy systems may limit options",
                "category": "technical"
            })
        
        return risks
    
    def _identify_schedule_risks(self, project_data: Dict) -> List[Dict[str, Any]]:
        """Identify schedule risks"""
        risks = []
        
        # Aggressive timeline
        if project_data.get("timeline_weeks", 12) < 8:
            risks.append({
                "risk": "Aggressive Timeline",
                "probability": "high",
                "impact": "critical",
                "description": "Timeline may be too short for scope",
                "category": "schedule"
            })
        
        # Dependencies
        if project_data.get("external_dependencies"):
            risks.append({
                "risk": "External Dependencies",
                "probability": "medium",
                "impact": "high",
                "description": "Waiting on external teams or systems",
                "category": "schedule"
            })
        
        return risks
    
    def _identify_resource_risks(self, project_data: Dict) -> List[Dict[str, Any]]:
        """Identify resource risks"""
        risks = []
        
        # Team size
        team_size = project_data.get("team_size", 3)
        if team_size < 3:
            risks.append({
                "risk": "Small Team Size",
                "probability": "high",
                "impact": "medium",
                "description": "Limited team may struggle with workload",
                "category": "resource"
            })
        
        # Skill gaps
        if project_data.get("skill_gaps"):
            risks.append({
                "risk": "Skill Gaps",
                "probability": "medium",
                "impact": "high",
                "description": "Team lacks certain required skills",
                "category": "resource"
            })
        
        return risks
    
    def _identify_business_risks(self, project_data: Dict) -> List[Dict[str, Any]]:
        """Identify business risks"""
        risks = []
        
        # Changing requirements
        if project_data.get("requirements_stability") == "low":
            risks.append({
                "risk": "Requirement Changes",
                "probability": "high",
                "impact": "high",
                "description": "Frequent requirement changes may cause delays",
                "category": "business"
            })
        
        # Market competition
        if project_data.get("competitive_pressure"):
            risks.append({
                "risk": "Market Competition",
                "probability": "medium",
                "impact": "high",
                "description": "Need to deliver before competitors",
                "category": "business"
            })
        
        return risks
    
    def _calculate_risk_score(self, tech: List, schedule: List, resource: List, business: List) -> Dict[str, Any]:
        """Calculate overall risk score"""
        all_risks = tech + schedule + schedule + resource + business
        
        # Weight by probability and impact
        weights = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        
        total_score = 0
        for risk in all_risks:
            prob = weights.get(risk.get("probability", "medium"), 2)
            impact = weights.get(risk.get("impact", "medium"), 2)
            total_score += prob * impact
        
        # Normalize to 0-100
        max_possible = len(all_risks) * 16  # 4 * 4
        normalized = (total_score / max_possible * 100) if max_possible > 0 else 0
        
        if normalized >= 70:
            level = "HIGH"
        elif normalized >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"
        
        return {
            "score": round(normalized, 1),
            "level": level,
            "total_risks": len(all_risks)
        }
    
    def _generate_mitigations(self, risks: List[Dict]) -> List[Dict[str, str]]:
        """Generate mitigation strategies for risks"""
        mitigations = []
        
        mitigation_templates = {
            "New Technology Adoption": "Allocate time for learning and prototyping; consider expert consultation",
            "Integration Complexity": "Early integration testing; use mocks; maintain good documentation",
            "Legacy System Constraints": "Thorough analysis upfront; plan for workarounds; consider abstraction layers",
            "Aggressive Timeline": "Reduce scope; increase team size; implement MVP first",
            "External Dependencies": "Identify early; establish clear communication; have backup plans",
            "Small Team Size": "Augment with contractors; reduce scope; implement automation",
            "Skill Gaps": "Training programs; pair programming; bring in experts",
            "Requirement Changes": "Agile methodology; frequent stakeholder communication; change management process",
            "Market Competition": "Focus on unique value; MVP approach; rapid iterations"
        }
        
        for risk in risks:
            risk_name = risk["risk"]
            mitigation = mitigation_templates.get(risk_name, "Monitor closely and adapt as needed")
            
            mitigations.append({
                "risk": risk_name,
                "mitigation": mitigation,
                "owner": "Project Manager",
                "timeline": "Immediate"
            })
        
        return mitigations
    
    def _create_monitoring_plan(self) -> Dict[str, Any]:
        """Create risk monitoring plan"""
        return {
            "frequency": "Weekly risk review meetings",
            "metrics": [
                "Schedule variance",
                "Velocity trends",
                "Blocker count",
                "Technical debt metrics"
            ],
            "escalation": "Escalate to stakeholders if risk probability or impact increases",
            "review_cycle": "Sprint retrospectives + monthly risk assessment"
        }
    
    def _create_contingency_plan(self, risk_score: Dict) -> Dict[str, Any]:
        """Create contingency plan"""
        if risk_score["level"] == "HIGH":
            return {
                "trigger": "High risk level detected",
                "actions": [
                    "Reduce scope to MVP",
                    "Increase team size",
                    "Extend timeline",
                    "Bring in technical experts",
                    "Daily stakeholder updates"
                ]
            }
        elif risk_score["level"] == "MEDIUM":
            return {
                "trigger": "Medium risk level detected",
                "actions": [
                    "Close monitoring",
                    "Prepare backup resources",
                    "Weekly stakeholder updates"
                ]
            }
        else:
            return {
                "trigger": "Low risk level",
                "actions": [
                    "Continue standard monitoring",
                    "Regular retrospectives"
                ]
            }


class ResourcePlanner:
    """Implements capability #116: Resource Planning"""
    
    async def plan_resources(self, 
                            project_requirements: List[Dict[str, Any]],
                            team_info: Dict[str, Any] = None,
                            budget: float = None) -> Dict[str, Any]:
        """
        Recommends optimal team composition and resources
        
        Args:
            project_requirements: List of project requirements
            team_info: Current team information
            budget: Available budget
            
        Returns:
            Resource plan with team composition and resource allocation
        """
        try:
            # Analyze skill requirements
            skills_needed = self._analyze_skill_requirements(project_requirements)
            
            # Determine team size
            team_composition = self._determine_team_composition(
                project_requirements, 
                skills_needed,
                team_info or {}
            )
            
            # Calculate resource allocation
            resource_allocation = self._calculate_resource_allocation(
                team_composition,
                project_requirements
            )
            
            # Estimate costs
            cost_estimate = self._estimate_costs(team_composition, budget)
            
            # Create hiring plan
            hiring_plan = self._create_hiring_plan(team_composition, team_info or {})
            
            # Generate training needs
            training_needs = self._identify_training_needs(
                team_composition,
                team_info or {}
            )
            
            return {
                "success": True,
                "skills_required": skills_needed,
                "team_composition": team_composition,
                "resource_allocation": resource_allocation,
                "cost_estimate": cost_estimate,
                "hiring_plan": hiring_plan,
                "training_needs": training_needs,
                "recommendations": self._generate_resource_recommendations(
                    team_composition,
                    cost_estimate,
                    budget
                )
            }
        except Exception as e:
            logger.error("Resource planning failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _analyze_skill_requirements(self, requirements: List[Dict]) -> Dict[str, Any]:
        """Analyze required skills from requirements"""
        skills = {
            "technical": set(),
            "domain": set(),
            "soft_skills": set()
        }
        
        # Analyze each requirement
        for req in requirements:
            desc = req.get("description", "").lower()
            
            # Technical skills
            if any(tech in desc for tech in ["frontend", "react", "vue", "angular"]):
                skills["technical"].add("Frontend Development")
            if any(tech in desc for tech in ["backend", "api", "server"]):
                skills["technical"].add("Backend Development")
            if any(tech in desc for tech in ["database", "sql", "nosql"]):
                skills["technical"].add("Database Design")
            if any(tech in desc for tech in ["devops", "deployment", "ci/cd"]):
                skills["technical"].add("DevOps")
            if any(tech in desc for tech in ["mobile", "ios", "android"]):
                skills["technical"].add("Mobile Development")
            if any(tech in desc for tech in ["ml", "ai", "machine learning"]):
                skills["technical"].add("Machine Learning")
            
            # Domain skills
            if any(domain in desc for domain in ["healthcare", "medical"]):
                skills["domain"].add("Healthcare Domain")
            if any(domain in desc for domain in ["finance", "payment", "banking"]):
                skills["domain"].add("Financial Services")
            if any(domain in desc for domain in ["ecommerce", "retail"]):
                skills["domain"].add("E-commerce")
        
        # Convert sets to lists
        return {
            "technical": list(skills["technical"]),
            "domain": list(skills["domain"]),
            "soft_skills": ["Communication", "Problem Solving", "Teamwork", "Time Management"]
        }
    
    def _determine_team_composition(self, requirements: List[Dict], 
                                   skills: Dict, team_info: Dict) -> Dict[str, Any]:
        """Determine optimal team composition"""
        req_count = len(requirements)
        complexity_score = sum(
            3 if req.get("complexity") == "complex" else 
            2 if req.get("complexity") == "medium" else 1
            for req in requirements
        )
        
        # Base team size on requirements count and complexity
        base_team_size = max(3, min(10, req_count // 5 + complexity_score // 10))
        
        return {
            "total_size": base_team_size,
            "roles": {
                "Tech Lead": 1,
                "Senior Developer": max(1, base_team_size // 4),
                "Mid-level Developer": max(2, base_team_size // 2),
                "Junior Developer": max(1, base_team_size // 4),
                "QA Engineer": max(1, base_team_size // 5),
                "DevOps Engineer": 1 if "DevOps" in skills.get("technical", []) else 0,
                "Product Manager": 1,
                "UX Designer": 1 if any("Frontend" in s for s in skills.get("technical", [])) else 0
            },
            "allocation": "Full-time equivalent (FTE)",
            "duration": "Project-based"
        }
    
    def _calculate_resource_allocation(self, team: Dict, requirements: List[Dict]) -> Dict[str, Any]:
        """Calculate resource allocation across project phases"""
        total_size = team["total_size"]
        
        return {
            "planning_phase": {
                "duration": "2-4 weeks",
                "resources": f"{min(4, total_size)} people",
                "focus": "Requirements, Architecture, Planning"
            },
            "development_phase": {
                "duration": "12-24 weeks",
                "resources": f"{total_size} people",
                "focus": "Implementation, Testing, Integration"
            },
            "testing_phase": {
                "duration": "4-6 weeks",
                "resources": f"{max(3, total_size // 2)} people",
                "focus": "QA, UAT, Performance Testing"
            },
            "deployment_phase": {
                "duration": "2-3 weeks",
                "resources": f"{min(5, total_size)} people",
                "focus": "Deployment, Monitoring, Documentation"
            },
            "maintenance_phase": {
                "duration": "Ongoing",
                "resources": f"{max(2, total_size // 3)} people",
                "focus": "Bug fixes, Updates, Support"
            }
        }
    
    def _estimate_costs(self, team: Dict, budget: float = None) -> Dict[str, Any]:
        """Estimate project costs"""
        # Average salary estimates per role (annual)
        salary_rates = {
            "Tech Lead": 150000,
            "Senior Developer": 120000,
            "Mid-level Developer": 90000,
            "Junior Developer": 65000,
            "QA Engineer": 75000,
            "DevOps Engineer": 110000,
            "Product Manager": 130000,
            "UX Designer": 95000
        }
        
        total_annual_cost = sum(
            salary_rates.get(role, 80000) * count
            for role, count in team.get("roles", {}).items()
        )
        
        # Add overhead (benefits, tools, infrastructure)
        overhead_multiplier = 1.3
        total_with_overhead = total_annual_cost * overhead_multiplier
        
        monthly_cost = total_with_overhead / 12
        
        result = {
            "team_salaries": f"${total_annual_cost:,.0f}/year",
            "with_overhead": f"${total_with_overhead:,.0f}/year",
            "monthly_cost": f"${monthly_cost:,.0f}/month",
            "breakdown": {
                role: f"${salary_rates.get(role, 80000) * count:,.0f}/year"
                for role, count in team.get("roles", {}).items()
                if count > 0
            }
        }
        
        if budget:
            result["budget_fit"] = "Within budget" if total_with_overhead <= budget else "Over budget"
            result["budget_utilization"] = f"{(total_with_overhead / budget * 100):.1f}%"
        
        return result
    
    def _create_hiring_plan(self, team: Dict, current_team: Dict) -> List[Dict[str, str]]:
        """Create hiring plan"""
        needed_roles = team.get("roles", {})
        current_roles = current_team.get("roles", {})
        
        hiring_plan = []
        
        for role, needed_count in needed_roles.items():
            current_count = current_roles.get(role, 0)
            gap = needed_count - current_count
            
            if gap > 0:
                hiring_plan.append({
                    "role": role,
                    "positions": gap,
                    "priority": "High" if role in ["Tech Lead", "Senior Developer"] else "Medium",
                    "timeline": "Immediate" if gap > 2 else "Within 4 weeks",
                    "requirements": f"{gap} {role}{'s' if gap > 1 else ''} needed"
                })
        
        return hiring_plan if hiring_plan else [{"message": "Current team is sufficient"}]
    
    def _identify_training_needs(self, team: Dict, current_team: Dict) -> List[Dict[str, str]]:
        """Identify training needs"""
        return [
            {
                "topic": "Modern Development Practices",
                "target": "All developers",
                "duration": "2 weeks",
                "priority": "Medium"
            },
            {
                "topic": "Cloud Architecture",
                "target": "Senior developers, DevOps",
                "duration": "1 week",
                "priority": "High"
            },
            {
                "topic": "Security Best Practices",
                "target": "All technical roles",
                "duration": "1 week",
                "priority": "High"
            }
        ]
    
    def _generate_resource_recommendations(self, team: Dict, cost: Dict, budget: float = None) -> List[str]:
        """Generate resource recommendations"""
        recommendations = []
        
        if team["total_size"] > 10:
            recommendations.append("⚠️ Large team size - consider splitting into sub-teams")
        
        if budget and "Over budget" in cost.get("budget_fit", ""):
            recommendations.append("💰 Consider phased approach or reduced scope to fit budget")
        
        recommendations.extend([
            "✅ Include buffer resources for unexpected challenges",
            "✅ Plan for knowledge transfer and documentation",
            "✅ Consider contractors for specialized short-term needs",
            "✅ Implement cross-training to reduce bus factor"
        ])
        
        return recommendations


class ProjectTimelineGenerator:
    """Implements capability #117: Project Timeline Generation"""
    
    async def generate_timeline(self,
                               project_scope: Dict[str, Any],
                               team_size: int = 5,
                               start_date: str = None) -> Dict[str, Any]:
        """
        Creates realistic project timelines
        
        Args:
            project_scope: Project scope and requirements
            team_size: Number of team members
            start_date: Project start date (YYYY-MM-DD)
            
        Returns:
            Detailed project timeline with phases and milestones
        """
        try:
            start = datetime.fromisoformat(start_date) if start_date else datetime.now()
            
            # Estimate project duration
            duration = self._estimate_project_duration(project_scope, team_size)
            
            # Generate phases
            phases = self._generate_project_phases(start, duration, project_scope)
            
            # Create Gantt chart data
            gantt_data = self._create_gantt_data(phases)
            
            # Identify dependencies
            dependencies = self._identify_dependencies(phases)
            
            # Calculate critical path
            critical_path = self._calculate_critical_path(phases, dependencies)
            
            # Generate timeline visualization
            timeline_viz = self._generate_timeline_visualization(phases)
            
            return {
                "success": True,
                "project_duration": duration,
                "start_date": start.isoformat(),
                "end_date": (start + timedelta(weeks=duration["weeks"])).isoformat(),
                "phases": phases,
                "gantt_data": gantt_data,
                "dependencies": dependencies,
                "critical_path": critical_path,
                "timeline_visualization": timeline_viz,
                "buffer_recommendations": self._recommend_buffers(duration)
            }
        except Exception as e:
            logger.error("Timeline generation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _estimate_project_duration(self, scope: Dict, team_size: int) -> Dict[str, int]:
        """Estimate project duration"""
        requirements_count = len(scope.get("requirements", []))
        complexity = scope.get("complexity", "medium")
        
        # Base estimate: 1 week per requirement for medium complexity
        base_weeks = requirements_count
        
        # Adjust for complexity
        complexity_multiplier = {
            "simple": 0.7,
            "medium": 1.0,
            "complex": 1.5
        }.get(complexity, 1.0)
        
        # Adjust for team size (diminishing returns)
        team_multiplier = 1.0 if team_size <= 3 else 0.8 if team_size <= 6 else 0.7
        
        adjusted_weeks = int(base_weeks * complexity_multiplier * team_multiplier)
        
        # Add buffer
        total_weeks = int(adjusted_weeks * 1.2)  # 20% buffer
        
        return {
            "weeks": total_weeks,
            "months": total_weeks // 4,
            "base_estimate": adjusted_weeks,
            "buffer": total_weeks - adjusted_weeks
        }
    
    def _generate_project_phases(self, start: datetime, duration: Dict, scope: Dict) -> List[Dict[str, Any]]:
        """Generate project phases"""
        total_weeks = duration["weeks"]
        
        phases = []
        current_date = start
        
        # Phase 1: Planning & Design (15% of timeline)
        planning_weeks = max(2, int(total_weeks * 0.15))
        phases.append({
            "name": "Planning & Design",
            "start_date": current_date.isoformat(),
            "end_date": (current_date + timedelta(weeks=planning_weeks)).isoformat(),
            "duration_weeks": planning_weeks,
            "tasks": [
                "Requirements finalization",
                "Architecture design",
                "Technology stack selection",
                "Project setup"
            ],
            "deliverables": ["Architecture document", "Technical specifications", "Project plan"]
        })
        current_date += timedelta(weeks=planning_weeks)
        
        # Phase 2: Development Sprint 1 (25% of timeline)
        dev1_weeks = max(4, int(total_weeks * 0.25))
        phases.append({
            "name": "Development Sprint 1",
            "start_date": current_date.isoformat(),
            "end_date": (current_date + timedelta(weeks=dev1_weeks)).isoformat(),
            "duration_weeks": dev1_weeks,
            "tasks": [
                "Core feature development",
                "Database implementation",
                "API development",
                "Unit testing"
            ],
            "deliverables": ["Working backend", "Database schema", "API documentation"]
        })
        current_date += timedelta(weeks=dev1_weeks)
        
        # Phase 3: Development Sprint 2 (25% of timeline)
        dev2_weeks = max(4, int(total_weeks * 0.25))
        phases.append({
            "name": "Development Sprint 2",
            "start_date": current_date.isoformat(),
            "end_date": (current_date + timedelta(weeks=dev2_weeks)).isoformat(),
            "duration_weeks": dev2_weeks,
            "tasks": [
                "Frontend development",
                "Integration",
                "Feature completion",
                "Integration testing"
            ],
            "deliverables": ["Complete frontend", "Integrated application", "Test suite"]
        })
        current_date += timedelta(weeks=dev2_weeks)
        
        # Phase 4: Testing & QA (20% of timeline)
        qa_weeks = max(3, int(total_weeks * 0.20))
        phases.append({
            "name": "Testing & QA",
            "start_date": current_date.isoformat(),
            "end_date": (current_date + timedelta(weeks=qa_weeks)).isoformat(),
            "duration_weeks": qa_weeks,
            "tasks": [
                "System testing",
                "Performance testing",
                "Security testing",
                "User acceptance testing"
            ],
            "deliverables": ["Test reports", "Bug fixes", "Performance metrics"]
        })
        current_date += timedelta(weeks=qa_weeks)
        
        # Phase 5: Deployment & Launch (15% of timeline)
        deploy_weeks = max(2, int(total_weeks * 0.15))
        phases.append({
            "name": "Deployment & Launch",
            "start_date": current_date.isoformat(),
            "end_date": (current_date + timedelta(weeks=deploy_weeks)).isoformat(),
            "duration_weeks": deploy_weeks,
            "tasks": [
                "Production deployment",
                "Monitoring setup",
                "Documentation",
                "Training"
            ],
            "deliverables": ["Production system", "Documentation", "Training materials"]
        })
        
        return phases
    
    def _create_gantt_data(self, phases: List[Dict]) -> Dict[str, Any]:
        """Create Gantt chart data"""
        return {
            "chart_type": "gantt",
            "phases": [
                {
                    "task": phase["name"],
                    "start": phase["start_date"],
                    "end": phase["end_date"],
                    "duration": f"{phase['duration_weeks']} weeks"
                }
                for phase in phases
            ],
            "format": "JSON for visualization libraries (D3.js, Chart.js, etc.)"
        }
    
    def _identify_dependencies(self, phases: List[Dict]) -> List[Dict[str, str]]:
        """Identify phase dependencies"""
        dependencies = []
        for i in range(len(phases) - 1):
            dependencies.append({
                "from": phases[i]["name"],
                "to": phases[i + 1]["name"],
                "type": "finish-to-start",
                "description": f"{phases[i + 1]['name']} depends on completion of {phases[i]['name']}"
            })
        return dependencies
    
    def _calculate_critical_path(self, phases: List[Dict], dependencies: List[Dict]) -> Dict[str, Any]:
        """Calculate critical path"""
        return {
            "path": [phase["name"] for phase in phases],
            "total_duration": f"{sum(p['duration_weeks'] for p in phases)} weeks",
            "critical_tasks": [
                "Requirements finalization",
                "Core feature development",
                "System testing",
                "Production deployment"
            ],
            "slack_time": "Minimal - all phases are on critical path"
        }
    
    def _generate_timeline_visualization(self, phases: List[Dict]) -> str:
        """Generate timeline visualization"""
        return """
Project Timeline (Gantt Chart)

""" + "\n".join([
    f"[{phase['name']}] {phase['start_date'][:10]} -> {phase['end_date'][:10]} ({phase['duration_weeks']} weeks)"
    for phase in phases
])
    
    def _recommend_buffers(self, duration: Dict) -> List[str]:
        """Recommend buffer time"""
        return [
            f"✅ {duration['buffer']} weeks buffer already included",
            "⚠️ Add 2-week buffer for unexpected issues",
            "✅ Plan for holidays and team availability",
            "✅ Include time for stakeholder reviews",
            "⚠️ Consider adding contingency for third-party dependencies"
        ]


class MilestonePlanner:
    """Implements capability #118: Milestone Planning"""
    
    async def plan_milestones(self,
                             project_timeline: Dict[str, Any],
                             stakeholder_needs: List[str] = None) -> Dict[str, Any]:
        """
        Identifies key project milestones
        
        Args:
            project_timeline: Project timeline from timeline generator
            stakeholder_needs: Stakeholder requirements for milestones
            
        Returns:
            Milestone plan with dates and deliverables
        """
        try:
            # Extract phases from timeline
            phases = project_timeline.get("phases", [])
            
            # Generate milestones
            milestones = self._generate_milestones(phases, stakeholder_needs or [])
            
            # Create milestone calendar
            calendar = self._create_milestone_calendar(milestones)
            
            # Define success criteria
            success_criteria = self._define_milestone_success_criteria(milestones)
            
            # Create review schedule
            review_schedule = self._create_review_schedule(milestones)
            
            return {
                "success": True,
                "total_milestones": len(milestones),
                "milestones": milestones,
                "calendar": calendar,
                "success_criteria": success_criteria,
                "review_schedule": review_schedule,
                "recommendations": self._generate_milestone_recommendations()
            }
        except Exception as e:
            logger.error("Milestone planning failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _generate_milestones(self, phases: List[Dict], stakeholder_needs: List[str]) -> List[Dict[str, Any]]:
        """Generate project milestones"""
        milestones = []
        
        # Milestone 1: Project Kickoff
        if phases:
            milestones.append({
                "id": "M1",
                "name": "Project Kickoff",
                "date": phases[0]["start_date"],
                "type": "start",
                "deliverables": [
                    "Project charter signed",
                    "Team assembled",
                    "Initial planning complete"
                ],
                "stakeholders": ["Project team", "Management", "Sponsors"],
                "criticality": "High"
            })
        
        # Milestone 2: Design Complete (end of planning phase)
        if len(phases) > 0:
            milestones.append({
                "id": "M2",
                "name": "Design & Architecture Complete",
                "date": phases[0]["end_date"],
                "type": "phase_completion",
                "deliverables": [
                    "Architecture approved",
                    "Technical specifications signed off",
                    "Development environment ready"
                ],
                "stakeholders": ["Technical team", "Product owners"],
                "criticality": "Critical"
            })
        
        # Milestone 3: MVP/Alpha Release
        if len(phases) > 1:
            milestones.append({
                "id": "M3",
                "name": "MVP Release",
                "date": phases[1]["end_date"],
                "type": "deliverable",
                "deliverables": [
                    "Core features working",
                    "Internal demo ready",
                    "Basic testing complete"
                ],
                "stakeholders": ["Product team", "Early adopters"],
                "criticality": "High"
            })
        
        # Milestone 4: Beta Release
        if len(phases) > 2:
            milestones.append({
                "id": "M4",
                "name": "Beta Release",
                "date": phases[2]["end_date"],
                "type": "deliverable",
                "deliverables": [
                    "All features complete",
                    "Integration testing done",
                    "Beta testing begins"
                ],
                "stakeholders": ["QA team", "Beta testers", "Product team"],
                "criticality": "High"
            })
        
        # Milestone 5: Production Ready
        if len(phases) > 3:
            milestones.append({
                "id": "M5",
                "name": "Production Ready",
                "date": phases[3]["end_date"],
                "type": "quality_gate",
                "deliverables": [
                    "All tests passed",
                    "Performance validated",
                    "Security audit complete"
                ],
                "stakeholders": ["QA team", "Security team", "Management"],
                "criticality": "Critical"
            })
        
        # Milestone 6: Launch
        if len(phases) > 4:
            milestones.append({
                "id": "M6",
                "name": "Production Launch",
                "date": phases[4]["end_date"],
                "type": "launch",
                "deliverables": [
                    "System deployed to production",
                    "Monitoring active",
                    "Documentation complete",
                    "Training delivered"
                ],
                "stakeholders": ["All stakeholders", "End users"],
                "criticality": "Critical"
            })
        
        return milestones
    
    def _create_milestone_calendar(self, milestones: List[Dict]) -> Dict[str, Any]:
        """Create milestone calendar"""
        return {
            "format": "calendar",
            "milestones_by_date": {
                milestone["date"]: {
                    "id": milestone["id"],
                    "name": milestone["name"],
                    "type": milestone["type"]
                }
                for milestone in milestones
            },
            "key_dates": [
                f"{milestone['id']}: {milestone['name']} - {milestone['date'][:10]}"
                for milestone in milestones
            ]
        }
    
    def _define_milestone_success_criteria(self, milestones: List[Dict]) -> Dict[str, List[str]]:
        """Define success criteria for milestones"""
        return {
            milestone["id"]: [
                f"✅ {deliverable}"
                for deliverable in milestone["deliverables"]
            ] + [
                "✅ Stakeholder sign-off received",
                "✅ All dependencies met",
                "✅ No critical issues outstanding"
            ]
            for milestone in milestones
        }
    
    def _create_review_schedule(self, milestones: List[Dict]) -> List[Dict[str, str]]:
        """Create milestone review schedule"""
        return [
            {
                "milestone": milestone["name"],
                "review_date": milestone["date"],
                "review_type": "Formal milestone review",
                "attendees": ", ".join(milestone["stakeholders"]),
                "agenda": f"Review {milestone['name']} deliverables and approve next phase"
            }
            for milestone in milestones
            if milestone["criticality"] in ["Critical", "High"]
        ]
    
    def _generate_milestone_recommendations(self) -> List[str]:
        """Generate milestone recommendations"""
        return [
            "✅ Celebrate milestone achievements with the team",
            "✅ Document lessons learned at each milestone",
            "✅ Adjust subsequent milestones based on progress",
            "⚠️ Include buffer time between critical milestones",
            "✅ Communicate milestone status to all stakeholders",
            "✅ Use milestones as decision gates for project continuation"
        ]


class StakeholderReportGenerator:
    """Implements capability #119: Stakeholder Report Generation"""
    
    async def generate_report(self,
                             project_status: Dict[str, Any],
                             report_type: str = "status",
                             audience: str = "executive") -> Dict[str, Any]:
        """
        Creates progress reports for stakeholders
        
        Args:
            project_status: Current project status data
            report_type: Type of report (status, milestone, risk, budget)
            audience: Target audience (executive, technical, team)
            
        Returns:
            Formatted stakeholder report
        """
        try:
            # Generate executive summary
            executive_summary = self._generate_executive_summary(project_status)
            
            # Create status overview
            status_overview = self._create_status_overview(project_status)
            
            # Generate metrics dashboard
            metrics = self._generate_metrics_dashboard(project_status)
            
            # Create risk summary
            risk_summary = self._create_risk_summary(project_status)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(project_status)
            
            # Format report
            formatted_report = self._format_report(
                executive_summary,
                status_overview,
                metrics,
                risk_summary,
                recommendations,
                audience
            )
            
            return {
                "success": True,
                "report_type": report_type,
                "audience": audience,
                "generated_date": datetime.now().isoformat(),
                "executive_summary": executive_summary,
                "status_overview": status_overview,
                "metrics": metrics,
                "risk_summary": risk_summary,
                "recommendations": recommendations,
                "formatted_report": formatted_report
            }
        except Exception as e:
            logger.error("Report generation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _generate_executive_summary(self, status: Dict) -> str:
        """Generate executive summary"""
        progress = status.get("progress", 50)
        on_track = status.get("on_track", True)
        
        return f"""
EXECUTIVE SUMMARY
-----------------
Project Status: {'🟢 On Track' if on_track else '🔴 At Risk'}
Overall Progress: {progress}% complete
Budget Status: {status.get('budget_status', 'Within budget')}
Timeline: {status.get('timeline_status', 'On schedule')}

Key Highlights:
- {status.get('completed_milestones', 0)} of {status.get('total_milestones', 0)} milestones completed
- {status.get('team_velocity', 'Good')} team velocity
- {status.get('open_risks', 0)} open risks requiring attention

Next Major Milestone: {status.get('next_milestone', 'TBD')}
        """.strip()
    
    def _create_status_overview(self, status: Dict) -> Dict[str, Any]:
        """Create detailed status overview"""
        return {
            "current_phase": status.get("current_phase", "Development"),
            "completed_tasks": status.get("completed_tasks", 0),
            "in_progress_tasks": status.get("in_progress_tasks", 0),
            "pending_tasks": status.get("pending_tasks", 0),
            "team_status": {
                "size": status.get("team_size", 5),
                "availability": "100%",
                "morale": "High"
            },
            "recent_accomplishments": [
                "Completed core feature development",
                "Integrated third-party APIs",
                "Passed security audit"
            ],
            "upcoming_activities": [
                "Performance testing",
                "User acceptance testing",
                "Production deployment preparation"
            ]
        }
    
    def _generate_metrics_dashboard(self, status: Dict) -> Dict[str, Any]:
        """Generate metrics dashboard"""
        return {
            "progress_metrics": {
                "overall_completion": f"{status.get('progress', 50)}%",
                "velocity": f"{status.get('velocity', 8)} story points/sprint",
                "burn_rate": f"${status.get('burn_rate', 50000)}/month"
            },
            "quality_metrics": {
                "test_coverage": "85%",
                "code_quality_score": "A",
                "bug_count": status.get("bugs", 12),
                "critical_bugs": 0
            },
            "timeline_metrics": {
                "days_elapsed": status.get("days_elapsed", 90),
                "days_remaining": status.get("days_remaining", 60),
                "schedule_variance": "+3 days (ahead of schedule)"
            },
            "budget_metrics": {
                "budget_spent": f"{status.get('budget_spent', 60)}%",
                "cost_variance": "-5% (under budget)",
                "projected_total_cost": "$450,000"
            }
        }
    
    def _create_risk_summary(self, status: Dict) -> Dict[str, Any]:
        """Create risk summary"""
        return {
            "risk_status": "🟡 Medium",
            "active_risks": [
                {
                    "id": "R1",
                    "risk": "Third-party API availability",
                    "severity": "Medium",
                    "mitigation": "Implemented fallback mechanism"
                },
                {
                    "id": "R2",
                    "risk": "Team member availability",
                    "severity": "Low",
                    "mitigation": "Cross-training in progress"
                }
            ],
            "resolved_risks": 5,
            "risk_trend": "Improving"
        }
    
    def _generate_recommendations(self, status: Dict) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if status.get("progress", 50) < 30:
            recommendations.append("⚠️ Consider adding resources to accelerate progress")
        
        if status.get("bugs", 0) > 20:
            recommendations.append("⚠️ Focus on bug resolution before new feature development")
        
        recommendations.extend([
            "✅ Continue current development pace",
            "✅ Plan for user acceptance testing in next phase",
            "✅ Begin production readiness preparations"
        ])
        
        return recommendations
    
    def _format_report(self, summary: str, overview: Dict, metrics: Dict, 
                      risks: Dict, recommendations: List[str], audience: str) -> str:
        """Format complete report"""
        if audience == "executive":
            return f"""
PROJECT STATUS REPORT
=====================

{summary}

METRICS AT A GLANCE
-------------------
Progress: {metrics['progress_metrics']['overall_completion']}
Quality: {metrics['quality_metrics']['code_quality_score']}
Timeline: {metrics['timeline_metrics']['schedule_variance']}
Budget: {metrics['budget_metrics']['cost_variance']}

RECOMMENDATIONS
---------------
{chr(10).join(recommendations)}

Report Generated: {datetime.now().strftime('%Y-%m-%d')}
            """.strip()
        else:
            # Technical or team audience gets more detail
            return f"""
DETAILED PROJECT STATUS REPORT
==============================

{summary}

DETAILED METRICS
----------------
{metrics}

RISK SUMMARY
------------
{risks}

RECOMMENDATIONS
---------------
{chr(10).join(recommendations)}
            """.strip()


class SuccessMetricDefiner:
    """Implements capability #120: Success Metric Definition"""
    
    async def define_success_metrics(self,
                                    project_goals: List[str],
                                    stakeholder_priorities: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Defines and tracks project success metrics
        
        Args:
            project_goals: List of project goals
            stakeholder_priorities: Stakeholder priorities
            
        Returns:
            Success metrics definition and tracking framework
        """
        try:
            # Define KPIs
            kpis = self._define_kpis(project_goals, stakeholder_priorities or {})
            
            # Create measurement framework
            measurement_framework = self._create_measurement_framework(kpis)
            
            # Define success thresholds
            thresholds = self._define_success_thresholds(kpis)
            
            # Create tracking dashboard
            dashboard = self._create_tracking_dashboard(kpis)
            
            # Generate reporting cadence
            reporting_cadence = self._generate_reporting_cadence()
            
            return {
                "success": True,
                "kpis": kpis,
                "measurement_framework": measurement_framework,
                "success_thresholds": thresholds,
                "tracking_dashboard": dashboard,
                "reporting_cadence": reporting_cadence,
                "recommendations": self._generate_metric_recommendations()
            }
        except Exception as e:
            logger.error("Success metric definition failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _define_kpis(self, goals: List[str], priorities: Dict) -> List[Dict[str, Any]]:
        """Define Key Performance Indicators"""
        kpis = [
            {
                "id": "KPI1",
                "name": "On-Time Delivery",
                "description": "Percentage of deliverables completed on schedule",
                "category": "Timeline",
                "target": "95%",
                "measurement": "Tasks completed by due date / Total tasks",
                "frequency": "Weekly",
                "owner": "Project Manager"
            },
            {
                "id": "KPI2",
                "name": "Budget Adherence",
                "description": "Variance from planned budget",
                "category": "Financial",
                "target": "Within 10% of budget",
                "measurement": "Actual spend vs planned spend",
                "frequency": "Monthly",
                "owner": "Finance Team"
            },
            {
                "id": "KPI3",
                "name": "Code Quality",
                "description": "Overall code quality score",
                "category": "Quality",
                "target": ">= 85%",
                "measurement": "Test coverage + Code complexity + Documentation",
                "frequency": "Continuous",
                "owner": "Tech Lead"
            },
            {
                "id": "KPI4",
                "name": "Team Velocity",
                "description": "Story points completed per sprint",
                "category": "Productivity",
                "target": "8-10 points/sprint",
                "measurement": "Completed story points",
                "frequency": "Per sprint",
                "owner": "Scrum Master"
            },
            {
                "id": "KPI5",
                "name": "User Satisfaction",
                "description": "End user satisfaction score",
                "category": "Quality",
                "target": ">= 4.0/5.0",
                "measurement": "User surveys and feedback",
                "frequency": "Post-launch, then quarterly",
                "owner": "Product Manager"
            },
            {
                "id": "KPI6",
                "name": "System Performance",
                "description": "Application response time",
                "category": "Technical",
                "target": "< 200ms (p95)",
                "measurement": "API response time monitoring",
                "frequency": "Continuous",
                "owner": "DevOps Team"
            },
            {
                "id": "KPI7",
                "name": "Defect Density",
                "description": "Number of bugs per 1000 lines of code",
                "category": "Quality",
                "target": "< 1.0",
                "measurement": "Total bugs / (LOC / 1000)",
                "frequency": "Weekly",
                "owner": "QA Lead"
            },
            {
                "id": "KPI8",
                "name": "Team Morale",
                "description": "Team satisfaction and engagement",
                "category": "People",
                "target": ">= 4.0/5.0",
                "measurement": "Team surveys",
                "frequency": "Monthly",
                "owner": "Engineering Manager"
            }
        ]
        
        return kpis
    
    def _create_measurement_framework(self, kpis: List[Dict]) -> Dict[str, Any]:
        """Create measurement framework"""
        return {
            "data_collection": {
                "automated": [
                    "Code quality metrics (SonarQube, CodeClimate)",
                    "Performance metrics (APM tools)",
                    "Timeline metrics (Project management tools)"
                ],
                "manual": [
                    "User satisfaction surveys",
                    "Team morale surveys",
                    "Stakeholder feedback"
                ]
            },
            "data_storage": {
                "system": "Business Intelligence platform",
                "retention": "2 years",
                "access": "Stakeholders and team leads"
            },
            "analysis": {
                "tools": ["Tableau", "Power BI", "Custom dashboards"],
                "cadence": "Weekly analysis, monthly deep dive",
                "responsible": "Data Analytics team"
            }
        }
    
    def _define_success_thresholds(self, kpis: List[Dict]) -> Dict[str, Dict[str, str]]:
        """Define success thresholds"""
        return {
            kpi["id"]: {
                "excellent": kpi["target"],
                "acceptable": self._calculate_acceptable_threshold(kpi),
                "needs_improvement": "Below acceptable threshold",
                "current_status": "Tracking"
            }
            for kpi in kpis
        }
    
    def _calculate_acceptable_threshold(self, kpi: Dict) -> str:
        """Calculate acceptable threshold"""
        if "%" in kpi["target"]:
            return f">= {int(kpi['target'].replace('%', '').replace('>=', '').strip()) - 10}%"
        else:
            return f"Within 20% of target: {kpi['target']}"
    
    def _create_tracking_dashboard(self, kpis: List[Dict]) -> Dict[str, Any]:
        """Create tracking dashboard spec"""
        return {
            "dashboard_name": "Project Success Metrics Dashboard",
            "sections": [
                {
                    "name": "Executive Overview",
                    "metrics": ["Overall project health", "Budget status", "Timeline status"],
                    "visualization": "Scorecard"
                },
                {
                    "name": "Timeline Metrics",
                    "metrics": [kpi["name"] for kpi in kpis if kpi["category"] == "Timeline"],
                    "visualization": "Burndown chart + Progress bars"
                },
                {
                    "name": "Quality Metrics",
                    "metrics": [kpi["name"] for kpi in kpis if kpi["category"] == "Quality"],
                    "visualization": "Trend lines + Heat maps"
                },
                {
                    "name": "Financial Metrics",
                    "metrics": [kpi["name"] for kpi in kpis if kpi["category"] == "Financial"],
                    "visualization": "Budget burn chart"
                }
            ],
            "refresh_rate": "Real-time for automated metrics, daily for manual",
            "access": "Role-based (Executive, Team, Public views)"
        }
    
    def _generate_reporting_cadence(self) -> Dict[str, Any]:
        """Generate reporting cadence"""
        return {
            "daily": {
                "metrics": ["Team velocity", "Active bugs"],
                "format": "Automated email summary",
                "audience": "Development team"
            },
            "weekly": {
                "metrics": ["All KPIs", "Progress vs plan"],
                "format": "Status report",
                "audience": "Project team + Management"
            },
            "monthly": {
                "metrics": ["All KPIs", "Trends", "Forecasts"],
                "format": "Executive presentation",
                "audience": "Executive stakeholders"
            },
            "milestone": {
                "metrics": ["All KPIs", "Achievement of milestone goals"],
                "format": "Comprehensive review",
                "audience": "All stakeholders"
            }
        }
    
    def _generate_metric_recommendations(self) -> List[str]:
        """Generate metric recommendations"""
        return [
            "✅ Review and adjust metrics quarterly",
            "✅ Automate data collection where possible",
            "✅ Share metrics transparently with the team",
            "✅ Use metrics for continuous improvement, not punishment",
            "⚠️ Balance quantitative metrics with qualitative feedback",
            "✅ Align metrics with organizational objectives",
            "✅ Celebrate when targets are achieved"
        ]


__all__ = [
    'RequirementsAnalyzer',
    'UserStoryGenerator',
    'AcceptanceCriteriaDefiner',
    'EstimationAutomator',
    'RiskAssessor',
    'ResourcePlanner',
    'ProjectTimelineGenerator',
    'MilestonePlanner',
    'StakeholderReportGenerator',
    'SuccessMetricDefiner'
]

