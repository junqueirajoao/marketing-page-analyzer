from typing import List, Optional

from pydantic import BaseModel


class AnalyzeBriefingRequest(BaseModel):
    briefing: str
    business_goal: Optional[str] = None
    target_audience: Optional[str] = None
    constraints: List[str] = []