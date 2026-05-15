"""
Tests for dynamic scoring service.
"""
from app.services.scoring_service import (
    calculate_scores,
    calculate_seo_score,
    calculate_storytelling_score,
    calculate_modules_score,
    calculate_brand_safety_score,
    calculate_overall_score,
)


def test_seo_score_decreases_without_title():
    """SEO score should decrease when title is missing."""
    normalized_page_with_title = {
        "metadata": {"title": "Test Page", "meta_description": "Test"},
        "headings": [{"level": 1, "text": "H1"}],
        "images": [],
        "links": ["link1", "link2", "link3"],
        "main_text": "A" * 500,
    }
    
    normalized_page_without_title = {
        "metadata": {"title": "", "meta_description": "Test"},
        "headings": [{"level": 1, "text": "H1"}],
        "images": [],
        "links": ["link1", "link2", "link3"],
        "main_text": "A" * 500,
    }
    
    score_with, _ = calculate_seo_score(normalized_page_with_title)
    score_without, _ = calculate_seo_score(normalized_page_without_title)
    
    assert score_without < score_with
    assert score_without <= score_with - 12  # At least 12 points penalty


def test_seo_score_decreases_without_meta_description():
    """SEO score should decrease when meta description is missing."""
    normalized_page_with_meta = {
        "metadata": {"title": "Test", "meta_description": "A" * 130},
        "headings": [{"level": 1, "text": "H1"}],
        "images": [],
        "links": ["link1", "link2", "link3"],
        "main_text": "A" * 500,
    }
    
    normalized_page_without_meta = {
        "metadata": {"title": "Test", "meta_description": ""},
        "headings": [{"level": 1, "text": "H1"}],
        "images": [],
        "links": ["link1", "link2", "link3"],
        "main_text": "A" * 500,
    }
    
    score_with, _ = calculate_seo_score(normalized_page_with_meta)
    score_without, _ = calculate_seo_score(normalized_page_without_meta)
    
    assert score_without < score_with


def test_seo_score_decreases_without_h1():
    """SEO score should decrease when H1 is missing."""
    normalized_page_with_h1 = {
        "metadata": {"title": "Test", "meta_description": "Test"},
        "headings": [{"level": 1, "text": "H1"}],
        "images": [],
        "links": ["link1", "link2", "link3"],
        "main_text": "A" * 500,
    }
    
    normalized_page_without_h1 = {
        "metadata": {"title": "Test", "meta_description": "Test"},
        "headings": [{"level": 2, "text": "H2"}],
        "images": [],
        "links": ["link1", "link2", "link3"],
        "main_text": "A" * 500,
    }
    
    score_with, _ = calculate_seo_score(normalized_page_with_h1)
    score_without, _ = calculate_seo_score(normalized_page_without_h1)
    
    assert score_without < score_with
    assert score_without <= score_with - 12


def test_storytelling_score_decreases_without_required_modules():
    """Storytelling score should decrease when required modules are missing."""
    pattern = {
        "required_modules": ["Main Banner", "Media with steps"],
        "narrative_steps": [],
        "cta_examples": ["Test CTA"],
    }
    
    detected_modules_complete = [
        {"matched_catalog_name": "Main Banner"},
        {"matched_catalog_name": "Media with steps"},
    ]
    
    detected_modules_incomplete = [
        {"matched_catalog_name": "Main Banner"},
    ]
    
    score_complete, _ = calculate_storytelling_score(
        pattern=pattern,
        detected_modules=detected_modules_complete,
        narrative_insights=[],
        storytelling_analysis={},
    )
    
    score_incomplete, _ = calculate_storytelling_score(
        pattern=pattern,
        detected_modules=detected_modules_incomplete,
        narrative_insights=[],
        storytelling_analysis={},
    )
    
    assert score_incomplete < score_complete
    # Complete should score high (90+) with all required modules
    assert score_complete >= 85


def test_storytelling_score_perfect_adherence():
    """Perfect adherence should score 90-100."""
    pattern = {
        "required_modules": ["Main Banner", "Accordion"],
        "narrative_steps": [
            {
                "name": "Apresentação",
                "recommended_modules": ["Main Banner"]
            },
            {
                "name": "Objeções",
                "recommended_modules": ["Accordion"]
            }
        ],
        "recommended_module_order": ["Main Banner", "Accordion"],
    }
    
    detected_modules = [
        {"matched_catalog_name": "Main Banner"},
        {"matched_catalog_name": "Accordion"},
    ]
    
    score, breakdown = calculate_storytelling_score(
        pattern=pattern,
        detected_modules=detected_modules,
        narrative_insights=[],
        storytelling_analysis={},
    )
    
    assert score >= 90, f"Expected score >= 90, got {score}"
    assert len(breakdown) > 0
    # Should have positive impacts
    assert any(item["impact"] > 0 for item in breakdown)


def test_storytelling_score_partial_adherence():
    """Partial adherence should score 55-85."""
    pattern = {
        "required_modules": [
            "Main Banner",
            "Accordion",
            "Media with steps"
        ],
        "narrative_steps": [
            {
                "name": "Apresentação",
                "recommended_modules": ["Main Banner"]
            },
            {
                "name": "Explicação",
                "recommended_modules": ["Media with steps"]
            }
        ],
    }
    
    # Only 2 of 3 required modules
    detected_modules = [
        {"matched_catalog_name": "Main Banner"},
        {"matched_catalog_name": "Accordion"},
    ]
    
    score, _ = calculate_storytelling_score(
        pattern=pattern,
        detected_modules=detected_modules,
        narrative_insights=[],
        storytelling_analysis={},
    )
    
    assert 55 <= score <= 85, f"Expected 55-85, got {score}"


def test_storytelling_score_poor_adherence():
    """Poor adherence should score below 50."""
    pattern = {
        "required_modules": [
            "Main Banner",
            "Accordion",
            "Media with steps",
            "Contract and tariffs"
        ],
        "narrative_steps": [
            {
                "name": "Apresentação",
                "recommended_modules": ["Main Banner"]
            },
            {
                "name": "Explicação",
                "recommended_modules": ["Media with steps"]
            },
            {
                "name": "Objeções",
                "recommended_modules": ["Accordion"]
            }
        ],
    }
    
    # Only 1 of 4 required modules
    detected_modules = [
        {"matched_catalog_name": "Main Banner"},
    ]
    
    # Add high severity insights
    narrative_insights = [
        {"severity": "high", "type": "missing_step"},
        {"severity": "high", "type": "compliance_risk"},
    ]
    
    score, _ = calculate_storytelling_score(
        pattern=pattern,
        detected_modules=detected_modules,
        narrative_insights=narrative_insights,
        storytelling_analysis={},
    )
    
    assert score < 50, f"Expected score < 50, got {score}"


def test_storytelling_module_matching_variations():
    """Module matching should handle name variations."""
    from app.services.scoring_service import modules_match
    
    # Test exact match
    assert modules_match("Main Banner", "Main Banner")
    
    # Test case insensitive
    assert modules_match("main banner", "Main Banner")
    
    # Test banner variations
    assert modules_match("Banner principal", "Main Banner")
    assert modules_match("Main Banner", "banner principal")
    
    # Test accordion variations
    assert modules_match("Accordion", "accordion")
    assert modules_match("FAQ Accordion", "Accordion")
    
    # Test non-matches
    assert not modules_match("Card", "Banner")
    assert not modules_match("Media", "Accordion")


def test_storytelling_breakdown_shows_positive_impacts():
    """Breakdown should show positive adherence, not just penalties."""
    pattern = {
        "required_modules": ["Main Banner", "Accordion"],
        "narrative_steps": [
            {
                "name": "Apresentação",
                "recommended_modules": ["Main Banner"]
            }
        ],
    }
    
    detected_modules = [
        {"matched_catalog_name": "Main Banner"},
        {"matched_catalog_name": "Accordion"},
    ]
    
    _, breakdown = calculate_storytelling_score(
        pattern=pattern,
        detected_modules=detected_modules,
        narrative_insights=[],
        storytelling_analysis={},
    )
    
    # Should have criteria with positive impacts
    positive_impacts = [
        item for item in breakdown if item["impact"] > 0
    ]
    assert len(positive_impacts) > 0
    
    # Should explain coverage
    coverage_items = [
        item for item in breakdown
        if "coverage" in item["criterion"]
    ]
    assert len(coverage_items) > 0


def test_modules_score_low_when_no_modules_detected():
    """Modules score should be low when no modules are detected."""
    score, _ = calculate_modules_score(
        detected_modules=[],
        module_plan={"add": [], "remove": [], "reorder": [], "keep": []},
        pattern=None,
    )
    
    assert score <= 30


def test_brand_safety_score_decreases_with_prohibited_terms():
    """Brand safety score should decrease with prohibited terms."""
    brand_rules = [
        {
            "rule": "Avoid financial promises",
            "bad_examples": ["garantido", "sem risco"],
        }
    ]
    
    normalized_page_safe = {
        "main_text": "Este é um produto financeiro seguro e regulado.",
        "metadata": {},
        "headings": [],
        "images": [],
        "links": [],
    }
    
    normalized_page_unsafe = {
        "main_text": "Lucro garantido sem risco para você!",
        "metadata": {},
        "headings": [],
        "images": [],
        "links": [],
    }
    
    score_safe, _ = calculate_brand_safety_score(
        normalized_page=normalized_page_safe,
        brand_rules=brand_rules,
        narrative_insights=[],
        pattern=None,
    )
    
    score_unsafe, _ = calculate_brand_safety_score(
        normalized_page=normalized_page_unsafe,
        brand_rules=brand_rules,
        narrative_insights=[],
        pattern=None,
    )
    
    assert score_unsafe < score_safe


def test_overall_score_is_weighted_average():
    """Overall score should be calculated as weighted average."""
    seo = 80
    storytelling = 90
    modules = 70
    brand_safety = 85
    
    overall = calculate_overall_score(
        seo_score=seo,
        storytelling_score=storytelling,
        modules_score=modules,
        brand_safety_score=brand_safety,
    )
    
    # Expected: 80*0.25 + 90*0.30 + 70*0.25 + 85*0.20 = 81.5 -> 82
    expected = round(
        seo * 0.25 + storytelling * 0.30 +
        modules * 0.25 + brand_safety * 0.20
    )
    
    assert overall == expected


def test_score_breakdown_explains_losses():
    """Score breakdown should explain why points were lost."""
    normalized_page = {
        "metadata": {"title": "", "meta_description": ""},
        "headings": [],
        "images": [],
        "links": [],
        "main_text": "Short",
    }
    
    _, breakdown = calculate_seo_score(normalized_page)
    
    assert len(breakdown) > 0
    assert any(item["criterion"] == "title_missing" for item in breakdown)
    assert any(
        item["criterion"] == "meta_description_missing"
        for item in breakdown
    )
    assert all("reason" in item for item in breakdown)
    assert all("impact" in item for item in breakdown)


def test_calculate_scores_returns_complete_structure():
    """calculate_scores should return score and score_breakdown."""
    result = calculate_scores(
        normalized_page={
            "metadata": {"title": "Test", "meta_description": "Test"},
            "headings": [{"level": 1, "text": "H1"}],
            "images": [],
            "links": ["link1", "link2", "link3"],
            "main_text": "A" * 500,
        },
        detected_modules=[{"matched_catalog_name": "Main Banner"}],
        module_plan={"add": [], "remove": [], "reorder": [], "keep": []},
        storytelling_analysis={},
        narrative_insights=[],
        brand_rules=[],
        pattern={"required_modules": ["Main Banner"], "narrative_steps": []},
    )
    
    assert "score" in result
    assert "score_breakdown" in result
    assert "overall" in result["score"]
    assert "seo" in result["score"]
    assert "storytelling" in result["score"]
    assert "modules" in result["score"]
    assert "brand_safety" in result["score"]
    assert "seo" in result["score_breakdown"]
    assert "storytelling" in result["score_breakdown"]
    assert "modules" in result["score_breakdown"]
    assert "brand_safety" in result["score_breakdown"]


# Made with Bob