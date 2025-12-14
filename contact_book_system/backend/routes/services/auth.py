from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import secrets

from routes.models.accounts_model import Account, TeacherRole, Subject
from routes.models.password_reset_model import PasswordResetToken
from routes.schemas.auth_schema import (
    LoginRequest, 
    LoginResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordResetConfirm
)
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


def generate_reset_token() -> str:
    """安全なリセットトークンを生成"""
    return secrets.token_urlsafe(32)


def send_reset_email(email: str, token: str):
    """パスワードリセットメールを送信（開発環境用）"""
    reset_link = f"http://localhost:8080/reset-password?token={token}"
    
    print("\n" + "="*60)
    print("📧 パスワードリセットメール（開発環境）")
    print("="*60)
    print(f"宛先: {email}")
    print(f"リセットリンク: {reset_link}")
    print(f"トークン: {token}")
    print(f"有効期限: 30分")
    print("="*60 + "\n")
    
    # 本番環境ではSMTPやメール送信サービスを使用
    # 例: SendGrid, AWS SES, Gmail SMTP など


# ログイン機能（email、パスワードで認証）
def authenticate_user(db: Session, login_data: LoginRequest) -> LoginResponse:
    try:
        account = db.query(Account).filter(
            Account.email == login_data.email,
        ).first()
        
        if not account:
            return LoginResponse(success=False, message="入力情報に誤りがあります。")

        # パスワード検証
        if not pwd_context.verify(login_data.password, account.password):
            return LoginResponse(success=False, message="入力情報に誤りがあります。")

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
            "last_name": account.last_name,
            "first_name": account.first_name,
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


def password_reset_request(request: PasswordResetRequest, db: Session) -> PasswordResetResponse:
    """パスワードリセット要求"""
    try:
        email = request.email
        
        # ユーザー検索
        account = db.query(Account).filter(Account.email == email).first()
        
        if account:
            # 既存の未使用トークンを無効化（オプション）
            db.query(PasswordResetToken).filter(
                PasswordResetToken.account_id == account.id,
                PasswordResetToken.used == False
            ).update({"used": True})
            
            # 新しいトークンを生成
            token = generate_reset_token()
            expires_at = datetime.utcnow() + timedelta(minutes=30)
            
            # トークンをデータベースに保存
            reset_token = PasswordResetToken(
                account_id=account.id,
                token=token,
                expires_at=expires_at,
                used=False
            )
            db.add(reset_token)
            db.commit()
            
            # メール送信
            send_reset_email(email, token)
        
        # セキュリティのため、常に成功レスポンスを返す
        return PasswordResetResponse(
            success=True,
            message="登録されているメールアドレスにパスワードリセット用のリンクを送信しました"
        )
        
    except Exception as e:
        print("Password reset request error:", e)
        import traceback
        traceback.print_exc()
        db.rollback()
        # セキュリティのため、エラーでも成功メッセージを返す
        return PasswordResetResponse(
            success=True,
            message="登録されているメールアドレスにパスワードリセット用のリンクを送信しました"
        )


def verify_reset_token(token: str, db: Session) -> dict:
    """トークンの有効性を確認"""
    try:
        # トークンを検索
        reset_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token
        ).first()
        
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="無効なトークンです"
            )
        
        # 使用済みチェック
        if reset_token.used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このトークンは既に使用されています"
            )
        
        # 有効期限チェック
        if datetime.utcnow() > reset_token.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="トークンの有効期限が切れています"
            )
        
        return {
            "success": True,
            "message": "有効なトークンです",
            "expires_at": reset_token.expires_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print("Verify token error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="トークンの検証中にエラーが発生しました"
        )


def password_reset_confirm(request: PasswordResetConfirm, db: Session) -> PasswordResetResponse:
    """パスワードリセット実行"""
    try:
        # トークンを検索
        reset_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == request.token
        ).first()
        
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="無効なトークンです"
            )
        
        # 使用済みチェック
        if reset_token.used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このトークンは既に使用されています"
            )
        
        # 有効期限チェック
        if datetime.utcnow() > reset_token.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="トークンの有効期限が切れています"
            )
        
        # パスワードの強度チェック
        if len(request.new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="パスワードは8文字以上である必要があります"
            )
        
        # アカウントを取得
        account = db.query(Account).filter(
            Account.id == reset_token.account_id
        ).first()
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="アカウントが見つかりません"
            )
        
        # パスワードをハッシュ化して更新
        hashed_password = pwd_context.hash(request.new_password)
        account.password = hashed_password
        
        # トークンを使用済みにする
        reset_token.used = True
        
        db.commit()
        
        return PasswordResetResponse(
            success=True,
            message="パスワードが正常にリセットされました"
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        print("Password reset confirm error:", e)
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="パスワードリセット中にエラーが発生しました"
        )
