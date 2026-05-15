"""
Manual test to verify UTF-8 encoding in API responses.
Run this with: python test_encoding_manual.py
"""
import requests
import json

# Test the API
url = "http://localhost:8000/analyze/briefing"
payload = {
    "briefing": "Criar página de crédito pessoal para conversão",
    "business_goal": "gerar leads",
    "target_audience": "microempreendedores",
    "constraints": ["tom simples"]
}

print("Sending request to API...")
response = requests.post(url, json=payload)

print(f"\nStatus Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"Encoding: {response.encoding}")

# Get response as text
response_text = response.text

# Check for proper Portuguese characters
print("\n=== Checking for CORRECT Portuguese characters ===")
correct_chars = ["módulo", "conversão", "crédito", "análise", "recomendação"]
for char in correct_chars:
    if char in response_text.lower():
        print(f"✓ Found: {char}")
    else:
        print(f"✗ NOT found: {char}")

# Check for broken encoding patterns
print("\n=== Checking for BROKEN encoding patterns ===")
broken_patterns = ["Ã³", "Ã£", "Ã©", "Ã¡", "Ã§", "MÃ³dulo", "conversÃ£o", "crÃ©dito"]
found_broken = False
for pattern in broken_patterns:
    if pattern in response_text:
        print(f"✗ FOUND BROKEN: {pattern}")
        found_broken = True

if not found_broken:
    print("✓ No broken encoding patterns found!")

# Parse JSON and check a few fields
print("\n=== Sample response fields ===")
data = response.json()
if "score_breakdown" in data and "seo" in data["score_breakdown"]:
    for item in data["score_breakdown"]["seo"][:2]:
        print(f"Reason: {item.get('reason', 'N/A')}")

print("\n=== Test Complete ===")

# Made with Bob
