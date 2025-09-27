FROM python:3

WORKDIR /app

# 依存関係インストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードコピー
COPY . .

# 開発用サーバー起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
