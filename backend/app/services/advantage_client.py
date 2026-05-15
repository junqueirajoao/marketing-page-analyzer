"""
IBM Consulting Advantage Client with Automatic Fallback
Orchestrates analysis using ICA when available, with local fallback.
"""
import os
import logging
from typing import Dict, Any, Optional

from app.services.ica_client import ICAClient
from app.services.local_agent_fallback import LocalAgentFallback
from app.services.catalog_context_builder import build_catalog_context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class AdvantageClient:
    """
    Main client for IBM Consulting Advantage integration.
    Attempts to use ICA orchestration, falls back to local agent on failure.
    """
    
    def __init__(self):
        """Initialize Advantage client with ICA and fallback."""
        self.ica_client = ICAClient()
        self.fallback_client = LocalAgentFallback()
        self.enable_fallback = os.getenv(
            "ENABLE_AGENT_FALLBACK",
            "true"
        ).lower() == "true"
        
        if self.ica_client.is_enabled():
            logger.info("[ADVANTAGE] ICA client enabled")
        else:
            logger.info("[ADVANTAGE] ICA client not configured")
        
        if self.enable_fallback:
            logger.info("[ADVANTAGE] Fallback enabled")
        else:
            logger.info("[ADVANTAGE] Fallback disabled")
    
    async def analyze_briefing(
        self, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a briefing using ICA or fallback.
        
        Args:
            payload: Dictionary containing:
                - input_type: Type of input (e.g., "briefing")
                - briefing: The briefing text
                - business_goal: Optional business goal
                - target_audience: Optional target audience
                - constraints: List of constraints
                - catalogs: Dictionary with catalogs
        
        Returns:
            Dictionary with analysis results
        """
        # First, generate local analysis for ICA payload
        logger.info("[ADVANTAGE] Generating local analysis for ICA payload")
        local_result = self.fallback_client.analyze_briefing(payload)
        
        # Try ICA if enabled
        if self.ica_client.is_enabled():
            ica_payload = self._build_ica_payload_from_local(
                local_result=local_result,
                business_goal=payload.get("business_goal", ""),
                target_audience=payload.get("target_audience", ""),
                page_type_hint=None
            )
            
            ica_result = await self.ica_client.call_orchestration(ica_payload)
            
            if ica_result:
                logger.info("[ADVANTAGE] Using ICA response")
                # Merge ICA response with local analysis
                return self._merge_ica_response(local_result, ica_result)
        
        # Use fallback
        if self.enable_fallback:
            logger.info("[FALLBACK] Using LocalAgentFallback")
            return local_result
        else:
            logger.error("[ADVANTAGE] ICA failed and fallback disabled")
            raise RuntimeError("ICA unavailable and fallback disabled")
    
    async def analyze_url(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a URL using ICA or fallback.
        
        Args:
            payload: Dictionary containing:
                - input_type: Type of input (e.g., "url")
                - url: The URL to analyze
                - business_goal: Optional business goal
                - target_audience: Optional target audience
                - page_type_hint: Optional page type hint
                - catalogs: Dictionary with catalogs
                - normalized_page: Normalized page data
        
        Returns:
            Dictionary with analysis results
        """
        # First, generate local analysis for ICA payload
        logger.info("[ADVANTAGE] Generating local analysis for ICA payload")
        local_result = self.fallback_client.analyze_url(payload)
        
        # Try ICA if enabled
        if self.ica_client.is_enabled():
            ica_payload = self._build_ica_payload_from_local(
                local_result=local_result,
                business_goal=payload.get("business_goal", ""),
                target_audience=payload.get("target_audience", ""),
                page_type_hint=payload.get("page_type_hint")
            )
            
            ica_result = await self.ica_client.call_orchestration(ica_payload)
            
            if ica_result:
                logger.info("[ADVANTAGE] Using ICA response")
                # Merge ICA response with local analysis
                return self._merge_ica_response(local_result, ica_result)
        
        # Use fallback
        if self.enable_fallback:
            logger.info("[FALLBACK] Using LocalAgentFallback")
            return local_result
        else:
            logger.error("[ADVANTAGE] ICA failed and fallback disabled")
            raise RuntimeError("ICA unavailable and fallback disabled")
    
    def _build_ica_payload_from_local(
        self,
        local_result: Dict[str, Any],
        business_goal: str,
        target_audience: str,
        page_type_hint: Optional[str]
    ) -> Dict[str, Any]:
        """
        Build ICA payload from local analysis result.
        
        Args:
            local_result: Local analysis result
            business_goal: Business goal
            target_audience: Target audience
            page_type_hint: Optional page type hint
        
        Returns:
            Structured payload for ICA
        """
        # Build catalog context for ICA
        catalogs = local_result.get("catalogs", {})
        storytelling_analysis = local_result.get("storytelling_analysis", {})
        page_type = (
            page_type_hint or
            storytelling_analysis.get("page_type") or
            storytelling_analysis.get("detected_page_type")
        )
        
        catalog_context = build_catalog_context(
            catalogs=catalogs,
            page_type=page_type,
            business_goal=business_goal,
            target_audience=target_audience,
            detected_modules=local_result.get("detected_modules", []),
            score_breakdown=local_result.get("score_breakdown", {}),
            narrative_insights=local_result.get("narrative_insights", []),
            max_items_per_catalog=8
        )
        
        return self.ica_client.build_ica_payload(
            normalized_page=local_result.get("normalized_page", {}),
            detected_modules=local_result.get("detected_modules", []),
            module_plan=local_result.get("module_plan", {}),
            storytelling_analysis=storytelling_analysis,
            score=local_result.get("score", 0.0),
            score_breakdown=local_result.get("score_breakdown", {}),
            narrative_insights=local_result.get("narrative_insights", []),
            business_goal=business_goal,
            target_audience=target_audience,
            page_type_hint=page_type_hint,
            catalog_context=catalog_context
        )
    
    def _merge_ica_response(
        self,
        local_result: Dict[str, Any],
        ica_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge ICA response with local analysis, preserving API contract.
        
        Args:
            local_result: Local analysis result
            ica_result: ICA orchestration result
        
        Returns:
            Merged result maintaining API contract
        """
        # Start with local result as base
        merged = local_result.copy()
        
        # Override with ICA results where available
        # Handle recommendations (ICA might use 'final_recommendations')
        if "recommendations" in ica_result:
            merged["recommendations"] = ica_result["recommendations"]
        elif "final_recommendations" in ica_result:
            merged["recommendations"] = ica_result["final_recommendations"]
        
        # Override narrative insights if provided
        if "narrative_insights" in ica_result:
            merged["narrative_insights"] = ica_result["narrative_insights"]
        
        # Override storytelling analysis if provided
        if "storytelling_analysis" in ica_result:
            merged["storytelling_analysis"] = ica_result[
                "storytelling_analysis"
            ]
        
        # Override module plan if provided
        if "module_plan" in ica_result:
            merged["module_plan"] = ica_result["module_plan"]
        
        # Override page summary if provided
        if "page_summary" in ica_result:
            merged["page_summary"] = ica_result["page_summary"]
        
        # Override scores if provided
        if "score" in ica_result:
            merged["score"] = ica_result["score"]
        
        if "score_breakdown" in ica_result:
            merged["score_breakdown"] = ica_result["score_breakdown"]
        
        # Add ICA metadata
        merged["ica_enhanced"] = True
        merged["analysis_source"] = "ica"
        
        return merged


# Backward compatibility: export LocalAgentFallback for existing code
__all__ = ["AdvantageClient", "LocalAgentFallback"]


# Made with Bob