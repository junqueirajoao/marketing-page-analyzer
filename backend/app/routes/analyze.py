from fastapi import APIRouter
from app.schemas.input import AnalyzeBriefingRequest
from app.services.report_builder import build_briefing_analysis_report

router = APIRouter()


@router.post("/briefing")
def analyze_briefing(payload: AnalyzeBriefingRequest):
    return build_briefing_analysis_report(payload)