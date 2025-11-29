#!/bin/bash
set -e
cd "$(dirname "$0")/.."

# Run inside the backend container
# Ensure containers are up
docker compose up -d

echo "1. Initializing Database..."
docker compose exec backend python scripts/init_db.py

echo "2. Seeding Accounts (Admin Only)..."
docker compose exec backend python scripts/seed_accounts.py --admin-only

echo "3. Skipping Sample Data..."
# docker compose exec backend python scripts/seed_sample_data.py

echo "4. Verifying Data..."
docker compose exec backend python scripts/verify_data.py

echo "Production setup completed successfully!"
