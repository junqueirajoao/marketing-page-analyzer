# Financial Marketing Pages Analyzer - Frontend

React + TypeScript + Vite + Tailwind CSS frontend for the **Financial Marketing Pages Analyzer**.

## Overview

Modern, responsive web interface for analyzing financial marketing pages using IBM Consulting Advantage (ICA) multi-agent orchestration.

## Prerequisites

- Node.js 18+ installed
- Backend running on http://localhost:8000
- npm or yarn package manager

## Installation

```bash
cd frontend
npm install
```

## Running the Development Server

```bash
npm run dev
```

The frontend will be available at **http://localhost:3000**

## Features

### Analyze by URL
- Scrapes and analyzes live marketing pages
- Provides SEO, storytelling, modules, and brand safety analysis
- Returns data-driven scores with explainability

### Analyze by Briefing
- Analyzes planned pages from text descriptions
- Recommends optimal module structure
- Suggests narrative flow and compliance guidelines

### Visual Components
- **Score Breakdown**: Visual representation of scores by dimension
- **Module Map**: Interactive module visualization
- **Narrative Insights**: Key storytelling recommendations
- **Collapsible Sections**: Organized, scannable results
- **JSON Result**: Raw API response for debugging

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── UrlAnalyzerForm.tsx       # URL analysis form
│   │   ├── BriefingAnalyzerForm.tsx  # Briefing analysis form
│   │   ├── AnalysisResult.tsx        # Main results component
│   │   ├── JsonResult.tsx            # Raw JSON display
│   │   ├── ModuleMap.tsx             # Module visualization
│   │   ├── ScoreBreakdown.tsx        # Score visualization
│   │   ├── NarrativeInsights.tsx     # Insights display
│   │   └── CollapsibleSection.tsx    # Reusable collapsible
│   ├── lib/
│   │   └── api.ts                    # API client with types
│   ├── App.tsx                       # Main app component
│   ├── main.tsx                      # Entry point
│   └── index.css                     # Tailwind CSS config
├── index.html
├── package.json
├── vite.config.ts                    # Vite configuration
├── tailwind.config.js                # Tailwind configuration
├── postcss.config.js                 # PostCSS configuration
├── tsconfig.json                     # TypeScript configuration
├── README.md                         # This file
└── SETUP.md                          # Detailed setup guide
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000`:

### Endpoints
- **POST** `/analyze/url` - Analyze a URL
- **POST** `/analyze/briefing` - Analyze a briefing
- **GET** `/health` - Health check

### Response Structure
```typescript
{
  analysis_id: string;
  score: {
    overall: number;
    seo: number;
    storytelling: number;
    modules: number;
    brand_safety: number;
  };
  score_breakdown: object;
  recommendations: array;
  module_plan: object;
  narrative_insights: array;
  storytelling_analysis: object;
  catalog_context: object;
  ica_enhanced: boolean;
  analysis_source: string;
}
```

## Technology Stack

- **React 18.2.0**: UI framework
- **TypeScript 5.2.2**: Type safety
- **Vite 5.0.8**: Build tool and dev server
- **Tailwind CSS 3.3.6**: Utility-first CSS
- **Axios 1.6.0**: HTTP client
- **Lucide React**: Icon library

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Development

### Code Style
- TypeScript strict mode enabled
- ESLint configured
- Prettier recommended

### Hot Module Replacement (HMR)
Vite provides instant HMR for fast development iteration.

### Environment Variables
Create `.env.local` for custom configuration:
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

### Backend Connection Issues
1. Verify backend is running: http://localhost:8000/health
2. Check CORS configuration in backend
3. Verify port 8000 is not blocked by firewall

### Build Errors
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear Vite cache: `rm -rf node_modules/.vite`

### TypeScript Errors
1. Restart TypeScript server in VS Code
2. Check `tsconfig.json` configuration
3. Verify all dependencies are installed

## Next Steps

For detailed setup instructions, see `SETUP.md`.

For backend documentation, see `../backend/README.md` and `../backend/ICA_INTEGRATION.md`.