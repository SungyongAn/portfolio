# 認証概要

## 認証方式

- メールアドレス＋パスワード認証（JWT）
- フロントエンドはAccess Tokenを利用してAPIにアクセス
- Refresh TokenでAccess Tokenを更新可能

## 認証フロー

ユーザー入力 → POST /api/auth/login → JWT発行 → APIアクセス
↓
Access Token期限切れ → POST /api/auth/refresh → Access Token再取得
↓
ログアウト → POST /api/auth/logout → Cookie削除 + Piniaストア削除

## 関連API

- `POST /api/auth/login`  
- `POST /api/auth/logout`  
- `POST /api/auth/refresh`  
- `GET /api/auth/me`  
- `PATCH /api/auth/password`  
- `POST /api/auth/password-reset/request`  
- `POST /api/auth/password-reset/execute`