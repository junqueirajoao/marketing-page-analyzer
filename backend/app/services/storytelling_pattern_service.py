from typing import Any, Dict, List, Optional


DEFAULT_STORYTELLING_ANALYSIS = {
    "detected_pattern_id": "",
    "detected_pattern_name": "",
    "recommended_storyline": [],
    "recommended_module_order": [],
    "narrative_steps": [],
    "tone_guidelines": [],
    "cta_examples": [],
    "compliance_guidelines": [],
    "avoid_copy": []
}


def get_storytelling_patterns(
    catalogs: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Return storytelling patterns from loaded catalogs."""
    patterns = catalogs.get("storytelling_patterns", [])
    if isinstance(patterns, list):
        return [pattern for pattern in patterns if isinstance(pattern, dict)]
    return []


def find_best_storytelling_pattern(
    patterns: List[Dict[str, Any]],
    page_type: Optional[str] = None,
    business_goal: Optional[str] = None,
    target_audience: Optional[str] = None,
    text_context: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Find the best storytelling pattern using simple fallback heuristics.
    Priority:
    1. exact page_type
    2. exact business_goal
    3. target_audience match
    4. text_context keyword match
    5. institutional/default fallback
    """
    safe_patterns = [
        pattern for pattern in patterns
        if isinstance(pattern, dict)
    ]
    if not safe_patterns:
        return None

    normalized_page_type = _normalize_value(page_type)
    normalized_goal = _normalize_value(business_goal)
    normalized_audience = _normalize_value(target_audience)
    normalized_context = _normalize_value(text_context)

    if normalized_page_type:
        for pattern in safe_patterns:
            if (
                _normalize_value(pattern.get("page_type"))
                == normalized_page_type
            ):
                return pattern

    if normalized_goal:
        for pattern in safe_patterns:
            if (
                _normalize_value(pattern.get("business_goal"))
                == normalized_goal
            ):
                return pattern

    if normalized_audience:
        for pattern in safe_patterns:
            if (
                _normalize_value(pattern.get("target_audience"))
                == normalized_audience
            ):
                return pattern

    if normalized_context:
        best_pattern = _find_pattern_by_keywords(
            safe_patterns,
            normalized_context
        )
        if best_pattern:
            return best_pattern

    for pattern in safe_patterns:
        page_type_value = _normalize_value(pattern.get("page_type"))
        if page_type_value in {"institucional", "institutional"}:
            return pattern

    return safe_patterns[0]


def build_storytelling_analysis(
    pattern: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Build a safe storytelling_analysis payload from a pattern."""
    if not pattern:
        return dict(DEFAULT_STORYTELLING_ANALYSIS)

    return {
        "detected_pattern_id": str(pattern.get("id") or ""),
        "detected_pattern_name": str(pattern.get("storytelling_name") or ""),
        "recommended_storyline": _build_recommended_storyline(pattern),
        "recommended_module_order": list(
            pattern.get("recommended_module_order") or []
        ),
        "narrative_steps": list(pattern.get("narrative_steps") or []),
        "tone_guidelines": list(pattern.get("tone_guidelines") or []),
        "cta_examples": list(pattern.get("cta_examples") or []),
        "compliance_guidelines": list(
            pattern.get("compliance_guidelines") or []
        ),
        "avoid_copy": list(pattern.get("avoid_copy") or [])
    }


def _build_recommended_storyline(pattern: Dict[str, Any]) -> List[str]:
    """Build a simple storyline list from narrative steps."""
    narrative_steps = pattern.get("narrative_steps") or []
    if not isinstance(narrative_steps, list):
        return []

    storyline: List[str] = []
    for step in narrative_steps:
        if not isinstance(step, dict):
            continue
        step_name = str(step.get("name") or "").strip()
        if step_name:
            storyline.append(step_name)

    if storyline:
        return storyline

    return list(pattern.get("recommended_module_order") or [])


def _find_pattern_by_keywords(
    patterns: List[Dict[str, Any]],
    text_context: str
) -> Optional[Dict[str, Any]]:
    """Find a pattern with the best keyword overlap against context."""
    context_words = {
        token for token in text_context.split()
        if len(token) >= 4
    }
    if not context_words:
        return None

    best_pattern: Optional[Dict[str, Any]] = None
    best_score = 0

    for pattern in patterns:
        keywords = _collect_pattern_keywords(pattern)
        score = len(context_words.intersection(keywords))
        if score > best_score:
            best_score = score
            best_pattern = pattern

    return best_pattern if best_score > 0 else None


def _collect_pattern_keywords(pattern: Dict[str, Any]) -> set[str]:
    """Collect searchable keywords from a pattern."""
    values: List[str] = []

    for field_name in [
        "page_type",
        "segment",
        "business_goal",
        "target_audience",
        "storytelling_name",
        "description"
    ]:
        field_value = pattern.get(field_name)
        if isinstance(field_value, str):
            values.append(field_value.lower())

    for field_name in [
        "emotional_journey",
        "recommended_module_order",
        "required_modules",
        "optional_modules",
        "tone_guidelines",
        "cta_examples"
    ]:
        field_value = pattern.get(field_name) or []
        if isinstance(field_value, list):
            values.extend(
                item.lower()
                for item in field_value
                if isinstance(item, str)
            )

    for step in pattern.get("narrative_steps") or []:
        if isinstance(step, dict):
            values.extend(
                str(step.get(field_name) or "").lower()
                for field_name in ["name", "objective", "copy_direction"]
            )

    tokens = set()
    for value in values:
        tokens.update(
            token for token in value.replace("→", " ").split()
            if len(token) >= 4
        )
    return tokens


def _normalize_value(value: Optional[str]) -> str:
    """Normalize optional values for comparisons."""
    if value is None:
        return ""
    return str(value).strip().lower()

# Made with Bob
