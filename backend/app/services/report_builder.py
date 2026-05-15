from app.schemas.input import AnalyzeBriefingRequest, AnalyzeUrlRequest
from app.services.catalog_loader import load_all_catalogs
from app.services.advantage_client import AdvantageClient
from app.services.scraper import fetch_page
from app.services.page_normalizer import normalize_page
from app.services.module_detector import detect_modules


async def build_briefing_analysis_report(
    payload: AnalyzeBriefingRequest
) -> dict:
    """
    Build briefing analysis report using ICA with fallback.
    
    Args:
        payload: Briefing analysis request
    
    Returns:
        Analysis report dictionary
    """
    catalogs = load_all_catalogs()
    agent_payload = {
        "input_type": "briefing",
        "briefing": payload.briefing,
        "business_goal": payload.business_goal,
        "target_audience": payload.target_audience,
        "constraints": payload.constraints,
        "catalogs": catalogs
    }
    agent_client = AdvantageClient()
    return await agent_client.analyze_briefing(agent_payload)


async def build_url_analysis_report(payload: AnalyzeUrlRequest) -> dict:
    """
    Build URL analysis report using ICA with fallback.
    
    Args:
        payload: URL analysis request
    
    Returns:
        Analysis report dictionary
    """
    # Load catalogs
    catalogs = load_all_catalogs()
    
    # Fetch and normalize page
    raw_page = await fetch_page(str(payload.url))
    normalized_page = normalize_page(raw_page)
    
    # Detect modules in the normalized page
    detected_modules = detect_modules(
        normalized_page,
        catalogs["modules_catalog"]
    )
    normalized_page["modules"] = detected_modules
    
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
    
    # Call agent with ICA integration
    agent_client = AdvantageClient()
    return await agent_client.analyze_url(agent_payload)

# Made with Bob
