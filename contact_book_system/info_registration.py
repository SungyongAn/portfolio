#!/usr/bin/env python3
"""
連絡帳管理システム - アカウント・サンプルデータ投入スクリプト（姓名分割対応版・ランダムメール版）
"""

import mysql.connector
import sys
import os
import random
import string
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
    'database': 'renrakucho_db',
    'charset': 'utf8mb4',
    'use_unicode': True
}

PASSWORDS = {
    'admin': 'admin123',
    'school_nurse': 'nurse123',
    'teacher': 'teacher123',
    'student': 'student123'
}

EMAIL_DOMAIN = '@school.com'
generated_emails = set()

# -------------------------------
# 名前分割（例: "佐藤 太郎" → ("佐藤", "太郎")）
# -------------------------------
def split_name(full):
    if " " in full:
        last, first = full.split(" ", 1)
    elif "　" in full:
        last, first = full.split("　", 1)
    else:
        return full, ""
    return last, first

# -------------------------------
# メールアドレス生成（英数字ランダム）
# -------------------------------
def generate_email(length=10):
    global generated_emails
    while True:
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        email = prefix + EMAIL_DOMAIN
        if email not in generated_emails:
            generated_emails.add(email)
            return email

# -------------------------------
# アカウント投入
# -------------------------------
def insert_accounts(cursor):
    print("\n【アカウントデータ投入】")

    admin_hash = pwd_context.hash(PASSWORDS['admin'])
    nurse_hash = pwd_context.hash(PASSWORDS['school_nurse'])
    teacher_hash = pwd_context.hash(PASSWORDS['teacher'])
    student_hash = pwd_context.hash(PASSWORDS['student'])

    # 管理者
    admin_email = generate_email()
    cursor.execute("""
        INSERT INTO accounts (email, last_name, first_name, password, role, status, grade, class_name, enrollment_year)
        VALUES (%s, %s, %s, %s, 'admin', 'enrolled', 0, '0', 2020)
    """, (admin_email, "システム", "管理者", admin_hash))
    print(f"✓ 管理者: 1件 ({admin_email})")

    # 養護教諭
    nurse_email = generate_email()
    cursor.execute("""
        INSERT INTO accounts (email, last_name, first_name, password, role, status, grade, class_name, enrollment_year)
        VALUES (%s, %s, %s, %s, 'school_nurse', 'enrolled', 0, '0', 2018)
    """, (nurse_email, "田中", "花子", nurse_hash))
    print(f"✓ 養護教諭: 1件 ({nurse_email})")

    # 教師
    teachers = [
        ("佐藤 太郎", teacher_hash, 1, "A", 2015, 1, 1),
        ("鈴木 美咲", teacher_hash, 1, "A", 2017, 2, 2),
        ("高橋 健一", teacher_hash, 0, "0", 2016, 3, 2)
    ]

    print("✓ 教師:")
    for full, pwd_hash, grade, cls, year, role_id, sub_id in teachers:
        last, first = split_name(full)
        email = generate_email()
        cursor.execute("""
            INSERT INTO accounts (email, last_name, first_name, password, role, status, grade, class_name, enrollment_year, teacher_role_id, subject_id)
            VALUES (%s, %s, %s, %s, 'teacher', 'enrolled', %s, %s, %s, %s, %s)
        """, (email, last, first, pwd_hash, grade, cls, year, role_id, sub_id))
        print(f"  - {full} ({email})")

    # 生徒
    students = [
        '青木 一郎', '石井 花', '上田 健太', '江藤 美咲', '大野 翔',
        '加藤 優子', '木村 大輔', '小林 さくら', '坂本 拓也', '佐々木 愛',
        '清水 悠斗', '杉山 結衣', '鈴木 颯太', '高木 美羽', '田中 陸',
        '谷口 咲希', '中村 蓮', '西田 葵', '野村 大和', '橋本 心春',
        '林 海斗', '原 ひまり', '藤田 悠真', '松本 結菜', '村田 蒼空',
        '森 陽菜', '山口 晴', '山田 凛', '吉田 翼', '渡辺 紬'
    ]

    print(f"✓ 生徒: {len(students)}件")
    for full in students:
        last, first = split_name(full)
        email = generate_email()
        cursor.execute("""
            INSERT INTO accounts (email, last_name, first_name, password, role, status, grade, class_name, enrollment_year, graduation_year)
            VALUES (%s, %s, %s, %s, 'student', 'enrolled', 1, 'A', 2024, 2027)
        """, (email, last, first, student_hash))
        print(f"  - {full} ({email})")

# -------------------------------
# サンプルデータ投入
# -------------------------------
def insert_sample_data(cursor):
    print("\n【サンプルデータ投入】")
    
    chat_rooms = [
        ('1年A組 連絡用', '1年A組の生徒と教員の連絡チャットルームです', 3),
        ('職員室', '教員同士の連絡用チャットルームです', 3)
    ]
    cursor.executemany("""
        INSERT INTO chat_rooms (name, description, creator_id)
        VALUES (%s, %s, %s)
    """, chat_rooms)
    print(f"✓ チャットルーム: {len(chat_rooms)}件")

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

# -------------------------------
# ログイン情報表示
# -------------------------------
def display_login_info(cursor):
    print("\n" + "=" * 80)
    print("【ログイン情報一覧】")
    print("=" * 80)

    for role, password in PASSWORDS.items():
        cursor.execute("""
            SELECT id, CONCAT(last_name, ' ', first_name) AS fullname, email
            FROM accounts
            WHERE role = %s
            ORDER BY id
            LIMIT 5
        """, (role,))

        results = cursor.fetchall()
        if results:
            role_name = {
                'admin': '管理者',
                'school_nurse': '養護教諭',
                'teacher': '教師',
                'student': '生徒'
            }.get(role, role)

            print(f"\n【{role_name}】共通パスワード: {password}")
            print("-" * 80)
            for account_id, fullname, email in results:
                print(f"  ID:{account_id:3} | {fullname:15} | メール: {email}")

# -------------------------------
# セットアップ検証
# -------------------------------
def verify_setup(cursor):
    print("\n【セットアップ検証】")
    cursor.execute("""
        SELECT role, COUNT(*) FROM accounts GROUP BY role ORDER BY role
    """)
    print("\nアカウント数:")
    for r, c in cursor.fetchall():
        print(f"  {r:15}: {c}件")
    return True

# -------------------------------
# メイン
# -------------------------------
def main():
    print("=" * 80)
    print("連絡帳管理システム - アカウント・サンプルデータ投入（姓名対応・ランダムメール）")
    print("=" * 80)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SET NAMES 'utf8mb4'")

        insert_accounts(cursor)
        conn.commit()

        insert_sample_data(cursor)
        conn.commit()

        verify_setup(cursor)
        display_login_info(cursor)

        print("\n✓ 完了しました")

    except Exception as e:
        print("❌ エラー:", e)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()
