from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class AnalyzeBriefingRequest(BaseModel):
    briefing: str
    business_goal: Optional[str] = None
    target_audience: Optional[str] = None
    constraints: List[str] = []

@router.post("/briefing")
def analyze_briefing(payload: AnalyzeBriefingRequest):
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
                "title": "Organizar a narrativa da página",
                "why": "O briefing precisa deixar mais claro o problema, a solução e o próximo passo esperado do usuário.",
                "suggestion": "Estruture a página em problema, solução, benefícios, prova e CTA.",
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
                    "reason": "Ajuda a reduzir objeções antes da conversão."
                }
            ]
        },
        "copy_suggestions": []
    }