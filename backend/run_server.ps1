# Script to run the FastAPI backend server on port 8000
# Usage: .\run_server.ps1

Write-Host "Starting Marketing Page Analyzer Backend on port 8000..." -ForegroundColor Green

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
} else {
    Write-Host "Warning: Virtual environment not found at .venv\" -ForegroundColor Yellow
    Write-Host "Please create it with: python -m venv .venv" -ForegroundColor Yellow
    Write-Host "Then install dependencies: pip install -r requirements.txt" -ForegroundColor Yellow
}

# Run uvicorn on port 8000
Write-Host "Starting server..." -ForegroundColor Cyan
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Made with Bob
