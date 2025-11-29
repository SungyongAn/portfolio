#!/bin/bash
set -e
cd "$(dirname "$0")/.."

echo "Running Backend Tests..."
# Ensure httpx version is compatible (just in case)
docker compose exec backend pip install httpx==0.25.2 > /dev/null 2>&1
docker compose exec backend python -m pytest
