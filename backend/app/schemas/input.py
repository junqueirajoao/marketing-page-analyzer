from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class AnalyzeBriefingRequest(BaseModel):
    briefing: str
    business_goal: Optional[str] = None
    target_audience: Optional[str] = None
    constraints: List[str] = []


class AnalyzeUrlRequest(BaseModel):
    url: HttpUrl
    business_goal: Optional[str] = None
    target_audience: Optional[str] = None
    page_type_hint: Optional[str] = None