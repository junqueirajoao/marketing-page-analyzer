"""
Script de teste rápido para validar a API
"""
import requests  # pylint: disable=import-error
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Testa o endpoint de health"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_analyze_url():
    """Testa análise por URL - AI-First (apenas URL obrigatória)"""
    # Payload mínimo - sistema infere automaticamente contexto
    payload = {
        "url": "https://www.example.com"
    }
    
    print("\n=== Testando /analyze/url (AI-First) ===")
    print("Sistema infere automaticamente: tipo, objetivo, público-alvo")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/analyze/url",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score geral: {result.get('score', {}).get('overall', 'N/A')}")
        print(f"Análise ID: {result.get('analysis_id', 'N/A')}")
        print("✓ Endpoint funcionando!")
        return True
    else:
        print(f"Erro: {response.text}")
        return False


def test_analyze_briefing():
    """Testa análise por briefing - AI-First (apenas briefing obrigatório)"""
    # Payload mínimo - sistema infere automaticamente contexto
    payload = {
        "briefing": "Criar página de crédito pessoal para MEI",
        "constraints": ["tom simples", "evitar promessas absolutas"]
    }
    
    print("\n=== Testando /analyze/briefing (AI-First) ===")
    print("Sistema infere automaticamente: tipo, objetivo, público-alvo")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/analyze/briefing",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score geral: {result.get('score', {}).get('overall', 'N/A')}")
        print(f"Análise ID: {result.get('analysis_id', 'N/A')}")
        print("✓ Endpoint funcionando!")
        return True
    else:
        print(f"Erro: {response.text}")
        return False


if __name__ == "__main__":
    print("=== Testando API do Financial Marketing Pages Analyzer ===\n")
    
    # Testa health
    if not test_health():
        print("❌ Health check falhou!")
        exit(1)
    
    # Testa analyze/briefing
    if not test_analyze_briefing():
        print("❌ Análise por briefing falhou!")
        exit(1)
    
    # Testa analyze/url (pode demorar mais)
    if not test_analyze_url():
        print("❌ Análise por URL falhou!")
        exit(1)
    
    print("\n✅ Todos os testes passaram!")
    print("O projeto está integrado e funcionando corretamente!")

# Made with Bob
