"""
IBM Consulting Advantage (ICA) Client
Handles communication with ICA orchestration API with automatic fallback.
"""
import os
import logging
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class ICAClient:
    """
    Client for IBM Consulting Advantage orchestration API.
    Implements timeout, error handling, and response validation.
    """
    
    def __init__(self):
        """Initialize ICA client with configuration from environment."""
        self.base_url = os.getenv("ADVANTAGE_BASE_URL", "")
        self.api_key = os.getenv("ADVANTAGE_API_KEY", "")
        self.orchestrator_id = os.getenv(
            "ADVANTAGE_ORCHESTRATOR_ID",
            "d5d0c63a-4a42-4431-b870-3f496a43fe10"
        )
        self.timeout = 30.0  # 30 seconds timeout
        self.enabled = bool(self.base_url and self.api_key)
        
        if not self.enabled:
            logger.warning(
                "[ICA] ICA client not configured. Missing ADVANTAGE_BASE_URL "
                "or ADVANTAGE_API_KEY. Will use fallback."
            )
    
    def is_enabled(self) -> bool:
        """Check if ICA client is properly configured."""
        return self.enabled
    
    async def call_orchestration(
        self,
        payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Call ICA orchestration with the provided payload.
        
        Args:
            payload: Dictionary containing analysis data:
                - normalized_page: Normalized page data
                - detected_modules: List of detected modules
                - module_plan: Module recommendations
                - storytelling_analysis: Storytelling pattern analysis
                - score: Overall score
                - score_breakdown: Detailed scoring
                - narrative_insights: List of insights
                - business_goal: Business goal
                - target_audience: Target audience
                - page_type_hint: Optional page type hint
        
        Returns:
            Dictionary with ICA response or None if failed
        """
        if not self.enabled:
            logger.info("[ICA] Client not enabled, skipping orchestration call")
            return None
        
        try:
            logger.info(
                f"[ICA] Calling orchestration {self.orchestrator_id}"
            )
            
            # Build request URL
            url = f"{self.base_url}/orchestrations/{self.orchestrator_id}/execute"
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Make async HTTP request with timeout
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=headers
                )
                
                # Check HTTP status
                if response.status_code != 200:
                    logger.warning(
                        f"[ICA] HTTP error {response.status_code}: "
                        f"{response.text[:200]}"
                    )
                    return None
                
                # Parse JSON response
                result = response.json()
                logger.info("[ICA] Response received successfully")
                
                # Validate response structure
                if not self._validate_response(result):
                    logger.warning(
                        "[ICA] Invalid response received, using fallback"
                    )
                    return None
                
                return result
                
        except httpx.TimeoutException:
            logger.warning(
                f"[ICA] Timeout after {self.timeout}s, using fallback"
            )
            return None
            
        except httpx.HTTPError as e:
            logger.warning(f"[ICA] HTTP error: {str(e)}, using fallback")
            return None
            
        except ValueError as e:
            logger.warning(f"[ICA] JSON decode error: {str(e)}, using fallback")
            return None
            
        except Exception as e:
            logger.error(
                f"[ICA] Unexpected error: {str(e)}, using fallback",
                exc_info=True
            )
            return None
    
    def _validate_response(self, response: Dict[str, Any]) -> bool:
        """
        Validate that ICA response has minimum required structure.
        
        Args:
            response: ICA response dictionary
        
        Returns:
            True if response is valid, False otherwise
        """
        if not isinstance(response, dict):
            logger.warning("[ICA] Response is not a dictionary")
            return False
        
        # Check for critical fields
        has_recommendations = (
            "recommendations" in response or
            "final_recommendations" in response
        )
        has_narrative = "narrative_insights" in response
        has_storytelling = "storytelling_analysis" in response
        
        if not has_recommendations:
            logger.warning("[ICA] Missing recommendations field")
            return False
        
        if not has_narrative:
            logger.warning("[ICA] Missing narrative_insights field")
            return False
        
        if not has_storytelling:
            logger.warning("[ICA] Missing storytelling_analysis field")
            return False
        
        # Validate recommendations structure
        recommendations = response.get(
            "recommendations",
            response.get("final_recommendations", [])
        )
        if not isinstance(recommendations, list):
            logger.warning("[ICA] Recommendations is not a list")
            return False
        
        # Validate narrative_insights structure
        narrative_insights = response.get("narrative_insights", [])
        if not isinstance(narrative_insights, list):
            logger.warning("[ICA] Narrative insights is not a list")
            return False
        
        # Validate storytelling_analysis structure
        storytelling = response.get("storytelling_analysis", {})
        if not isinstance(storytelling, dict):
            logger.warning("[ICA] Storytelling analysis is not a dict")
            return False
        
        logger.info("[ICA] Response validation passed")
        return True
    
    def build_ica_payload(
        self,
        normalized_page: Dict[str, Any],
        detected_modules: list,
        module_plan: Dict[str, Any],
        storytelling_analysis: Dict[str, Any],
        score: float,
        score_breakdown: Dict[str, Any],
        narrative_insights: list,
        business_goal: str,
        target_audience: str,
        page_type_hint: Optional[str] = None,
        catalog_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build structured payload for ICA orchestration.
        
        Args:
            normalized_page: Normalized page data
            detected_modules: List of detected modules
            module_plan: Module recommendations
            storytelling_analysis: Storytelling pattern analysis
            score: Overall score
            score_breakdown: Detailed scoring
            narrative_insights: List of insights
            business_goal: Business goal
            target_audience: Target audience
            page_type_hint: Optional page type hint
            catalog_context: Optional catalog context with relevant rules
        
        Returns:
            Structured payload dictionary for ICA
        """
        payload = {
            "normalized_page": normalized_page,
            "detected_modules": detected_modules,
            "module_plan": module_plan,
            "storytelling_analysis": storytelling_analysis,
            "score": score,
            "score_breakdown": score_breakdown,
            "narrative_insights": narrative_insights,
            "business_goal": business_goal,
            "target_audience": target_audience,
            "page_type_hint": page_type_hint or "",
            "instructions": self._build_instructions()
        }
        
        # Add catalog context if provided
        if catalog_context:
            payload["catalog_context"] = catalog_context
            logger.info(
                f"[ICA] Added catalog_context with "
                f"{len(catalog_context.get('relevant_modules', []))} modules, "
                f"{len(catalog_context.get('relevant_storytelling_patterns', []))} patterns, "
                f"{len(catalog_context.get('relevant_seo_rules', []))} SEO rules, "
                f"{len(catalog_context.get('relevant_brand_rules', []))} brand rules"
            )
        
        return payload
    
    def _build_instructions(self) -> str:
        """
        Build instructions for ICA agents.
        
        Returns:
            Instructions string for agents
        """
        return (
            "Use catalog_context as the source of domain knowledge. "
            "Do not invent rules, modules or storytelling patterns "
            "outside the provided context. "
            "Base your recommendations on the relevant_modules, "
            "relevant_storytelling_patterns, relevant_seo_rules, "
            "and relevant_brand_rules provided in catalog_context."
        )


# Made with Bob