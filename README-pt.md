# Financial Marketing Pages Analyzer

Aplicação web com IA para análise e recomendação de melhorias em páginas de marketing financeiro.

## Visão geral

O Financial Marketing Pages Analyzer ajuda times de Marketing Digital, UX, Conteúdo e canais digitais a avaliarem páginas de marketing financeiro de forma mais rápida, consistente e com resultados mais acionáveis. A solução analisa **URLs de páginas reais**, fazendo scraping do conteúdo, detectando módulos, avaliando storytelling, verificando SEO e analisando conformidade de marca para entregar recomendações abrangentes e acionáveis.

O projeto foi desenvolvido para um hackathon utilizando duas ferramentas principais:

- **IBM Consulting Advantage**: camada de agentes especializados para análise, raciocínio e recomendações.
- **IBM Bob**: suporte ao desenvolvimento no VS Code para acelerar implementação, testes, documentação e refatoração.

## Problema

Revisar páginas de marketing geralmente requer várias análises manuais simultâneas:

- SEO técnico e semântico.
- Clareza da proposta de valor.
- Estrutura modular da página.
- Storytelling e progressão narrativa.
- Qualidade dos CTAs.
- Tom de marca.
- Riscos de linguagem em contexto financeiro.

Esse processo pode ser lento, inconsistente e dependente de múltiplos especialistas. Este projeto propõe um assistente multiagente que consolida essas análises e entrega um plano de melhoria priorizado.

## Solução

O sistema recebe uma **URL de página** e gera um relatório abrangente com:

- Score geral da página.
- Score por dimensão: SEO, storytelling, módulos e segurança de marca.
- Módulos detectados e estrutura.
- Diagnóstico executivo.
- Top prioridades.
- Sugestões de palavras-chave.
- Recomendações de módulos para manter, remover, mover ou adicionar.
- Nova estrutura narrativa sugerida.
- Análise de storytelling.
- Checklist para o time de Marketing.

## Arquitetura

```text
Usuário
  |
  | URL da Página
  v
Frontend Web (React + Vite)
  |
  v
Backend FastAPI
  |
  | Scraping + Parsing + Detecção de Módulos
  v
Serviço de Scoring
  |
  | Score SEO + Score Storytelling + Score Módulos + Score Brand Safety
  v
Catalog Context Builder
  |
  | Injeta relevant_seo_rules, relevant_brand_rules,
  | relevant_storytelling_patterns, relevant_modules
  v
Orquestração IBM Consulting Advantage (ICA)
  |
  | Page Strategy Orchestrator
  | ├── SEO Agent
  | ├── Module Strategy Agent
  | ├── Storytelling Agent
  | └── Brand and Compliance Agent
  v
Recommendation Agent
  |
  | Consolida achados em recomendações acionáveis
  v
Resposta Estruturada
  |
  | score, score_breakdown, recommendations, module_plan,
  | narrative_insights, storytelling_analysis, detected_modules,
  | page_diagnostics, catalog_context
  v
Dashboard com componentes visuais
```

**Componentes-Chave:**

- **Catalog Context Builder**: Injeta conhecimento especializado de domínio dos catálogos locais nos agentes ICA sem necessidade de configuração de Knowledge Base/embedding
- **Orquestração ICA**: Sistema multiagente com padrão supervisor coordenando agentes especializados
- **Fallback Local**: Fallback automático para processamento local se ICA não estiver disponível
- **Scoring Data-Driven**: Scoring transparente e auditável baseado em regras dos catálogos

## Agentes

O sistema utiliza IBM Consulting Advantage (ICA) com os seguintes agentes especializados:

### Page Strategy Orchestrator

Coordena a análise multiagente, identifica o tipo da página, consolida achados dos agentes especializados e garante recomendações coerentes.

### SEO Agent

Avalia title, meta description, H1, hierarquia de headings, intenção de busca, palavras-chave, links internos e oportunidades de SEO on-page usando `relevant_seo_rules` do contexto de catálogo.

### Module Strategy Agent

Analisa a composição da página em módulos, recomendando o que manter, remover, reordenar ou adicionar com base em `relevant_modules` e padrões de storytelling do contexto de catálogo.

### Storytelling Agent

Avalia a progressão narrativa (gancho, contexto, solução, benefícios, prova, CTA) usando `relevant_storytelling_patterns` para garantir que a página siga uma estrutura narrativa apropriada para seu tipo e objetivo.

### Brand and Compliance Agent

Verifica clareza, tom institucional, compliance financeiro (YMYL) e segurança de linguagem usando `relevant_brand_rules`. Sinaliza riscos como promessas absolutas, linguagem agressiva, urgência artificial e falta de disclaimers (CET, análise de crédito).

### Recommendation Agent

Consolida achados de todos os agentes em um plano de ação priorizado com classificação de impacto/esforço, resumo executivo, quick wins e checklist de implementação.

## Stack técnica

### Frontend

- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- shadcn/ui.
- Recharts.
- Lucide React.

### Backend

- Python 3.11+.
- FastAPI.
- Uvicorn.
- Pydantic.
- HTTPX.
- BeautifulSoup.
- Trafilatura.
- Readability.
- python-dotenv.
- Pytest.

### Opcional

- Playwright para páginas renderizadas por JavaScript.
- ChromaDB ou FAISS para RAG.
- SQLite para histórico de análises.
- Exportação em Markdown ou PDF.

## Estrutura de pastas

```text
marketing-page-analyzer/
  README.md
  README-pt.md
  .gitignore

  docs/
    guia-tecnico-hackathon.md

  backend/
    .env
    requirements.txt
    ICA_INTEGRATION.md
    RUNNING.md
    run_server.ps1
    run_server.sh
    test_api.ps1
    test_api.py
    app/
      main.py
      __init__.py
      routes/
        analyze.py
        health.py
        __init__.py
      schemas/
        input.py
        __init__.py
      services/
        scraper.py
        page_normalizer.py
        module_detector.py
        scoring_service.py
        storytelling_pattern_service.py
        catalog_loader.py
        catalog_context_builder.py
        ica_client.py
        advantage_client.py
        local_agent_fallback.py
        report_builder.py
        __init__.py
      data/
        modules_catalog.json
        storytelling_patterns.json
        brand_rules.json
        seo_rules.json
      tests/
        test_catalog_context_builder.py
        test_encoding.py
        test_ica_integration.py
        test_scoring.py
        test_storytelling_integration.py
      utils/
        analysis_messages.py
        __init__.py

  frontend/
    package.json
    vite.config.ts
    README.md
    SETUP.md
    src/
      main.tsx
      App.tsx
      index.css
      lib/
        api.ts
      components/
        UrlAnalyzerForm.tsx
        BriefingAnalyzerForm.tsx
        AnalysisResult.tsx
        JsonResult.tsx
        ModuleMap.tsx
        ScoreBreakdown.tsx
        NarrativeInsights.tsx
        CollapsibleSection.tsx
```

## Setup do backend

Entre na pasta do backend:

```bash
cd backend
```

Crie o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install fastapi uvicorn pydantic pydantic-settings httpx beautifulsoup4 trafilatura readability-lxml lxml python-dotenv pytest
```

Ou use:

```bash
pip install -r requirements.txt
```

Rode a API:

```bash
uvicorn app.main:app --reload --port 8000
```

Teste:

```bash
curl http://localhost:8000/health
```

## Setup do frontend

Entre na pasta do frontend:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Rode o projeto:

```bash
npm run dev
```

## Variáveis de ambiente

Crie um arquivo `.env` no backend baseado no `.env.example`:

```env
APP_NAME=marketing-page-analyzer
ENVIRONMENT=development
ADVANTAGE_BASE_URL=https://example.ibm-advantage-api.com
ADVANTAGE_API_KEY=replace-me
ADVANTAGE_ORCHESTRATOR_ID=replace-me
ENABLE_AGENT_FALLBACK=true
```

## Endpoints

### `GET /health`

Verifica se a API está ativa.

Resposta:

```json
{
  "status": "ok"
}
```

### `POST /analyze/url`

Analisa uma página a partir de uma URL.

**Arquitetura AI-First**: O sistema infere automaticamente contexto, detecta padrões narrativos, identifica intenção, classifica tipo de página, identifica público provável, seleciona padrões de storytelling e constrói catalog_context baseado em URL, conteúdo extraído, módulos detectados, análise de storytelling, score breakdown e narrative insights.

Entrada (todos os campos opcionais exceto `url`):

```json
{
  "url": "https://www.exemplo.com.br/pagina"
}
```

## Exemplo de resposta

```json
{
  "analysis_id": "analysis_20260515_120000",
  "score": {
    "overall": 82,
    "seo": 78,
    "storytelling": 85,
    "modules": 80,
    "brand_safety": 90
  },
  "score_breakdown": {
    "seo": {
      "score": 78,
      "issues": [
        {
          "rule_id": "seo_rule_001",
          "severity": "high",
          "description": "Title tag ausente ou muito genérico"
        }
      ]
    },
    "storytelling": {
      "score": 85,
      "pattern_match": "conversion_funnel",
      "missing_elements": ["social_proof"]
    },
    "modules": {
      "score": 80,
      "detected_count": 8,
      "recommended_count": 10
    },
    "brand_safety": {
      "score": 90,
      "risks": []
    }
  },
  "page_summary": {
    "detected_type": "product",
    "primary_goal": "conversion",
    "main_topic": "financial solution"
  },
  "recommendations": [
    {
      "priority": "high",
      "area": "SEO",
      "title": "Reescrever meta description",
      "why": "A descrição atual não comunica benefício nem intenção de busca.",
      "suggestion": "Use uma descrição com benefício claro, palavra-chave principal e CTA suave.",
      "impact": "high",
      "effort": "low"
    }
  ],
  "module_plan": {
    "keep": ["hero", "benefits", "cta_primary"],
    "remove": ["generic_text"],
    "reorder": [
      {"module": "social_proof", "from": 8, "to": 4}
    ],
    "add": ["faq", "trust_badges"]
  },
  "narrative_insights": [
    {
      "insight": "Página não apresenta problema claro antes de apresentar solução",
      "impact": "medium",
      "recommendation": "Adicionar módulo de contexto explicando dores do cliente"
    }
  ],
  "storytelling_analysis": {
    "pattern_used": "conversion_funnel",
    "pattern_strength": "medium",
    "narrative_flow_score": 75,
    "missing_steps": ["objection_handling"]
  },
  "catalog_context": {
    "relevant_modules": ["hero", "benefits", "faq", "cta_primary"],
    "relevant_storytelling_patterns": ["conversion_funnel"],
    "relevant_seo_rules": ["seo_rule_001", "seo_rule_002"],
    "relevant_brand_rules": ["brand_rule_001"]
  },
  "ica_enhanced": true,
  "analysis_source": "ica"
}
```

## Catálogos locais

O projeto usa catálogos JSON para fornecer conhecimento especializado de domínio aos agentes ICA através do mecanismo de **catalog_context**, eliminando a necessidade de configuração de Knowledge Base ou embedding na fase de MVP.

### `modules_catalog.json`

Define mais de 50 tipos de módulos com metadados detalhados:
- ID do módulo, nome, nome de exibição, tipo genérico
- Propósito, descrição, sinônimos
- Dicas de detecção, conteúdo comum, elementos de UI
- Cenários bons/ruins para uso
- Regras de recomendação (keepWhen, removeWhen, improveWhen)

Exemplos: hero, benefits, FAQ, social proof, simulator, CTA, trust badges, educational content, comparison tables, testimonials.

### `storytelling_patterns.json`

Define padrões narrativos por tipo de página com:
- Tipo de página, segmento, objetivo de negócio, público-alvo
- Nome e descrição do storytelling
- Estágios da jornada emocional
- Passos narrativos com módulos recomendados
- Módulos obrigatórios/opcionais/a evitar
- Ordem recomendada de módulos
- Diretrizes de tom, diretrizes de compliance
- Exemplos de CTA, padrões de copy a evitar
- Regras de avaliação para agentes

Exemplos: conversion funnel, educational journey, campaign landing, institutional positioning.

### `seo_rules.json`

Define regras de SEO com:
- ID da regra, categoria, severidade
- Descrição, applies_to (tipos de página)
- Verificações (campo, comprimento mín/máx, requisitos)
- Exemplos ruins/bons
- Ação recomendada
- Impacto no score (missing, too_short, too_long, generic)
- Orientação para agentes

Categorias: metadata, headings, content, links, technical.

### `brand_rules.json`

Define regras de marca e compliance com:
- ID da regra, categoria, subcategoria, severidade
- Descrição, applies_to (tipos de página)
- Exemplos ruins, alternativas seguras
- Palavras-chave de detecção
- Ação recomendada, módulos recomendados
- Orientação para agentes

Categorias: compliance (promessas financeiras, YMYL, disclaimers), tom (institucional, clareza), segurança de linguagem (agressivo, urgência, afirmações absolutas).

### Como funciona o catalog_context

O serviço **Catalog Context Builder**:
1. Analisa a página
2. Seleciona os itens mais relevantes de cada catálogo (máximo 8 por catálogo)
3. Compacta-os para campos essenciais
4. Injeta-os no payload ICA como `catalog_context`
5. Agentes ICA usam este contexto como fonte de conhecimento de domínio

Esta abordagem fornece:
- **Conhecimento especializado** sem necessidade de configuração de Knowledge Base
- **Raciocínio transparente** - agentes citam regras/padrões específicos
- **Recomendações auditáveis** - rastreáveis até entradas do catálogo
- **Manutenção fácil** - atualizar catálogos sem retreinamento

## Fallback local

Para evitar bloqueios durante a demo, o backend possui um fallback local caso a integração com IBM Consulting Advantage não esteja configurada.

Exemplo:

```python
class LocalAgentFallback:
    async def analyze_page(self, payload: dict) -> dict:
        return {
            "scores": {
                "overall": 78,
                "seo": 72,
                "storytelling": 81,
                "modules": 76,
                "brand_safety": 88
            },
            "executive_summary": "Análise simulada para fallback de demo.",
            "top_priorities": [
                {
                    "area": "SEO",
                    "impact": "high",
                    "effort": "low",
                    "title": "Melhorar title e meta description"
                }
            ]
        }
```

## Backlog

### P0

- Criar backend FastAPI.
- Criar endpoint `/health`.
- Criar endpoint `/analyze/url` para análise baseada em URL.
- Implementar scraper e parser de página.
- Implementar normalizador de página.
- Implementar detector de módulos.
- Criar catálogos JSON (módulos, padrões de storytelling, regras de marca, regras de SEO).
- Criar cliente para IBM Consulting Advantage.
- Criar fallback local.
- Criar frontend com formulário de URL.
- Criar tela de resultado.
- Criar cards de score.
- Criar lista de recomendações.
- Criar visualização de módulos.
- Criar prompts dos agentes.
- Criar roteiro de demo.

### P1

- Adicionar Playwright para páginas JavaScript.
- Adicionar upload de mockup.
- Adicionar histórico de análises.
- Adicionar exportação em Markdown.
- Adicionar testes unitários.
- Adicionar estados de loading e tratamento de erros.

### P2

- Adicionar RAG com páginas aprovadas.
- Adicionar benchmarking com concorrentes.
- Adicionar comparação antes/depois.
- Adicionar geração de wireframe sugerido.
- Adicionar priorização visual por impacto e esforço.

## Prompts para IBM Bob

### Backend

```text
Crie um backend FastAPI para uma aplicação chamada Marketing Page Analyzer.

Requisitos:
- Endpoint GET /health.
- Endpoint POST /analyze/url para análise de página baseada em URL.
- Usar Pydantic para validação.
- Separar routes, schemas e services.
- Criar services para scraping, parsing, detecção de módulos e cliente do IBM Consulting Advantage.
- Criar fallback local para demo caso a chamada ao IBM Consulting Advantage não esteja configurada.
- Manter o código simples, testável e bem organizado.
```

### Scraper

```text
Implemente um service scraper.py em Python.

Requisitos:
- Receber uma URL.
- Baixar HTML com httpx.
- Extrair title, meta description, canonical, headings H1 a H3, links, imagens e texto principal.
- Usar BeautifulSoup e trafilatura quando apropriado.
- Retornar um dicionário estruturado.
- Tratar erros de timeout, URLs inválidas e HTML vazio.
```

### Frontend

```text
Crie uma interface React com TypeScript para o Marketing Page Analyzer.

Requisitos:
- Interface simples e focada para análise de página baseada em URL.
- Campo de entrada de URL (obrigatório).
- Botão para iniciar análise.
- Tela de resultado com score geral, scores por área, módulos detectados, resumo executivo, top prioridades, mapa de módulos e recomendações.
- Usar Tailwind CSS.
- Componentes reutilizáveis.
- Criar arquivo lib/api.ts para chamadas ao backend.
- Enfatizar análise automática com IA nas mensagens da UI.
```

### Testes

```text
Crie testes unitários com pytest para os services:
- module_detector.py.
- page_normalizer.py.
- scoring_service.py.

Cenários:
- Página sem title.
- Página sem meta description.
- Página com múltiplos H1s.
- Página com headings fora de ordem.
- Página com módulos vazios.
- Análise de URL com conteúdo real de página.
```

## Integração IBM Consulting Advantage (ICA)

O sistema utiliza **IBM Consulting Advantage** para orquestração multiagente com fallback automático para processamento local.

### Recursos Principais

- **Injeção de Catalog Context**: Backend injeta `catalog_context` com regras, padrões e módulos relevantes no payload ICA
- **Sem Necessidade de Knowledge Base**: Catalog context fornece conhecimento especializado de domínio sem configuração de KB/embedding
- **Fallback Automático**: Se ICA não estiver disponível, sistema usa fallback de agente local
- **Scoring Transparente**: Scoring data-driven baseado em regras de catálogo com explicabilidade completa
- **Rastreabilidade de Agentes**: Cada recomendação cita regras/padrões específicos do catálogo

### Configuração

Configure as variáveis de ambiente em `backend/.env`:

```env
ADVANTAGE_BASE_URL=https://api.ibm.com/consulting-advantage
ADVANTAGE_API_KEY=your_api_key_here
ADVANTAGE_ORCHESTRATOR_ID=d5d0c63a-4a42-4431-b870-3f496a43fe10
ENABLE_AGENT_FALLBACK=true
```

### Instruções para Agentes

Os agentes ICA recebem instruções para:
- Usar `catalog_context` como fonte de conhecimento de domínio
- Não inventar regras, módulos ou padrões fora do contexto fornecido
- Basear recomendações em `relevant_modules`, `relevant_storytelling_patterns`, `relevant_seo_rules` e `relevant_brand_rules`
- Citar IDs específicos de regras e padrões nas recomendações
- Fornecer explicabilidade para todos os scores e recomendações

Para documentação detalhada da integração, consulte `backend/ICA_INTEGRATION.md`.

## Roteiro de demo

### Abertura

"O problema que queremos resolver é que otimizar páginas de marketing requer olhar SEO, conteúdo, UX, storytelling, marca e segurança de linguagem ao mesmo tempo. Esse processo normalmente é manual, demorado e pouco padronizado."

### Fluxo

1. Abrir o app.
2. Colar uma URL pública de página de marketing.
3. Rodar a análise.
4. Sistema faz scraping e parsing da página.
5. Sistema detecta módulos e estrutura.
6. Mostrar o score geral.
7. Mostrar módulos detectados.
8. Mostrar oportunidades de SEO.
9. Mostrar o plano de módulos.
10. Mostrar o storytelling recomendado.
11. Mostrar narrative insights.
12. Mostrar top prioridades.

### Fechamento

"A solução usa IBM Consulting Advantage para orquestrar agentes especialistas e IBM Bob para acelerar o desenvolvimento de software. O resultado é uma análise padronizada, explicável e acionável para times de Marketing Digital baseada em conteúdo real de página."

## Critérios de aceite

- O usuário consegue analisar uma URL.
- O sistema faz scraping e parsing de conteúdo real de página.
- O sistema detecta módulos automaticamente.
- A API retorna JSON estruturado.
- O dashboard exibe o score geral e scores por área.
- A solução retorna pelo menos cinco recomendações priorizadas.
- As recomendações indicam impacto e esforço.
- O sistema funciona mesmo com o fallback local.
- O README permite rodar o projeto localmente.

## Roadmap sugerido

### Fase 1

- Backend.
- Frontend.
- Scraper.
- Normalização.
- Fallback.
- Dashboard básico.

### Fase 2

- Integração com IBM Consulting Advantage.
- Agentes especializados.
- Catálogos de módulos e storytelling.
- Melhorias de UI.



## Observações

Este projeto não substitui revisão humana de marca, jurídico ou compliance. Ele atua como acelerador de diagnóstico e priorização, ajudando times a encontrarem oportunidades de melhoria com mais velocidade e consistência.
