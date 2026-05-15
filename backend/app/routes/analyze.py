from fastapi import APIRouter
from fastapi.responses import Response
from app.schemas.input import AnalyzeUrlRequest
from app.services.report_builder import build_url_analysis_report
import json

router = APIRouter()


@router.post("/url")
async def analyze_url(payload: AnalyzeUrlRequest):
    """
    Analyze a marketing page by URL.
    
    The system automatically:
    - Scrapes and parses the page
    - Detects modules and structure
    - Analyzes storytelling and narrative flow
    - Evaluates SEO and compliance
    - Provides actionable recommendations
    """
    result = await build_url_analysis_report(payload)
    json_str = json.dumps(result, ensure_ascii=False, indent=None)
    json_bytes = json_str.encode('utf-8')
    return Response(
        content=json_bytes,
        media_type="application/json; charset=utf-8"
    )