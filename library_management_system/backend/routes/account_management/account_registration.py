from sqlalchemy.orm import Session
from sqlalchemy import or_
from routes.models import Account
from typing import List


# 新規ユーザー登録
def users_register(db: Session, users: List[dict]):

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


# ユーザー情報の抽出（単独条件のみ）
def search_accounts(db: Session, filters: List[dict]):
    query = db.query(Account)
    or_conditions = []

    for f in filters:
        # dict 内に1項目しかない前提
        if "user_id" in f:
            or_conditions.append(Account.user_id == f["user_id"])
        elif "username" in f:
            or_conditions.append(Account.username == f["username"])
        elif "admission_year" in f:
            or_conditions.append(Account.admission_year == f["admission_year"])
        elif "graduation_year" in f:
            or_conditions.append(Account.graduation_year == f["graduation_year"])
        elif "email" in f:
            or_conditions.append(Account.email == f["email"])
        elif "affiliation" in f:
            or_conditions.append(Account.affiliation == f["affiliation"])

    if or_conditions:
        query = query.filter(or_(*or_conditions))
    
    users_list = query.all()

    return users_list


# ユーザー情報の削除
def delete_users(db: Session, user_ids: list[str]) -> dict:
    try:
        # 削除対象ユーザーを検索
        users_to_delete = db.query(Account).filter(Account.user_id.in_(user_ids)).all()

        # 削除
        for user in users_to_delete:
            db.delete(user)
        db.commit()

        return {"success": True, "message": f"{len(users_to_delete)}件のユーザーを削除しました。"}

    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"削除処理中にエラーが発生しました: {str(e)}"}


# ユーザー情報の変更
