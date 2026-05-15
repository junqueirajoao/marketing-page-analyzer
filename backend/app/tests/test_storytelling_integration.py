from app.services.advantage_client import LocalAgentFallback
from app.services.catalog_loader import (
    load_storytelling_patterns,
    normalize_storytelling_pattern,
)
from app.services.storytelling_pattern_service import (
    find_best_storytelling_pattern,
    get_storytelling_patterns,
)


def _sample_rich_pattern():
    return {
        "id": "pattern_credito_pessoal",
        "page_type": "credito_pessoal",
        "segment": "financial_services",
        "business_goal": "conversao",
        "target_audience": "pessoa_fisica",
        "storytelling_name": (
            "Problema → Alívio financeiro → Segurança → Conversão"
        ),
        "description": "Pattern para página de crédito pessoal.",
        "emotional_journey": ["urgencia", "clareza", "seguranca", "acao"],
        "narrative_steps": [
            {
                "step": 1,
                "name": "Dor financeira",
                "objective": "Apresentar a dor principal.",
                "recommended_modules": ["Main Banner"],
                "copy_direction": "Reconheça o problema."
            },
            {
                "step": 2,
                "name": "Alívio financeiro",
                "objective": "Mostrar como a solução ajuda.",
                "recommended_modules": ["Media with steps"],
                "copy_direction": "Explique o alívio com clareza."
            }
        ],
        "recommended_module_order": [
            "Breadcrumb Header",
            "Main Banner",
            "Media with steps"
        ],
        "required_modules": ["Main Banner", "Media with steps"],
        "optional_modules": ["Breadcrumb Header"],
        "avoid_modules_when": [
            {
                "module": "Carrossel",
                "reason": "Pode dispersar atenção em contexto de urgência."
            }
        ],
        "headline_examples": ["Organize sua vida financeira hoje."],
        "cta_examples": ["Simule seu crédito agora"],
        "tone_guidelines": ["claro", "educativo"],
        "compliance_guidelines": ["Não prometer aprovação garantida."],
        "avoid_copy": ["dinheiro sem análise"],
        "agent_evaluation_rules": {
            "strong_pattern_when": ["dor e urgência estão explícitas"],
            "weak_pattern_when": ["não há CTA claro"]
        }
    }


def _sample_institutional_pattern():
    return {
        "id": "pattern_institucional",
        "page_type": "institucional",
        "segment": "general",
        "business_goal": "awareness",
        "target_audience": "geral",
        "storytelling_name": "Institucional",
        "description": "Pattern institucional padrão.",
        "emotional_journey": [],
        "narrative_steps": [
            {
                "step": 1,
                "name": "Apresentação",
                "objective": "Apresentar a empresa.",
                "recommended_modules": ["Main Banner"],
                "copy_direction": "Mostre a proposta de valor."
            }
        ],
        "recommended_module_order": ["Main Banner"],
        "required_modules": ["Main Banner"],
        "optional_modules": [],
        "avoid_modules_when": [],
        "headline_examples": [],
        "cta_examples": ["Conheça mais"],
        "tone_guidelines": ["claro"],
        "compliance_guidelines": [],
        "avoid_copy": [],
        "agent_evaluation_rules": {
            "strong_pattern_when": [],
            "weak_pattern_when": []
        }
    }


def _sample_catalogs():
    return {
        "modules_catalog": [
            {"id": "module_01", "name": "Breadcrumb Header"},
            {"id": "module_09", "name": "Main Banner"},
            {"id": "module_12", "name": "Media with steps"},
            {"id": "module_99", "name": "Carrossel"}
        ],
        "storytelling_patterns": [
            _sample_rich_pattern(),
            _sample_institutional_pattern()
        ],
        "brand_rules": []
    }


def test_load_storytelling_patterns_returns_new_structure():
    patterns = load_storytelling_patterns()

    assert isinstance(patterns, list)
    assert patterns
    assert "id" in patterns[0]
    assert "storytelling_name" in patterns[0]
    assert "narrative_steps" in patterns[0]
    assert "recommended_module_order" in patterns[0]


def test_normalize_legacy_storytelling_pattern():
    legacy_pattern = {
        "page_type": "produto",
        "pattern": ["Problema", "Solução", "CTA"],
        "description": "Estrutura antiga."
    }

    normalized = normalize_storytelling_pattern(legacy_pattern)

    assert normalized["id"] == "pattern_produto"
    assert normalized["storytelling_name"] == "produto"
    assert normalized["recommended_module_order"] == [
        "Problema", "Solução", "CTA"
    ]
    assert normalized["narrative_steps"][0]["name"] == "Problema"
    assert normalized["required_modules"] == []


def test_select_pattern_by_page_type():
    patterns = get_storytelling_patterns(_sample_catalogs())

    pattern = find_best_storytelling_pattern(
        patterns=patterns,
        page_type="credito_pessoal"
    )

    assert pattern is not None
    assert pattern["id"] == "pattern_credito_pessoal"


def test_select_pattern_by_business_goal():
    patterns = get_storytelling_patterns(_sample_catalogs())

    pattern = find_best_storytelling_pattern(
        patterns=patterns,
        business_goal="conversao"
    )

    assert pattern is not None
    assert pattern["id"] == "pattern_credito_pessoal"


def test_return_default_pattern_when_no_match():
    patterns = get_storytelling_patterns(_sample_catalogs())

    pattern = find_best_storytelling_pattern(
        patterns=patterns,
        page_type="desconhecido",
        business_goal="sem_match",
        target_audience="sem_match",
        text_context="contexto sem aderência"
    )

    assert pattern is not None
    assert pattern["id"] == "pattern_institucional"


def test_analyze_briefing_returns_storytelling_analysis():
    client = LocalAgentFallback()
    catalogs = _sample_catalogs()

    result = client.analyze_briefing({
        "briefing": "Página de crédito pessoal com foco em conversao.",
        "business_goal": "conversao",
        "target_audience": "pessoa_fisica",
        "constraints": [],
        "catalogs": catalogs
    })

    assert "storytelling_analysis" in result
    assert (
        result["storytelling_analysis"]["detected_pattern_id"]
        == "pattern_credito_pessoal"
    )
    assert result["storytelling_analysis"]["recommended_module_order"] == [
        "Breadcrumb Header",
        "Main Banner",
        "Media with steps"
    ]


def test_analyze_url_returns_storytelling_analysis():
    client = LocalAgentFallback()
    catalogs = _sample_catalogs()

    result = client.analyze_url({
        "url": "https://example.com/credito-pessoal",
        "business_goal": "conversao",
        "target_audience": "pessoa_fisica",
        "page_type_hint": "credito_pessoal",
        "catalogs": catalogs,
        "normalized_page": {
            "metadata": {},
            "headings": [],
            "links": [],
            "images": [],
            "main_text": "Crédito pessoal com simulação simples.",
            "modules": [],
            "error": None
        }
    })

    assert "storytelling_analysis" in result
    assert (
        result["storytelling_analysis"]["detected_pattern_name"]
        == "Problema → Alívio financeiro → Segurança → Conversão"
    )
    assert result["storytelling_analysis"]["cta_examples"] == [
        "Simule seu crédito agora"
    ]


def test_module_plan_uses_required_modules_and_recommended_order():
    client = LocalAgentFallback()
    pattern = _sample_rich_pattern()

    module_plan = client._build_module_plan(
        catalogs=_sample_catalogs(),
        pattern=pattern,
        detected_modules=[
            {"matched_catalog_name": "Main Banner"},
            {"matched_catalog_name": "Carrossel"}
        ]
    )

    assert module_plan["reorder"][0]["module_type"] == "Main Banner"
    assert any(
        item["module_type"] == "Media with steps"
        for item in module_plan["add"]
    )
    assert any(
        item["module_type"] == "Carrossel"
        for item in module_plan["remove"]
    )

# Made with Bob
