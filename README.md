# Financial Marketing Pages Analyzer

Multi-agent web application for analyzing and recommending improvements to financial marketing pages.

## Overview

Financial Marketing Pages Analyzer helps Digital Marketing, UX, Content, and digital channel teams evaluate financial marketing pages faster, more consistently, and with more actionable outputs. The solution analyzes URLs, natural-language briefings, and, in a future evolution, mockups, returning recommendations about SEO, modular structure, narrative, content clarity, and brand safety.

The project was designed for a hackathon using two main tools:

- **IBM Consulting Advantage**: specialized agent layer for analysis, reasoning, and recommendations.
- **IBM Bob**: VS Code development support to accelerate implementation, testing, documentation, and refactoring.

## Problem

Reviewing marketing pages usually requires several manual analyses at the same time:

- Technical and semantic SEO.
- Value proposition clarity.
- Page module structure.
- Storytelling and narrative progression.
- CTA quality.
- Brand tone.
- Language risks in a financial context.

This process can be slow, inconsistent, and dependent on multiple specialists. This project proposes a multi-agent assistant that consolidates these analyses and delivers a prioritized improvement plan.

## Solution

The system receives a URL or briefing and generates a report with:

- Overall page score.
- Score by dimension: SEO, storytelling, modules, and brand safety.
- Executive diagnosis.
- Top priorities.
- Keyword suggestions.
- Module recommendations to keep, remove, move, or add.
- Suggested new narrative structure.
- Before/after copy suggestions.
- Checklist for the Marketing team.

## Architecture

```text
User
  |
  | URL or briefing
  v
Web Frontend (React + Vite)
  |
  v
FastAPI Backend
  |
  | Scraping + Normalization + Module Detection
  v
Scoring Service
  |
  | SEO Score + Storytelling Score + Modules Score + Brand Safety Score
  v
Catalog Context Builder
  |
  | Injects relevant_seo_rules, relevant_brand_rules,
  | relevant_storytelling_patterns, relevant_modules
  v
IBM Consulting Advantage (ICA) Orchestration
  |
  | Page Strategy Orchestrator
  | ├── SEO Agent
  | ├── Module Strategy Agent
  | ├── Storytelling Agent
  | └── Brand and Compliance Agent
  v
Recommendation Agent
  |
  | Consolidates findings into actionable recommendations
  v
Structured Response
  |
  | score, score_breakdown, recommendations, module_plan,
  | narrative_insights, storytelling_analysis, catalog_context
  v
Dashboard with visual components
```

**Key Components:**

- **Catalog Context Builder**: Injects specialized domain knowledge from local catalogs into ICA agents without requiring Knowledge Base/embedding setup
- **ICA Orchestration**: Multi-agent system with supervisor pattern coordinating specialized agents
- **Local Fallback**: Automatic fallback to local processing if ICA is unavailable
- **Data-Driven Scoring**: Transparent, auditable scoring based on catalog rules

## Agents

The system uses IBM Consulting Advantage (ICA) with the following specialized agents:

### Page Strategy Orchestrator

Coordinates the multi-agent analysis, identifies page type, consolidates findings from specialized agents, and ensures coherent recommendations.

### SEO Agent

Evaluates title, meta description, H1, headings hierarchy, search intent, keywords, internal links, and on-page SEO opportunities using `relevant_seo_rules` from catalog context.

### Module Strategy Agent

Analyzes page composition in modules, recommending what to keep, remove, reorder, or add based on `relevant_modules` and storytelling patterns from catalog context.

### Storytelling Agent

Evaluates narrative progression (hook, context, solution, benefits, proof, CTA) using `relevant_storytelling_patterns` to ensure the page follows an appropriate narrative structure for its type and goal.

### Brand and Compliance Agent

Checks clarity, institutional tone, financial compliance (YMYL), and language safety using `relevant_brand_rules`. Flags risks like absolute promises, aggressive language, artificial urgency, and missing disclaimers (CET, credit analysis).

### Recommendation Agent

Consolidates findings from all agents into a prioritized action plan with impact/effort classification, executive summary, quick wins, and implementation checklist.

## Technical stack

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

### Optional

- Playwright for JavaScript-rendered pages.
- ChromaDB or FAISS for RAG.
- SQLite for analysis history.
- Markdown or PDF export.

## Folder structure

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

## Backend setup

Enter the backend folder:

```bash
cd backend
```

Create the virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install fastapi uvicorn pydantic pydantic-settings httpx beautifulsoup4 trafilatura readability-lxml lxml python-dotenv pytest
```

Or use:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

Test it:

```bash
curl http://localhost:8000/health
```

## Frontend setup

Enter the frontend folder:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Run the project:

```bash
npm run dev
```

## Environment variables

Create a `.env` file in the backend based on `.env.example`:

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

Checks whether the API is running.

Response:

```json
{
  "status": "ok"
}
```

### `POST /analyze/url`

Analyzes a page from a URL.

Input:

```json
{
  "url": "https://www.example.com/page",
  "business_goal": "conversion",
  "target_audience": "individual interested in a financial product",
  "page_type_hint": "product"
}
```

### `POST /analyze/briefing`

Analyzes a planned page from a briefing.

Input:

```json
{
  "briefing": "Create a page to promote a financial solution for small businesses.",
  "business_goal": "generate leads",
  "target_audience": "micro-entrepreneurs and small businesses",
  "constraints": ["simple tone", "avoid absolute promises"]
}
```

## Example response

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
          "description": "Title tag missing or too generic"
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
      "title": "Rewrite meta description",
      "why": "The current description does not communicate a benefit or search intent.",
      "suggestion": "Use a description with a clear benefit, primary keyword, and soft CTA.",
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
      "insight": "Page lacks clear problem statement before presenting solution",
      "impact": "medium",
      "recommendation": "Add context module explaining customer pain points"
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

## Local catalogs

The project uses JSON catalogs to provide specialized domain knowledge to ICA agents through the **catalog_context** mechanism, eliminating the need for Knowledge Base or embedding setup in the MVP phase.

### `modules_catalog.json`

Defines 50+ module types with detailed metadata:
- Module ID, name, display name, generic type
- Purpose, description, synonyms
- Detection hints, common content, UI elements
- Good for / bad for scenarios
- Recommendation rules (keepWhen, removeWhen, improveWhen)

Examples: hero, benefits, FAQ, social proof, simulator, CTA, trust badges, educational content, comparison tables, testimonials.

### `storytelling_patterns.json`

Defines narrative patterns by page type with:
- Page type, segment, business goal, target audience
- Storytelling name and description
- Emotional journey stages
- Narrative steps with recommended modules
- Required/optional/avoid modules
- Recommended module order
- Tone guidelines, compliance guidelines
- CTA examples, avoid copy patterns
- Agent evaluation rules

Examples: conversion funnel, educational journey, campaign landing, institutional positioning.

### `seo_rules.json`

Defines SEO rules with:
- Rule ID, category, severity
- Description, applies_to (page types)
- Checks (field, min/max length, requirements)
- Bad/good examples
- Recommended action
- Score impact (missing, too_short, too_long, generic)
- Agent guidance

Categories: metadata, headings, content, links, technical.

### `brand_rules.json`

Defines brand and compliance rules with:
- Rule ID, category, subcategory, severity
- Description, applies_to (page types)
- Bad examples, safe alternatives
- Detection keywords
- Recommended action, recommended modules
- Agent guidance

Categories: compliance (financial promises, YMYL, disclaimers), tone (institutional, clarity), language safety (aggressive, urgency, absolute claims).

### How catalog_context works

The **Catalog Context Builder** service:
1. Analyzes the page type, business goal, target audience
2. Selects the most relevant items from each catalog (max 8 per catalog)
3. Compacts them to essential fields
4. Injects them into the ICA payload as `catalog_context`
5. ICA agents use this context as their source of domain knowledge

This approach provides:
- **Specialized knowledge** without requiring Knowledge Base setup
- **Transparent reasoning** - agents cite specific rules/patterns
- **Auditable recommendations** - traceable to catalog entries
- **Easy maintenance** - update catalogs without retraining

## Local fallback

To avoid blockers during the demo, the backend should have a local fallback if the IBM Consulting Advantage integration is not configured.

Example:

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
            "executive_summary": "Simulated analysis for demo fallback.",
            "top_priorities": [
                {
                    "area": "SEO",
                    "impact": "high",
                    "effort": "low",
                    "title": "Improve title and meta description"
                }
            ]
        }
```

## Backlog

### P0

- Create FastAPI backend.
- Create `/health` endpoint.
- Create `/analyze/url` endpoint.
- Create `/analyze/briefing` endpoint.
- Implement simple scraper.
- Implement page normalizer.
- Create JSON catalogs.
- Create client for IBM Consulting Advantage.
- Create local fallback.
- Create frontend with URL form.
- Create frontend with briefing form.
- Create result screen.
- Create score cards.
- Create recommendation list.
- Create module visualization.
- Create agent prompts.
- Create demo script.

### P1

- Add Playwright for JavaScript pages.
- Add mockup upload.
- Add analysis history.
- Add Markdown export.
- Add unit tests.
- Add loading states and error handling.

### P2

- Add RAG with approved pages.
- Add competitor benchmarking.
- Add before/after comparison.
- Add suggested wireframe generation.
- Add visual prioritization by impact and effort.

## Prompts for IBM Bob

### Backend

```text
Create a FastAPI backend for an application called Marketing Page Analyzer.

Requirements:
- GET /health endpoint.
- POST /analyze/url endpoint.
- POST /analyze/briefing endpoint.
- Use Pydantic for validation.
- Separate routes, schemas, and services.
- Create services for scraping, normalization, module detection, and the IBM Consulting Advantage client.
- Create a local fallback for the demo if the IBM Consulting Advantage call is not configured.
- Keep the code simple, testable, and well organized.
```

### Scraper

```text
Implement a scraper.py service in Python.

Requirements:
- Receive a URL.
- Download HTML with httpx.
- Extract title, meta description, canonical, H1 to H3 headings, links, images, and main text.
- Use BeautifulSoup and trafilatura when appropriate.
- Return a structured dictionary.
- Handle timeout errors, invalid URLs, and empty HTML.
```

### Frontend

```text
Create a React with TypeScript interface for Marketing Page Analyzer.

Requirements:
- Home screen with tabs for URL analysis and briefing analysis.
- Fields for business goal and target audience.
- Button to start analysis.
- Result screen with overall score, scores by area, executive summary, top priorities, module map, and copy suggestions.
- Use Tailwind CSS.
- Reusable components.
- Create a lib/api.ts file for backend calls.
```

### Tests

```text
Create unit tests with pytest for the services:
- seo_static_analyzer.py.
- module_detector.py.
- page_normalizer.py.

Scenarios:
- Page without title.
- Page without meta description.
- Page with multiple H1s.
- Page with headings out of order.
- Page with empty modules.
- Briefing that is too short.
```

## IBM Consulting Advantage (ICA) Integration

The system uses **IBM Consulting Advantage** for multi-agent orchestration with automatic fallback to local processing.

### Key Features

- **Catalog Context Injection**: Backend injects `catalog_context` with relevant rules, patterns, and modules into ICA payload
- **No Knowledge Base Required**: Catalog context provides specialized domain knowledge without KB/embedding setup
- **Automatic Fallback**: If ICA is unavailable, system uses local agent fallback
- **Transparent Scoring**: Data-driven scoring based on catalog rules with full explainability
- **Agent Traceability**: Each recommendation cites specific catalog rules/patterns

### Configuration

Set environment variables in `backend/.env`:

```env
ADVANTAGE_BASE_URL=https://api.ibm.com/consulting-advantage
ADVANTAGE_API_KEY=your_api_key_here
ADVANTAGE_ORCHESTRATOR_ID=d5d0c63a-4a42-4431-b870-3f496a43fe10
ENABLE_AGENT_FALLBACK=true
```

### Agent Instructions

ICA agents receive instructions to:
- Use `catalog_context` as the source of domain knowledge
- Not invent rules, modules, or patterns outside provided context
- Base recommendations on `relevant_modules`, `relevant_storytelling_patterns`, `relevant_seo_rules`, and `relevant_brand_rules`
- Cite specific rule IDs and pattern IDs in recommendations
- Provide explainability for all scores and recommendations

For detailed integration documentation, see `backend/ICA_INTEGRATION.md`.

## Demo script

### Opening

"The problem we want to solve is that optimizing marketing pages requires looking at SEO, content, UX, storytelling, brand, and language safety at the same time. This process is usually manual, time-consuming, and not very standardized."

### Flow

1. Open the app.
2. Paste a public URL or enter a briefing.
3. Enter the business goal.
4. Enter the target audience.
5. Run the analysis.
6. Show the overall score.
7. Show SEO opportunities.
8. Show the module plan.
9. Show the recommended storytelling.
10. Show copy suggestions.
11. Show top priorities.

### Closing

"The solution uses IBM Consulting Advantage to orchestrate specialist agents and IBM Bob to accelerate software development. The result is a standardized, explainable, and actionable analysis for Digital Marketing teams."

## Acceptance criteria

- The user can analyze a URL.
- The user can analyze a briefing.
- The API returns structured JSON.
- The dashboard displays the overall score and scores by area.
- The solution returns at least five prioritized recommendations.
- The recommendations indicate impact and effort.
- The system works even with the local fallback.
- The README allows the project to be run locally.

## Suggested roadmap

### Phase 1

- Backend.
- Frontend.
- Scraper.
- Normalization.
- Fallback.
- Basic dashboard.

### Phase 2

- IBM Consulting Advantage integration.
- Specialized agents.
- Module and storytelling catalogs.
- UI improvements.

### Phase 3

- Mockups.
- History.
- Export.
- RAG.
- Benchmarking.

## Notes

This project does not replace human brand, legal, or compliance review. It acts as a diagnostic and prioritization accelerator, helping teams find improvement opportunities faster and more consistently.
