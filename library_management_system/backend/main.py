from fastapi import FastAPI
from routes.api import account_management, auth, material_management
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 認証
app.include_router(auth.router, prefix="/auth")

# アカウント管理
app.include_router(account_management.router, prefix="/account-management")

# 資料管理
app.include_router(material_management.router, prefix="/material-management")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE など全部OK
    allow_headers=["*"],   # 全てのヘッダを許可
)
