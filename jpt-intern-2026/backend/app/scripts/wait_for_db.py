import os
import time
import sys
from urllib.parse import urlparse

import pymysql


def parse_database_url(database_url: str):
    """
    DATABASE_URL を安全にパースする
    例: mysql+pymysql://user:pass@host:3306/dbname?charset=utf8mb4
    """
    parsed = urlparse(database_url)

    if not parsed.scheme.startswith("mysql"):
        raise ValueError("Only MySQL URLs are supported")

    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "database": parsed.path.lstrip("/"),
    }


def wait_for_db():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        print("❌ DATABASE_URL is not set")
        sys.exit(1)

    config = parse_database_url(database_url)

    max_retries = int(os.environ.get("DB_MAX_RETRIES", 30))
    retry_interval = int(os.environ.get("DB_RETRY_INTERVAL", 2))

    print("⏳ Waiting for DB to be ready...")
    print(f"   Host: {config['host']}:{config['port']}")
    print(f"   DB  : {config['database']}")

    for attempt in range(1, max_retries + 1):
        try:
            conn = pymysql.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                connect_timeout=5,
            )
            conn.close()

            print("✅ DB is ready!")
            return

        except Exception as e:
            print(f"⚠️  Attempt {attempt}/{max_retries} failed: {e}")
            time.sleep(retry_interval)

    print("❌ DB connection failed after max retries.")
    sys.exit(1)


if __name__ == "__main__":
    wait_for_db()
