FROM node:20

WORKDIR /app

# 依存関係インストール
COPY package*.json ./
RUN npm install

# ソースコードコピー
COPY . .

# Vite 開発サーバー起動
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
