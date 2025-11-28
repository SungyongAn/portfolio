import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import (
    auth,
    account_management,
    renrakucho_management,
    chat,
    archive_management
)
from routes.websocket import notifications

app = FastAPI(
    title="Contact Book System API",
    description="API for school contact book management",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://contact-book-system.pages.dev",
        "http://localhost:3000",
        "*"  # 開発中は全て許可
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント（重要！）
@app.get("/")
async def root():
    return {
        "message": "Contact Book System API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    }

# ヘルスチェック
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# データベース接続テスト（起動時）
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🚀 Application Starting...")
    
    # 環境変数確認
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # ホスト部分のみ表示（セキュリティのため）
        host = db_url.split("@")[1].split("/")[0] if "@" in db_url else "Unknown"
        print(f"✓ DATABASE_URL configured (host: {host})")
    else:
        print("✗ DATABASE_URL not configured!")
    
    # データベース接続テスト
    try:
        from routes.db.db import engine
        with engine.connect() as conn:
            print("✓ Database connection successful!")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
    
    print("=" * 50)

# ルーター登録
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(account_management.router, prefix="/account-management", tags=["Account Management"])
app.include_router(renrakucho_management.router, prefix="/renrakucho-management", tags=["Renrakucho"])
app.include_router(notifications.router, prefix="/notifications", tags=["WebSocket"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(archive_management.router, prefix="/archive", tags=["Archive"])

# Render用のポート設定
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
