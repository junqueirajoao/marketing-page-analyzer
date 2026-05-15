"""
Tests for IBM Consulting Advantage (ICA) Integration.

Tests ICA client, fallback mechanism, and API contract preservation.

Note: Test payloads include business_goal, target_audience, and page_type_hint
for comprehensive testing, but these fields are OPTIONAL in the actual API.
The AI-first architecture automatically infers these values when not provided.
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import httpx

from app.services.ica_client import ICAClient
from app.services.advantage_client import AdvantageClient
from app.services.local_agent_fallback import LocalAgentFallback

# Use anyio for async tests
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_catalogs():
    """Mock catalogs for testing."""
    return {
        "modules_catalog": [],
        "storytelling_patterns": [],
        "brand_rules": []
    }


@pytest.fixture
def sample_briefing_payload(mock_catalogs):
    """Sample briefing payload for testing."""
    return {
        "input_type": "briefing",
        "briefing": "Test briefing content",
        "business_goal": "conversao",
        "target_audience": "empresas",
        "constraints": [],
        "catalogs": mock_catalogs
    }


@pytest.fixture
def sample_url_payload(mock_catalogs):
    """Sample URL payload for testing."""
    return {
        "input_type": "url",
        "url": "https://example.com",
        "business_goal": "conversao",
        "target_audience": "empresas",
        "page_type_hint": "produto",
        "catalogs": mock_catalogs,
        "normalized_page": {
            "metadata": {},
            "headings": [],
            "images": [],
            "links": [],
            "main_text": "Test content",
            "modules": []
        }
    }


@pytest.fixture
def valid_ica_response():
    """Valid ICA response for testing."""
    return {
        "recommendations": [
            {
                "priority": "high",
                "area": "storytelling",
                "title": "Test recommendation",
                "why": "Test reason",
                "suggestion": "Test suggestion",
                "impact": "high",
                "effort": "medium"
            }
        ],
        "narrative_insights": [
            {
                "id": "test_insight",
                "type": "module_gap",
                "severity": "high",
                "title": "Test insight",
                "description": "Test description",
                "related_modules": [],
                "recommended_actions": []
            }
        ],
        "storytelling_analysis": {
            "pattern_name": "Test Pattern",
            "confidence": 0.9
        },
        "module_plan": {
            "keep": [],
            "remove": [],
            "reorder": [],
            "add": []
        },
        "score": {
            "overall": 85.0,
            "seo": 80.0,
            "storytelling": 90.0,
            "modules": 85.0,
            "brand_safety": 90.0
        },
        "score_breakdown": {
            "seo": [],
            "storytelling": [],
            "modules": [],
            "brand_safety": []
        }
    }


class TestICAClient:
    """Test ICA client functionality."""
    
    def test_ica_client_initialization_with_config(self):
        """Test ICA client initializes correctly with config."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key',
            'ADVANTAGE_ORCHESTRATOR_ID': 'test_id'
        }):
            client = ICAClient()
            assert client.is_enabled() is True
            assert client.base_url == 'https://test.api.com'
            assert client.orchestrator_id == 'test_id'
    
    def test_ica_client_initialization_without_config(self):
        """Test ICA client handles missing configuration."""
        with patch.dict('os.environ', {}, clear=True):
            client = ICAClient()
            assert client.is_enabled() is False
    
    async def test_ica_call_success(self, valid_ica_response):
        """Test successful ICA orchestration call."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key'
        }):
            client = ICAClient()
            
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = valid_ica_response
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.post = \
                    AsyncMock(return_value=mock_response)
                
                result = await client.call_orchestration({})
                
                assert result is not None
                assert "recommendations" in result
                assert "narrative_insights" in result
    
    async def test_ica_call_timeout(self):
        """Test ICA timeout handling."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key'
        }):
            client = ICAClient()
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.post = \
                    AsyncMock(side_effect=httpx.TimeoutException("Timeout"))
                
                result = await client.call_orchestration({})
                
                assert result is None
    
    async def test_ica_call_http_error(self):
        """Test ICA HTTP error handling."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key'
        }):
            client = ICAClient()
            
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.post = \
                    AsyncMock(return_value=mock_response)
                
                result = await client.call_orchestration({})
                
                assert result is None
    
    async def test_ica_call_invalid_response(self):
        """Test ICA invalid response handling."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key'
        }):
            client = ICAClient()
            
            # Missing required fields
            invalid_response = {"some_field": "value"}
            
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = invalid_response
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.post = \
                    AsyncMock(return_value=mock_response)
                
                result = await client.call_orchestration({})
                
                assert result is None
    
    def test_validate_response_valid(self, valid_ica_response):
        """Test response validation with valid response."""
        client = ICAClient()
        assert client._validate_response(valid_ica_response) is True
    
    def test_validate_response_missing_recommendations(self):
        """Test response validation with missing recommendations."""
        client = ICAClient()
        invalid_response = {
            "narrative_insights": [],
            "storytelling_analysis": {}
        }
        assert client._validate_response(invalid_response) is False
    
    def test_validate_response_missing_narrative_insights(self):
        """Test response validation with missing narrative insights."""
        client = ICAClient()
        invalid_response = {
            "recommendations": [],
            "storytelling_analysis": {}
        }
        assert client._validate_response(invalid_response) is False
    
    def test_validate_response_not_dict(self):
        """Test response validation with non-dict response."""
        client = ICAClient()
        # Test with non-dict types (intentionally wrong types for testing)
        assert client._validate_response([]) is False  # type: ignore
        assert client._validate_response("string") is False  # type: ignore
        assert client._validate_response(None) is False  # type: ignore


class TestAdvantageClient:
    """Test Advantage client with ICA and fallback."""
    
    async def test_analyze_briefing_with_ica_success(
        self,
        sample_briefing_payload,
        valid_ica_response
    ):
        """Test briefing analysis with successful ICA call."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key',
            'ENABLE_AGENT_FALLBACK': 'true'
        }):
            client = AdvantageClient()
            
            with patch.object(
                client.ica_client,
                'call_orchestration',
                AsyncMock(return_value=valid_ica_response)
            ):
                result = await client.analyze_briefing(
                    sample_briefing_payload
                )
                
                assert result is not None
                assert "recommendations" in result
                assert "narrative_insights" in result
                assert result.get("ica_enhanced") is True
                assert result.get("analysis_source") == "ica"
    
    async def test_analyze_briefing_fallback_on_ica_failure(
        self,
        sample_briefing_payload
    ):
        """Test briefing analysis falls back on ICA failure."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key',
            'ENABLE_AGENT_FALLBACK': 'true'
        }):
            client = AdvantageClient()
            
            with patch.object(
                client.ica_client,
                'call_orchestration',
                AsyncMock(return_value=None)
            ):
                result = await client.analyze_briefing(
                    sample_briefing_payload
                )
                
                assert result is not None
                assert "recommendations" in result
                assert "narrative_insights" in result
                # Should not have ICA metadata
                assert result.get("ica_enhanced") is not True
    
    async def test_analyze_url_with_ica_success(
        self,
        sample_url_payload,
        valid_ica_response
    ):
        """Test URL analysis with successful ICA call."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key',
            'ENABLE_AGENT_FALLBACK': 'true'
        }):
            client = AdvantageClient()
            
            with patch.object(
                client.ica_client,
                'call_orchestration',
                AsyncMock(return_value=valid_ica_response)
            ):
                result = await client.analyze_url(sample_url_payload)
                
                assert result is not None
                assert "recommendations" in result
                assert "narrative_insights" in result
                assert result.get("ica_enhanced") is True
    
    async def test_analyze_url_fallback_on_ica_failure(
        self,
        sample_url_payload
    ):
        """Test URL analysis falls back on ICA failure."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': 'https://test.api.com',
            'ADVANTAGE_API_KEY': 'test_key',
            'ENABLE_AGENT_FALLBACK': 'true'
        }):
            client = AdvantageClient()
            
            with patch.object(
                client.ica_client,
                'call_orchestration',
                AsyncMock(return_value=None)
            ):
                result = await client.analyze_url(sample_url_payload)
                
                assert result is not None
                assert "recommendations" in result
                assert "narrative_insights" in result
    
    async def test_fallback_disabled_raises_error(
        self,
        sample_briefing_payload
    ):
        """Test error when ICA fails and fallback is disabled."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': '',
            'ADVANTAGE_API_KEY': '',
            'ENABLE_AGENT_FALLBACK': 'false'
        }):
            client = AdvantageClient()
            
            with pytest.raises(RuntimeError):
                await client.analyze_briefing(sample_briefing_payload)


class TestAPIContractPreservation:
    """Test that API contract is preserved with ICA integration."""
    
    async def test_briefing_response_contract(self, sample_briefing_payload):
        """Test briefing response maintains expected contract."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': '',
            'ADVANTAGE_API_KEY': '',
            'ENABLE_AGENT_FALLBACK': 'true'
        }):
            client = AdvantageClient()
            result = await client.analyze_briefing(sample_briefing_payload)
            
            # Check required fields
            assert "analysis_id" in result
            assert "score" in result
            assert "score_breakdown" in result
            assert "page_summary" in result
            assert "recommendations" in result
            assert "module_plan" in result
            assert "narrative_insights" in result
            assert "storytelling_analysis" in result
            assert "catalog_context" in result
            assert "agent_trace" in result
            
            # Check types
            assert isinstance(result["score"], dict)
            assert "overall" in result["score"]
            assert isinstance(result["score"]["overall"], (int, float))
            assert isinstance(result["score_breakdown"], dict)
            assert isinstance(result["recommendations"], list)
            assert isinstance(result["narrative_insights"], list)
    
    async def test_url_response_contract(self, sample_url_payload):
        """Test URL response maintains expected contract."""
        with patch.dict('os.environ', {
            'ADVANTAGE_BASE_URL': '',
            'ADVANTAGE_API_KEY': '',
            'ENABLE_AGENT_FALLBACK': 'true'
        }):
            client = AdvantageClient()
            result = await client.analyze_url(sample_url_payload)
            
            # Check required fields
            assert "analysis_id" in result
            assert "score" in result
            assert "score_breakdown" in result
            assert "page_summary" in result
            assert "recommendations" in result
            assert "module_plan" in result
            assert "narrative_insights" in result
            assert "storytelling_analysis" in result
            assert "catalog_context" in result
            assert "agent_trace" in result
            assert "page_diagnostics" in result
            assert "detected_modules" in result
            
            # Check types
            assert isinstance(result["score"], dict)
            assert "overall" in result["score"]
            assert isinstance(result["score"]["overall"], (int, float))
            assert isinstance(result["score_breakdown"], dict)
            assert isinstance(result["recommendations"], list)
            assert isinstance(result["narrative_insights"], list)
            assert isinstance(result["detected_modules"], list)


class TestLocalAgentFallback:
    """Test local agent fallback functionality."""
    
    def test_local_agent_briefing_analysis(
        self,
        sample_briefing_payload
    ):
        """Test local agent can analyze briefing."""
        fallback = LocalAgentFallback()
        result = fallback.analyze_briefing(sample_briefing_payload)
        
        assert result is not None
        assert "recommendations" in result
        assert "narrative_insights" in result
        assert "storytelling_analysis" in result
    
    def test_local_agent_url_analysis(self, sample_url_payload):
        """Test local agent can analyze URL."""
        fallback = LocalAgentFallback()
        result = fallback.analyze_url(sample_url_payload)
        
        assert result is not None
        assert "recommendations" in result
        assert "narrative_insights" in result
        assert "storytelling_analysis" in result
        assert "page_diagnostics" in result


# Made with Bob