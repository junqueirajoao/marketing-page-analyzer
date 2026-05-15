"""
Local Agent Fallback
Provides local analysis when ICA is unavailable.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.services.storytelling_pattern_service import (
    build_storytelling_analysis,
    find_best_storytelling_pattern,
    get_storytelling_patterns,
)
from app.services.scoring_service import calculate_scores
from app.utils.analysis_messages import (
    AGENT_NAMES,
    AGENT_SUMMARIES,
    RECOMMENDATION_MESSAGES,
    NARRATIVE_INSIGHT_MESSAGES,
    NARRATIVE_INSIGHT_TYPES,
    SEVERITY_LEVELS,
    MODULE_PLAN_MESSAGES,
    PAGE_SUMMARY_MESSAGES,
    STATUS_MESSAGES,
    PRIORITY_LEVELS,
    IMPACT_LEVELS,
    EFFORT_LEVELS,
    AREA_NAMES,
    format_message
)


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
                - narrative_insights
                - catalog_context
                - agent_trace
        """
        # Extract payload data
        briefing = payload.get("briefing", "")
        business_goal = payload.get("business_goal", "nao_informado")
        target_audience = payload.get("target_audience", "nao_informado")
        constraints = payload.get("constraints", [])
        catalogs = payload.get("catalogs", {})
        
        storytelling_pattern = self._select_storytelling_pattern(
            catalogs=catalogs,
            page_type=None,
            business_goal=business_goal,
            target_audience=target_audience,
            text_context=briefing,
        )
        storytelling_analysis = build_storytelling_analysis(
            storytelling_pattern
        )

        agent_trace = self._build_agent_trace(briefing, business_goal)
        analysis_id = self._generate_analysis_id()
        page_summary = self._build_page_summary(
            briefing, business_goal, target_audience
        )
        recommendations = self._generate_recommendations(
            business_goal=business_goal,
            constraints=constraints,
            pattern=storytelling_pattern,
            text_context=briefing,
        )
        module_plan = self._build_module_plan(
            catalogs=catalogs,
            pattern=storytelling_pattern,
            detected_modules=[],
        )
        narrative_insights = self._generate_narrative_insights(
            pattern=storytelling_pattern,
            detected_modules=[],
            catalogs=catalogs,
        )
        catalog_context = self._build_catalog_context(catalogs)
        
        # Calculate dynamic scores
        scoring_result = calculate_scores(
            normalized_page={
                "metadata": {},
                "headings": [],
                "images": [],
                "links": [],
                "main_text": briefing,
            },
            detected_modules=[],
            module_plan=module_plan,
            storytelling_analysis=storytelling_analysis,
            narrative_insights=narrative_insights,
            brand_rules=catalogs.get("brand_rules", []),
            seo_rules=catalogs.get("seo_rules", []),
            pattern=storytelling_pattern,
        )

        return {
            "analysis_id": analysis_id,
            "score": scoring_result["score"],
            "score_breakdown": scoring_result["score_breakdown"],
            "page_summary": page_summary,
            "recommendations": recommendations,
            "module_plan": module_plan,
            "narrative_insights": narrative_insights,
            "catalog_context": catalog_context,
            "agent_trace": agent_trace,
            "storytelling_analysis": storytelling_analysis,
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
                - narrative_insights
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
        
        text_context = self._build_url_context(
            url=url,
            business_goal=business_goal,
            normalized_page=normalized_page,
        )
        storytelling_pattern = self._select_storytelling_pattern(
            catalogs=catalogs,
            page_type=page_type_hint,
            business_goal=business_goal,
            target_audience=target_audience,
            text_context=text_context,
        )
        storytelling_analysis = build_storytelling_analysis(
            storytelling_pattern
        )

        page_diagnostics = self._build_page_diagnostics(normalized_page)
        agent_trace = self._build_url_agent_trace(url)
        analysis_id = self._generate_analysis_id()
        page_summary = self._build_url_page_summary(
            url, business_goal, target_audience, page_type_hint
        )
        recommendations = self._generate_recommendations(
            business_goal=business_goal,
            constraints=[],
            pattern=storytelling_pattern,
            text_context=text_context,
        )
        module_plan = self._build_module_plan(
            catalogs=catalogs,
            pattern=storytelling_pattern,
            detected_modules=normalized_page.get("modules", []),
        )
        narrative_insights = self._generate_narrative_insights(
            pattern=storytelling_pattern,
            detected_modules=normalized_page.get("modules", []),
            catalogs=catalogs,
        )
        catalog_context = self._build_catalog_context(catalogs)
        
        # Calculate dynamic scores
        scoring_result = calculate_scores(
            normalized_page=normalized_page,
            detected_modules=normalized_page.get("modules", []),
            module_plan=module_plan,
            storytelling_analysis=storytelling_analysis,
            narrative_insights=narrative_insights,
            brand_rules=catalogs.get("brand_rules", []),
            seo_rules=catalogs.get("seo_rules", []),
            pattern=storytelling_pattern,
        )

        return {
            "analysis_id": analysis_id,
            "score": scoring_result["score"],
            "score_breakdown": scoring_result["score_breakdown"],
            "page_summary": page_summary,
            "recommendations": recommendations,
            "module_plan": module_plan,
            "narrative_insights": narrative_insights,
            "catalog_context": catalog_context,
            "agent_trace": agent_trace,
            "page_diagnostics": page_diagnostics,
            "storytelling_analysis": storytelling_analysis,
            "detected_modules": normalized_page.get("modules", []),
        }
    
    def _generate_analysis_id(self) -> str:
        """Generate a unique analysis ID."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"analysis_{timestamp}"
    
    def _build_agent_trace(
        self, briefing: str, business_goal: str
    ) -> List[Dict[str, Any]]:
        """Build the agent trace showing simulated agent execution."""
        trace = []
        
        # Orchestrator Agent
        trace.append({
            "agent": AGENT_NAMES["orchestrator"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["orchestrator_briefing"]
        })
        
        # SEO Agent
        trace.append({
            "agent": AGENT_NAMES["seo"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["seo_briefing"]
        })
        
        # Module Strategy Agent
        trace.append({
            "agent": AGENT_NAMES["module_strategy"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["module_strategy_briefing"]
        })
        
        # Storytelling Agent
        trace.append({
            "agent": AGENT_NAMES["storytelling"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["storytelling_briefing"]
        })
        
        # Brand Safety Agent
        trace.append({
            "agent": AGENT_NAMES["brand_safety"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["brand_safety"]
        })
        
        # Recommendation Agent
        trace.append({
            "agent": AGENT_NAMES["recommendation"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["recommendation"]
        })
        
        return trace
    
    def _build_page_summary(
        self, briefing: str, business_goal: str, target_audience: str
    ) -> Dict[str, str]:
        """Build page summary based on briefing analysis."""
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
            "main_topic": "Tópico extraído da análise do briefing"
        }
    
    def _generate_recommendations(
        self,
        business_goal: str,
        constraints: List[str],
        pattern: Optional[Dict[str, Any]],
        text_context: str,
    ) -> List[Dict[str, Any]]:
        """Generate pattern-based recommendations."""
        recommendations: List[Dict[str, Any]] = []

        narrative_steps = []
        if pattern:
            narrative_steps = [
                str(step.get("name"))
                for step in pattern.get("narrative_steps", [])
                if isinstance(step, dict) and step.get("name")
            ]

        if narrative_steps:
            recommendations.append({
                "priority": PRIORITY_LEVELS["high"],
                "area": AREA_NAMES["storytelling"],
                "title": RECOMMENDATION_MESSAGES["narrative_title"],
                "why": RECOMMENDATION_MESSAGES["narrative_why"],
                "suggestion": format_message(
                    RECOMMENDATION_MESSAGES["narrative_suggestion"],
                    sequence=" → ".join(narrative_steps)
                ),
                "impact": IMPACT_LEVELS["high"],
                "effort": EFFORT_LEVELS["medium"]
            })

        cta_examples = []
        if pattern:
            cta_examples = list(pattern.get("cta_examples") or [])
        if cta_examples:
            recommendations.append({
                "priority": PRIORITY_LEVELS["high"],
                "area": AREA_NAMES["conversion"],
                "title": RECOMMENDATION_MESSAGES["cta_title"],
                "why": RECOMMENDATION_MESSAGES["cta_why"],
                "suggestion": format_message(
                    RECOMMENDATION_MESSAGES["cta_suggestion"],
                    examples="; ".join(cta_examples[:3])
                ),
                "impact": IMPACT_LEVELS["high"],
                "effort": EFFORT_LEVELS["low"]
            })

        compliance_guidelines = []
        avoid_copy = []
        if pattern:
            compliance_guidelines = list(
                pattern.get("compliance_guidelines") or []
            )
            avoid_copy = list(pattern.get("avoid_copy") or [])
        if compliance_guidelines or avoid_copy:
            safety_parts = []
            if compliance_guidelines:
                safety_parts.append(
                    format_message(
                        RECOMMENDATION_MESSAGES["brand_safety_compliance"],
                        guidelines="; ".join(compliance_guidelines[:3])
                    )
                )
            if avoid_copy:
                safety_parts.append(
                    format_message(
                        RECOMMENDATION_MESSAGES["brand_safety_avoid"],
                        avoid="; ".join(avoid_copy[:3])
                    )
                )
            recommendations.append({
                "priority": PRIORITY_LEVELS["high"],
                "area": AREA_NAMES["brand_safety"],
                "title": RECOMMENDATION_MESSAGES["brand_safety_title"],
                "why": RECOMMENDATION_MESSAGES["brand_safety_why"],
                "suggestion": " ".join(safety_parts),
                "impact": IMPACT_LEVELS["high"],
                "effort": EFFORT_LEVELS["low"]
            })

        avoid_modules_when = []
        if pattern:
            avoid_modules_when = list(pattern.get("avoid_modules_when") or [])
        for avoid_rule in avoid_modules_when:
            if not isinstance(avoid_rule, dict):
                continue
            module_name = str(avoid_rule.get("module") or "").strip()
            reason = str(avoid_rule.get("reason") or "").strip()
            if module_name and reason:
                recommendations.append({
                    "priority": PRIORITY_LEVELS["medium"],
                    "area": AREA_NAMES["modules"],
                    "title": format_message(
                        RECOMMENDATION_MESSAGES["avoid_module_title"],
                        module=module_name
                    ),
                    "why": reason,
                    "suggestion": format_message(
                        RECOMMENDATION_MESSAGES["avoid_module_suggestion"],
                        module=module_name
                    ),
                    "impact": IMPACT_LEVELS["medium"],
                    "effort": EFFORT_LEVELS["low"]
                })

        if len(text_context) < 200:
            recommendations.append({
                "priority": PRIORITY_LEVELS["medium"],
                "area": AREA_NAMES["seo"],
                "title": RECOMMENDATION_MESSAGES["expand_content_title"],
                "why": RECOMMENDATION_MESSAGES["expand_content_why"],
                "suggestion": (
                    RECOMMENDATION_MESSAGES["expand_content_suggestion"]
                ),
                "impact": IMPACT_LEVELS["medium"],
                "effort": EFFORT_LEVELS["medium"]
            })

        if constraints:
            recommendations.append({
                "priority": PRIORITY_LEVELS["low"],
                "area": AREA_NAMES["execution"],
                "title": RECOMMENDATION_MESSAGES["validate_constraints_title"],
                "why": RECOMMENDATION_MESSAGES["validate_constraints_why"],
                "suggestion": format_message(
                    RECOMMENDATION_MESSAGES["validate_constraints_suggestion"],
                    constraints="; ".join(constraints[:3])
                ),
                "impact": IMPACT_LEVELS["medium"],
                "effort": EFFORT_LEVELS["low"]
            })

        return recommendations

    def _build_module_plan(
        self,
        catalogs: Dict[str, Any],
        pattern: Optional[Dict[str, Any]],
        detected_modules: List[Dict[str, Any]],
    ) -> Dict[str, List[Any]]:
        """Build module plan using the detected storytelling pattern."""
        detected_names = [
            str(module.get("matched_catalog_name") or "").strip()
            for module in detected_modules
            if isinstance(module, dict)
        ]
        detected_name_set = {name for name in detected_names if name}

        required_modules = []
        optional_modules = []
        recommended_order = []
        avoid_modules_when = []
        if pattern:
            required_modules = list(pattern.get("required_modules") or [])
            optional_modules = list(pattern.get("optional_modules") or [])
            recommended_order = list(
                pattern.get("recommended_module_order") or []
            )
            avoid_modules_when = list(
                pattern.get("avoid_modules_when") or []
            )

        keep = []
        for module_name in detected_names:
            if (
                module_name in recommended_order
                or module_name in required_modules
            ):
                keep.append(module_name)

        reorder = []
        for index, module_name in enumerate(recommended_order, start=1):
            if module_name in detected_name_set:
                reorder.append({
                    "module_type": module_name,
                    "suggested_position": index,
                    "reason": MODULE_PLAN_MESSAGES["reorder_reason"]
                })

        add = []
        for module_name in required_modules:
            if module_name not in detected_name_set:
                add.append({
                    "module_type": module_name,
                    "reason": MODULE_PLAN_MESSAGES["add_required_reason"]
                })

        for module_name in optional_modules:
            if (
                module_name not in detected_name_set
                and module_name in recommended_order
            ):
                add.append({
                    "module_type": module_name,
                    "reason": MODULE_PLAN_MESSAGES["add_optional_reason"]
                })

        remove = []
        for avoid_rule in avoid_modules_when:
            if not isinstance(avoid_rule, dict):
                continue
            module_name = str(avoid_rule.get("module") or "").strip()
            reason = str(avoid_rule.get("reason") or "").strip()
            if module_name and module_name in detected_name_set:
                remove.append({
                    "module_type": module_name,
                    "reason": reason
                })

        if not detected_name_set:
            for module_name in required_modules:
                if not any(
                    item.get("module_type") == module_name for item in add
                ):
                    add.append({
                        "module_type": module_name,
                        "reason": (
                            MODULE_PLAN_MESSAGES["add_no_modules_reason"]
                        )
                    })

        return {
            "keep": keep,
            "remove": remove,
            "reorder": reorder,
            "add": add
        }

    def _generate_narrative_insights(
        self,
        pattern: Optional[Dict[str, Any]],
        detected_modules: List[Dict[str, Any]],
        catalogs: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Generate narrative insights based on storytelling pattern."""
        insights: List[Dict[str, Any]] = []
        
        if not pattern:
            return insights
        
        # Extract pattern data
        narrative_steps = pattern.get("narrative_steps", [])
        required_modules = pattern.get("required_modules", [])
        recommended_order = pattern.get("recommended_module_order", [])
        compliance_guidelines = pattern.get("compliance_guidelines", [])
        avoid_modules_when = pattern.get("avoid_modules_when", [])
        emotional_journey = pattern.get("emotional_journey", [])
        
        # Get detected module names
        detected_module_names = {
            str(m.get("matched_catalog_name", "")).strip()
            for m in detected_modules
            if isinstance(m, dict)
        }
        
        # Check for missing required modules (module_gap)
        for required_module in required_modules:
            if required_module not in detected_module_names:
                module_id = (
                    f"insight_missing_module_"
                    f"{required_module.lower().replace(' ', '_')}"
                )
                insights.append({
                    "id": module_id,
                    "type": NARRATIVE_INSIGHT_TYPES["module_gap"],
                    "severity": SEVERITY_LEVELS["high"],
                    "title": format_message(
                        NARRATIVE_INSIGHT_MESSAGES["module_gap_title"]
                    ),
                    "description": format_message(
                        NARRATIVE_INSIGHT_MESSAGES["module_gap_description"],
                        module_name=required_module
                    ),
                    "related_modules": [required_module],
                    "recommended_actions": [
                        f"Adicionar módulo '{required_module}'",
                        "Revisar arquitetura da página",
                        "Validar com o storytelling pattern"
                    ]
                })
        
        # Check for missing narrative steps (missing_step)
        for step in narrative_steps:
            if not isinstance(step, dict):
                continue
            step_name = str(step.get("name", "")).strip()
            step_modules = step.get("recommended_modules", [])
            
            # Check if any of the step's recommended modules are present
            has_step_module = any(
                mod in detected_module_names for mod in step_modules
            )
            
            if not has_step_module and step_modules:
                step_id = (
                    f"insight_missing_step_"
                    f"{step_name.lower().replace(' ', '_')}"
                )
                insights.append({
                    "id": step_id,
                    "type": NARRATIVE_INSIGHT_TYPES["missing_step"],
                    "severity": SEVERITY_LEVELS["high"],
                    "title": format_message(
                        NARRATIVE_INSIGHT_MESSAGES["missing_step_title"],
                        step_name=step_name
                    ),
                    "description": format_message(
                        NARRATIVE_INSIGHT_MESSAGES["missing_step_description"],
                        step_name=step_name
                    ),
                    "related_modules": step_modules,
                    "recommended_actions": [
                        f"Adicionar etapa narrativa: {step_name}",
                        f"Considerar módulos: {', '.join(step_modules[:3])}",
                        "Revisar progressão do storytelling"
                    ]
                })
        
        # Check for missing objection handling (FAQ/Accordion)
        has_faq = any(
            "accordion" in str(m.get("matched_catalog_name", "")).lower()
            or "faq" in str(m.get("matched_catalog_name", "")).lower()
            for m in detected_modules
        )
        
        if not has_faq and "Accordion" in required_modules:
            insights.append({
                "id": "insight_missing_objection_handling",
                "type": NARRATIVE_INSIGHT_TYPES["missing_objection_handling"],
                "severity": SEVERITY_LEVELS["high"],
                "title": NARRATIVE_INSIGHT_MESSAGES["missing_objection_handling_title"],
                "description": NARRATIVE_INSIGHT_MESSAGES["missing_objection_handling_description"],
                "related_modules": ["Accordion", "FAQ"],
                "recommended_actions": [
                    "Adicionar seção de FAQ",
                    "Incluir perguntas sobre segurança e condições",
                    "Reduzir incertezas antes da conversão"
                ]
            })
        
        # Check for poor module order (narrative_break)
        if detected_modules and recommended_order:
            detected_order = [
                str(m.get("matched_catalog_name", "")).strip()
                for m in detected_modules
                if isinstance(m, dict)
            ]
            
            # Simple check: if modules are present but not in order
            order_issues = []
            for i, module_name in enumerate(detected_order):
                if module_name in recommended_order:
                    recommended_pos = recommended_order.index(module_name)
                    if i > 0 and recommended_pos < len(recommended_order) - 1:
                        # Check if previous module should come after
                        prev_module = detected_order[i-1]
                        if prev_module in recommended_order:
                            prev_pos = recommended_order.index(prev_module)
                            if prev_pos > recommended_pos:
                                order_issues.append(module_name)
            
            if order_issues:
                insights.append({
                    "id": "insight_narrative_break",
                    "type": NARRATIVE_INSIGHT_TYPES["narrative_break"],
                    "severity": SEVERITY_LEVELS["medium"],
                    "title": NARRATIVE_INSIGHT_MESSAGES["narrative_break_title"],
                    "description": NARRATIVE_INSIGHT_MESSAGES["narrative_break_description"],
                    "related_modules": order_issues[:3],
                    "recommended_actions": [
                        "Reorganizar módulos conforme storytelling pattern",
                        f"Seguir ordem recomendada: {' → '.join(recommended_order[:5])}",
                        "Validar progressão narrativa"
                    ]
                })
        
        # Check for compliance risks
        brand_rules = catalogs.get("brand_rules", [])
        if brand_rules and compliance_guidelines:
            insights.append({
                "id": "insight_compliance_check",
                "type": NARRATIVE_INSIGHT_TYPES["compliance_risk"],
                "severity": SEVERITY_LEVELS["medium"],
                "title": NARRATIVE_INSIGHT_MESSAGES["compliance_risk_title"],
                "description": format_message(
                    NARRATIVE_INSIGHT_MESSAGES["compliance_risk_description"],
                    issue="Validar conformidade com diretrizes de marca"
                ),
                "related_modules": [],
                "recommended_actions": [
                    f"Seguir: {'; '.join(compliance_guidelines[:3])}",
                    "Revisar copy contra regras de marca",
                    "Evitar promessas absolutas"
                ]
            })
        
        # Check for weak value proposition (missing benefit modules)
        has_benefits = any(
            "card" in str(m.get("matched_catalog_name", "")).lower()
            or "icon" in str(m.get("matched_catalog_name", "")).lower()
            or "benefit" in str(m.get("matched_catalog_name", "")).lower()
            for m in detected_modules
        )
        
        if not has_benefits:
            insights.append({
                "id": "insight_weak_value_proposition",
                "type": NARRATIVE_INSIGHT_TYPES["weak_value_proposition"],
                "severity": SEVERITY_LEVELS["medium"],
                "title": NARRATIVE_INSIGHT_MESSAGES["weak_value_proposition_title"],
                "description": NARRATIVE_INSIGHT_MESSAGES["weak_value_proposition_description"],
                "related_modules": ["Card with icon", "Image Icon"],
                "recommended_actions": [
                    "Adicionar módulo de benefícios escaneáveis",
                    "Destacar vantagens práticas",
                    "Usar ícones para facilitar leitura"
                ]
            })
        
        # Check for poor emotional journey alignment
        if emotional_journey and len(emotional_journey) > 0:
            insights.append({
                "id": "insight_emotional_journey",
                "type": NARRATIVE_INSIGHT_TYPES["poor_module_order"],
                "severity": SEVERITY_LEVELS["low"],
                "title": NARRATIVE_INSIGHT_MESSAGES["poor_module_order_title"],
                "description": format_message(
                    NARRATIVE_INSIGHT_MESSAGES["poor_module_order_description"],
                    journey=" → ".join(emotional_journey)
                ),
                "related_modules": recommended_order[:3],
                "recommended_actions": [
                    f"Seguir jornada emocional: {' → '.join(emotional_journey)}",
                    "Alinhar módulos com progressão emocional",
                    "Validar fluxo narrativo"
                ]
            })
        
        return insights
    
    def _build_catalog_context(
        self, catalogs: Dict[str, Any]
    ) -> Dict[str, int]:
        """Build catalog context showing available resources."""
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
        """Build agent trace for URL analysis."""
        trace = []
        
        # Orchestrator Agent
        trace.append({
            "agent": AGENT_NAMES["orchestrator"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["orchestrator_url"]
        })
        
        # SEO Agent
        trace.append({
            "agent": AGENT_NAMES["seo"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["seo_url"]
        })
        
        # Module Strategy Agent
        trace.append({
            "agent": AGENT_NAMES["module_strategy"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["module_strategy_url"]
        })
        
        # Storytelling Agent
        trace.append({
            "agent": AGENT_NAMES["storytelling"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["storytelling_url"]
        })
        
        # Brand Safety Agent
        trace.append({
            "agent": AGENT_NAMES["brand_safety"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["brand_safety_url"]
        })
        
        # Recommendation Agent
        trace.append({
            "agent": AGENT_NAMES["recommendation"],
            "status": STATUS_MESSAGES["completed"],
            "summary": AGENT_SUMMARIES["recommendation_url"]
        })
        
        return trace
    
    
    def _build_url_page_summary(
        self,
        url: str,
        business_goal: str,
        target_audience: str,
        page_type_hint: Optional[str]
    ) -> Dict[str, str]:
        """Build page summary for URL analysis."""
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
                detected_type = "desconhecido"
        
        # Extract topic from URL
        main_topic = format_message(
            PAGE_SUMMARY_MESSAGES["main_topic_url"],
            url=url
        )
        
        return {
            "detected_type": detected_type,
            "primary_goal": business_goal,
            "main_topic": main_topic
        }
    
    def _select_storytelling_pattern(
        self,
        catalogs: Dict[str, Any],
        page_type: Optional[str],
        business_goal: Optional[str],
        target_audience: Optional[str],
        text_context: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        patterns = get_storytelling_patterns(catalogs)
        return find_best_storytelling_pattern(
            patterns=patterns,
            page_type=page_type,
            business_goal=business_goal,
            target_audience=target_audience,
            text_context=text_context,
        )

    def _build_url_context(
        self,
        url: str,
        business_goal: Optional[str],
        normalized_page: Dict[str, Any],
    ) -> str:
        main_text = str(normalized_page.get("main_text") or "")
        goal = str(business_goal or "")
        return " ".join(part for part in [url, goal, main_text] if part)
    
    def _build_page_diagnostics(
        self, normalized_page: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build page diagnostics from normalized page data."""
        metadata = normalized_page.get("metadata", {})
        headings = normalized_page.get("headings", [])
        links = normalized_page.get("links", [])
        images = normalized_page.get("images", [])
        modules = normalized_page.get("modules", [])
        error = normalized_page.get("error")
        
        return {
            "has_title": bool(metadata.get("title", "").strip()),
            "has_meta_description": bool(
                metadata.get("meta_description", "").strip()
            ),
            "headings_count": len(headings),
            "links_count": len(links),
            "images_count": len(images),
            "has_error": error is not None,
            "modules_detected_count": len(modules)
        }


# Made with Bob