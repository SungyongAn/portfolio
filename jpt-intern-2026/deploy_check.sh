#!/bin/bash

echo "=================================="
echo "      Deploy Check Start"
echo "=================================="

# ----------------------------
# 1. 必須ファイル確認
# ----------------------------
echo ""
echo "[1] Files Check"

if [ -f .env ]; then
  echo "✔ .env exists"
else
  echo "✖ .env not found"
fi

if [ -f backend/.env ]; then
  echo "✔ backend/.env exists"
else
  echo "✖ backend/.env not found"
fi

# ----------------------------
# 2. Docker確認
# ----------------------------
echo ""
echo "[2] Docker Containers"

docker compose ps

# ----------------------------
# 3. Frontend Build
# ----------------------------
echo ""
echo "[3] Frontend Build"

cd frontend || exit
npm run build
cd ..

# ----------------------------
# 4. Backend Lint
# ----------------------------
echo ""
echo "[4] Backend Ruff Check"

docker compose exec backend ruff check .

# ----------------------------
# 5. Alembic Current
# ----------------------------
echo ""
echo "[5] Alembic Migration Check"

docker compose exec backend alembic current

HEADS=$(docker compose exec backend alembic heads 2>/dev/null | tr -d '\r')
CURRENT=$(docker compose exec backend alembic current 2>/dev/null | tr -d '\r')

if echo "$CURRENT" | grep -q "(head)"; then
  echo "✔ マイグレーションは最新です"
else
  echo "✖ 未適用のマイグレーションがあります"
  echo "  heads  : $HEADS"
  echo "  current: $CURRENT"
  echo "  → alembic upgrade head を実行してください"
fi

# ----------------------------
# 6. Git Status
# ----------------------------
echo ""
echo "[6] Git Status"

git status --short

# ----------------------------
# 7. DATABASE_URL 整合チェック
# ----------------------------
echo ""
echo "[7] DATABASE_URL Check"

MYSQL_PASSWORD=$(grep "^MYSQL_PASSWORD=" .env | cut -d '=' -f2)
DATABASE_URL=$(grep "^DATABASE_URL=" backend/.env)

if echo "$DATABASE_URL" | grep -q "$MYSQL_PASSWORD"; then
  echo "✔ DATABASE_URL password matches MYSQL_PASSWORD"
else
  echo "✖ DATABASE_URL password mismatch"
fi

# ----------------------------
# Finish
# ----------------------------
echo ""
echo "=================================="
echo "      Deploy Check Complete"
echo "=================================="