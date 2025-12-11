# 開発環境用Dockerfile
FROM node:20-alpine

WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# アプリケーションのソースをコピー
COPY . .

# Viteの開発サーバーを起動（ホストを0.0.0.0に設定）
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
