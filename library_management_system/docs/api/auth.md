# 認証 API

ベースパス： `/api/auth`

| メソッド | パス | 概要 | 認証 |
|---------|------|------|------|
| POST | `/login` | ログイン・トークン発行 | 不要 |
| POST | `/logout` | ログアウト・Refresh Token削除 | 必要 |
| POST | `/refresh` | Access Token更新 | Cookie |
| GET | `/me` | 自分のユーザー情報取得 | 必要 |
| PATCH | `/password` | パスワード変更 | 必要 |
| POST | `/password-reset/request` | パスワードリセット申請（メール送信） | 不要 |
| POST | `/password-reset/execute` | パスワードリセット実行 | 不要 |

### GET /me
**Response**
```
user_id, role, is_committee, school_id, name, grade, class_name
```

### POST /password-reset/request
**Request**
```
email
```
**Response**
```
message（"送信しました"固定・メールアドレスの存在有無を返さない）
```

### POST/password-reset/execute
**Request**
```
token, new_password
```
**Response**
```
message（成功時）/ エラー（トークン無効・期限切れ・使用済み）
```

### POST /login
**Request**
```
email, password
```
**Response**
```
access_token, expires_in, user_id, role, is_committee, school_id, name
```

### POST /refresh
**Cookie**: `refresh_token`（HttpOnly）
**Response**
```
access_token, expires_in
```

### PATCH /password
**Request**
```
current_password, new_password
```

---

## 関連ユースケース

- UC-01 ログイン
- UC-02 パスワードリセット申請
- UC-03 パスワードリセット実行
- UC-04 パスワード変更