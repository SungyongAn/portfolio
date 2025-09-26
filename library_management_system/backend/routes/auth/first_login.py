import bcrypt
from sqlalchemy.orm import Session
from routes.models import Account


# 初回ユーザー認証
def first_authenticate(db: Session, user_id: str, e_mail: str):

    user = db.query(Account).filter(
        Account.user_id == user_id,
        Account.email == e_mail,
        ).first()

    # ユーザーID、パスワードが一致しない場合
    if not user:
        return {"success": False, "message": "ユーザーIDまたはメールアドレスが見つかりません"}

    # パスワード登録済みの場合
    if user.password != "":
        return {"success": False, "message": "このユーザーIDはすでにパスワードが設定されています"}

    return {
        "success": True,
        "username": user.username,
        }


# パスワードの登録
def set_pass(db: Session, user_id: str, password: str):

    user = db.query(Account).filter(Account.user_id == user_id.strip()).first()

    # パスワードをハッシュ化
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user.password = hashed_pw
    db.commit()

    return {"success": True, "message": "password_registration_completed"}
