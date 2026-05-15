from fastapi import APIRouter
from app.schemas.input import AnalyzeBriefingRequest, AnalyzeUrlRequest
from app.services.report_builder import (
    build_briefing_analysis_report,
    build_url_analysis_report
)

router = APIRouter()


@router.post("/briefing")
async def analyze_briefing(payload: AnalyzeBriefingRequest):
    return await build_briefing_analysis_report(payload)


@router.post("/url")
async def analyze_url(payload: AnalyzeUrlRequest):
    return await build_url_analysis_report(payload)