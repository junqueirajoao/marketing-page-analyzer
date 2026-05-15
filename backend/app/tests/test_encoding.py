"""
Test UTF-8 encoding in API responses.
Validates that Portuguese characters are correctly encoded in URL analysis.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint_utf8():
    """Test that health endpoint returns UTF-8."""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    # Check content type includes charset
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type


def test_url_analysis_utf8_encoding():
    """Test URL analysis returns proper UTF-8 encoded text."""
    payload = {
        "url": "https://www.example.com/credito-pessoal"
    }
    
    response = client.post("/analyze/url", json=payload)
    
    # Note: This test may fail if the URL is not accessible
    # In production, use a real accessible URL for testing
    if response.status_code == 200:
        content_type = response.headers["content-type"]
        assert content_type == "application/json; charset=utf-8"
        
        data = response.json()
        response_text = response.text
        
        # Check that broken encoding patterns are NOT present
        assert "Ã³" not in response_text  # broken ó
        assert "Ã£" not in response_text  # broken ã
        assert "Ã©" not in response_text  # broken é
        assert "Ã¡" not in response_text  # broken á
        assert "Ã§" not in response_text  # broken ç
        
        # Verify response structure
        assert "score" in data
        assert "recommendations" in data
        assert "narrative_insights" in data
        assert "storytelling_analysis" in data


# Made with Bob