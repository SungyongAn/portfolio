from db_utils import get_db, get_password_hash


from app.models.accounts_model import Account

def seed_accounts(admin_only=False):
    print(f"Seeding accounts (Admin only: {admin_only})...")
    db = next(get_db())
    
    # Passwords
    passwords = {
        'admin': 'admin123',
        'school_nurse': 'nurse123',
        'teacher': 'teacher123',
        'student': 'student123'
    }
    
    hashed_pw = {k: get_password_hash(v) for k, v in passwords.items()}

    # Base accounts (Admin)
    accounts = [
        {
            "name": "システム管理者",
            "password": hashed_pw['admin'],
            "role": "admin",
            "status": "enrolled",
            "grade": 0,
            "class_name": "0",
            "enrollment_year": 2020
        }
    ]

    if not admin_only:
        # Nurse
        accounts.append({
            "name": "田中 花子",
            "password": hashed_pw['school_nurse'],
            "role": "school_nurse",
            "status": "enrolled",
            "grade": 0,
            "class_name": "0",
            "enrollment_year": 2018
        })
        
        # Teachers
        accounts.extend([
            {
                "name": "佐藤 太郎",
                "password": hashed_pw['teacher'],
                "role": "teacher",
                "status": "enrolled",
                "grade": 1,
                "class_name": "1",
                "enrollment_year": 2015
            },
            {
                "name": "鈴木 美咲",
                "password": hashed_pw['teacher'],
                "role": "teacher",
                "status": "enrolled",
                "grade": 2,
                "class_name": "2",
                "enrollment_year": 2017
            },
            {
                "name": "高橋 健一",
                "password": hashed_pw['teacher'],
                "role": "teacher",
                "status": "enrolled",
                "grade": 3,
                "class_name": "2",
                "enrollment_year": 2016
            }
        ])

    # Students
    if not admin_only:
        student_names = [
            '青木 一郎', '石井 花', '上田 健太', '江藤 美咲', '大野 翔',
            '加藤 優子', '木村 大輔', '小林 さくら', '坂本 拓也', '佐々木 愛',
            '清水 悠斗', '杉山 結衣', '鈴木 颯太', '高木 美羽', '田中 陸',
            '谷口 咲希', '中村 蓮', '西田 葵', '野村 大和', '橋本 心春',
            '林 海斗', '原 ひまり', '藤田 悠真', '松本 結菜', '村田 蒼空',
            '森 陽菜', '山口 晴', '山田 凛', '吉田 翼', '渡辺 紬'
        ]
        
        for name in student_names:
            accounts.append({
                "name": name,
                "password": hashed_pw['student'],
                "role": "student",
                "status": "enrolled",
                "grade": 1,
                "class_name": "A",
                "enrollment_year": 2024,
                "graduation_year": 2027
            })

    count = 0
    for data in accounts:
        # Check if exists
        exists = db.query(Account).filter(Account.name == data["name"]).first()
        if not exists:
            account = Account(**data)
            db.add(account)
            count += 1
    
    db.commit()
    print(f"Seeded {count} accounts.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Seed initial accounts.')
    parser.add_argument('--admin-only', action='store_true', help='Seed only the admin account')
    args = parser.parse_args()
    
    seed_accounts(admin_only=args.admin_only)
