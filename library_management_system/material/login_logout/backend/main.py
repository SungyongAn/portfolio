from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from routes.db import get_db
from routes.models import User
from routes.auth_utils import verify_password
from routes.schema import (
    LoginRequest,
    )

app = FastAPI()


@app.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # DBからユーザーを検索
    user = db.query(User).filter(User.user_id == request.userId).first()
    if not user:
        raise HTTPException(status_code=401, detail="ユーザーIDまたはパスワードが違います")

    # パスワード認証（bcryptハッシュ前提）
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="ユーザーIDまたはパスワードが違います")

    return {"message": f"ログイン成功: {user.username}", "role": user.role}
