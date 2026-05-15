"""
Tests for Catalog Context Builder
"""
import pytest
from app.services.catalog_context_builder import build_catalog_context


@pytest.fixture
def sample_catalogs():
    """Sample catalogs for testing."""
    return {
        "modules_catalog": [
            {
                "id": "main_banner",
                "name": "Main Banner",
                "display_name": "Main Banner",
                "generic_type": "hero",
                "description": "Hero banner module",
                "purpose": "Capture attention",
                "good_for": ["landing pages"],
                "bad_for": ["dense content"],
                "recommendation_rules": {
                    "keepWhen": ["high impact needed"],
                    "removeWhen": ["too many CTAs"],
                    "improveWhen": ["unclear message"]
                }
            },
            {
                "id": "accordion",
                "name": "Accordion",
                "display_name": "Accordion",
                "generic_type": "faq",
                "description": "FAQ accordion",
                "purpose": "Answer questions",
                "good_for": ["FAQs"],
                "bad_for": ["critical info"],
                "recommendation_rules": {
                    "keepWhen": ["many questions"],
                    "removeWhen": ["single item"],
                    "improveWhen": ["unclear questions"]
                }
            },
            {
                "id": "card_with_icon",
                "name": "Card with Icon",
                "display_name": "Card with Icon",
                "generic_type": "card",
                "description": "Icon card module",
                "purpose": "Show benefits",
                "good_for": ["benefits"],
                "bad_for": ["long text"],
                "recommendation_rules": {
                    "keepWhen": ["visual appeal needed"],
                    "removeWhen": ["too many cards"],
                    "improveWhen": ["icons unclear"]
                }
            }
        ],
        "storytelling_patterns": [
            {
                "id": "pattern_credito_pessoal",
                "page_type": "credito_pessoal",
                "storytelling_name": "Crédito Pessoal Pattern",
                "description": "Pattern for personal credit pages",
                "business_goal": "conversao",
                "target_audience": "pessoa_fisica",
                "narrative_steps": [
                    {
                        "step": 1,
                        "name": "Proposta",
                        "objective": "Present offer",
                        "recommended_modules": ["main_banner"],
                        "copy_direction": "Clear value"
                    }
                ],
                "required_modules": ["main_banner", "accordion"],
                "recommended_module_order": ["main_banner", "accordion"],
                "tone_guidelines": ["clear", "trustworthy"],
                "agent_evaluation_rules": {
                    "strong_pattern_when": ["has required modules"],
                    "weak_pattern_when": ["missing FAQ"]
                }
            },
            {
                "id": "pattern_investimentos",
                "page_type": "investimentos",
                "storytelling_name": "Investimentos Pattern",
                "description": "Pattern for investment pages",
                "business_goal": "educacao",
                "target_audience": "pessoa_fisica",
                "narrative_steps": [],
                "required_modules": ["card_with_icon"],
                "recommended_module_order": ["card_with_icon"],
                "tone_guidelines": ["educational"],
                "agent_evaluation_rules": {
                    "strong_pattern_when": [],
                    "weak_pattern_when": []
                }
            }
        ],
        "seo_rules": [
            {
                "id": "seo_rule_001",
                "category": "metadata",
                "severity": "high",
                "rule_name": "Title claro",
                "description": "Title must be clear",
                "applies_to": ["all"],
                "recommended_action": "Rewrite title",
                "score_impact": {"missing": -20},
                "agent_guidance": {
                    "agent": "SEO Agent",
                    "recommendation_priority": "high"
                }
            },
            {
                "id": "seo_rule_002",
                "category": "metadata",
                "severity": "high",
                "rule_name": "Meta description",
                "description": "Meta description required",
                "applies_to": ["all"],
                "recommended_action": "Add meta description",
                "score_impact": {"missing": -15},
                "agent_guidance": {
                    "agent": "SEO Agent",
                    "recommendation_priority": "high"
                }
            },
            {
                "id": "seo_rule_003",
                "category": "headings",
                "severity": "medium",
                "rule_name": "H1 único",
                "description": "Single H1 required",
                "applies_to": ["credito_pessoal"],
                "recommended_action": "Ensure single H1",
                "score_impact": {"multiple": -8},
                "agent_guidance": {
                    "agent": "SEO Agent",
                    "recommendation_priority": "medium"
                }
            }
        ],
        "brand_rules": [
            {
                "id": "brand_rule_001",
                "category": "compliance",
                "severity": "high",
                "rule_name": "Evitar promessas absolutas",
                "description": "Avoid absolute promises",
                "applies_to": ["credito_pessoal"],
                "recommended_action": "Use conditional language",
                "safe_alternatives": ["Sujeito à análise"],
                "detection_keywords": ["garantido", "aprovado"],
                "agent_guidance": {
                    "agent": "Brand Agent",
                    "rewrite_required": True,
                    "risk_score_impact": 25
                }
            },
            {
                "id": "brand_rule_002",
                "category": "tone_of_voice",
                "severity": "medium",
                "rule_name": "Linguagem clara",
                "description": "Use clear language",
                "applies_to": ["all"],
                "recommended_action": "Simplify jargon",
                "safe_alternatives": ["Termos simples"],
                "detection_keywords": ["jargão"],
                "agent_guidance": {
                    "agent": "Brand Agent",
                    "rewrite_required": True,
                    "risk_score_impact": 8
                }
            }
        ]
    }


def test_build_catalog_context_basic(sample_catalogs):
    """Test basic catalog context building."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        page_type="credito_pessoal",
        business_goal="conversao",
        target_audience="pessoa_fisica"
    )
    
    assert "relevant_modules" in result
    assert "relevant_storytelling_patterns" in result
    assert "relevant_seo_rules" in result
    assert "relevant_brand_rules" in result
    
    assert isinstance(result["relevant_modules"], list)
    assert isinstance(result["relevant_storytelling_patterns"], list)
    assert isinstance(result["relevant_seo_rules"], list)
    assert isinstance(result["relevant_brand_rules"], list)


def test_storytelling_pattern_matching(sample_catalogs):
    """Test storytelling pattern selection by page type."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        page_type="credito_pessoal",
        business_goal="conversao",
        target_audience="pessoa_fisica"
    )
    
    patterns = result["relevant_storytelling_patterns"]
    assert len(patterns) > 0
    
    # Should prioritize exact match
    first_pattern = patterns[0]
    assert first_pattern["page_type"] == "credito_pessoal"
    assert first_pattern["business_goal"] == "conversao"


def test_seo_rules_high_severity_priority(sample_catalogs):
    """Test that high severity SEO rules are prioritized."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        page_type="credito_pessoal"
    )
    
    seo_rules = result["relevant_seo_rules"]
    assert len(seo_rules) > 0
    
    # High severity rules should be included
    high_severity_count = sum(
        1 for rule in seo_rules if rule["severity"] == "high"
    )
    assert high_severity_count > 0


def test_seo_rules_mentioned_in_score_breakdown(sample_catalogs):
    """Test that SEO rules mentioned in score breakdown are prioritized."""
    score_breakdown = {
        "metadata": {
            "score": 50,
            "issues": [
                {
                    "rule_id": "seo_rule_001",
                    "message": "Title missing"
                }
            ]
        }
    }
    
    result = build_catalog_context(
        catalogs=sample_catalogs,
        score_breakdown=score_breakdown
    )
    
    seo_rules = result["relevant_seo_rules"]
    rule_ids = [rule["id"] for rule in seo_rules]
    
    # Mentioned rule should be included
    assert "seo_rule_001" in rule_ids


def test_brand_rules_page_type_filtering(sample_catalogs):
    """Test brand rules filtering by page type."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        page_type="credito_pessoal"
    )
    
    brand_rules = result["relevant_brand_rules"]
    assert len(brand_rules) > 0
    
    # Should include rules that apply to credito_pessoal
    applicable_rules = [
        rule for rule in brand_rules
        if "credito_pessoal" in rule.get("applies_to", []) or
        "all" in rule.get("applies_to", [])
    ]
    assert len(applicable_rules) > 0


def test_modules_from_detected_modules(sample_catalogs):
    """Test that detected modules are included in context."""
    detected_modules = [
        {"id": "main_banner", "confidence": 0.95},
        {"id": "accordion", "confidence": 0.85}
    ]
    
    result = build_catalog_context(
        catalogs=sample_catalogs,
        detected_modules=detected_modules
    )
    
    modules = result["relevant_modules"]
    module_ids = [mod["id"] for mod in modules]
    
    assert "main_banner" in module_ids
    assert "accordion" in module_ids


def test_modules_from_storytelling_pattern(sample_catalogs):
    """Test that required modules from pattern are included."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        page_type="credito_pessoal"
    )
    
    modules = result["relevant_modules"]
    module_ids = [mod["id"] for mod in modules]
    
    # Required modules from pattern should be included
    assert "main_banner" in module_ids
    assert "accordion" in module_ids


def test_compact_module_structure(sample_catalogs):
    """Test that modules are compacted to essential fields."""
    detected_modules = [{"id": "main_banner", "confidence": 0.95}]
    
    result = build_catalog_context(
        catalogs=sample_catalogs,
        detected_modules=detected_modules
    )
    
    modules = result["relevant_modules"]
    assert len(modules) > 0
    
    module = modules[0]
    # Essential fields should be present
    assert "id" in module
    assert "name" in module
    assert "display_name" in module
    assert "description" in module
    assert "purpose" in module
    assert "good_for" in module
    assert "recommendation_rules" in module
    
    # Non-essential fields should not be present
    assert "synonyms" not in module
    assert "detection_hints" not in module


def test_compact_seo_rule_structure(sample_catalogs):
    """Test that SEO rules are compacted to essential fields."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        page_type="credito_pessoal"
    )
    
    seo_rules = result["relevant_seo_rules"]
    assert len(seo_rules) > 0
    
    rule = seo_rules[0]
    # Essential fields should be present
    assert "id" in rule
    assert "category" in rule
    assert "severity" in rule
    assert "rule_name" in rule
    assert "description" in rule
    assert "recommended_action" in rule
    
    # Non-essential fields should not be present
    assert "bad_examples" not in rule
    assert "good_examples" not in rule


def test_max_items_per_catalog(sample_catalogs):
    """Test that max_items_per_catalog limit is respected."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        max_items_per_catalog=2
    )
    
    assert len(result["relevant_modules"]) <= 2
    assert len(result["relevant_storytelling_patterns"]) <= 2
    assert len(result["relevant_seo_rules"]) <= 2
    assert len(result["relevant_brand_rules"]) <= 2


def test_fallback_when_no_matches(sample_catalogs):
    """Test fallback behavior when no matches found."""
    result = build_catalog_context(
        catalogs=sample_catalogs,
        page_type="nonexistent_page_type"
    )
    
    # Should still return some rules as fallback
    assert len(result["relevant_seo_rules"]) > 0
    assert len(result["relevant_brand_rules"]) > 0
    
    # Should prioritize high severity rules in fallback
    seo_rules = result["relevant_seo_rules"]
    high_severity = [r for r in seo_rules if r["severity"] == "high"]
    assert len(high_severity) > 0


def test_empty_catalogs():
    """Test behavior with empty catalogs."""
    empty_catalogs = {
        "modules_catalog": [],
        "storytelling_patterns": [],
        "seo_rules": [],
        "brand_rules": []
    }
    
    result = build_catalog_context(
        catalogs=empty_catalogs,
        page_type="credito_pessoal"
    )
    
    assert result["relevant_modules"] == []
    assert result["relevant_storytelling_patterns"] == []
    assert result["relevant_seo_rules"] == []
    assert result["relevant_brand_rules"] == []


def test_none_parameters():
    """Test behavior with None parameters."""
    catalogs = {
        "modules_catalog": [],
        "storytelling_patterns": [],
        "seo_rules": [],
        "brand_rules": []
    }
    
    result = build_catalog_context(
        catalogs=catalogs,
        page_type=None,
        business_goal=None,
        target_audience=None,
        detected_modules=None,
        score_breakdown=None,
        narrative_insights=None
    )
    
    # Should not raise errors
    assert isinstance(result, dict)
    assert "relevant_modules" in result


# Made with Bob