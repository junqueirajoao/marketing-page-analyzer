# Script de teste para a API do Financial Marketing Pages Analyzer

Write-Host "=== Testando API do Financial Marketing Pages Analyzer ===" -ForegroundColor Cyan
Write-Host ""

# Teste 1: Health Check
Write-Host "1. Testando Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "   OK: Health check passou" -ForegroundColor Green
} catch {
    Write-Host "   ERRO: Health check falhou" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Teste 2: Analise por Briefing
Write-Host "2. Testando /analyze/briefing..." -ForegroundColor Yellow

$briefingPayload = @{
    briefing = "Criar pagina de credito pessoal para MEI"
    business_goal = "gerar leads"
    target_audience = "microempreendedores"
    constraints = @("tom simples")
} | ConvertTo-Json

try {
    $briefingResponse = Invoke-RestMethod -Uri "http://localhost:8000/analyze/briefing" -Method Post -Body $briefingPayload -ContentType "application/json"
    Write-Host "   OK: Analise concluida" -ForegroundColor Green
    Write-Host "   - Score Geral: $($briefingResponse.score.overall)" -ForegroundColor Gray
    Write-Host "   - Score SEO: $($briefingResponse.score.seo)" -ForegroundColor Gray
} catch {
    Write-Host "   ERRO: Analise por briefing falhou" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Todos os testes passaram! ===" -ForegroundColor Green
Write-Host "O projeto esta funcionando corretamente!" -ForegroundColor Cyan

# Made with Bob
