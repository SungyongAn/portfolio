#!/bin/bash
set -e
cd "$(dirname "$0")/.."

# Load environment variables
# Run inside the backend container
# Ensure containers are up
docker compose up -d

echo "1. Initializing Database..."
docker compose exec backend python scripts/init_db.py

echo "2. Seeding Accounts..."
docker compose exec backend python scripts/seed_accounts.py

echo "3. Seeding Sample Data..."
docker compose exec backend python scripts/seed_sample_data.py

echo "4. Verifying Data..."
docker compose exec backend python scripts/verify_data.py

echo "Setup completed successfully!"
