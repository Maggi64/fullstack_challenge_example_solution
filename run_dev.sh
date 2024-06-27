#!/bin/bash

# Colors
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'         # No color

# Function to run a command with stdbuf and prefix its output
run_with_prefix() {
    local label=$1
    shift 1
    stdbuf -oL "$@" 2>&1 | while IFS= read -r line; do
        echo -e "${label}${YELLOW} | ${NC}${line}"
    done &
}

# Start Vite development server (frontend)
FORCE_COLOR=1 run_with_prefix "${BLUE}frontend" npm run --prefix ./frontend dev

# Start uvicorn server (backend)
PYTHONUNBUFFERED=1 run_with_prefix "${GREEN}backend " uvicorn backend.src.main:app --host 0.0.0.0 --port "${BACKEND_PORT}" --reload --use-colors --reload-dir ./backend/src

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
