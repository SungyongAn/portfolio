from fastapi import FastAPI
from routes.api import (
    auth,
    account_management,
    renrakucho_management,
    chat,
    archive_management
    )
from routes.websocket import notifications
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ルーター登録
app.include_router(auth.router, prefix="/auth")

app.include_router(account_management.router, prefix="/account-management")

app.include_router(renrakucho_management.router, prefix="/renrakucho-management")

app.include_router(notifications.router, prefix="/notifications")

app.include_router(chat.router, prefix="/chat")

app.include_router(archive_management.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
