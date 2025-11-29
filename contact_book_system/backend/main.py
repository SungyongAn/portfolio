import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント（GET と HEAD の両方に対応）
@app.get("/")
@app.head("/")  # ← これを追加
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

# ヘルスチェック（GET と HEAD の両方に対応）
@app.get("/health")
@app.head("/health")  # ← これを追加
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
        host = db_url.split("@")[1].split("/")[0] if "@" in db_url else "Unknown"
        print(f"✓ DATABASE_URL configured (host: {host})")
    else:
        print("✗ DATABASE_URL not configured!")
    
    # データベース接続テスト
    try:
        from routes.db.database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Database connection successful!")
    except ImportError as e:
        print(f"✗ Database module import failed: {e}")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        import traceback
        traceback.print_exc()  # 詳細なエラー情報を表示
    
    print("=" * 50)

# ルーター登録
try:
    from routes.api import (
        auth,
        account_management,
        renrakucho_management,
        chat,
        archive_management
    )
    from routes.websocket import notifications
    
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(account_management.router, prefix="/account-management", tags=["Account Management"])
    app.include_router(renrakucho_management.router, prefix="/renrakucho-management", tags=["Renrakucho"])
    app.include_router(notifications.router, prefix="/notifications", tags=["WebSocket"])
    app.include_router(chat.router, prefix="/chat", tags=["Chat"])
    app.include_router(archive_management.router, prefix="/archive", tags=["Archive"])
    
    print("✓ All routers loaded successfully")
except ImportError as e:
    print(f"⚠️ Some routers could not be loaded: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
