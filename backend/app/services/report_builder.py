from app.schemas.input import AnalyzeBriefingRequest
from app.services.catalog_loader import load_all_catalogs


def build_briefing_analysis_report(payload: AnalyzeBriefingRequest) -> dict:
    # Load all catalogs to provide context
    catalogs = load_all_catalogs()
    
    return {
        "analysis_id": "demo_001",
        "score": {
            "overall": 78,
            "seo": 72,
            "storytelling": 81,
            "modules": 76,
            "brand_safety": 88
        },
        "page_summary": {
            "detected_type": "produto",
            "primary_goal": payload.business_goal or "nao_informado",
            "main_topic": "tema identificado a partir do briefing"
        },
        "recommendations": [
            {
                "priority": "high",
                "area": "storytelling",
                "title": "Organizar a narrativa da pagina",
                "why": (
                    "O briefing precisa deixar mais claro o problema, "
                    "a solucao e o proximo passo esperado do usuario."
                ),
                "suggestion": (
                    "Estruture a pagina em problema, solucao, "
                    "beneficios, prova e CTA."
                ),
                "impact": "high",
                "effort": "medium"
            }
        ],
        "module_plan": {
            "keep": [],
            "remove": [],
            "reorder": [],
            "add": [
                {
                    "module_type": "FAQ",
                    "reason": "Ajuda a reduzir objecoes antes da conversao."
                }
            ]
        },
        "copy_suggestions": [],
        "catalog_context": {
            "modules_available_count": len(catalogs["modules_catalog"]),
            "storytelling_patterns_count": len(
                catalogs["storytelling_patterns"]
            ),
            "brand_rules_count": len(catalogs["brand_rules"])
        }
    }