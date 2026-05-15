# Como Executar o Backend - Financial Marketing Pages Analyzer

## Visão Geral

Este guia descreve como executar o backend do **Financial Marketing Pages Analyzer** com integração IBM Consulting Advantage (ICA) e fallback local.

## Pré-requisitos

- Python 3.11+
- pip
- Ambiente virtual Python

## Setup Inicial

### 1. Criar Ambiente Virtual

```bash
cd backend
python -m venv .venv
```

### 2. Ativar Ambiente Virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` no diretório `backend/`:

```env
# IBM Consulting Advantage Configuration
ADVANTAGE_BASE_URL=https://api.ibm.com/consulting-advantage
ADVANTAGE_API_KEY=your_api_key_here
ADVANTAGE_ORCHESTRATOR_ID=d5d0c63a-4a42-4431-b870-3f496a43fe10
ENABLE_AGENT_FALLBACK=true

# Application Settings
APP_NAME=Financial Marketing Pages Analyzer
ENVIRONMENT=development
DEBUG=false
LOG_LEVEL=INFO
```

**Nota:** Se você não tiver credenciais ICA, o sistema usará automaticamente o fallback local.

## Executar o Backend

### Opção 1: Scripts Automatizados

**Windows (PowerShell):**
```powershell
cd backend
.\run_server.ps1
```

**Linux/Mac:**
```bash
cd backend
chmod +x run_server.sh
./run_server.sh
```

### Opção 2: Comando Manual

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Opção 3: Porta Padrão (8000)

```bash
cd backend
uvicorn app.main:app --reload
```

## Verificação

### 1. Health Check

Acesse: http://localhost:8001/health

Resposta esperada:
```json
{
  "status": "ok"
}
```

### 2. API Documentation

Acesse: http://localhost:8001/docs

Você verá a documentação interativa Swagger UI com todos os endpoints disponíveis.

### 3. Testar Análise

Use o script de teste:

**Windows:**
```powershell
.\test_api.ps1
```

**Python:**
```bash
python test_api.py
```

## Portas Utilizadas

- **Backend API**: 8001 (configurável)
- **Frontend**: 3000 (Vite configurado)

## CORS Configuration

O backend aceita requisições de:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:5173` (porta padrão Vite)
- `http://127.0.0.1:5173`

## Arquitetura do Backend

```
Backend FastAPI
├── Scraping & Normalization
├── Module Detection
├── Scoring Service (data-driven)
├── Storytelling Pattern Service
├── Catalog Context Builder
├── ICA Client (with fallback)
└── Report Builder
```

## Troubleshooting

### Porta 8001 já em uso

**Windows:**
```powershell
# Encontrar processo
netstat -ano | findstr :8001
# Matar processo (substitua <PID>)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8001 | xargs kill -9
```

### Virtual Environment não encontrado

```bash
python -m venv .venv
# Ativar e instalar dependências
pip install -r requirements.txt
```

### Erro de CORS

Verifique se:
1. Frontend está rodando em porta permitida (3000 ou 5173)
2. CORS está configurado em `app/main.py`

### ICA não responde

O sistema automaticamente usa fallback local. Verifique logs:
```
[ICA] Timeout after 30s, using fallback
[FALLBACK] Using LocalAgentFallback
```

### Erro de encoding UTF-8

O sistema está configurado para UTF-8. Se houver problemas:
1. Verifique `test_encoding.py`
2. Confirme que arquivos JSON estão em UTF-8
3. Verifique configuração do terminal

### Catálogos não carregam

Verifique se os arquivos existem:
- `app/data/modules_catalog.json`
- `app/data/storytelling_patterns.json`
- `app/data/seo_rules.json`
- `app/data/brand_rules.json`

## Testes

### Executar Todos os Testes

```bash
cd backend
python -m pytest -v
```

### Executar Testes Específicos

```bash
# Testes de ICA
python -m pytest app/tests/test_ica_integration.py -v

# Testes de Scoring
python -m pytest app/tests/test_scoring.py -v

# Testes de Catalog Context
python -m pytest app/tests/test_catalog_context_builder.py -v
```

## Logs

O sistema gera logs detalhados:

```
[ICA] Calling orchestration d5d0c63a-4a42-4431-b870-3f496a43fe10
[ICA] Response received successfully
[CATALOG_CONTEXT] Building context for page_type=product
[CATALOG_CONTEXT] Selected 8 modules, 3 patterns, 8 SEO rules, 8 brand rules
[ADVANTAGE] Using ICA response
```

## Próximos Passos

1. Configure credenciais ICA em `.env`
2. Execute o frontend: `cd frontend && npm run dev`
3. Teste análise completa via interface
4. Consulte `ICA_INTEGRATION.md` para detalhes da integração

## Suporte

Para problemas ou dúvidas:
1. Verifique logs do backend
2. Consulte `ICA_INTEGRATION.md`
3. Execute testes: `pytest -v`
4. Verifique documentação API: http://localhost:8001/docs