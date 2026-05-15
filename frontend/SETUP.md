# Frontend Setup and Testing Guide - Financial Marketing Pages Analyzer

## Overview

Complete setup and testing guide for the **Financial Marketing Pages Analyzer** frontend.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Backend running on port 8001
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Complete Setup Instructions

### Step 1: Install Dependencies

Navigate to the frontend directory:

```bash
cd frontend
npm install
```

This will install all required dependencies:
- **React 18.2.0**: UI framework
- **TypeScript 5.2.2**: Type safety
- **Vite 5.0.8**: Build tool
- **Tailwind CSS 3.3.6**: Styling
- **Axios 1.6.0**: HTTP client
- **Lucide React**: Icons

### Step 2: Start the Backend

In a separate terminal:

**Windows (PowerShell):**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8001
```

**Linux/Mac:**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

**Verify backend is running:**
- Health check: http://localhost:8001/health
- API docs: http://localhost:8001/docs

### Step 3: Start the Frontend

In the frontend terminal:

```bash
npm run dev
```

The frontend will start on **http://localhost:3000**

## Testing the Application

### Testing URL Analysis

1. Open http://localhost:3000 in your browser
2. Select the **"Analyze by URL"** tab
3. Enter test data:
   - **URL**: `https://www.example.com/financial-product`
   - **Business Goal**: `conversion` or `lead generation`
   - **Target Audience**: `individuals` or `businesses`
   - **Page Type Hint**: `product`, `campaign`, or `educational`
4. Click **"Analyze URL"**
5. Wait for analysis (loading spinner appears)
6. View results with:
   - **Overall Score**: Aggregate quality score
   - **Score Breakdown**: SEO, Storytelling, Modules, Brand Safety
   - **Recommendations**: Prioritized action items
   - **Module Plan**: Keep/remove/reorder/add modules
   - **Narrative Insights**: Storytelling recommendations
   - **Catalog Context**: Relevant rules and patterns used

### Testing Briefing Analysis

1. Click the **"Analyze by Briefing"** tab
2. Enter a test briefing:
   ```
   Create a landing page for personal credit product targeting individuals
   seeking financial solutions. The page should explain benefits, requirements,
   simulation, and application process. Emphasize transparency and security.
   ```
3. Fill optional fields:
   - **Business Goal**: `conversion`
   - **Target Audience**: `individuals seeking credit`
   - **Constraints**: `institutional tone, avoid absolute promises, include disclaimers`
4. Click **"Analyze Briefing"**
5. Wait for analysis
6. View structured recommendations for the planned page

### Expected Response Structure

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
      "issues": [...]
    },
    "storytelling": {
      "score": 85,
      "pattern_match": "conversion_funnel",
      "missing_elements": [...]
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
  "recommendations": [...],
  "module_plan": {
    "keep": [...],
    "remove": [...],
    "reorder": [...],
    "add": [...]
  },
  "narrative_insights": [...],
  "storytelling_analysis": {...},
  "catalog_context": {
    "relevant_modules": [...],
    "relevant_storytelling_patterns": [...],
    "relevant_seo_rules": [...],
    "relevant_brand_rules": [...]
  },
  "ica_enhanced": true,
  "analysis_source": "ica"
}
```

## Expected Behavior

### Success Case
- ✅ Loading spinner appears during analysis
- ✅ Results display in organized sections
- ✅ Scores show with visual indicators
- ✅ Recommendations are prioritized and actionable
- ✅ Module plan shows clear changes
- ✅ Narrative insights provide context
- ✅ Raw JSON available for debugging
- ✅ No error messages

### Error Cases
- ❌ **Missing Required Field**: Red error message appears
- ❌ **Backend Not Running**: Connection error with troubleshooting tips
- ❌ **Invalid URL**: Validation error from backend
- ❌ **Network Error**: Friendly error message with retry option
- ❌ **ICA Timeout**: System uses fallback, analysis still completes

## Troubleshooting

### Frontend won't start
- Make sure Node.js 18+ is installed: `node --version`
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is already in use

### Backend connection errors
- Verify backend is running on http://localhost:8001
- Check backend health endpoint: http://localhost:8001/health
- Ensure no firewall is blocking the connection

### TypeScript errors in editor
- These are expected before running `npm install`
- After installation, restart your editor
- TypeScript errors don't prevent the app from running

### CORS errors
- The backend should already have CORS configured
- If you see CORS errors, check backend/app/main.py

## Visual Components

The frontend includes several visual components:

### Score Breakdown
- Visual representation of scores by dimension
- Color-coded indicators (green/yellow/red)
- Detailed issue breakdown per category

### Module Map
- Interactive visualization of detected modules
- Shows module position and confidence
- Highlights recommended changes

### Narrative Insights
- Key storytelling recommendations
- Impact assessment
- Actionable suggestions

### Collapsible Sections
- Organized, scannable results
- Expand/collapse for better UX
- Preserves state during navigation

## Integration with ICA

The frontend displays ICA-enhanced results:
- **ica_enhanced**: Boolean flag indicating ICA usage
- **analysis_source**: "ica" or "fallback"
- **catalog_context**: Shows which rules/patterns were used
- **Explainability**: Each recommendation cites specific catalog entries

## Performance

- **Fast Loading**: Vite HMR for instant updates
- **Optimized Build**: Production build with code splitting
- **Responsive**: Works on desktop, tablet, and mobile
- **Accessible**: Semantic HTML and ARIA labels

## File Structure Reference

```
frontend/
├── src/
│   ├── components/
│   │   ├── UrlAnalyzerForm.tsx      # Handles URL input and submission
│   │   ├── BriefingAnalyzerForm.tsx # Handles briefing input and submission
│   │   └── JsonResult.tsx           # Displays raw JSON response
│   ├── lib/
│   │   └── api.ts                   # API client with TypeScript types
│   ├── App.tsx                      # Main component with tabs and state
│   ├── main.tsx                     # React entry point
│   └── index.css                    # Tailwind CSS configuration
├── public/                          # Static assets (auto-created)
├── index.html                       # HTML template
├── package.json                     # Dependencies and scripts
├── vite.config.ts                   # Vite configuration
├── tailwind.config.js               # Tailwind CSS configuration
├── postcss.config.js                # PostCSS configuration
└── tsconfig.json                    # TypeScript configuration