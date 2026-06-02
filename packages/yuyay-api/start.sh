#!/bin/sh
# Start Grafana Alloy in background
alloy run /app/alloy/config.alloy &

# Start uvicorn in foreground
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT