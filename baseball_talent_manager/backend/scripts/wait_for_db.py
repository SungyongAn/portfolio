import os
import time
from urllib.parse import urlparse

import pymysql

db_url = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:root@db:3306/baseball_talent_manager"
)

p = urlparse(db_url)

for i in range(30):
    try:
        conn = pymysql.connect(
            host=p.hostname,
            port=p.port or 3306,
            user=p.username,
            password=p.password,
            database=p.path.lstrip("/"),
        )
        conn.close()
        print("DB is ready!")
        break
    except Exception:
        print(f"DB not ready, retrying... ({i+1}/30)")
        time.sleep(1)
else:
    print("DB did not become ready in time.")
    exit(1)
