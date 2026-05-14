import json
from pathlib import Path
from typing import List, Dict, Any


def _get_data_dir() -> Path:
    """
    Get the data directory path relative to this file.
    Assumes the code runs from the backend directory.
    """
    # This file is in backend/app/services/catalog_loader.py
    # Data files are in backend/app/data/
    current_file = Path(__file__)
    data_dir = current_file.parent.parent / "data"
    return data_dir


def load_modules_catalog() -> List[Dict[str, Any]]:
    """
    Load the modules catalog from JSON file.
    
    Returns:
        List of module definitions with name, best_for, purpose, etc.
    """
    data_dir = _get_data_dir()
    catalog_path = data_dir / "modules_catalog.json"
    
    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_storytelling_patterns() -> List[Dict[str, Any]]:
    """
    Load storytelling patterns from JSON file.
    
    Returns:
        List of storytelling patterns with page_type, pattern, description.
    """
    data_dir = _get_data_dir()
    patterns_path = data_dir / "storytelling_patterns.json"
    
    with open(patterns_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_brand_rules() -> List[Dict[str, Any]]:
    """
    Load brand and compliance rules from JSON file.
    
    Returns:
        List of brand rules with rule, bad_examples, suggestion.
    """
    data_dir = _get_data_dir()
    rules_path = data_dir / "brand_rules.json"
    
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_catalogs() -> Dict[str, Any]:
    """
    Load all catalogs at once.
    
    Returns:
        Dictionary with keys: modules_catalog, storytelling_patterns,
        brand_rules
    """
    return {
        "modules_catalog": load_modules_catalog(),
        "storytelling_patterns": load_storytelling_patterns(),
        "brand_rules": load_brand_rules()
    }

# Made with Bob
