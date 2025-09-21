import bcrypt
from sqlalchemy.orm import Session
from routes.models import Account


def authenticate(db: Session, user_id: str, password: str):

    user = db.query(Account).filter(Account.user_id == user_id.strip()).first()

    hashed = user.password.encode('utf-8') if isinstance(user.password, str) else user.password

    if not bcrypt.checkpw(password.encode('utf-8'), hashed):
        return {"success": False, "reason": "password_incorrect"}

    return {
        "success": True,
        "role": user.role,
        "username": user.username,
        }
