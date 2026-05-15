# IBM Consulting Advantage (ICA) Integration

## Overview

This document describes the integration of **IBM Consulting Advantage (ICA)** orchestration with automatic fallback to local agent processing for the **Financial Marketing Pages Analyzer**.

## Architecture

The system implements a robust multi-layer architecture:

1. **ICA Client** (`ica_client.py`) - Handles communication with ICA API
2. **Advantage Client** (`advantage_client.py`) - Orchestrates ICA with fallback
3. **Catalog Context Builder** (`catalog_context_builder.py`) - Injects specialized domain knowledge
4. **Local Agent Fallback** (`local_agent_fallback.py`) - Provides local processing when ICA unavailable

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# IBM Consulting Advantage Configuration
ADVANTAGE_BASE_URL=https://api.ibm.com/consulting-advantage
ADVANTAGE_API_KEY=your_api_key_here
ADVANTAGE_ORCHESTRATOR_ID=d5d0c63a-4a42-4431-b870-3f496a43fe10
ENABLE_AGENT_FALLBACK=true

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
```

### Configuration Options

- **ADVANTAGE_BASE_URL**: Base URL for ICA API
- **ADVANTAGE_API_KEY**: API key for authentication
- **ADVANTAGE_ORCHESTRATOR_ID**: Orchestration ID to use (default: d5d0c63a-4a42-4431-b870-3f496a43fe10)
- **ENABLE_AGENT_FALLBACK**: Enable/disable automatic fallback (default: true)

## How It Works

### Request Flow

```
FastAPI Request
    ↓
Report Builder
    ↓
Advantage Client
    ↓
┌─────────────────────┐
│ Try ICA Client      │
│ - Build payload     │
│ - Call orchestration│
│ - Validate response │
└─────────────────────┘
    ↓
┌─────────────────────┐
│ ICA Success?        │
├─────────────────────┤
│ YES → Return ICA    │
│ NO  → Use Fallback  │
└─────────────────────┘
    ↓
Local Agent Fallback
    ↓
Return Analysis
```

### Fallback Scenarios

The system automatically falls back to local processing when:

1. **No Credentials**: `ADVANTAGE_BASE_URL` or `ADVANTAGE_API_KEY` not configured
2. **Timeout**: ICA doesn't respond within 30 seconds
3. **HTTP Error**: ICA returns non-200 status code
4. **Invalid Response**: ICA response missing required fields
5. **Network Error**: Connection issues or other HTTP errors

### Logging

The system provides clear logging for debugging:

```
[ICA] Calling orchestration d5d0c63a-4a42-4431-b870-3f496a43fe10
[ICA] Response received successfully
[ADVANTAGE] Using ICA response
```

Or on fallback:

```
[ICA] Timeout after 30s, using fallback
[FALLBACK] Using LocalAgentFallback
```

## ICA Payload Structure

The system sends a structured payload to ICA with **catalog_context** for specialized domain knowledge:

```json
{
  "normalized_page": {
    "metadata": {
      "title": "...",
      "meta_description": "...",
      "canonical": "..."
    },
    "headings": {
      "h1": ["..."],
      "h2": ["..."],
      "h3": ["..."]
    },
    "images": [],
    "links": {
      "internal": [],
      "external": []
    },
    "main_text": "..."
  },
  "detected_modules": [
    {
      "id": "hero",
      "confidence": 0.95,
      "position": 1
    }
  ],
  "module_plan": {
    "keep": ["hero", "benefits"],
    "remove": ["generic_text"],
    "reorder": [{"module": "social_proof", "from": 8, "to": 4}],
    "add": ["faq", "trust_badges"]
  },
  "storytelling_analysis": {
    "pattern_used": "conversion_funnel",
    "pattern_strength": "medium",
    "missing_steps": ["objection_handling"]
  },
  "score": {
    "overall": 85,
    "seo": 80,
    "storytelling": 90,
    "modules": 75,
    "brand_safety": 100
  },
  "score_breakdown": {
    "seo": {
      "score": 80,
      "issues": [
        {
          "rule_id": "seo_rule_001",
          "severity": "high",
          "description": "Title tag missing or too generic"
        }
      ]
    },
    "storytelling": {
      "score": 90,
      "pattern_match": "conversion_funnel",
      "missing_elements": ["social_proof"]
    },
    "modules": {
      "score": 75,
      "detected_count": 8,
      "recommended_count": 10
    },
    "brand_safety": {
      "score": 100,
      "risks": []
    }
  },
  "narrative_insights": [
    {
      "insight": "Page lacks clear problem statement",
      "impact": "medium",
      "recommendation": "Add context module"
    }
  ],
  "catalog_context": {
    "relevant_modules": [
      {
        "id": "hero",
        "name": "Hero",
        "purpose": "...",
        "good_for": ["..."],
        "recommendation_rules": {}
      }
    ],
    "relevant_storytelling_patterns": [
      {
        "id": "conversion_funnel",
        "page_type": "product",
        "narrative_steps": [],
        "required_modules": ["hero", "benefits", "cta_primary"]
      }
    ],
    "relevant_seo_rules": [
      {
        "id": "seo_rule_001",
        "severity": "high",
        "rule_name": "Clear, unique, specific title",
        "recommended_action": "..."
      }
    ],
    "relevant_brand_rules": [
      {
        "id": "brand_rule_001",
        "severity": "high",
        "rule_name": "Avoid absolute financial promises",
        "safe_alternatives": ["..."]
      }
    ]
  },
  "business_goal": "conversion",
  "target_audience": "businesses",
  "page_type_hint": "product",
  "instructions": "Use catalog_context as the source of domain knowledge..."
}
```

### Key Payload Components

- **normalized_page**: Scraped and normalized page data
- **detected_modules**: Modules identified by module detector with confidence scores
- **module_plan**: Initial recommendations for module changes
- **storytelling_analysis**: Pattern analysis from storytelling service
- **score**: Overall and dimensional scores from scoring service
- **score_breakdown**: Detailed scoring with issues and rule violations
- **narrative_insights**: Key insights about narrative structure
- **catalog_context**: **Specialized domain knowledge** injected from local catalogs
- **instructions**: Explicit instructions for ICA agents to use catalog_context

## Catalog Context: The Key Innovation

The **catalog_context** mechanism is the core innovation that enables specialized agent behavior without requiring Knowledge Base or embedding setup:

### What is catalog_context?

A structured payload section containing the most relevant items from each local catalog:
- **relevant_modules**: Up to 8 most relevant module definitions
- **relevant_storytelling_patterns**: Up to 8 most relevant narrative patterns
- **relevant_seo_rules**: Up to 8 most relevant SEO rules
- **relevant_brand_rules**: Up to 8 most relevant brand/compliance rules

### How is it built?

The `catalog_context_builder.py` service:
1. Analyzes page type, business goal, target audience
2. Scores each catalog item for relevance
3. Selects top items per catalog (max 8 each)
4. Compacts them to essential fields
5. Injects into ICA payload

### Why is it important?

- **No Knowledge Base needed**: Provides specialized knowledge without KB/embedding infrastructure
- **Transparent reasoning**: Agents cite specific rule IDs and pattern IDs
- **Auditable recommendations**: Every recommendation traceable to catalog entry
- **Easy maintenance**: Update catalogs without retraining or re-indexing
- **Context-aware**: Different context for different page types/goals

### Agent Instructions

ICA agents receive explicit instructions:
```
Use catalog_context as the source of domain knowledge.
Do not invent rules, modules or storytelling patterns outside the provided context.
Base your recommendations on the relevant_modules, relevant_storytelling_patterns,
relevant_seo_rules, and relevant_brand_rules provided in catalog_context.
```

## Response Validation

ICA responses must include:

- `recommendations` or `final_recommendations` (list)
- `narrative_insights` (list)
- `storytelling_analysis` (dict)

Missing any of these triggers automatic fallback.

## API Contract Preservation

The integration maintains the existing API contract:

### Response Structure

```json
{
  "analysis_id": "analysis_20260515_120000",
  "score": {
    "overall": 85,
    "seo": 80,
    "storytelling": 90,
    "modules": 75,
    "brand_safety": 100
  },
  "score_breakdown": {},
  "page_summary": {},
  "recommendations": [],
  "module_plan": {},
  "narrative_insights": [],
  "storytelling_analysis": {},
  "catalog_context": {},
  "agent_trace": [],
  "ica_enhanced": true,
  "analysis_source": "ica"
}
```

### Additional Fields (ICA Enhanced)

When ICA is used successfully:
- `ica_enhanced`: `true`
- `analysis_source`: `"ica"`

## Testing

### Run ICA Integration Tests

```bash
cd backend
.venv\Scripts\python.exe -m pytest app/tests/test_ica_integration.py -v
```

### Test Coverage

The test suite covers:

1. ✅ ICA client initialization with/without config
2. ✅ Successful ICA orchestration call
3. ✅ Timeout handling
4. ✅ HTTP error handling
5. ✅ Invalid response handling
6. ✅ Response validation
7. ✅ Briefing analysis with ICA
8. ✅ URL analysis with ICA
9. ✅ Automatic fallback on failure
10. ✅ Error when fallback disabled
11. ✅ API contract preservation

### Run All Tests

```bash
cd backend
.venv\Scripts\python.exe -m pytest -q
```

## Security

### API Key Protection

- API keys are loaded from environment variables
- Never logged or exposed in responses
- Not included in error messages

### Payload Security

- Sensitive data is not logged
- Only necessary data sent to ICA
- Response validation prevents injection

## Performance

### Timeout Configuration

- Default: 30 seconds
- Configurable in `ica_client.py`
- Prevents hanging requests

### Fallback Speed

- Fallback is instantaneous
- No retry delays
- Application never blocks

## Troubleshooting

### ICA Not Being Called

Check:
1. Environment variables are set
2. `.env` file is in `backend/` directory
3. Check logs for configuration warnings

### Always Using Fallback

Check:
1. API key is valid
2. Base URL is correct
3. Network connectivity to ICA
4. Check logs for specific error

### Invalid Response Errors

Check:
1. ICA orchestration ID is correct
2. ICA response structure matches expectations
3. Check logs for validation details

## Development

### Adding New ICA Features

1. Update `ica_client.py` for new API calls
2. Update `advantage_client.py` for orchestration
3. Add tests in `test_ica_integration.py`
4. Update this documentation

### Modifying Payload Structure

1. Update `build_ica_payload()` in `ica_client.py`
2. Update tests with new structure
3. Verify ICA accepts new format

## Monitoring

### Key Metrics to Monitor

- ICA success rate
- Fallback usage rate
- Average response time
- Timeout frequency
- Error types and frequency

### Log Levels

- `INFO`: Normal operation
- `WARNING`: Fallback triggered
- `ERROR`: Unexpected errors

## Made with Bob