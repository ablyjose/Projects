#!/bin/bash

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Starting F1 Data Analysis App..."

# Function to handle cleanup on exit
cleanup() {
    echo "Stopping all services..."
    kill $PID_BACKEND 2>/dev/null
    kill $PID_FRONTEND 2>/dev/null
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

# Start Backend
echo "Starting Backend..."
cd "$SCRIPT_DIR/web-app/backend"
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi
$PYTHON_CMD -m uvicorn main:app --reload --port 8000 &
PID_BACKEND=$!

# Start Frontend
echo "Starting Frontend..."
cd "$SCRIPT_DIR/web-app/frontend"
npm run dev &
PID_FRONTEND=$!

echo "Both services started."
echo "Backend PID: $PID_BACKEND"
echo "Frontend PID: $PID_FRONTEND"
echo "Press Ctrl+C to stop both."

# Wait for processes
wait $PID_BACKEND $PID_FRONTEND
