"""
パスワードハッシュ生成スクリプト

FastAPIプロジェクト内で実行して、正しいパスワードハッシュを生成します。
生成されたハッシュをSQLで直接データベースに設定してください。

使用方法:
1. FastAPIプロジェクトのルートディレクトリに配置
2. python3 generate_password_hashes.py を実行
3. 出力されたSQL文をMySQLで実行
"""

from passlib.context import CryptContext

# auth.pyと同じ設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# パスワード設定
passwords = {
    'admin123': 'admin',
    'nurse123': 'school_nurse', 
    'teacher123': 'teacher',
    'student123': 'student'
}

print("=" * 80)
print("パスワードハッシュ生成")
print("=" * 80)
print()

# ハッシュを生成
hashes = {}
for password, role in passwords.items():
    hashed = pwd_context.hash(password)
    hashes[role] = hashed
    print(f"{role:15} | {password:12} | {hashed}")

print()
print("=" * 80)
print("MySQLで実行するSQL文")
print("=" * 80)
print()

# SQL文を生成
for role, hashed in hashes.items():
    print(f"UPDATE accounts SET password = '{hashed}' WHERE role = '{role}';")

print()
print("=" * 80)
print("使用方法:")
print("1. 上記のSQL文をコピー")
print("2. MySQLに接続: docker-compose exec db mysql -u root -p renrakucho_db")
print("3. SQL文を貼り付けて実行")
print("4. COMMIT; を実行")
print("=" * 80)

