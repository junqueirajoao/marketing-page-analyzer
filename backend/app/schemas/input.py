from typing import List, Optional

from pydantic import BaseModel, HttpUrl, Field


class AnalyzeBriefingRequest(BaseModel):
    """
    Request schema for briefing-based analysis.
    
    AI-First Architecture: The system automatically infers context,
    detects narrative patterns, identifies intent, classifies page type,
    identifies likely audience, selects storytelling patterns, and builds
    catalog_context based on briefing content.
    
    Only 'briefing' is required. Optional fields (business_goal,
    target_audience) are for compatibility/future use and are NOT
    exposed in the main UX.
    """
    briefing: str = Field(
        ...,
        description="Natural language briefing describing the page"
    )
    business_goal: Optional[str] = Field(
        None,
        description=(
            "Optional: Business goal (e.g., 'conversion', "
            "'lead generation'). System infers if not provided."
        )
    )
    target_audience: Optional[str] = Field(
        None,
        description=(
            "Optional: Target audience description. "
            "System infers if not provided."
        )
    )
    constraints: List[str] = Field(
        default_factory=list,
        description=(
            "Optional constraints like 'simple tone', "
            "'avoid absolute promises'"
        )
    )


class AnalyzeUrlRequest(BaseModel):
    """
    Request schema for URL-based analysis.
    
    AI-First Architecture: The system automatically infers context,
    detects narrative patterns, identifies intent, classifies page type,
    identifies likely audience, selects storytelling patterns, and builds
    catalog_context based on URL, extracted content, detected modules,
    storytelling analysis, score breakdown, and narrative insights.
    
    Only 'url' is required. Optional fields (business_goal,
    target_audience, page_type_hint) are for compatibility/future use
    and are NOT exposed in the main UX.
    """
    url: HttpUrl = Field(..., description="URL of the page to analyze")
    business_goal: Optional[str] = Field(
        None,
        description=(
            "Optional: Business goal (e.g., 'conversion', "
            "'lead generation'). System infers if not provided."
        )
    )
    target_audience: Optional[str] = Field(
        None,
        description=(
            "Optional: Target audience description. "
            "System infers if not provided."
        )
    )
    page_type_hint: Optional[str] = Field(
        None,
        description=(
            "Optional: Page type hint (e.g., 'product', 'campaign'). "
            "System infers if not provided."
        )
    )

# Made with Bob
