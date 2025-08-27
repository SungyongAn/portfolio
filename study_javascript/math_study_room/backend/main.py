from fastapi import FastAPI
from routes import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE など全部OK
    allow_headers=["*"],   # 全てのヘッダを許可
)
