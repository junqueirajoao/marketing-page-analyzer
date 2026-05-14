from app.schemas.input import AnalyzeBriefingRequest
from app.services.catalog_loader import load_all_catalogs
from app.services.advantage_client import LocalAgentFallback


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

# Made with Bob
