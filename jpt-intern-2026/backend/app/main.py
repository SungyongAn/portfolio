from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    auth,
    users,
    projects,
    tasks,
    admin_tasks,
    budget,
    notifications,
    departments,
    dashboard,
)

app = FastAPI(
    title="開発管理統合アプリケーション API",
    version="0.1.0",
)

# CORSミドルウェア設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://158.101.148.143",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(admin_tasks.router)
app.include_router(dashboard.router)
app.include_router(budget.router)
app.include_router(notifications.router)
app.include_router(departments.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
