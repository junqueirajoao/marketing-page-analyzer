from app.schemas.input import AnalyzeBriefingRequest, AnalyzeUrlRequest
from app.services.catalog_loader import load_all_catalogs
from app.services.advantage_client import LocalAgentFallback
from app.services.scraper import fetch_page
from app.services.page_normalizer import normalize_page


def build_briefing_analysis_report(payload: AnalyzeBriefingRequest) -> dict:
    catalogs = load_all_catalogs()
    agent_payload = {
        "input_type": "briefing",
        "briefing": payload.briefing,
        "business_goal": payload.business_goal,
        "target_audience": payload.target_audience,
        "constraints": payload.constraints,
        "catalogs": catalogs
    }
    agent_client = LocalAgentFallback()
    return agent_client.analyze_briefing(agent_payload)


async def build_url_analysis_report(payload: AnalyzeUrlRequest) -> dict:
    # Load catalogs
    catalogs = load_all_catalogs()
    
    # Fetch and normalize page
    raw_page = await fetch_page(str(payload.url))
    normalized_page = normalize_page(raw_page)
    
    # Build agent payload with normalized page data
    agent_payload = {
        "input_type": "url",
        "url": str(payload.url),
        "business_goal": payload.business_goal,
        "target_audience": payload.target_audience,
        "page_type_hint": payload.page_type_hint,
        "catalogs": catalogs,
        "normalized_page": normalized_page
    }
    
    # Call agent
    agent_client = LocalAgentFallback()
    return agent_client.analyze_url(agent_payload)

# Made with Bob
