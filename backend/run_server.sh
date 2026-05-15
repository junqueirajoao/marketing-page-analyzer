#!/bin/bash
# Script to run the FastAPI backend server on port 8001
# Usage: ./run_server.sh

echo "Starting Marketing Page Analyzer Backend on port 8001..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Warning: Virtual environment not found at .venv/"
    echo "Please create it with: python -m venv .venv"
    echo "Then install dependencies: pip install -r requirements.txt"
fi

# Run uvicorn on port 8001
echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Made with Bob
