from fastapi import FastAPI

from backend.routes import api

app = FastAPI()
app.include_router(api.router)
