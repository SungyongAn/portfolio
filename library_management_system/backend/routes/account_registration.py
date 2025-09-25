from sqlalchemy.orm import Session
from routes.models import Account
from typing import List


# 新規ユーザー登録
def users_register(db: Session, users: List[dict]):

    try:
        # print(f"受信したデータ: {users}")  # デバッグ用
        registered_users = []
        
        for u in users:
            existing_user = db.query(Account).filter(Account.user_id == u['user_id']).first()
            existing_email = db.query(Account).filter(Account.email == u['email']).first()

            if existing_user and existing_email:
                return {
                    "success": False,
                    "message": f"ユーザーID「{u['user_id']}」およびメール「{u['email']}」は既に存在します。"
                    }
            elif existing_user:
                return {
                    "success": False,
                    "message": f"ユーザーID「{u['user_id']}」は既に存在します。"
                    }
            elif existing_email:
                return {
                "success": False,
                "message": f"メール「{u['email']}」は既に存在します。"
                }

            new_user = Account(
                user_id=u['user_id'],
                username=u['username'],
                admission_year=u['admission_year'],
                graduation_year=u['graduation_year'],
                email=u['email'],
                affiliation=u['affiliation'],
                password=""  # 登録時に必須ないとエラーになる
            )
            db.add(new_user)
            registered_users.append(new_user)
        db.commit()
    
        result = [
            {
                "userId": u.user_id,
                "username": u.username,
                "admission_year": u.admission_year,
                "graduation_year": u.graduation_year,
                "email": u.email,
                "affiliation": u.affiliation
            }
            for u in registered_users
        ]
        
        return {"success": True, "message": "新規ユーザー情報の登録を完了しました。", "users": result}

    except Exception as e:
        # print(f"エラー発生: {e}")  # デバッグ用
        raise

