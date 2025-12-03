#!/usr/bin/env python3
"""
連絡帳管理システム - アカウント・サンプルデータ投入スクリプト

init.sql実行後に、アカウントとサンプルデータのみを投入します。

前提条件:
- init.sqlでデータベース、テーブル、マスタデータが作成済みであること

使用方法:
1. pip install mysql-connector-python passlib bcrypt
2. python3 setup_accounts_only.py
"""

import mysql.connector
import sys
import os
from passlib.context import CryptContext
from datetime import datetime

# パスワードハッシュ設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# データベース接続設定
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'appuser'),
    'password': os.getenv('DB_PASSWORD', 'apppass'),
    'database': 'renrakucho_db',  # データベース名を明示的に指定
    'charset': 'utf8mb4',
    'use_unicode': True
}

# パスワード設定
PASSWORDS = {
    'admin': 'admin123',
    'school_nurse': 'nurse123',
    'teacher': 'teacher123',
    'student': 'student123'
}


def insert_accounts(cursor):
    """アカウントデータを投入"""
    print("\n【アカウントデータ投入】")
    
    # パスワードハッシュを生成
    admin_hash = pwd_context.hash(PASSWORDS['admin'])
    nurse_hash = pwd_context.hash(PASSWORDS['school_nurse'])
    teacher_hash = pwd_context.hash(PASSWORDS['teacher'])
    student_hash = pwd_context.hash(PASSWORDS['student'])
    
    # 管理者
    cursor.execute("""
        INSERT INTO accounts (name, password, role, status, grade, class_name, enrollment_year, teacher_role_id, subject_id)
        VALUES ('システム管理者', %s, 'admin', 'enrolled', 0, '0', 2020, NULL, NULL)
    """, (admin_hash,))
    print("✓ 管理者: 1件")
    
    # 養護教諭
    cursor.execute("""
        INSERT INTO accounts (name, password, role, status, grade, class_name, enrollment_year, teacher_role_id, subject_id)
        VALUES ('田中 花子', %s, 'school_nurse', 'enrolled', 0, '0', 2018, NULL, NULL)
    """, (nurse_hash,))
    print("✓ 養護教諭: 1件")
    
    # 教師
    teachers = [
        ('佐藤 太郎', teacher_hash, 1, 'A', 2015, 1, 1),
        ('鈴木 美咲', teacher_hash, 1, 'A', 2017, 2, 2),
        ('高橋 健一', teacher_hash, 0, '0', 2016, 3, 2)
    ]
    cursor.executemany("""
        INSERT INTO accounts (name, password, role, status, grade, class_name, enrollment_year, teacher_role_id, subject_id)
        VALUES (%s, %s, 'teacher', 'enrolled', %s, %s, %s, %s, %s)
    """, teachers)
    print(f"✓ 教師: {len(teachers)}件")
    
    # 生徒（1年A組 30名）
    students = [
        '青木 一郎', '石井 花', '上田 健太', '江藤 美咲', '大野 翔',
        '加藤 優子', '木村 大輔', '小林 さくら', '坂本 拓也', '佐々木 愛',
        '清水 悠斗', '杉山 結衣', '鈴木 颯太', '高木 美羽', '田中 陸',
        '谷口 咲希', '中村 蓮', '西田 葵', '野村 大和', '橋本 心春',
        '林 海斗', '原 ひまり', '藤田 悠真', '松本 結菜', '村田 蒼空',
        '森 陽菜', '山口 晴', '山田 凛', '吉田 翼', '渡辺 紬'
    ]
    
    student_data = [(name, student_hash, 1, 'A', 2024, 2027) for name in students]
    cursor.executemany("""
        INSERT INTO accounts (name, password, role, status, grade, class_name, enrollment_year, graduation_year, teacher_role_id, subject_id)
        VALUES (%s, %s, 'student', 'enrolled', %s, %s, %s, %s, NULL, NULL)
    """, student_data)
    print(f"✓ 生徒: {len(students)}件")


def insert_sample_data(cursor):
    """サンプルデータを投入"""
    print("\n【サンプルデータ投入】")
    
    # チャットルーム
    chat_rooms = [
        ('1年A組 連絡用', '1年A組の生徒と教員の連絡チャットルームです', 3),
        ('職員室', '教員同士の連絡用チャットルームです', 3)
    ]
    cursor.executemany("""
        INSERT INTO chat_rooms (name, description, creator_id)
        VALUES (%s, %s, %s)
    """, chat_rooms)
    print(f"✓ チャットルーム: {len(chat_rooms)}件")
    
    # 連絡帳サンプル（簡略版）
    today = datetime.now().date()
    entries = [
        (6, today, today, 5, 5, '今日も元気です！', '【授業】数学のテストで満点が取れました。', False),
        (7, today, today, 4, 5, '体調良好です', '【授業】英語のプレゼンテーションをしました。', False),
        (8, today, today, 5, 4, '', '【授業】理科の実験が面白かったです。', False)
    ]
    cursor.executemany("""
        INSERT INTO renrakucho_entries (student_id, submitted_date, target_date, physical_condition, mental_state, physical_mental_notes, daily_reflection, is_read)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, entries)
    print(f"✓ 連絡帳サンプル: {len(entries)}件")


def verify_setup(cursor):
    """セットアップを検証"""
    print("\n【セットアップ検証】")
    
    # アカウント数を確認
    cursor.execute("""
        SELECT role, COUNT(*) 
        FROM accounts 
        GROUP BY role 
        ORDER BY role
    """)
    print("\nアカウント数:")
    for role, count in cursor.fetchall():
        print(f"  {role:15}: {count}件")
    
    # 文字コード確認
    cursor.execute("SELECT id, name FROM accounts WHERE id = 1")
    result = cursor.fetchone()
    print("\n文字コード確認:")
    print(f"  ID 1: {result[1]}")
    if '?' not in result[1] and len(result[1]) <= 20:
        print("  ✓ 文字コードOK")
    else:
        print("  ⚠️ 文字化けの可能性があります")
    
    # パスワード検証
    print("\nパスワード検証:")
    all_valid = True
    for role, password in PASSWORDS.items():
        cursor.execute(
            "SELECT password FROM accounts WHERE role = %s LIMIT 1",
            (role,)
        )
        result = cursor.fetchone()
        if result:
            is_valid = pwd_context.verify(password, result[0])
            status = "✓ OK" if is_valid else "✗ NG"
            print(f"  {role:15}: {status}")
            if not is_valid:
                all_valid = False
    
    return all_valid


def main():
    """メイン処理"""
    print("=" * 80)
    print("連絡帳管理システム - アカウント・サンプルデータ投入")
    print("=" * 80)
    print("\n前提条件: init.sqlでデータベース・テーブル・マスタデータが作成済みであること")
    
    try:
        # データベースに接続
        print("\n【MySQL接続】")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✓ 接続成功")
        
        # 文字コード設定
        cursor.execute("SET NAMES 'utf8mb4'")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET collation_connection = 'utf8mb4_unicode_ci'")
        
        # 確認
        print("\nアカウントとサンプルデータを投入します。")
        response = input("続行しますか？ (yes/no): ")
        
        if response.lower() != 'yes':
            print("キャンセルしました。")
            sys.exit(0)
        
        # データ投入
        insert_accounts(cursor)
        conn.commit()
        
        insert_sample_data(cursor)
        conn.commit()
        
        # 検証
        all_valid = verify_setup(cursor)
        
        print("\n" + "=" * 80)
        if all_valid:
            print("✅ セットアップが完了しました！")
            print("\nログイン情報:")
            print("  管理者     - ID: 1, 名前: システム管理者, パスワード: admin123")
            print("  養護教諭   - ID: 2, 名前: 田中 花子,     パスワード: nurse123")
            print("  教師       - ID: 3, 名前: 佐藤 太郎,     パスワード: teacher123")
            print("  生徒       - ID: 6, 名前: 青木 一郎,     パスワード: student123")
        else:
            print("⚠️  セットアップは完了しましたが、一部に問題があります。")
        print("=" * 80)
        
    except mysql.connector.Error as e:
        print(f"\n❌ データベースエラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nデータベース接続を閉じました。")


if __name__ == "__main__":
    main()
