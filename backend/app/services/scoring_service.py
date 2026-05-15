"""
Dynamic scoring service for marketing page analysis.
Calculates scores based on actual page data and analysis results.
"""
from typing import Dict, Any, List, Optional


def calculate_scores(
    normalized_page: Dict[str, Any],
    detected_modules: List[Dict[str, Any]],
    module_plan: Dict[str, List[Any]],
    storytelling_analysis: Dict[str, Any],
    narrative_insights: List[Dict[str, Any]],
    brand_rules: List[Dict[str, Any]],
    pattern: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Calculate all scores dynamically based on analysis data.
    
    Returns:
        Dictionary with scores and score_breakdown
    """
    seo_score, seo_breakdown = calculate_seo_score(normalized_page)
    
    storytelling_score, storytelling_breakdown = (
        calculate_storytelling_score(
            pattern=pattern,
            detected_modules=detected_modules,
            narrative_insights=narrative_insights,
            storytelling_analysis=storytelling_analysis,
        )
    )
    
    modules_score, modules_breakdown = calculate_modules_score(
        detected_modules=detected_modules,
        module_plan=module_plan,
        pattern=pattern,
    )
    
    brand_safety_score, brand_safety_breakdown = (
        calculate_brand_safety_score(
            normalized_page=normalized_page,
            brand_rules=brand_rules,
            narrative_insights=narrative_insights,
            pattern=pattern,
        )
    )
    
    overall_score = calculate_overall_score(
        seo_score=seo_score,
        storytelling_score=storytelling_score,
        modules_score=modules_score,
        brand_safety_score=brand_safety_score,
    )
    
    return {
        "score": {
            "overall": overall_score,
            "seo": seo_score,
            "storytelling": storytelling_score,
            "modules": modules_score,
            "brand_safety": brand_safety_score,
        },
        "score_breakdown": {
            "seo": seo_breakdown,
            "storytelling": storytelling_breakdown,
            "modules": modules_breakdown,
            "brand_safety": brand_safety_breakdown,
        }
    }


def calculate_seo_score(
    normalized_page: Dict[str, Any]
) -> tuple[int, List[Dict[str, Any]]]:
    """
    Calculate SEO score based on page metadata and structure.
    Starts at 100 and deducts points for issues.
    """
    score = 100
    breakdown = []
    
    metadata = normalized_page.get("metadata", {})
    headings = normalized_page.get("headings", [])
    images = normalized_page.get("images", [])
    links = normalized_page.get("links", [])
    main_text = normalized_page.get("main_text", "")
    
    # Title checks
    title = metadata.get("title", "").strip()
    if not title:
        score -= 20
        breakdown.append({
            "criterion": "title_missing",
            "impact": -20,
            "reason": "Tag de título ausente."
        })
    elif len(title) < 30 or len(title) > 60:
        score -= 8
        breakdown.append({
            "criterion": "title_length",
            "impact": -8,
            "reason": f"Título com {len(title)} caracteres (ideal: 30-60)."
        })
    
    # Meta description checks
    meta_desc = metadata.get("meta_description", "").strip()
    if not meta_desc:
        score -= 15
        breakdown.append({
            "criterion": "meta_description_missing",
            "impact": -15,
            "reason": "Meta description ausente."
        })
    elif len(meta_desc) < 120 or len(meta_desc) > 160:
        score -= 8
        breakdown.append({
            "criterion": "meta_description_length",
            "impact": -8,
            "reason": (
                f"Meta description com {len(meta_desc)} caracteres "
                "(ideal: 120-160)."
            )
        })
    
    # H1 checks
    h1_count = sum(1 for h in headings if h.get("level") == 1)
    if h1_count == 0:
        score -= 20
        breakdown.append({
            "criterion": "h1_missing",
            "impact": -20,
            "reason": "H1 ausente na página."
        })
    elif h1_count > 1:
        score -= 8
        breakdown.append({
            "criterion": "multiple_h1",
            "impact": -8,
            "reason": f"Múltiplos H1 detectados ({h1_count})."
        })
    
    # H2 checks
    h2_count = sum(1 for h in headings if h.get("level") == 2)
    if h2_count == 0:
        score -= 6
        breakdown.append({
            "criterion": "h2_missing",
            "impact": -6,
            "reason": "Ausência de H2 para estruturar conteúdo."
        })
    
    # Image alt checks
    images_without_alt = sum(
        1 for img in images
        if not img.get("alt", "").strip()
    )
    if images_without_alt > 0:
        penalty = min(15, images_without_alt * 3)
        score -= penalty
        breakdown.append({
            "criterion": "images_without_alt",
            "impact": -penalty,
            "reason": (
                f"{images_without_alt} imagens sem atributo alt."
            )
        })
    
    # Internal links check
    if len(links) < 3:
        score -= 5
        breakdown.append({
            "criterion": "few_internal_links",
            "impact": -5,
            "reason": "Poucos links internos detectados."
        })
    
    # Main text length check
    if len(main_text) < 300:
        score -= 10
        breakdown.append({
            "criterion": "short_content",
            "impact": -10,
            "reason": (
                f"Conteúdo textual muito curto ({len(main_text)} "
                "caracteres)."
            )
        })
    
    return max(0, min(100, score)), breakdown


def normalize_module_identifier(value: str) -> str:
    """
    Normalize module identifier for robust matching.
    Converts to lowercase and removes extra spaces.
    """
    return str(value).strip().lower()


def modules_match(
    detected_name: str,
    pattern_name: str
) -> bool:
    """
    Check if detected module matches pattern module name.
    Handles variations like "Main Banner" vs "Banner principal".
    """
    norm_detected = normalize_module_identifier(detected_name)
    norm_pattern = normalize_module_identifier(pattern_name)
    
    # Exact match
    if norm_detected == norm_pattern:
        return True
    
    # Partial match for common variations
    if "banner" in norm_detected and "banner" in norm_pattern:
        return True
    if "accordion" in norm_detected and "accordion" in norm_pattern:
        return True
    if "card" in norm_detected and "card" in norm_pattern:
        return True
    if "media" in norm_detected and "media" in norm_pattern:
        return True
    if "breadcrumb" in norm_detected and "breadcrumb" in norm_pattern:
        return True
    
    return False


def calculate_storytelling_score(
    pattern: Optional[Dict[str, Any]],
    detected_modules: List[Dict[str, Any]],
    narrative_insights: List[Dict[str, Any]],
    storytelling_analysis: Dict[str, Any],
) -> tuple[int, List[Dict[str, Any]]]:
    """
    Calculate storytelling score based on pattern adherence.
    
    Model: Weighted sum of adherence criteria (0-100)
    - Required modules coverage: 30 points
    - Narrative steps coverage: 25 points
    - Narrative order alignment: 20 points
    - Objections and security: 15 points
    - Insights quality: 10 points
    """
    breakdown = []
    
    if not pattern:
        breakdown.append({
            "criterion": "no_pattern_detected",
            "impact": 0,
            "reason": "Nenhum storytelling pattern detectado."
        })
        return 50, breakdown
    
    detected_module_names = [
        str(m.get("matched_catalog_name", "")).strip()
        for m in detected_modules
        if isinstance(m, dict) and m.get("matched_catalog_name")
    ]
    
    # 1. Required modules coverage (30 points)
    required_modules = pattern.get("required_modules", [])
    if required_modules:
        matched_required = sum(
            1 for req in required_modules
            if any(modules_match(det, req) for det in detected_module_names)
        )
        coverage_ratio = matched_required / len(required_modules)
        required_score = round(30 * coverage_ratio)
        
        breakdown.append({
            "criterion": "required_modules_coverage",
            "impact": required_score,
            "reason": (
                f"Cobertura de módulos obrigatórios: {matched_required}/"
                f"{len(required_modules)} ({int(coverage_ratio*100)}%)."
            )
        })
    else:
        required_score = 30
        breakdown.append({
            "criterion": "required_modules_coverage",
            "impact": 30,
            "reason": "Pattern não define módulos obrigatórios."
        })
    
    # 2. Narrative steps coverage (25 points)
    narrative_steps = pattern.get("narrative_steps", [])
    if narrative_steps:
        covered_steps = 0
        for step in narrative_steps:
            if not isinstance(step, dict):
                continue
            step_modules = step.get("recommended_modules", [])
            has_step_module = any(
                any(
                    modules_match(det, step_mod)
                    for det in detected_module_names
                )
                for step_mod in step_modules
            )
            if has_step_module:
                covered_steps += 1
        
        steps_ratio = covered_steps / len(narrative_steps)
        narrative_score = round(25 * steps_ratio)
        
        breakdown.append({
            "criterion": "narrative_steps_coverage",
            "impact": narrative_score,
            "reason": (
                f"Etapas narrativas cobertas: {covered_steps}/"
                f"{len(narrative_steps)} ({int(steps_ratio*100)}%)."
            )
        })
    else:
        narrative_score = 25
        breakdown.append({
            "criterion": "narrative_steps_coverage",
            "impact": 25,
            "reason": "Pattern não define etapas narrativas."
        })
    
    # 3. Narrative order alignment (20 points)
    recommended_order = pattern.get("recommended_module_order", [])
    if recommended_order and detected_module_names:
        # Check how many detected modules are in recommended order
        in_order_count = sum(
            1 for det in detected_module_names
            if any(modules_match(det, rec) for rec in recommended_order)
        )
        
        if in_order_count > 0:
            order_ratio = in_order_count / len(detected_module_names)
            order_score = round(20 * order_ratio)
        else:
            order_score = 10  # Give some points for having modules
        
        breakdown.append({
            "criterion": "narrative_order_alignment",
            "impact": order_score,
            "reason": (
                f"Alinhamento com ordem recomendada: {in_order_count}/"
                f"{len(detected_module_names)} módulos presentes no pattern."
            )
        })
    else:
        order_score = 20
        breakdown.append({
            "criterion": "narrative_order_alignment",
            "impact": 20,
            "reason": "Ordem narrativa não aplicável."
        })
    
    # 4. Objections and security (15 points)
    objection_score = 15
    objection_modules = ["Accordion", "Contract and tariffs", "FAQ"]
    
    has_objection_handling = any(
        any(modules_match(det, obj) for det in detected_module_names)
        for obj in objection_modules
    )
    
    requires_objection = any(
        any(modules_match(req, obj) for obj in objection_modules)
        for req in required_modules
    )
    
    if requires_objection:
        if has_objection_handling:
            objection_score = 15
            breakdown.append({
                "criterion": "objection_handling",
                "impact": 15,
                "reason": (
                    "Módulos de objeção/segurança presentes "
                    "conforme pattern."
                )
            })
        else:
            objection_score = 5
            breakdown.append({
                "criterion": "objection_handling",
                "impact": 5,
                "reason": (
                    "Módulos de objeção/segurança ausentes "
                    "(requeridos pelo pattern)."
                )
            })
    else:
        breakdown.append({
            "criterion": "objection_handling",
            "impact": 15,
            "reason": "Tratamento de objeções não requerido pelo pattern."
        })
    
    # 5. Insights quality (10 points)
    insights_score = 10
    
    high_insights = [
        i for i in narrative_insights if i.get("severity") == "high"
    ]
    medium_insights = [
        i for i in narrative_insights if i.get("severity") == "medium"
    ]
    low_insights = [
        i for i in narrative_insights if i.get("severity") == "low"
    ]
    
    insights_penalty = (
        len(high_insights) * 5 +
        len(medium_insights) * 2 +
        len(low_insights) * 1
    )
    insights_score = max(0, 10 - insights_penalty)
    
    if insights_penalty > 0:
        breakdown.append({
            "criterion": "insights_quality",
            "impact": insights_score,
            "reason": (
                f"Qualidade dos insights: {len(high_insights)} high, "
                f"{len(medium_insights)} medium, {len(low_insights)} low."
            )
        })
    else:
        breakdown.append({
            "criterion": "insights_quality",
            "impact": 10,
            "reason": "Nenhum insight narrativo crítico detectado."
        })
    
    # Total score
    total_score = (
        required_score +
        narrative_score +
        order_score +
        objection_score +
        insights_score
    )
    
    return max(0, min(100, total_score)), breakdown


def calculate_modules_score(
    detected_modules: List[Dict[str, Any]],
    module_plan: Dict[str, List[Any]],
    pattern: Optional[Dict[str, Any]],
) -> tuple[int, List[Dict[str, Any]]]:
    """
    Calculate modules score based on detection quality and coverage.
    """
    score = 100
    breakdown = []
    
    # No modules detected
    if not detected_modules or len(detected_modules) == 0:
        score = 30
        breakdown.append({
            "criterion": "no_modules_detected",
            "impact": -70,
            "reason": "Nenhum módulo detectado na página."
        })
        return max(0, min(100, score)), breakdown
    
    # Calculate average confidence
    confidences = [
        m.get("confidence", 0)
        for m in detected_modules
        if isinstance(m, dict)
    ]
    avg_confidence = (
        sum(confidences) / len(confidences) if confidences else 0
    )
    
    if avg_confidence < 0.5:
        score -= 20
        breakdown.append({
            "criterion": "low_confidence",
            "impact": -20,
            "reason": (
                f"Confiança média baixa na detecção ({avg_confidence:.2f})."
            )
        })
    
    # Check modules to add (missing required)
    modules_to_add = module_plan.get("add", [])
    if len(modules_to_add) > 0:
        penalty = min(30, len(modules_to_add) * 10)
        score -= penalty
        breakdown.append({
            "criterion": "missing_required_modules",
            "impact": -penalty,
            "reason": (
                f"{len(modules_to_add)} módulos obrigatórios ausentes."
            )
        })
    
    # Check modules to remove
    modules_to_remove = module_plan.get("remove", [])
    if len(modules_to_remove) > 0:
        penalty = min(24, len(modules_to_remove) * 8)
        score -= penalty
        breakdown.append({
            "criterion": "modules_to_remove",
            "impact": -penalty,
            "reason": (
                f"{len(modules_to_remove)} módulos inadequados detectados."
            )
        })
    
    # Check modules to reorder
    modules_to_reorder = module_plan.get("reorder", [])
    if len(modules_to_reorder) > 2:
        penalty = min(15, (len(modules_to_reorder) - 2) * 5)
        score -= penalty
        breakdown.append({
            "criterion": "poor_module_order",
            "impact": -penalty,
            "reason": (
                f"{len(modules_to_reorder)} módulos fora da ordem "
                "recomendada."
            )
        })
    
    # Bonus for good coverage
    if pattern:
        required_modules = pattern.get("required_modules", [])
        detected_names = {
            str(m.get("matched_catalog_name", "")).strip()
            for m in detected_modules
        }
        coverage = sum(
            1 for req in required_modules if req in detected_names
        )
        if required_modules and coverage == len(required_modules):
            score = min(100, score + 10)
            breakdown.append({
                "criterion": "full_coverage",
                "impact": 10,
                "reason": "Todos os módulos obrigatórios presentes."
            })
    
    return max(0, min(100, score)), breakdown


def calculate_brand_safety_score(
    normalized_page: Dict[str, Any],
    brand_rules: List[Dict[str, Any]],
    narrative_insights: List[Dict[str, Any]],
    pattern: Optional[Dict[str, Any]],
) -> tuple[int, List[Dict[str, Any]]]:
    """
    Calculate brand safety score based on compliance rules.
    """
    score = 100
    breakdown = []
    
    main_text = normalized_page.get("main_text", "").lower()
    
    # Check for prohibited terms from brand rules
    for rule in brand_rules:
        if not isinstance(rule, dict):
            continue
        bad_examples = rule.get("bad_examples", [])
        for bad_term in bad_examples:
            if str(bad_term).lower() in main_text:
                score -= 20
                breakdown.append({
                    "criterion": "prohibited_term",
                    "impact": -20,
                    "reason": (
                        f"Termo proibido detectado: '{bad_term}' "
                        f"({rule.get('rule', 'regra de marca')})."
                    )
                })
    
    # Check for financial promises
    dangerous_terms = [
        "garantido", "sem risco", "aprovação garantida",
        "lucro garantido", "renda garantida", "100% seguro"
    ]
    for term in dangerous_terms:
        if term in main_text:
            score -= 25
            breakdown.append({
                "criterion": "financial_promise",
                "impact": -25,
                "reason": f"Promessa financeira absoluta: '{term}'."
            })
    
    # Check for artificial urgency
    urgency_terms = [
        "última chance", "só hoje", "corre", "rápido",
        "não perca", "oferta expira"
    ]
    urgency_count = sum(1 for term in urgency_terms if term in main_text)
    if urgency_count > 2:
        score -= 15
        breakdown.append({
            "criterion": "artificial_urgency",
            "impact": -15,
            "reason": "Urgência artificial excessiva detectada."
        })
    
    # Check compliance insights
    compliance_insights = [
        i for i in narrative_insights
        if i.get("type") == "compliance_risk"
    ]
    for insight in compliance_insights:
        severity = insight.get("severity", "medium")
        if severity == "high":
            score -= 15
            breakdown.append({
                "criterion": "compliance_risk_high",
                "impact": -15,
                "reason": insight.get("title", "Risco de compliance alto.")
            })
        elif severity == "medium":
            score -= 8
            breakdown.append({
                "criterion": "compliance_risk_medium",
                "impact": -8,
                "reason": (
                    insight.get("title", "Risco de compliance médio.")
                )
            })
    
    # Check avoid_copy from pattern
    if pattern:
        avoid_copy = pattern.get("avoid_copy", [])
        for avoid_term in avoid_copy:
            if str(avoid_term).lower() in main_text:
                score -= 10
                breakdown.append({
                    "criterion": "pattern_avoid_copy",
                    "impact": -10,
                    "reason": (
                        f"Termo a evitar no pattern: '{avoid_term}'."
                    )
                })
    
    return max(0, min(100, score)), breakdown


def calculate_overall_score(
    seo_score: int,
    storytelling_score: int,
    modules_score: int,
    brand_safety_score: int,
) -> int:
    """
    Calculate overall score as weighted average.
    
    Weights:
    - SEO: 25%
    - Storytelling: 30%
    - Modules: 25%
    - Brand Safety: 20%
    """
    overall = (
        seo_score * 0.25 +
        storytelling_score * 0.30 +
        modules_score * 0.25 +
        brand_safety_score * 0.20
    )
    return round(overall)


# Made with Bob