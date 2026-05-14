from typing import Dict, Any, List, Optional
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
                - catalogs: Dictionary with modules_catalog,
                           storytelling_patterns, brand_rules
        
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
    
    def analyze_url(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a URL using simulated agent logic.
        
        Args:
            payload: Dictionary containing:
                - input_type: Type of input (e.g., "url")
                - url: The URL to analyze
                - business_goal: Optional business goal
                - target_audience: Optional target audience
                - page_type_hint: Optional page type hint
                - catalogs: Dictionary with modules_catalog,
                           storytelling_patterns, brand_rules
                - normalized_page: Normalized page data from scraper
        
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
                - page_diagnostics
        """
        # Extract payload data
        url = payload.get("url", "")
        business_goal = payload.get("business_goal", "nao_informado")
        target_audience = payload.get("target_audience", "nao_informado")
        page_type_hint = payload.get("page_type_hint")
        catalogs = payload.get("catalogs", {})
        normalized_page = payload.get("normalized_page", {})
        
        # Build page diagnostics from normalized page
        page_diagnostics = self._build_page_diagnostics(normalized_page)
        
        # Simulate agent trace for URL analysis
        agent_trace = self._build_url_agent_trace(url)
        
        # Build analysis response
        analysis_id = self._generate_analysis_id()
        
        # Simulate scoring (slightly different from briefing)
        scores = self._calculate_url_scores(url)
        
        # Build page summary for URL
        page_summary = self._build_url_page_summary(
            url, business_goal, target_audience, page_type_hint
        )
        
        # Generate recommendations for URL
        recommendations = self._generate_url_recommendations(
            url, business_goal
        )
        
        # Build module plan
        module_plan = self._build_module_plan(url, catalogs)
        
        # Generate copy suggestions
        copy_suggestions = self._generate_url_copy_suggestions(url)
        
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
            "agent_trace": agent_trace,
            "page_diagnostics": page_diagnostics
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
            "summary": (
                "Analyzed briefing structure and coordinated agent workflow"
            )
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
            Dictionary with overall, seo, storytelling, modules,
            brand_safety scores.
        """
        # Simple heuristic: longer briefings get slightly better scores
        base_score = 70
        length_bonus = min(len(briefing) // 100, 15)
        constraint_penalty = len(constraints) * 2
        
        seo_score = max(
            60, min(95, base_score + length_bonus - constraint_penalty)
        )
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
                "Structure the page with: problem statement, solution "
                "overview, key benefits, social proof, and clear CTA."
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
            "why": (
                "Addressing common questions builds trust and reduces "
                "friction."
            ),
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
            "suggested": (
                "Benefit-focused headline that addresses user pain point"
            ),
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
    
    def _build_url_agent_trace(self, url: str) -> List[Dict[str, Any]]:
        """
        Build agent trace for URL analysis.
        
        Returns:
            List of agent execution steps.
        """
        trace = []
        
        # Orchestrator Agent
        trace.append({
            "agent": "Orchestrator Agent",
            "status": "completed",
            "summary": "Analyzed URL structure and coordinated workflow"
        })
        
        # SEO Agent
        trace.append({
            "agent": "SEO Agent",
            "status": "completed",
            "summary": "Evaluated URL SEO potential and metadata"
        })
        
        # Module Strategy Agent
        trace.append({
            "agent": "Module Strategy Agent",
            "status": "completed",
            "summary": "Analyzed page modules and structure"
        })
        
        # Storytelling Agent
        trace.append({
            "agent": "Storytelling Agent",
            "status": "completed",
            "summary": "Evaluated narrative flow from URL context"
        })
        
        # Brand Safety Agent
        trace.append({
            "agent": "Brand Safety Agent",
            "status": "completed",
            "summary": "Verified brand compliance"
        })
        
        # Recommendation Agent
        trace.append({
            "agent": "Recommendation Agent",
            "status": "completed",
            "summary": "Generated actionable recommendations"
        })
        
        return trace
    
    def _calculate_url_scores(self, url: str) -> Dict[str, int]:
        """
        Calculate scores for URL analysis.
        
        Returns:
            Dictionary with scores.
        """
        # Simple heuristic based on URL characteristics
        base_score = 75
        
        # URLs with https get bonus
        https_bonus = 5 if url.startswith("https://") else 0
        
        seo_score = max(65, min(95, base_score + https_bonus))
        storytelling_score = max(70, min(95, base_score))
        modules_score = max(65, min(95, base_score))
        brand_safety_score = max(80, min(95, base_score + 10))
        
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
    
    def _build_url_page_summary(
        self,
        url: str,
        business_goal: str,
        target_audience: str,
        page_type_hint: Optional[str]
    ) -> Dict[str, str]:
        """
        Build page summary for URL analysis.
        
        Returns:
            Dictionary with page summary.
        """
        # Use page_type_hint if provided, otherwise detect from URL
        if page_type_hint:
            detected_type = page_type_hint
        else:
            url_lower = url.lower()
            if "product" in url_lower or "produto" in url_lower:
                detected_type = "produto"
            elif "service" in url_lower or "servico" in url_lower:
                detected_type = "servico"
            elif "event" in url_lower or "evento" in url_lower:
                detected_type = "evento"
            else:
                detected_type = "unknown"
        
        # Extract topic from URL
        main_topic = f"Topic identified from URL: {url}"
        
        return {
            "detected_type": detected_type,
            "primary_goal": business_goal,
            "main_topic": main_topic
        }
    
    def _generate_url_recommendations(
        self, url: str, business_goal: str
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations for URL analysis.
        
        Returns:
            List of recommendations.
        """
        recommendations = []
        
        # SEO recommendation
        recommendations.append({
            "priority": "high",
            "area": "seo",
            "title": "Optimize page metadata and structure",
            "why": (
                "Well-structured metadata improves search visibility "
                "and click-through rates."
            ),
            "suggestion": (
                "Add descriptive title tags, meta descriptions, "
                "and structured data markup."
            ),
            "impact": "high",
            "effort": "medium"
        })
        
        # Content recommendation
        recommendations.append({
            "priority": "medium",
            "area": "storytelling",
            "title": "Enhance content narrative flow",
            "why": "Clear storytelling guides users toward conversion.",
            "suggestion": (
                "Structure content with problem-solution-action flow "
                "and clear value propositions."
            ),
            "impact": "high",
            "effort": "medium"
        })
        
        # Module recommendation
        recommendations.append({
            "priority": "medium",
            "area": "modules",
            "title": "Add social proof elements",
            "why": "Testimonials and case studies build credibility.",
            "suggestion": (
                "Include customer testimonials, case studies, "
                "or trust badges."
            ),
            "impact": "medium",
            "effort": "low"
        })
        
        return recommendations
    
    def _generate_url_copy_suggestions(
        self, url: str
    ) -> List[Dict[str, str]]:
        """
        Generate copy suggestions for URL analysis.
        
        Returns:
            List of copy suggestions.
        """
        suggestions = []
        
        suggestions.append({
            "section": "headline",
            "current": "Generic page headline",
            "suggested": (
                "Clear, benefit-driven headline addressing user needs"
            ),
            "reason": (
                "Strong headlines capture attention and set expectations"
            )
        })
        
        suggestions.append({
            "section": "subheadline",
            "current": "Basic description",
            "suggested": (
                "Compelling subheadline explaining key value proposition"
            ),
            "reason": (
                "Subheadlines provide context and reinforce main message"
            )
        })
        
    def _build_page_diagnostics(
        self, normalized_page: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build page diagnostics from normalized page data.
        
        Args:
            normalized_page: Normalized page data containing metadata,
                           headings, links, images, etc.
        
        Returns:
            Dictionary with page diagnostics including:
                - has_title: Whether page has a title
                - has_meta_description: Whether page has meta description
                - headings_count: Number of headings
                - links_count: Number of links
                - images_count: Number of images
                - has_error: Whether there was an error fetching/parsing
        """
        metadata = normalized_page.get("metadata", {})
        headings = normalized_page.get("headings", [])
        links = normalized_page.get("links", [])
        images = normalized_page.get("images", [])
        error = normalized_page.get("error")
        
        return {
            "has_title": bool(metadata.get("title", "").strip()),
            "has_meta_description": bool(
                metadata.get("meta_description", "").strip()
            ),
            "headings_count": len(headings),
            "links_count": len(links),
            "images_count": len(images),
            "has_error": error is not None
        }

        suggestions.append({
            "section": "cta",
            "current": "Learn more",
            "suggested": "Get started with your free trial",
            "reason": "Specific CTAs with clear value drive higher conversions"
        })
        
        return suggestions


# Made with Bob