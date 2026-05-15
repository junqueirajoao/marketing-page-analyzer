import json
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_STORYTELLING_FIELDS = [
    "id",
    "page_type",
    "storytelling_name",
    "description",
    "narrative_steps",
    "recommended_module_order"
]


def _get_data_dir() -> Path:
    """
    Get the data directory path relative to this file.
    Assumes the code runs from the backend directory.
    """
    current_file = Path(__file__)
    return current_file.parent.parent / "data"


def _load_json_file(file_path: Path, catalog_name: str) -> Any:
    """Load and parse a JSON file with clear error messages."""
    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Catalog file not found for {catalog_name}: {file_path}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Invalid JSON in {catalog_name} catalog: {file_path} "
            f"(line {exc.lineno}, column {exc.colno})"
        ) from exc


def _ensure_list(data: Any, catalog_name: str) -> List[Dict[str, Any]]:
    """Ensure catalog content is a list of dictionaries."""
    if not isinstance(data, list):
        raise RuntimeError(
            f"{catalog_name} catalog must be a JSON array of objects."
        )

    valid_items: List[Dict[str, Any]] = []
    for item in data:
        if isinstance(item, dict):
            valid_items.append(item)

    return valid_items


def normalize_storytelling_pattern(pattern: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize storytelling patterns to the richer structure.

    Supports both the new rich format and the legacy format:
    {
        "page_type": "...",
        "pattern": [...],
        "description": "..."
    }
    """
    page_type = str(pattern.get("page_type") or "institucional").strip()
    description = str(pattern.get("description") or "").strip()

    if "storytelling_name" in pattern or "id" in pattern:
        normalized = {
            "id": str(pattern.get("id") or f"pattern_{page_type}"),
            "page_type": page_type,
            "segment": str(pattern.get("segment") or ""),
            "business_goal": str(pattern.get("business_goal") or ""),
            "target_audience": str(pattern.get("target_audience") or ""),
            "storytelling_name": str(
                pattern.get("storytelling_name") or page_type
            ),
            "description": description,
            "emotional_journey": list(pattern.get("emotional_journey") or []),
            "narrative_steps": list(pattern.get("narrative_steps") or []),
            "recommended_module_order": list(
                pattern.get("recommended_module_order") or []
            ),
            "required_modules": list(pattern.get("required_modules") or []),
            "optional_modules": list(pattern.get("optional_modules") or []),
            "avoid_modules_when": list(
                pattern.get("avoid_modules_when") or []
            ),
            "headline_examples": list(pattern.get("headline_examples") or []),
            "cta_examples": list(pattern.get("cta_examples") or []),
            "tone_guidelines": list(pattern.get("tone_guidelines") or []),
            "compliance_guidelines": list(
                pattern.get("compliance_guidelines") or []
            ),
            "avoid_copy": list(pattern.get("avoid_copy") or []),
            "agent_evaluation_rules": dict(
                pattern.get("agent_evaluation_rules") or {}
            )
        }
    else:
        legacy_steps = list(pattern.get("pattern") or [])
        normalized = {
            "id": f"pattern_{page_type}",
            "page_type": page_type,
            "segment": "",
            "business_goal": "",
            "target_audience": "",
            "storytelling_name": page_type,
            "description": description,
            "emotional_journey": [],
            "narrative_steps": [
                {
                    "step": index + 1,
                    "name": str(step_name),
                    "objective": "",
                    "recommended_modules": [],
                    "copy_direction": ""
                }
                for index, step_name in enumerate(legacy_steps)
            ],
            "recommended_module_order": [
                str(step_name) for step_name in legacy_steps
            ],
            "required_modules": [],
            "optional_modules": [],
            "avoid_modules_when": [],
            "headline_examples": [],
            "cta_examples": [],
            "tone_guidelines": [],
            "compliance_guidelines": [],
            "avoid_copy": [],
            "agent_evaluation_rules": {
                "strong_pattern_when": [],
                "weak_pattern_when": []
            }
        }

    return normalized


def _is_valid_storytelling_pattern(pattern: Dict[str, Any]) -> bool:
    """Light validation for normalized storytelling patterns."""
    for field_name in REQUIRED_STORYTELLING_FIELDS:
        value = pattern.get(field_name)
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, list) and len(value) == 0:
            return False
    return True


def load_modules_catalog() -> List[Dict[str, Any]]:
    """Load the modules catalog from JSON file."""
    data_dir = _get_data_dir()
    catalog_path = data_dir / "modules_catalog.json"
    raw_data = _load_json_file(catalog_path, "modules_catalog")
    return _ensure_list(raw_data, "modules_catalog")


def load_storytelling_patterns() -> List[Dict[str, Any]]:
    """
    Load storytelling patterns from JSON file.

    Returns a normalized list supporting both legacy and rich structures.
    Optional fields are filled with safe defaults.
    """
    data_dir = _get_data_dir()
    patterns_path = data_dir / "storytelling_patterns.json"
    raw_data = _load_json_file(patterns_path, "storytelling_patterns")
    raw_patterns = _ensure_list(raw_data, "storytelling_patterns")

    normalized_patterns = [
        normalize_storytelling_pattern(pattern)
        for pattern in raw_patterns
    ]
    valid_patterns = [
        pattern for pattern in normalized_patterns
        if _is_valid_storytelling_pattern(pattern)
    ]

    if not valid_patterns and normalized_patterns:
        raise RuntimeError(
            "No valid storytelling patterns found. Each pattern must include: "
            + ", ".join(REQUIRED_STORYTELLING_FIELDS)
        )

    return valid_patterns


def load_brand_rules() -> List[Dict[str, Any]]:
    """Load brand and compliance rules from JSON file."""
    data_dir = _get_data_dir()
    rules_path = data_dir / "brand_rules.json"
    raw_data = _load_json_file(rules_path, "brand_rules")
    return _ensure_list(raw_data, "brand_rules")


def load_all_catalogs() -> Dict[str, Any]:
    """Load all catalogs at once."""
    return {
        "modules_catalog": load_modules_catalog(),
        "storytelling_patterns": load_storytelling_patterns(),
        "brand_rules": load_brand_rules()
    }


# Made with Bob
