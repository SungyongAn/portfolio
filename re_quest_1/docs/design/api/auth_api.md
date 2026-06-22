# auth_api.md

# 認証API設計

## 1. 概要

本ドキュメントは、`re_quest1` における認証APIを定義する。

既存 `quest_1` のログイン仕様を基準とし、
ASP.NET Core Web API で JWT 認証を実装する。

---

## 2. 認証方式

認証方式は JWT とする。

```text
JWT
```

APIリクエスト時は、Authorization Header にアクセストークンを付与する。

```text
Authorization: Bearer <token>
```

---

## 3. ログインAPI

## Endpoint

```text
POST /api/auth/login
```

---

## Request

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

---

## Request項目

| 項目     | 型     | 必須 | 概要           |
| -------- | ------ | ---- | -------------- |
| email    | string | ○    | メールアドレス |
| password | string | ○    | パスワード     |

---

## Response

```json
{
  "access_token": "xxxxx",
  "token_type": "bearer"
}
```

---

## Response項目

| 項目         | 型     | 概要                |
| ------------ | ------ | ------------------- |
| access_token | string | JWTアクセストークン |
| token_type   | string | bearer固定          |

---

## 4. エラーレスポンス

## ログイン失敗

```json
{
  "detail": "Invalid email or password"
}
```

## Status

```text
401 Unauthorized
```

---

## バリデーションエラー

```json
{
  "detail": "Validation Error"
}
```

## Status

```text
422 Validation Error
```

---

## 5. ASP.NET Core実装方針

## Controller

```text
AuthController
```

---

## Service

```text
AuthService
```

---

## DTO

### Request

```text
LoginRequest
```

### Response

```text
LoginResponse
```

---

## 6. AuthServiceの責務

AuthService は以下を担当する。

- ユーザー検索
- パスワード検証
- JWT生成
- ログイン失敗時の例外処理

---

## 7. 処理フロー

```text
Login Request
 ↓

AuthController
 ↓

AuthService
 ↓

UserRepository
 ↓

Password Verification
 ↓

JWT Generate
 ↓

Login Response
```

---

## 8. セキュリティ方針

- パスワードは平文保存しない
- パスワードハッシュを検証する
- ログイン失敗時に詳細な理由を返しすぎない
- JWTには必要最小限の情報のみ含める
- JWTの有効期限を設定する

---

## 9. JWTに含める情報

| Claim         | 概要           |
| ------------- | -------------- |
| sub           | ユーザーID     |
| email         | メールアドレス |
| role          | ロール         |
| department_id | 所属部門ID     |

---

## 10. フロントエンド連携

フロントエンドでは、ログイン成功後に `access_token` を保持する。

## 保存先

第1段階では既存PoCと同様に、フロントエンド側の状態管理に保持する。

```text
authStore
```

---

## APIリクエスト時

共通APIクライアントで Authorization Header を付与する。

```text
Authorization: Bearer <token>
```

---

## 11. 第1段階方針

第1段階では既存PoCの認証方式を維持する。

変更しない内容

- JWT認証
- Authorization Header
- ログインAPI
- レスポンス形式

---

## 12. 今後の改善候補

移植完了後、以下を検討する。

- HttpOnly Cookie化
- Refresh Token導入
- CSRF対策
- ログイン試行回数制限
- トークン失効管理
- パスワードリセット機能

---

## 13. まとめ

認証APIでは、既存PoCのJWT認証を維持し、
ASP.NET Core Web APIで同等のログイン処理を実装する。

第1段階では改善よりも既存仕様の再現を優先する。
