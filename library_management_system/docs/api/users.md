# ユーザー管理 API

ベースパス：`/api/users`

| メソッド | パス         | 概要               | 権限  |
| -------- | ------------ | ------------------ | ----- |
| GET      | `/`          | 生徒一覧取得       | admin |
| POST     | `/`          | 生徒アカウント登録 | admin |
| GET      | `/{user_id}` | 生徒詳細取得       | admin |
| DELETE   | `/{user_id}` | 生徒アカウント削除 | admin |

### GET /

**Query**

```
school_id, name, email, page, per_page
```

**Response**

```
users: [{ id, school_id, school_name, email, name, role, is_committee, grade, class_name, is_active, created_at }], total, page, per_page
```

### POST /

**Request**

```
school_id, email, name, role, is_committee, grade, class_name, password
```

### DELETE /{user_id}

- 貸出中資料がある場合は400エラーを返す

---

## 関連ユースケース

- UC-26 生徒アカウント登録
- UC-27 生徒アカウント削除
- UC-28 生徒一覧取得
- UC-29 生徒詳細取得
