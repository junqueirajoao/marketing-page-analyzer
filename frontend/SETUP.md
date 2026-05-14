# Frontend Setup and Testing Guide

## Complete Setup Instructions

### Step 1: Install Dependencies

Open PowerShell and navigate to the frontend directory:

```powershell
cd "C:\Users\014590631\Documents\Projetos Python\Bob-a-thon\marketing-page-analyzer\frontend"
npm install
```

This will install all required dependencies including:
- React 18.2.0
- TypeScript 5.2.2
- Vite 5.0.8
- Tailwind CSS 3.3.6
- Axios 1.6.0

### Step 2: Start the Backend

In a separate PowerShell window:

```powershell
cd "C:\Users\014590631\Documents\Projetos Python\Bob-a-thon\marketing-page-analyzer\backend"
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8001
```

Verify the backend is running by visiting: http://localhost:8001/health

### Step 3: Start the Frontend

In the frontend PowerShell window:

```powershell
npm run dev
```

The frontend will start on http://localhost:3000

## Testing URL Analysis

1. Open http://localhost:3000 in your browser
2. Make sure the "Analyze by URL" tab is selected
3. Enter a test URL, for example:
   - URL: `https://www.example.com`
   - Business Goal: `increase conversions`
   - Target Audience: `small business owners`
   - Page Type Hint: `landing page`
4. Click "Analyze URL"
5. Wait for the loading spinner
6. View the JSON response with:
   - analysis_id
   - score (overall, seo, storytelling, modules, brand_safety)
   - page_summary
   - recommendations
   - module_plan
   - copy_suggestions
   - catalog_context
   - agent_trace
   - page_diagnostics (including modules_detected_count)

## Testing Briefing Analysis

1. Click on the "Analyze by Briefing" tab
2. Enter a test briefing, for example:
   ```
   We need a landing page for our new SaaS product targeting small businesses.
   The page should highlight our key features, pricing, and customer testimonials.
   We want to emphasize ease of use and quick setup.
   ```
3. Fill in optional fields:
   - Business Goal: `generate leads`
   - Target Audience: `small business owners`
   - Constraints: `mobile-first, no video, budget limit`
4. Click "Analyze Briefing"
5. Wait for the loading spinner
6. View the JSON response with the same structure as URL analysis

## Expected Behavior

### Success Case
- Loading spinner appears while analyzing
- JSON result displays in a formatted code block
- Result includes all expected fields
- No error messages

### Error Cases
- **Missing Required Field**: Red error message appears
- **Backend Not Running**: Error message about connection failure
- **Invalid URL**: Error message from backend validation
- **Network Error**: Friendly error message displayed

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

## Next Steps

After validating the basic integration:
1. The next task will implement the visual dashboard with cards and charts
2. Module detection results will be displayed visually
3. Scores will be shown with progress bars
4. Recommendations will be displayed in organized cards

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