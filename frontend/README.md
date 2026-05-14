# Marketing Page Analyzer - Frontend

React + TypeScript + Vite + Tailwind CSS frontend for the Marketing Page Analyzer.

## Prerequisites

- Node.js 18+ installed
- Backend running on http://localhost:8001

## Installation

```bash
cd frontend
npm install
```

## Running the Development Server

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Usage

### Analyze by URL
1. Select the "Analyze by URL" tab
2. Enter a URL (required)
3. Optionally fill in business goal, target audience, and page type hint
4. Click "Analyze URL"
5. View the JSON response with analysis results

### Analyze by Briefing
1. Select the "Analyze by Briefing" tab
2. Enter your briefing text (required)
3. Optionally fill in business goal, target audience, and constraints
4. Click "Analyze Briefing"
5. View the JSON response with analysis results

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── UrlAnalyzerForm.tsx      # URL analysis form
│   │   ├── BriefingAnalyzerForm.tsx # Briefing analysis form
│   │   └── JsonResult.tsx           # JSON result display
│   ├── lib/
│   │   └── api.ts                   # API client functions
│   ├── App.tsx                      # Main app component
│   ├── main.tsx                     # Entry point
│   └── index.css                    # Tailwind CSS imports
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## API Integration

The frontend connects to the backend API at `http://localhost:8001`:
- POST `/analyze/url` - Analyze a URL
- POST `/analyze/briefing` - Analyze a briefing

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.