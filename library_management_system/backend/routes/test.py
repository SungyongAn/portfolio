from sqlalchemy.orm import Session
from routes.models import Account
from typing import List


# 新規ユーザー登録
def users_register(db: Session, users: List[dict]):

    for u in users:
        # 重複チェック
        existing = db.query(Account).filter(
            (Account.user_id == u['userId']) | (Account.email == u['email'])
        ).first()
        if existing:
            return {"success": False, "message": f"{u['userId']} または {u['email']} は既に存在します。"}

        new_user = Account(
            user_id=u['user_id'],
            student_name=u['student_name'],
            enrollment_year=u['enrollment_year'],
            graduation_year=u['graduation_year'],
            email=u['email'],
            school_name=u['school_name']
        )
        db.add(new_user)
    
    db.commit()
    
    result = [
        {
            "userId": u.user_id,
            "studentName": u.student_name,
            "enrollmentYear": u.enrollment_year,
            "graduationYear": u.graduation_year,
            "email": u.email,
            "schoolName": u.school_name
        }
        for u in registered_users
    ]
    
    return {"success": True, "message": "新規ユーザー情報の登録を完了しました。", "users": result}

if __name__ == "__main__":
    test_users = [
        {
            "user_id": "student001",
            "username": "田中太郎",
            "enrollment_year": 2023,
            "graduation_year": 2027,
            "email": "tanaka@example.com",
            "affiliation": "B校"
        },
        {
            "user_id": "student002",
            "username": "佐藤花子",
            "enrollment_year": 2024,
            "graduation_year": 2028,
            "email": "sato@example.com",
            "affiliation": "B校"
        },
        {
            "user_id": "student003",
            "username": "鈴木一郎",
            "enrollment_year": 2022,
            "graduation_year": 2026,
            "email": "suzuki@example.com",
            "affiliation": "B校"
        }
    ]


    # テスト用のモックDBセッション（実際のテストでは本物のDBセッションを使用）
    class MockSession:
        def query(self, model):
            return MockQuery()
        
        def add(self, obj):
            print(f"DBに追加: {obj.user_id} - {obj.username}")
        
        def commit(self):
            print("データベースにコミットしました")
    
    class MockQuery:
        def filter(self, *args):
            return self
        
        def first(self):
            return None  # 重複なしとしてテスト
    
    # テスト実行
    print("=== ユーザー登録テスト実行 ===")
    print("テストデータ:")
    for i, user in enumerate(test_users, 1):
        print(f"  ユーザー{i}: {user['user_id']} - {user['student_name']}")
    
    print("\n=== 関数実行結果 ===")
    mock_db = MockSession()
    result = users_register(mock_db, test_users)
    
    print(f"成功: {result['success']}")
    print(f"メッセージ: {result['message']}")
    print(f"登録されたユーザー数: {len(result['users'])}")
    
    print("\n=== 登録されたユーザー情報 ===")
    for user in result['users']:
        print(f"  ID: {user['userId']}, 名前: {user['studentName']}, 
            "f"入学年: {user['enrollmentYear']}, 卒業年: {user['graduationYear']}, 学校名：{user['affiliation']}")
    
    print("\n注意: 実際の使用時は本物のSQLAlchemyセッションを使用してください")
