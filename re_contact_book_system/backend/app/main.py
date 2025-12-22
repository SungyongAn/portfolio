from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, journals, users, teachers
from app.db import engine, Base

# テーブル作成（本番ではAlembic使用）
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="連絡帳管理システムAPI",
    version="1.0.0"
)

# CORS設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Viteのデフォルトポート
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(users.router)
app.include_router(teachers.router)


@app.get("/")
def read_root():
    return {"message": "連絡帳管理システムAPI"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
