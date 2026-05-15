from pydantic import BaseModel, HttpUrl, Field


class AnalyzeUrlRequest(BaseModel):
    """
    Request schema for URL-based analysis.
    
    AI-Powered Page Analysis: The system automatically scrapes the page,
    detects modules, analyzes storytelling patterns, evaluates SEO,
    checks brand compliance, and provides actionable recommendations.
    
    Only 'url' is required - the system handles everything else automatically.
    """
    url: HttpUrl = Field(
        ...,
        description="URL of the marketing page to analyze"
    )


# Made with Bob
