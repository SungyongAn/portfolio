import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, measurements, users

load_dotenv()

# FastAPIアプリケーション作成
app = FastAPI(
    title="野球部タレントマネジメントシステムAPI",
    description="高校野球部の測定記録管理システムのバックエンドAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(measurements.router)


# ルートエンドポイント
@app.get("/")
def read_root():
    """
    APIルート

    システムの基本情報を返す
    """
    return {
        "message": "野球部タレントマネジメントシステムAPI",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }
