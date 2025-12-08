#!/usr/bin/env python3
"""
アカウント情報出力スクリプト（姓名対応版）
データベースから全アカウント情報を取得して、各種形式で出力します
"""

import sys
import json
import csv
from datetime import datetime
import mysql.connector

# データベース接続設定
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'rootpass',
    'database': 'renrakucho_db'
}

# パスワード情報（表示用）
ROLE_PASSWORDS = {
    'admin': 'admin123',
    'school_nurse': 'nurse123',
    'teacher': 'teacher123',
    'student': 'student123'
}

# 日本語表示名
ROLE_NAMES_JA = {
    'admin': '管理者',
    'school_nurse': '養護教諭',
    'teacher': '教師',
    'student': '生徒'
}

def fetch_all_accounts():
    """データベースから全アカウント情報を取得（姓名対応）"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                id,
                last_name,
                first_name,
                email,
                role,
                created_at,
                updated_at
            FROM accounts
            ORDER BY 
                FIELD(role, 'admin', 'school_nurse', 'teacher', 'student'),
                id
        """)
        
        accounts = cursor.fetchall()
        conn.close()
        return accounts

    except mysql.connector.Error as err:
        print(f"❌ データベースエラー: {err}")
        return None


def export_to_text(accounts, filename='accounts.txt'):
    """テキスト形式で出力（姓名対応）"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("連絡帳管理システム - アカウント情報一覧（姓名対応）\n")
            f.write(f"出力日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
            f.write("=" * 100 + "\n\n")
            
            current_role = None
            
            for account in accounts:
                role = account['role']
                
                if role != current_role:
                    current_role = role
                    role_name = ROLE_NAMES_JA.get(role, role)
                    password = ROLE_PASSWORDS.get(role, '（未設定）')
                    
                    f.write("\n" + "-" * 100 + "\n")
                    f.write(f"【{role_name}】 共通パスワード: {password}\n")
                    f.write("-" * 100 + "\n")
                
                fullname = f"{account['last_name']} {account['first_name']}"
                
                f.write(f"  ID: {account['id']}\n")
                f.write(f"  名前: {fullname}\n")
                f.write(f"  メール: {account['email']}\n")
                f.write(f"  登録日: {account['created_at']}\n\n")
            
            f.write("=" * 100 + "\n")
            f.write(f"合計: {len(accounts)}件のアカウント\n")
            f.write("=" * 100 + "\n")
        
        print(f"✓ テキストファイル作成: {filename}")
        return True

    except IOError as err:
        print(f"❌ ファイル書き込みエラー: {err}")
        return False


def export_to_csv(accounts, filename='accounts.csv'):
    """CSV形式で出力（姓名対応）"""
    try:
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            
            writer.writerow([
                'ID', '姓', '名', '氏名(結合)', 
                'メールアドレス', '役割', '役割（日本語）', 
                'パスワード', '登録日時', '更新日時'
            ])
            
            for account in accounts:
                fullname = f"{account['last_name']} {account['first_name']}"
                role = account['role']
                
                writer.writerow([
                    account['id'],
                    account['last_name'],
                    account['first_name'],
                    fullname,
                    account['email'],
                    role,
                    ROLE_NAMES_JA.get(role, role),
                    ROLE_PASSWORDS.get(role, ''),
                    account['created_at'],
                    account['updated_at']
                ])
        
        print(f"✓ CSVファイル作成: {filename}")
        return True

    except IOError as err:
        print(f"❌ ファイル書き込みエラー: {err}")
        return False


def export_to_json(accounts, filename='accounts.json'):
    """JSON形式で出力（姓名対応）"""
    try:
        data = {
            'export_date': datetime.now().isoformat(),
            'total_count': len(accounts),
            'accounts': []
        }
        
        for account in accounts:
            role = account['role']
            fullname = f"{account['last_name']} {account['first_name']}"
            
            data['accounts'].append({
                'id': account['id'],
                'last_name': account['last_name'],
                'first_name': account['first_name'],
                'full_name': fullname,
                'email': account['email'],
                'role': role,
                'role_name_ja': ROLE_NAMES_JA.get(role, role),
                'password': ROLE_PASSWORDS.get(role, ''),
                'created_at': str(account['created_at']),
                'updated_at': str(account['updated_at'])
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ JSONファイル作成: {filename}")
        return True

    except IOError as err:
        print(f"❌ ファイル書き込みエラー: {err}")
        return False


def export_to_login_sheet(accounts, filename='login_info.txt'):
    """ログイン情報シート形式で出力（姓名対応）"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("連絡帳管理システム - ログイン情報（姓名対応）\n")
            f.write("=" * 80 + "\n\n")
            
            roles = {}
            for account in accounts:
                role = account['role']
                roles.setdefault(role, []).append(account)
            
            for role in ['admin', 'school_nurse', 'teacher', 'student']:
                if role not in roles:
                    continue
                
                role_name = ROLE_NAMES_JA.get(role, role)
                password = ROLE_PASSWORDS.get(role, '（未設定）')
                
                f.write(f"\n【{role_name}】\n")
                f.write(f"共通パスワード: {password}\n")
                f.write("-" * 80 + "\n")
                
                for a in roles[role]:
                    fullname = f"{a['last_name']} {a['first_name']}"
                    f.write(f"名前: {fullname:20} | メール: {a['email']}\n")
                
                f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write("※ パスワードは役割ごとに共通です\n")
            f.write("=" * 80 + "\n")
        
        print(f"✓ ログイン情報シート作成: {filename}")
        return True

    except IOError as err:
        print(f"❌ ファイル書き込みエラー: {err}")
        return False


def display_summary(accounts):
    """アカウント情報のサマリーを表示（変更なし）"""
    print("\n" + "=" * 80)
    print("アカウント情報サマリー")
    print("=" * 80)
    
    role_counts = {}
    for account in accounts:
        role = account['role']
        role_counts[role] = role_counts.get(role, 0) + 1
    
    for role in ['admin', 'school_nurse', 'teacher', 'student']:
        if role in role_counts:
            role_name = ROLE_NAMES_JA.get(role, role)
            count = role_counts[role]
            password = ROLE_PASSWORDS.get(role, '（未設定）')
            print(f"  {role_name:10} : {count:3}件  (パスワード: {password})")
    
    print("-" * 80)
    print(f"  合計: {len(accounts)}件")
    print("=" * 80)


def main():
    print("=" * 80)
    print("連絡帳管理システム - アカウント情報出力ツール（姓名対応）")
    print("=" * 80)
    
    print("\nデータベースからアカウント情報を取得中...")
    accounts = fetch_all_accounts()
    
    if not accounts:
        print("❌ アカウント情報の取得に失敗しました。")
        sys.exit(1)
    
    if len(accounts) == 0:
        print("⚠️ アカウントが登録されていません。")
        sys.exit(0)
    
    print(f"✓ {len(accounts)}件のアカウント情報を取得しました。")
    
    display_summary(accounts)
    
    print("\nファイルを出力中...")
    print("-" * 80)
    
    success_count = 0
    if export_to_text(accounts): success_count += 1
    if export_to_csv(accounts): success_count += 1
    if export_to_json(accounts): success_count += 1
    if export_to_login_sheet(accounts): success_count += 1
    
    print("-" * 80)
    
    if success_count == 4:
        print("\n✅ すべてのファイルを正常に出力しました！")
    else:
        print(f"\n⚠️ 一部のファイル出力に失敗しました。（{success_count}/4 成功）")
    
    print()


if __name__ == "__main__":
    main()
