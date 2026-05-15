# IBM Consulting Advantage (ICA) Integration

## Overview

This document describes the integration of IBM Consulting Advantage (ICA) orchestration with automatic fallback to local agent processing.

## Architecture

The system implements a robust three-layer architecture:

1. **ICA Client** (`ica_client.py`) - Handles communication with ICA API
2. **Advantage Client** (`advantage_client.py`) - Orchestrates ICA with fallback
3. **Local Agent Fallback** (`local_agent_fallback.py`) - Provides local processing

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

The system sends a structured payload to ICA:

```json
{
  "normalized_page": {
    "metadata": {},
    "headings": [],
    "images": [],
    "links": [],
    "main_text": "..."
  },
  "detected_modules": [],
  "module_plan": {
    "keep": [],
    "remove": [],
    "reorder": [],
    "add": []
  },
  "storytelling_analysis": {},
  "score": {
    "overall": 85,
    "seo": 80,
    "storytelling": 90,
    "modules": 75,
    "brand_safety": 100
  },
  "score_breakdown": {},
  "narrative_insights": [],
  "business_goal": "conversao",
  "target_audience": "empresas",
  "page_type_hint": "produto"
}
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