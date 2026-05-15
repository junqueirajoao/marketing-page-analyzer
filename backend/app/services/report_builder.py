from app.schemas.input import AnalyzeUrlRequest
from app.services.catalog_loader import load_all_catalogs
from app.services.advantage_client import AdvantageClient
from app.services.scraper import fetch_page
from app.services.page_normalizer import normalize_page
from app.services.module_detector import detect_modules


async def build_url_analysis_report(payload: AnalyzeUrlRequest) -> dict:
    """
    Build URL analysis report using ICA with fallback.
    
    This is the core analysis pipeline:
    1. Load catalogs (modules, storytelling patterns, brand rules)
    2. Scrape and parse the page
    3. Detect modules in the page structure
    4. Send to ICA orchestrator for AI-powered analysis
    5. Return comprehensive analysis with recommendations
    
    Args:
        payload: URL analysis request containing the page URL
    
    Returns:
        Analysis report dictionary with scores, recommendations,
        module plan, narrative insights, and agent trace
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
        "catalogs": catalogs,
        "normalized_page": normalized_page
    }
    
    # Call agent with ICA integration
    agent_client = AdvantageClient()
    return await agent_client.analyze_url(agent_payload)


# Made with Bob
