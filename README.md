# Marketing Page Analyzer

Multi-agent web application for analyzing and recommending improvements to digital marketing pages for a financial institution.

## Overview

Marketing Page Analyzer helps Digital Marketing, UX, Content, and digital channel teams evaluate pages faster, more consistently, and with more actionable outputs. The solution analyzes URLs, natural-language briefings, and, in a future evolution, mockups, returning recommendations about SEO, modular structure, narrative, content clarity, and brand safety.

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
Web Frontend
  |
  v
FastAPI Backend
  |
  | scraping, extraction, and normalization
  v
Page Intelligence Layer
  |
  | structured payload
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
Consolidated result
  |
  v
Dashboard and recommendation report
```

## Agents

### Orchestrator Agent

Coordinates the analysis, identifies the page type, and consolidates the results from the other agents.

### SEO Agent

Evaluates title, meta description, H1, headings, search intent, keywords, and on-page improvement opportunities.

### Module Strategy Agent

Analyzes the page composition in modules, recommending what to keep, remove, move, rewrite, or add.

### Storytelling Agent

Evaluates whether the page follows a narrative that fits its goal, such as conversion, education, campaign, or institutional positioning.

### Brand Safety Agent

Checks clarity, tone, sensitive language, and possible risks from overly strong claims in a financial context.

### Recommendation Agent

Transforms findings from the other agents into an action plan prioritized by impact and effort.

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
  "analysis_id": "ana_123",
  "score": {
    "overall": 82,
    "seo": 78,
    "storytelling": 85,
    "modules": 80,
    "brand_safety": 90
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
    "keep": [],
    "remove": [],
    "reorder": [],
    "add": []
  },
  "copy_suggestions": []
}
```

## Local catalogs

The project uses JSON catalogs to reduce generic recommendations and provide context to the agents.

### `modules_catalog.json`

Defines module types such as hero, benefits, FAQ, social proof, simulator, CTA, and educational content.

### `storytelling_patterns.json`

Defines narrative patterns by page type, such as product, campaign, financial education, and institutional pages.

### `brand_rules.json`

Defines tone and language safety rules, such as avoiding absolute promises and simplifying financial terms.

### `keyword_topics.json`

Defines initial topics and keywords to support SEO suggestions without relying on paid APIs in the MVP.

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

## Prompts for IBM Consulting Advantage

### Orchestrator Agent

```text
You are the Orchestrator Agent for a marketing page analyzer for a financial institution.

Your task is to coordinate specialized analyses of SEO, modules, storytelling, content, and brand safety.

Use the normalized page data, business goal, target audience, and available catalogs.

You must:
1. Identify the probable page type.
2. Define the main page intent.
3. Consolidate findings from the specialized agents.
4. Return a single, clear, prioritized response.

Criteria:
- Be practical.
- Prioritize high-impact recommendations.
- Do not invent data.
- Flag uncertainty when necessary.
- Avoid generic recommendations.
- Return only valid JSON.
```

### SEO Agent

```text
You are an SEO specialist for financial services marketing pages.

Analyze metadata, headings, main text, links, and page structure.

Evaluate:
- Title tag.
- Meta description.
- H1.
- H2 and H3 hierarchy.
- Primary keyword.
- Secondary keywords.
- Search intent.
- Internal links.
- Snippet opportunities.

Return valid JSON with score, issues, recommendations, suggested title, suggested meta description, primary keyword, and secondary keywords.
```

### Module Strategy Agent

```text
You are a UX and content strategist specialized in modular marketing pages.

You will receive detected modules and a catalog of possible modules.

Evaluate:
- Which modules to keep.
- Which modules to remove.
- Which modules to reposition.
- Which modules to rewrite.
- Which modules to add.

Consider the page type, business goal, and target audience.
Return valid JSON with rationale and expected impact.
```

### Storytelling Agent

```text
You are a storytelling specialist for digital marketing pages.

Analyze whether the page has a clear narrative progression:
- Hook.
- Context or problem.
- Solution.
- Benefits.
- Proof.
- CTA.
- Objection handling.

Compare the current structure with the ideal pattern for the page type.
Return score, diagnosis, recommended structure, and copy suggestions.
Return only valid JSON.
```

### Brand Safety Agent

```text
You are a brand and content safety reviewer for a financial institution.

Analyze:
- Clarity.
- Institutional tone.
- Absolute promises.
- Complex financial terms.
- Interpretation risks.
- Ambiguous CTAs.
- Need for human review.

Use the provided brand rules.
Return valid JSON with score, risks, problematic excerpts, rewrite suggestions, and human review indication.
```

### Recommendation Agent

```text
You are a digital marketing consultant responsible for transforming analyses into an action plan.

You will receive findings from the SEO, module, storytelling, and brand safety agents.

Create:
- Executive summary.
- Top 5 priorities.
- Quick wins.
- Structural improvements.
- Copy suggestions.
- New module order.
- Final checklist.

Classify each recommendation by impact, effort, and area.
Return only valid JSON.
```

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
