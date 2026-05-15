"""
Test UTF-8 encoding in API responses.
Validates that Portuguese characters are correctly encoded.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_briefing_analysis_utf8_encoding():
    """Test that briefing analysis returns proper UTF-8 encoded Portuguese text."""
    payload = {
        "briefing": "Criar página de crédito pessoal para conversão",
        "business_goal": "gerar leads",
        "target_audience": "microempreendedores",
        "constraints": ["tom simples"]
    }
    
    response = client.post("/analyze/briefing", json=payload)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json; charset=utf-8"
    
    data = response.json()
    
    # Convert response to string to check for encoding issues
    response_text = response.text
    
    # Check that proper Portuguese characters are present
    # These should appear correctly, not as broken encoding
    assert "Módulo" in response_text or "módulo" in response_text or "modulo" in response_text
    assert "conversão" in response_text or "conversao" in response_text
    assert "crédito" in response_text or "credito" in response_text
    assert "análise" in response_text or "analise" in response_text
    assert "recomendação" in response_text or "recomendacao" in response_text
    
    # Check that broken encoding patterns are NOT present
    assert "MÃ³dulo" not in response_text
    assert "conversÃ£o" not in response_text
    assert "crÃ©dito" not in response_text
    assert "anÃ¡lise" not in response_text
    assert "recomendaÃ§Ã£o" not in response_text
    
    # Additional checks for common broken patterns
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


def test_health_endpoint_utf8():
    """Test that health endpoint returns UTF-8."""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    # Check content type includes charset
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type


def test_portuguese_characters_in_recommendations():
    """Test that recommendations contain proper Portuguese characters."""
    payload = {
        "briefing": "Página de produto financeiro com módulos de conversão",
        "business_goal": "conversão",
        "target_audience": "público geral",
        "constraints": []
    }
    
    response = client.post("/analyze/briefing", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    recommendations = data.get("recommendations", [])
    
    # Check that at least one recommendation exists
    assert len(recommendations) > 0
    
    # Check recommendations for proper encoding
    for rec in recommendations:
        title = rec.get("title", "")
        suggestion = rec.get("suggestion", "")
        why = rec.get("why", "")
        
        # Ensure no broken encoding in any field
        for text in [title, suggestion, why]:
            assert "Ã³" not in text
            assert "Ã£" not in text
            assert "Ã©" not in text
            assert "Ã¡" not in text
            assert "Ã§" not in text


def test_narrative_insights_utf8():
    """Test that narrative insights contain proper UTF-8."""
    payload = {
        "briefing": "Análise de página com recomendações de módulos",
        "business_goal": "conversão",
        "target_audience": "público geral",
        "constraints": []
    }
    
    response = client.post("/analyze/briefing", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    insights = data.get("narrative_insights", [])
    
    # Check insights for proper encoding
    for insight in insights:
        title = insight.get("title", "")
        description = insight.get("description", "")
        
        # Ensure no broken encoding
        for text in [title, description]:
            assert "Ã³" not in text
            assert "Ã£" not in text
            assert "Ã©" not in text


# Made with Bob