"""
Catalog Context Builder
Builds relevant, compact catalog context for ICA agents without
requiring Knowledge Base.
"""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


def build_catalog_context(
    catalogs: Dict[str, List[Dict[str, Any]]],
    page_type: Optional[str] = None,
    business_goal: Optional[str] = None,
    target_audience: Optional[str] = None,
    detected_modules: Optional[List[Dict[str, Any]]] = None,
    score_breakdown: Optional[Dict[str, Any]] = None,
    narrative_insights: Optional[List[Dict[str, Any]]] = None,
    max_items_per_catalog: int = 8
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Build compact, relevant catalog context for ICA agents.
    
    Args:
        catalogs: Dictionary with all catalogs (modules_catalog,
                  storytelling_patterns, seo_rules, brand_rules)
        page_type: Page type (e.g., "credito_pessoal", "investimentos")
        business_goal: Business goal (e.g., "conversao", "educacao")
        target_audience: Target audience (e.g., "pessoa_fisica", "empresas")
        detected_modules: List of detected modules with confidence
        score_breakdown: Score breakdown with issues
        narrative_insights: List of narrative insights
        max_items_per_catalog: Maximum items per catalog (default: 8)
    
    Returns:
        Dictionary with relevant context:
        {
            "relevant_modules": [...],
            "relevant_storytelling_patterns": [...],
            "relevant_seo_rules": [...],
            "relevant_brand_rules": [...]
        }
    """
    detected_modules = detected_modules or []
    score_breakdown = score_breakdown or {}
    narrative_insights = narrative_insights or []
    
    logger.info(
        f"[CATALOG_CONTEXT] Building context for page_type={page_type}, "
        f"business_goal={business_goal}, target_audience={target_audience}"
    )
    
    # Extract catalog data
    modules_catalog = catalogs.get("modules_catalog", [])
    storytelling_patterns = catalogs.get("storytelling_patterns", [])
    seo_rules = catalogs.get("seo_rules", [])
    brand_rules = catalogs.get("brand_rules", [])
    
    # Build context for each catalog
    relevant_modules = _select_relevant_modules(
        modules_catalog=modules_catalog,
        detected_modules=detected_modules,
        storytelling_patterns=storytelling_patterns,
        page_type=page_type,
        max_items=max_items_per_catalog
    )
    
    relevant_storytelling = _select_relevant_storytelling_patterns(
        storytelling_patterns=storytelling_patterns,
        page_type=page_type,
        business_goal=business_goal,
        target_audience=target_audience,
        max_items=max_items_per_catalog
    )
    
    relevant_seo = _select_relevant_seo_rules(
        seo_rules=seo_rules,
        page_type=page_type,
        score_breakdown=score_breakdown,
        max_items=max_items_per_catalog
    )
    
    relevant_brand = _select_relevant_brand_rules(
        brand_rules=brand_rules,
        page_type=page_type,
        score_breakdown=score_breakdown,
        narrative_insights=narrative_insights,
        max_items=max_items_per_catalog
    )
    
    logger.info(
        f"[CATALOG_CONTEXT] Selected {len(relevant_modules)} modules, "
        f"{len(relevant_storytelling)} patterns, "
        f"{len(relevant_seo)} SEO rules, "
        f"{len(relevant_brand)} brand rules"
    )
    
    return {
        "relevant_modules": relevant_modules,
        "relevant_storytelling_patterns": relevant_storytelling,
        "relevant_seo_rules": relevant_seo,
        "relevant_brand_rules": relevant_brand
    }


def _select_relevant_modules(
    modules_catalog: List[Dict[str, Any]],
    detected_modules: List[Dict[str, Any]],
    storytelling_patterns: List[Dict[str, Any]],
    page_type: Optional[str],
    max_items: int
) -> List[Dict[str, Any]]:
    """
    Select relevant modules based on detected modules and
    storytelling patterns.
    """
    relevant_module_ids = set()
    
    # Add detected modules
    for module in detected_modules:
        module_id = module.get("id") or module.get("module_id")
        if module_id:
            relevant_module_ids.add(module_id)
    
    # Add required/recommended modules from matching storytelling pattern
    if page_type:
        for pattern in storytelling_patterns:
            if pattern.get("page_type") == page_type:
                # Add required modules
                for module_id in pattern.get("required_modules", []):
                    relevant_module_ids.add(module_id)
                
                # Add recommended modules from narrative steps
                for step in pattern.get("narrative_steps", []):
                    for module_id in step.get("recommended_modules", []):
                        relevant_module_ids.add(module_id)
                
                break
    
    # Find modules in catalog and compact them
    relevant_modules = []
    for module in modules_catalog:
        if module.get("id") in relevant_module_ids:
            relevant_modules.append(_compact_module(module))
            if len(relevant_modules) >= max_items:
                break
    
    return relevant_modules


def _select_relevant_storytelling_patterns(
    storytelling_patterns: List[Dict[str, Any]],
    page_type: Optional[str],
    business_goal: Optional[str],
    target_audience: Optional[str],
    max_items: int
) -> List[Dict[str, Any]]:
    """
    Select relevant storytelling patterns based on page type,
    goal, and audience.
    """
    scored_patterns = []
    
    for pattern in storytelling_patterns:
        score = 0
        
        # Exact match on page_type (highest priority)
        if page_type and pattern.get("page_type") == page_type:
            score += 100
        
        # Match on business_goal
        if business_goal and pattern.get("business_goal") == business_goal:
            score += 50
        
        # Match on target_audience
        pattern_audience = pattern.get("target_audience")
        if target_audience and pattern_audience == target_audience:
            score += 30
        
        # Partial match on page_type (contains)
        if page_type and page_type in str(pattern.get("page_type", "")):
            score += 20
        
        if score > 0:
            scored_patterns.append((score, pattern))
    
    # Sort by score descending
    scored_patterns.sort(key=lambda x: x[0], reverse=True)
    
    # Take top patterns and compact them
    relevant_patterns = []
    for _, pattern in scored_patterns[:max_items]:
        relevant_patterns.append(_compact_storytelling_pattern(pattern))
    
    # If no matches, return top high-priority patterns as fallback
    if not relevant_patterns:
        logger.info("[CATALOG_CONTEXT] No matching patterns, using fallback")
        for pattern in storytelling_patterns[:max_items]:
            relevant_patterns.append(_compact_storytelling_pattern(pattern))
    
    return relevant_patterns


def _select_relevant_seo_rules(
    seo_rules: List[Dict[str, Any]],
    page_type: Optional[str],
    score_breakdown: Dict[str, Any],
    max_items: int
) -> List[Dict[str, Any]]:
    """
    Select relevant SEO rules based on severity, page type,
    and score issues.
    """
    scored_rules = []
    
    # Extract rule IDs mentioned in score breakdown
    mentioned_rule_ids = set()
    for category_data in score_breakdown.values():
        if isinstance(category_data, dict):
            for issue in category_data.get("issues", []):
                rule_id = issue.get("rule_id")
                if rule_id:
                    mentioned_rule_ids.add(rule_id)
    
    for rule in seo_rules:
        score = 0
        rule_id = rule.get("id", "")
        severity = rule.get("severity", "").lower()
        applies_to = rule.get("applies_to", [])
        
        # Mentioned in score breakdown (highest priority)
        if rule_id in mentioned_rule_ids:
            score += 200
        
        # High severity rules
        if severity == "high":
            score += 100
        elif severity == "medium":
            score += 50
        elif severity == "low":
            score += 20
        
        # Applies to page type
        if page_type:
            if "all" in applies_to:
                score += 30
            elif page_type in applies_to:
                score += 60
        else:
            # If no page_type, prioritize "all" rules
            if "all" in applies_to:
                score += 40
        
        if score > 0:
            scored_rules.append((score, rule))
    
    # Sort by score descending
    scored_rules.sort(key=lambda x: x[0], reverse=True)
    
    # Take top rules and compact them
    relevant_rules = []
    for _, rule in scored_rules[:max_items]:
        relevant_rules.append(_compact_seo_rule(rule))
    
    # If no matches, return top high severity rules as fallback
    if not relevant_rules:
        logger.info(
            "[CATALOG_CONTEXT] No matching SEO rules, "
            "using high severity fallback"
        )
        high_severity = [
            r for r in seo_rules if r.get("severity") == "high"
        ]
        for rule in high_severity[:max_items]:
            relevant_rules.append(_compact_seo_rule(rule))
    
    return relevant_rules


def _select_relevant_brand_rules(
    brand_rules: List[Dict[str, Any]],
    page_type: Optional[str],
    score_breakdown: Dict[str, Any],
    narrative_insights: List[Dict[str, Any]],
    max_items: int
) -> List[Dict[str, Any]]:
    """
    Select relevant brand rules based on severity, page type,
    and detected issues.
    """
    scored_rules = []
    
    # Extract keywords from narrative insights
    insight_keywords = set()
    for insight in narrative_insights:
        insight_text = str(insight.get("insight", "")).lower()
        insight_keywords.update(insight_text.split())
    
    # Extract rule IDs mentioned in score breakdown
    mentioned_rule_ids = set()
    for category_data in score_breakdown.values():
        if isinstance(category_data, dict):
            for issue in category_data.get("issues", []):
                rule_id = issue.get("rule_id")
                if rule_id:
                    mentioned_rule_ids.add(rule_id)
    
    for rule in brand_rules:
        score = 0
        rule_id = rule.get("id", "")
        severity = rule.get("severity", "").lower()
        applies_to = rule.get("applies_to", [])
        detection_keywords = rule.get("detection_keywords", [])
        
        # Mentioned in score breakdown (highest priority)
        if rule_id in mentioned_rule_ids:
            score += 200
        
        # High severity rules
        if severity == "high":
            score += 100
        elif severity == "medium":
            score += 50
        elif severity == "low":
            score += 20
        
        # Applies to page type
        if page_type:
            if "all" in applies_to:
                score += 30
            elif page_type in applies_to:
                score += 60
        else:
            # If no page_type, prioritize "all" rules
            if "all" in applies_to:
                score += 40
        
        # Detection keywords match insights
        for keyword in detection_keywords:
            if keyword.lower() in insight_keywords:
                score += 40
                break
        
        if score > 0:
            scored_rules.append((score, rule))
    
    # Sort by score descending
    scored_rules.sort(key=lambda x: x[0], reverse=True)
    
    # Take top rules and compact them
    relevant_rules = []
    for _, rule in scored_rules[:max_items]:
        relevant_rules.append(_compact_brand_rule(rule))
    
    # If no matches, return top high severity rules as fallback
    if not relevant_rules:
        logger.info(
            "[CATALOG_CONTEXT] No matching brand rules, "
            "using high severity fallback"
        )
        high_severity = [
            r for r in brand_rules if r.get("severity") == "high"
        ]
        for rule in high_severity[:max_items]:
            relevant_rules.append(_compact_brand_rule(rule))
    
    return relevant_rules


def _compact_module(module: Dict[str, Any]) -> Dict[str, Any]:
    """Compact module to essential fields for ICA."""
    return {
        "id": module.get("id"),
        "name": module.get("name"),
        "display_name": module.get("display_name"),
        "generic_type": module.get("generic_type"),
        "description": module.get("description"),
        "purpose": module.get("purpose"),
        "good_for": module.get("good_for", []),
        "bad_for": module.get("bad_for", []),
        "recommendation_rules": module.get("recommendation_rules", {})
    }


def _compact_storytelling_pattern(pattern: Dict[str, Any]) -> Dict[str, Any]:
    """Compact storytelling pattern to essential fields for ICA."""
    return {
        "id": pattern.get("id"),
        "page_type": pattern.get("page_type"),
        "storytelling_name": pattern.get("storytelling_name"),
        "description": pattern.get("description"),
        "business_goal": pattern.get("business_goal"),
        "target_audience": pattern.get("target_audience"),
        "narrative_steps": pattern.get("narrative_steps", []),
        "required_modules": pattern.get("required_modules", []),
        "recommended_module_order": pattern.get(
            "recommended_module_order", []
        ),
        "tone_guidelines": pattern.get("tone_guidelines", []),
        "agent_evaluation_rules": pattern.get("agent_evaluation_rules", {})
    }


def _compact_seo_rule(rule: Dict[str, Any]) -> Dict[str, Any]:
    """Compact SEO rule to essential fields for ICA."""
    return {
        "id": rule.get("id"),
        "category": rule.get("category"),
        "severity": rule.get("severity"),
        "rule_name": rule.get("rule_name"),
        "description": rule.get("description"),
        "recommended_action": rule.get("recommended_action"),
        "score_impact": rule.get("score_impact", {}),
        "agent_guidance": rule.get("agent_guidance", {})
    }


def _compact_brand_rule(rule: Dict[str, Any]) -> Dict[str, Any]:
    """Compact brand rule to essential fields for ICA."""
    return {
        "id": rule.get("id"),
        "category": rule.get("category"),
        "severity": rule.get("severity"),
        "rule_name": rule.get("rule_name"),
        "description": rule.get("description"),
        "applies_to": rule.get("applies_to", []),
        "recommended_action": rule.get("recommended_action"),
        "safe_alternatives": rule.get("safe_alternatives", []),
        "detection_keywords": rule.get("detection_keywords", []),
        "agent_guidance": rule.get("agent_guidance", {})
    }


# Made with Bob