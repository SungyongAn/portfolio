from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from routes.models.accounts_model import Account, TeacherRole, Subject
from routes.schemas.auth_schema import LoginRequest, LoginResponse
from routes.db.db import get_db

# パスワードハッシュ化の設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT設定
SECRET_KEY = "your-secret-key-change-this-in-production"  # 本番環境では環境変数から読み込む
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24時間

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWTトークンを作成"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ログイン機能（ID、パスワードで認証）
def authenticate_user(db: Session, login_data: LoginRequest) -> LoginResponse:
    try:
        account = db.query(Account).filter(
            Account.email == login_data.id,
        ).first()
        
        if not account:
            return LoginResponse(success=False, message="入力情報に誤りがあります。")

        # パスワード検証
        if not pwd_context.verify(login_data.password, account.password):
            return LoginResponse(success=False, message="入力情報に誤りがあります。")
        
        print(f"[LOGIN] ログイン成功 - ID: {account.id}, 名前: {account.name}, ロール: {account.role.value}")

        # JWTトークンを作成
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": account.id},
            expires_delta=access_token_expires
        )

        # レスポンスデータ
        response_data = {
            "id": account.id,
            "grade": account.grade,
            "class_name": account.class_name,
            "name": account.name,
            "role": account.role.value,
            "status": account.status.value,
            "enrollment_year": account.enrollment_year,
            "graduation_year": account.graduation_year,
            "access_token": access_token,
            "token_type": "bearer"
        }

        # 教師の場合の追加情報
        if account.role.value == "teacher":
            if account.teacher_role_id:
                teacher_role = db.query(TeacherRole).filter(TeacherRole.id == account.teacher_role_id).first()
                if teacher_role:
                    response_data["teacher_role"] = {
                        "id": teacher_role.id,
                        "code": teacher_role.code,
                        "name": teacher_role.name
                    }
            if account.subject_id:
                subject = db.query(Subject).filter(Subject.id == account.subject_id).first()
                if subject:
                    response_data["subject"] = {
                        "id": subject.id,
                        "code": subject.code,
                        "name": subject.name
                    }

        return LoginResponse(success=True, message="ログインに成功しました", data=response_data)

    except Exception as e:
        print("Authenticate error:", e)
        import traceback
        traceback.print_exc()
        return LoginResponse(success=False, message="認証処理中にエラーが発生しました。")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Account:
    """
    現在ログイン中のユーザーを取得
    
    使用例:
    @router.get("/protected")
    def protected_route(current_user: Account = Depends(get_current_user)):
        return {"user_id": current_user.id, "name": current_user.name}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証に失敗しました",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # トークンを取得
        token = credentials.credentials
        
        # トークンをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user_id = int(user_id)
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError as e:
        print("JWT decode error:", e)
        raise credentials_exception
    
    # データベースからユーザーを取得
    user = db.query(Account).filter(Account.id == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    return user
