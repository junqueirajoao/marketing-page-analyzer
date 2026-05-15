# Financial Marketing Pages Analyzer

Aplicação web multiagente para análise e recomendação de melhorias em páginas de marketing financeiro.

## Visão geral

O Financial Marketing Pages Analyzer ajuda times de Marketing Digital, UX, Conteúdo e canais digitais a avaliarem páginas de marketing financeiro de forma mais rápida, padronizada e acionável. A solução analisa URLs, briefings em linguagem natural e, em uma evolução futura, mockups, retornando recomendações sobre SEO, estrutura modular, narrativa, clareza de conteúdo e segurança de marca.

O projeto foi pensado para um hackathon com duas ferramentas principais:

- **IBM Consulting Advantage**: camada de agentes especializados para análise, raciocínio e recomendações.
- **IBM Bob**: apoio ao desenvolvimento no VS Code para acelerar implementação, testes, documentação e refatoração.

## Problema

Revisar páginas de marketing costuma exigir várias análises manuais ao mesmo tempo:

- SEO técnico e semântico.
- Clareza da proposta de valor.
- Estrutura dos módulos da página.
- Storytelling e progressão narrativa.
- Qualidade dos CTAs.
- Tom de marca.
- Riscos de linguagem em contexto financeiro.

Esse processo pode ser demorado, inconsistente e dependente de múltiplos especialistas. A proposta deste projeto é criar um assistente multiagente que consolida essas análises e entrega um plano de melhoria priorizado.

## Solução

O sistema recebe uma URL ou briefing e gera um relatório com:

- Score geral da página.
- Score por dimensão: SEO, storytelling, módulos e segurança de marca.
- Diagnóstico executivo.
- Top prioridades.
- Sugestões de palavras-chave.
- Recomendações de módulos para manter, remover, mover ou adicionar.
- Nova estrutura narrativa sugerida.
- Sugestões de copy antes/depois.
- Checklist para o time de Marketing.

## Arquitetura

```text
Usuário
  |
  | URL ou briefing
  v
Frontend Web
  |
  v
Backend FastAPI
  |
  | scraping, extração e normalização
  v
Page Intelligence Layer
  |
  | payload estruturado
  v
IBM Consulting Advantage
  |
  | Orchestrator Agent
  | SEO Agent
  | Module Strategy Agent
  | Storytelling Agent
  | Brand Safety Agent
  | Recommendation Agent
  v
Resultado consolidado
  |
  v
Dashboard e relatório de recomendações
```

## Agentes

### Orchestrator Agent

Coordena a análise, identifica o tipo da página e consolida os resultados dos demais agentes.

### SEO Agent

Avalia title, meta description, H1, headings, intenção de busca, palavras-chave e oportunidades de melhoria on-page.

### Module Strategy Agent

Analisa a composição da página em módulos, recomendando o que manter, remover, mover, reescrever ou adicionar.

### Storytelling Agent

Avalia se a página segue uma narrativa adequada ao objetivo, como conversão, educação, campanha ou posicionamento institucional.

### Brand Safety Agent

Verifica clareza, tom, linguagem sensível e possíveis riscos de promessas fortes demais em contexto financeiro.

### Recommendation Agent

Transforma os achados dos demais agentes em um plano de ação priorizado por impacto e esforço.

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
  .env.example

  docs/
    architecture.md
    agent-prompts.md
    demo-script.md
    backlog.md

  backend/
    requirements.txt
    app/
      main.py
      config.py
      routes/
        analyze.py
        health.py
      schemas/
        input.py
        output.py
        page.py
      services/
        scraper.py
        page_normalizer.py
        module_detector.py
        seo_static_analyzer.py
        advantage_client.py
        report_builder.py
      data/
        modules_catalog.json
        storytelling_patterns.json
        brand_rules.json
        keyword_topics.json
      tests/
        test_seo_static_analyzer.py
        test_module_detector.py
        test_page_normalizer.py

  frontend/
    package.json
    vite.config.ts
    src/
      main.tsx
      App.tsx
      lib/
        api.ts
        types.ts
      pages/
        Home.tsx
        AnalysisResult.tsx
      components/
        UrlAnalyzerForm.tsx
        BriefingAnalyzerForm.tsx
        ScoreCard.tsx
        RecommendationList.tsx
        ModuleMap.tsx
        StorytellingTimeline.tsx
        SeoPanel.tsx
        CopySuggestions.tsx
        PriorityMatrix.tsx
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

Crie um arquivo `.env` no backend a partir do `.env.example`:

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

Entrada:

```json
{
  "url": "https://www.exemplo.com.br/pagina",
  "business_goal": "conversao",
  "target_audience": "pessoa física interessada em produto financeiro",
  "page_type_hint": "produto"
}
```

### `POST /analyze/briefing`

Analisa uma página planejada a partir de um briefing.

Entrada:

```json
{
  "briefing": "Criar uma página para divulgar uma solução financeira para pequenos negócios.",
  "business_goal": "gerar leads",
  "target_audience": "microempreendedores e pequenas empresas",
  "constraints": ["tom simples", "evitar promessas absolutas"]
}
```

## Exemplo de resposta

```json
{
  "analysis_id": "ana_123",
  "score": {
    "overall": 82,
    "seo": 78,
    "storytelling": 85,
    "modules": 80,
    "brand_safety": 90
  },
  "page_summary": {
    "detected_type": "produto",
    "primary_goal": "conversao",
    "main_topic": "solução financeira"
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
    "keep": [],
    "remove": [],
    "reorder": [],
    "add": []
  },
  "copy_suggestions": []
}
```

## Catálogos locais

O projeto usa catálogos JSON para reduzir recomendações genéricas e dar contexto aos agentes.

### `modules_catalog.json`

Define tipos de módulos, como hero, benefícios, FAQ, prova social, simulador, CTA e conteúdo educativo.

### `storytelling_patterns.json`

Define padrões narrativos por tipo de página, como produto, campanha, educação financeira e institucional.

### `brand_rules.json`

Define regras de tom e segurança de linguagem, como evitar promessas absolutas e simplificar termos financeiros.

### `keyword_topics.json`

Define temas e palavras-chave iniciais para apoiar sugestões de SEO sem depender de APIs pagas no MVP.

## Fallback local

Para evitar bloqueios durante a demo, o backend deve ter um fallback local caso a integração com IBM Consulting Advantage não esteja configurada.

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
- Criar endpoint `/analyze/url`.
- Criar endpoint `/analyze/briefing`.
- Implementar scraper simples.
- Implementar normalizador de página.
- Criar catálogos JSON.
- Criar cliente para IBM Consulting Advantage.
- Criar fallback local.
- Criar frontend com formulário de URL.
- Criar frontend com formulário de briefing.
- Criar tela de resultado.
- Criar cards de score.
- Criar lista de recomendações.
- Criar visualização de módulos.
- Criar prompts dos agentes.
- Criar roteiro de demo.

### P1

- Adicionar Playwright para páginas com JavaScript.
- Adicionar upload de mockup.
- Adicionar histórico de análises.
- Adicionar exportação em Markdown.
- Adicionar testes unitários.
- Adicionar loading states e tratamento de erro.

### P2

- Adicionar RAG com páginas aprovadas.
- Adicionar benchmark com concorrentes.
- Adicionar comparação antes/depois.
- Adicionar geração de wireframe sugerido.
- Adicionar priorização visual por impacto e esforço.

## Prompts para IBM Bob

### Backend

```text
Crie um backend FastAPI para um aplicativo chamado Marketing Page Analyzer.

Requisitos:
- Endpoint GET /health.
- Endpoint POST /analyze/url.
- Endpoint POST /analyze/briefing.
- Usar Pydantic para validação.
- Separar routes, schemas e services.
- Criar services para scraper, normalização, detecção de módulos e cliente do IBM Consulting Advantage.
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
- Usar BeautifulSoup e trafilatura quando fizer sentido.
- Retornar um dicionário estruturado.
- Tratar erros de timeout, URL inválida e HTML vazio.
```

### Frontend

```text
Crie uma interface React com TypeScript para o Marketing Page Analyzer.

Requisitos:
- Tela inicial com tabs para análise por URL e análise por briefing.
- Campos para objetivo de negócio e público-alvo.
- Botão para iniciar análise.
- Tela de resultado com score geral, scores por área, resumo executivo, top prioridades, mapa de módulos e sugestões de copy.
- Usar Tailwind CSS.
- Componentes reutilizáveis.
- Criar um arquivo lib/api.ts para chamadas ao backend.
```

### Testes

```text
Crie testes unitários com pytest para os serviços:
- seo_static_analyzer.py.
- module_detector.py.
- page_normalizer.py.

Cenários:
- Página sem title.
- Página sem meta description.
- Página com múltiplos H1.
- Página com headings fora de ordem.
- Página com módulos vazios.
- Briefing curto demais.
```

## Prompts para IBM Consulting Advantage

### Orchestrator Agent

```text
Você é o Orchestrator Agent de um analisador de páginas de marketing para uma instituição financeira.

Sua tarefa é coordenar análises especializadas de SEO, módulos, storytelling, conteúdo e segurança de marca.

Use os dados normalizados da página, o objetivo de negócio, o público-alvo e os catálogos disponíveis.

Você deve:
1. Identificar o tipo provável da página.
2. Definir a intenção principal da página.
3. Consolidar os achados dos agentes especializados.
4. Retornar uma resposta única, clara e priorizada.

Critérios:
- Seja prático.
- Priorize recomendações de alto impacto.
- Não invente dados.
- Sinalize incertezas quando necessário.
- Evite recomendações genéricas.
- Retorne apenas JSON válido.
```

### SEO Agent

```text
Você é um especialista em SEO para páginas de marketing de serviços financeiros.

Analise metadados, headings, texto principal, links e estrutura da página.

Avalie:
- Title tag.
- Meta description.
- H1.
- Hierarquia de H2 e H3.
- Palavra-chave principal.
- Palavras-chave secundárias.
- Intenção de busca.
- Links internos.
- Oportunidades para snippets.

Retorne JSON válido com score, problemas, recomendações, title sugerido, meta description sugerida, palavra-chave principal e palavras-chave secundárias.
```

### Module Strategy Agent

```text
Você é um estrategista de UX e conteúdo especializado em páginas modulares de marketing.

Você receberá módulos detectados e um catálogo de módulos possíveis.

Avalie:
- Quais módulos manter.
- Quais módulos remover.
- Quais módulos mudar de posição.
- Quais módulos reescrever.
- Quais módulos adicionar.

Considere tipo da página, objetivo de negócio e público-alvo.
Retorne JSON válido com justificativa e impacto esperado.
```

### Storytelling Agent

```text
Você é um especialista em storytelling para páginas digitais de marketing.

Analise se a página tem progressão narrativa clara:
- Gancho.
- Contexto ou problema.
- Solução.
- Benefícios.
- Prova.
- CTA.
- Redução de objeções.

Compare a estrutura atual com o padrão ideal para o tipo da página.
Retorne score, diagnóstico, estrutura recomendada e sugestões de copy.
Retorne apenas JSON válido.
```

### Brand Safety Agent

```text
Você é um revisor de marca e segurança de conteúdo para uma instituição financeira.

Analise:
- Clareza.
- Tom institucional.
- Promessas absolutas.
- Termos financeiros complexos.
- Riscos de interpretação.
- CTAs ambíguos.
- Necessidade de revisão humana.

Use as regras de marca fornecidas.
Retorne JSON válido com score, riscos, trechos problemáticos, sugestões de reescrita e indicação de revisão humana.
```

### Recommendation Agent

```text
Você é um consultor de marketing digital responsável por transformar análises em plano de ação.

Você receberá achados dos agentes de SEO, módulos, storytelling e brand safety.

Crie:
- Resumo executivo.
- Top 5 prioridades.
- Quick wins.
- Melhorias estruturais.
- Sugestões de copy.
- Nova ordem de módulos.
- Checklist final.

Classifique cada recomendação por impacto, esforço e área.
Retorne apenas JSON válido.
```

## Roteiro de demo

### Abertura

"O problema que queremos resolver é que otimizar páginas de marketing exige olhar SEO, conteúdo, UX, storytelling, marca e segurança de linguagem ao mesmo tempo. Esse processo normalmente é manual, demorado e pouco padronizado."

### Fluxo

1. Abrir o app.
2. Colar uma URL pública ou inserir um briefing.
3. Informar objetivo de negócio.
4. Informar público-alvo.
5. Rodar análise.
6. Mostrar score geral.
7. Mostrar oportunidades de SEO.
8. Mostrar plano de módulos.
9. Mostrar storytelling recomendado.
10. Mostrar sugestões de copy.
11. Mostrar top prioridades.

### Fechamento

"A solução usa IBM Consulting Advantage para orquestrar agentes especialistas e IBM Bob para acelerar a construção do software. O resultado é uma análise padronizada, explicável e acionável para times de Marketing Digital."

## Critérios de aceite

- O usuário consegue analisar uma URL.
- O usuário consegue analisar um briefing.
- A API retorna JSON estruturado.
- O dashboard exibe score geral e scores por área.
- A solução retorna pelo menos cinco recomendações priorizadas.
- As recomendações indicam impacto e esforço.
- O sistema funciona mesmo com fallback local.
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

### Fase 3

- Mockups.
- Histórico.
- Exportação.
- RAG.
- Benchmark.

## Observações

Este projeto não substitui revisão humana de marca, jurídico ou compliance. Ele atua como acelerador de diagnóstico e priorização, ajudando times a encontrarem oportunidades de melhoria com mais velocidade e consistência.
