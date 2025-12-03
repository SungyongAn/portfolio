#!/usr/bin/env python3
"""
パスワードハッシュ更新スクリプト
init.sql実行後に、正しいパスワードハッシュを設定します

使用方法:
1. 必要なパッケージをインストール:
   pip install mysql-connector-python passlib bcrypt

2. データベース接続情報を環境変数または直接編集で設定

3. スクリプトを実行:
   python3 update_passwords.py
"""

import sys
import mysql.connector
from passlib.context import CryptContext

# passlib の設定（auth.pyと同じ）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# データベース接続設定（環境変数または直接指定）
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'rootpass',
    'database': 'renrakucho_db'
}

# パスワード設定（平文パスワード: 対象role）
PASSWORDS = {
    'admin123': 'admin',         # 管理者用
    'nurse123': 'school_nurse',  # 養護教諭用
    'teacher123': 'teacher',     # 教師用
    'student123': 'student'      # 生徒用
}


def test_connection():
    """データベース接続テスト"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✓ データベース接続成功")
            conn.close()
            return True
    except mysql.connector.Error as err:
        print(f"✗ データベース接続失敗: {err}")
        print("\n接続情報を確認してください:")
        print(f"  ホスト: {DB_CONFIG['host']}")
        print(f"  ポート: {DB_CONFIG['port']}")
        print(f"  ユーザー: {DB_CONFIG['user']}")
        print(f"  データベース: {DB_CONFIG['database']}")
        return False


def generate_hashes():
    """パスワードハッシュを生成して表示"""
    print("\n" + "=" * 80)
    print("生成されるパスワードハッシュ:")
    print("=" * 80)
    
    for password, role in PASSWORDS.items():
        hashed = pwd_context.hash(password)
        print(f"{role:15} | {password:12} → {hashed}")
    
    print("=" * 80)


def update_passwords():
    """データベース内の全アカウントのパスワードを更新"""
    try:
        # データベースに接続
        print("\nデータベースに接続中...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n" + "=" * 80)
        print("パスワードハッシュ更新開始")
        print("=" * 80)
        
        total_updated = 0
        
        for password, role in PASSWORDS.items():
            # パスワードハッシュを生成
            hashed = pwd_context.hash(password)
            
            # 該当するroleのアカウントを更新
            cursor.execute(
                "UPDATE accounts SET password = %s WHERE role = %s",
                (hashed, role)
            )
            
            affected_rows = cursor.rowcount
            total_updated += affected_rows
            print(f"✓ {role:15} ({password:12}): {affected_rows}件更新")
        
        # コミット
        conn.commit()
        
        print("=" * 80)
        print(f"✅ パスワードハッシュの更新が完了しました！（合計 {total_updated}件）")
        print("=" * 80)
        
        # 検証
        print("\n【更新後のアカウント数】")
        cursor.execute("SELECT role, COUNT(*) FROM accounts GROUP BY role ORDER BY role")
        for role, count in cursor.fetchall():
            print(f"  {role:15}: {count}件")
        
        return True
        
    except mysql.connector.Error as err:
        print(f"\n❌ エラーが発生しました: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("\nデータベース接続を閉じました。")


def verify_passwords():
    """更新後のパスワードを検証"""
    try:
        print("\n" + "=" * 80)
        print("パスワード検証")
        print("=" * 80)
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        all_valid = True
        
        for password, role in PASSWORDS.items():
            # 該当roleの最初のアカウントを取得
            cursor.execute(
                "SELECT id, name, password FROM accounts WHERE role = %s LIMIT 1",
                (role,)
            )
            account = cursor.fetchone()
            
            if account:
                # パスワード検証
                is_valid = pwd_context.verify(password, account['password'])
                status = "✓ OK" if is_valid else "✗ NG"
                print(f"{role:15} | {account['name']:15} | {status}")
                
                if not is_valid:
                    all_valid = False
            else:
                print(f"{role:15} | アカウントなし")
        
        print("=" * 80)
        
        if all_valid:
            print("✅ すべてのパスワードが正しく設定されています！")
        else:
            print("⚠️  一部のパスワードに問題があります。")
        
        conn.close()
        return all_valid
        
    except mysql.connector.Error as err:
        print(f"❌ 検証エラー: {err}")
        return False


def main():
    """メイン処理"""
    print("=" * 80)
    print("連絡帳管理システム - パスワードハッシュ更新ツール")
    print("=" * 80)
    
    # 接続テスト
    if not test_connection():
        print("\n終了します。")
        sys.exit(1)
    
    # 生成されるハッシュを表示
    generate_hashes()
    
    # 確認
    print("\n上記のパスワードでデータベースを更新しますか？")
    response = input("続行する場合は 'yes' と入力してください: ")
    
    if response.lower() != 'yes':
        print("キャンセルしました。")
        sys.exit(0)
    
    # パスワード更新
    if update_passwords():
        # 検証
        verify_passwords()
        print("\n✅ すべての処理が完了しました！")
    else:
        print("\n❌ 更新に失敗しました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
