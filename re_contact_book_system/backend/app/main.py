from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, journals, users, teachers
import os

# FastAPIアプリケーション作成
app = FastAPI(
    title="連絡帳管理システムAPI",
    description="学校向け連絡帳管理システムのバックエンドAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(users.router)
app.include_router(teachers.router)


# ルートエンドポイント
@app.get("/")
def read_root():
    """
    APIルート
    
    システムの基本情報を返す
    """
    return {
        "message": "連絡帳管理システムAPI",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    ヘルスチェック
    
    システムの稼働状態を確認
    """
    return {
        "status": "healthy",
        "service": "journal-system-api"
    }


# アプリケーション起動時の処理
@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    print("=" * 70)
    print("連絡帳管理システムAPI 起動中...")
    print(f"ドキュメント: http://localhost:8000/docs")
    print(f"ReDoc: http://localhost:8000/redoc")
    print("=" * 70)


# アプリケーション終了時の処理
@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    print("=" * 70)
    print("連絡帳管理システムAPI 終了")
    print("=" * 70)
