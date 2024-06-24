#!/bin/bash

# Start Vite development server (frontend)
FORCE_COLOR=1 npm run --prefix ./frontend dev &

# Start uvicorn server (backend)
uvicorn backend.src.main:app --host 0.0.0.0 --port ${BACKEND_PORT} --reload --reload-dir "/app/backend/src" &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?