import os
import time
import pymysql

DATABASE_URL = os.environ.get("DATABASE_URL", "")

# DATABASE_URLからDB接続情報を解析
# 形式: mysql+pymysql://user:password@host:port/dbname
url = DATABASE_URL.replace("mysql+pymysql://", "")
user_pass, rest = url.split("@")
user, password = user_pass.split(":")
host_port, dbname = rest.split("/")
host, port = host_port.split(":") if ":" in host_port else (host_port, "3306")

max_retries = 30
retry_interval = 2

for i in range(max_retries):
    try:
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=dbname,
        )
        conn.close()
        print("DB is ready.")
        break
    except Exception as e:
        print(f"Waiting for DB... ({i + 1}/{max_retries}): {e}")
        time.sleep(retry_interval)
else:
    print("DB connection failed after max retries.")
    exit(1)