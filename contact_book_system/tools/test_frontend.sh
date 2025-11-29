#!/bin/bash
set -e
cd "$(dirname "$0")/.."

echo "Running Frontend Tests..."
# Install dependencies inside container to ensure vitest is available
docker compose exec frontend npm install
docker compose exec frontend npm test -- --run
