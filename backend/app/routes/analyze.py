from fastapi import APIRouter
from fastapi.responses import Response
from app.schemas.input import AnalyzeBriefingRequest, AnalyzeUrlRequest
from app.services.report_builder import (
    build_briefing_analysis_report,
    build_url_analysis_report
)
import json

router = APIRouter()


@router.post("/briefing")
async def analyze_briefing(payload: AnalyzeBriefingRequest):
    result = await build_briefing_analysis_report(payload)
    json_str = json.dumps(result, ensure_ascii=False, indent=None)
    json_bytes = json_str.encode('utf-8')
    return Response(
        content=json_bytes,
        media_type="application/json; charset=utf-8"
    )


@router.post("/url")
async def analyze_url(payload: AnalyzeUrlRequest):
    result = await build_url_analysis_report(payload)
    json_str = json.dumps(result, ensure_ascii=False, indent=None)
    json_bytes = json_str.encode('utf-8')
    return Response(
        content=json_bytes,
        media_type="application/json; charset=utf-8"
    )