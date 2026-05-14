from typing import Dict, Any, List
from datetime import datetime


class LocalAgentFallback:
    """
    Local fallback implementation simulating IBM Consulting Advantage agents.
    This class provides mock responses that follow the expected agent payload
    structure and response contract.
    """
    
    def __init__(self):
        """Initialize the local agent fallback."""
        self.agent_names = [
            "Orchestrator Agent",
            "SEO Agent",
            "Module Strategy Agent",
            "Storytelling Agent",
            "Brand Safety Agent",
            "Recommendation Agent"
        ]
    
    def analyze_briefing(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a briefing using simulated agent logic.
        
        Args:
            payload: Dictionary containing:
                - input_type: Type of input (e.g., "briefing")
                - briefing: The briefing text
                - business_goal: Optional business goal
                - target_audience: Optional target audience
                - constraints: List of constraints
                - catalogs: Dictionary with modules_catalog, storytelling_patterns,
                           brand_rules
        
        Returns:
            Dictionary with analysis results including:
                - analysis_id
                - score
                - page_summary
                - recommendations
                - module_plan
                - copy_suggestions
                - catalog_context
                - agent_trace
        """
        # Extract payload data
        briefing = payload.get("briefing", "")
        business_goal = payload.get("business_goal", "nao_informado")
        target_audience = payload.get("target_audience", "nao_informado")
        constraints = payload.get("constraints", [])
        catalogs = payload.get("catalogs", {})
        
        # Simulate agent trace
        agent_trace = self._build_agent_trace(briefing, business_goal)
        
        # Build analysis response
        analysis_id = self._generate_analysis_id()
        
        # Simulate scoring from different agents
        scores = self._calculate_scores(briefing, constraints)
        
        # Build page summary
        page_summary = self._build_page_summary(
            briefing, business_goal, target_audience
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            briefing, business_goal, constraints
        )
        
        # Build module plan
        module_plan = self._build_module_plan(briefing, catalogs)
        
        # Generate copy suggestions
        copy_suggestions = self._generate_copy_suggestions(briefing)
        
        # Build catalog context
        catalog_context = self._build_catalog_context(catalogs)
        
        return {
            "analysis_id": analysis_id,
            "score": scores,
            "page_summary": page_summary,
            "recommendations": recommendations,
            "module_plan": module_plan,
            "copy_suggestions": copy_suggestions,
            "catalog_context": catalog_context,
            "agent_trace": agent_trace
        }
    
    def _generate_analysis_id(self) -> str:
        """Generate a unique analysis ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"analysis_{timestamp}"
    
    def _build_agent_trace(
        self, briefing: str, business_goal: str
    ) -> List[Dict[str, Any]]:
        """
        Build the agent trace showing simulated agent execution.
        
        Returns:
            List of agent execution steps with name, status, and summary.
        """
        trace = []
        
        # Orchestrator Agent
        trace.append({
            "agent": "Orchestrator Agent",
            "status": "completed",
            "summary": "Analyzed briefing structure and coordinated agent workflow"
        })
        
        # SEO Agent
        trace.append({
            "agent": "SEO Agent",
            "status": "completed",
            "summary": "Evaluated SEO potential and keyword opportunities"
        })
        
        # Module Strategy Agent
        trace.append({
            "agent": "Module Strategy Agent",
            "status": "completed",
            "summary": "Recommended module composition based on page goals"
        })
        
        # Storytelling Agent
        trace.append({
            "agent": "Storytelling Agent",
            "status": "completed",
            "summary": "Analyzed narrative flow and storytelling structure"
        })
        
        # Brand Safety Agent
        trace.append({
            "agent": "Brand Safety Agent",
            "status": "completed",
            "summary": "Verified compliance with brand guidelines"
        })
        
        # Recommendation Agent
        trace.append({
            "agent": "Recommendation Agent",
            "status": "completed",
            "summary": "Synthesized insights and prioritized recommendations"
        })
        
        return trace
    
    def _calculate_scores(
        self, briefing: str, constraints: List[str]
    ) -> Dict[str, int]:
        """
        Calculate simulated scores for different aspects.
        
        Returns:
            Dictionary with overall, seo, storytelling, modules, brand_safety scores.
        """
        # Simple heuristic: longer briefings get slightly better scores
        base_score = 70
        length_bonus = min(len(briefing) // 100, 15)
        constraint_penalty = len(constraints) * 2
        
        seo_score = max(60, min(95, base_score + length_bonus - constraint_penalty))
        storytelling_score = max(65, min(95, base_score + length_bonus + 5))
        modules_score = max(60, min(95, base_score + length_bonus))
        brand_safety_score = max(75, min(95, base_score + 15))
        
        overall_score = (
            seo_score + storytelling_score + modules_score + brand_safety_score
        ) // 4
        
        return {
            "overall": overall_score,
            "seo": seo_score,
            "storytelling": storytelling_score,
            "modules": modules_score,
            "brand_safety": brand_safety_score
        }
    
    def _build_page_summary(
        self, briefing: str, business_goal: str, target_audience: str
    ) -> Dict[str, str]:
        """
        Build page summary based on briefing analysis.
        
        Returns:
            Dictionary with detected_type, primary_goal, main_topic.
        """
        # Simple heuristic to detect page type
        briefing_lower = briefing.lower()
        
        if "produto" in briefing_lower or "product" in briefing_lower:
            detected_type = "produto"
        elif "servico" in briefing_lower or "service" in briefing_lower:
            detected_type = "servico"
        elif "evento" in briefing_lower or "event" in briefing_lower:
            detected_type = "evento"
        else:
            detected_type = "institucional"
        
        return {
            "detected_type": detected_type,
            "primary_goal": business_goal,
            "main_topic": "Topic extracted from briefing analysis"
        }
    
    def _generate_recommendations(
        self, briefing: str, business_goal: str, constraints: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on briefing analysis.
        
        Returns:
            List of recommendation dictionaries.
        """
        recommendations = []
        
        # Storytelling recommendation
        recommendations.append({
            "priority": "high",
            "area": "storytelling",
            "title": "Organize page narrative structure",
            "why": (
                "The briefing needs clearer problem-solution-action flow "
                "to guide users effectively."
            ),
            "suggestion": (
                "Structure the page with: problem statement, solution overview, "
                "key benefits, social proof, and clear CTA."
            ),
            "impact": "high",
            "effort": "medium"
        })
        
        # SEO recommendation
        if len(briefing) < 200:
            recommendations.append({
                "priority": "medium",
                "area": "seo",
                "title": "Expand content for better SEO coverage",
                "why": (
                    "Brief content may limit keyword opportunities and "
                    "search visibility."
                ),
                "suggestion": (
                    "Add detailed sections covering user questions, "
                    "use cases, and benefits."
                ),
                "impact": "medium",
                "effort": "high"
            })
        
        # Module recommendation
        recommendations.append({
            "priority": "medium",
            "area": "modules",
            "title": "Add FAQ module to reduce objections",
            "why": "Addressing common questions builds trust and reduces friction.",
            "suggestion": (
                "Include FAQ module with 5-7 questions covering pricing, "
                "implementation, and support."
            ),
            "impact": "medium",
            "effort": "low"
        })
        
        return recommendations
    
    def _build_module_plan(
        self, briefing: str, catalogs: Dict[str, Any]
    ) -> Dict[str, List[Any]]:
        """
        Build module plan with keep, remove, reorder, add suggestions.
        
        Returns:
            Dictionary with keep, remove, reorder, add lists.
        """
        modules_catalog = catalogs.get("modules_catalog", [])
        
        # Suggest adding FAQ and testimonials for most pages
        add_suggestions = []
        
        # Find FAQ module
        for module in modules_catalog:
            if module.get("name") == "FAQ":
                add_suggestions.append({
                    "module_type": "FAQ",
                    "reason": "Helps reduce objections before conversion."
                })
                break
        
        # Find testimonials module
        for module in modules_catalog:
            if module.get("name") == "Testimonials":
                add_suggestions.append({
                    "module_type": "Testimonials",
                    "reason": "Social proof increases trust and credibility."
                })
                break
        
        return {
            "keep": [],
            "remove": [],
            "reorder": [],
            "add": add_suggestions
        }
    
    def _generate_copy_suggestions(
        self, briefing: str
    ) -> List[Dict[str, str]]:
        """
        Generate copy improvement suggestions.
        
        Returns:
            List of copy suggestion dictionaries.
        """
        suggestions = []
        
        # Generic copy suggestions
        suggestions.append({
            "section": "headline",
            "current": "Generic headline",
            "suggested": "Benefit-focused headline that addresses user pain point",
            "reason": "Clear value proposition improves engagement"
        })
        
        suggestions.append({
            "section": "cta",
            "current": "Click here",
            "suggested": "Start your free trial today",
            "reason": "Action-oriented CTAs with value increase conversions"
        })
        
        return suggestions
    
    def _build_catalog_context(
        self, catalogs: Dict[str, Any]
    ) -> Dict[str, int]:
        """
        Build catalog context showing available resources.
        
        Returns:
            Dictionary with counts of available catalog items.
        """
        return {
            "modules_available_count": len(
                catalogs.get("modules_catalog", [])
            ),
            "storytelling_patterns_count": len(
                catalogs.get("storytelling_patterns", [])
            ),
            "brand_rules_count": len(
                catalogs.get("brand_rules", [])
            )
        }


# Made with Bob