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


# Note: Capabilities 116-120 would continue here with similar implementations:
# ResourcePlanner, ProjectTimelineGenerator, MilestonePlanner, StakeholderReportGenerator, SuccessMetricDefiner

__all__ = [
    'RequirementsAnalyzer',
    'UserStoryGenerator',
    'AcceptanceCriteriaDefiner',
    'EstimationAutomator',
    'RiskAssessor'
]

