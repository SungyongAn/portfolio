
---

# api.md

---

## 1. API概要
- ベースURL：/api
- 認証方式：JWT（Access + Refresh）
- データ形式：JSON
- 認証必須APIは Authorization ヘッダーを使用

```コード
Authorization: Bearer {access_token}
```

---

## 2. 認証系API

---

### 2.1 ログイン

### POST /api/auth/login

### 認証
不要

### Request
```JSON
{
  "email": "EmailStr",
  "password": "str"
}
```

### Response
```JSON
{
  "access_token": "str",
  "user_id": "int",
  "grade": "int | null",
  "name": "str",
  "role": "member | manager | coach | director"
  
}
```

### エラー
- 認証失敗

---

### 2.2 トークン再発行

### POST /api/auth/refresh

### 認証

Refreshトークン（HttpOnly Cookie）

### Request
```JSON
{
}
```

### Response
```JSON
{
  "access_token": "str"
}
```

---

### 2.3 ログアウト

### POST /api/auth/logout

### 認証
必要（全ロール）

### Request
```JSON
{
}
```

### Response
```JSON
{
  "message": "logged out"
}
```

---

## 3 承認フロー管理

---

### 3.1 承認フロー発行（マネージャー→部員への確認依頼）

### POST /api/measurements/{measurement_id}/submit

### 認証
必要

### ロール
manager
- 測定記録を部員確認待ち状態にする

### Request
```JSON
{
}
```

### Response
```JSON
{
  "measurement_id": "int",
  "message": "str"
}
```

### 3.2 部員承認・否認

### PATCH /api/measurements/{measurement_id}/member-approve

### 認証
必要

### ロール
member

- 部員が承認または否認する

### 3.3 コーチ最終承認・否認

### PATCH /api/measurements/{measurement_id}/coach-approve

### 認証
必要

### ロール
coach
- コーチが最終承認または否認する

### 3.2・3.3 共通Request
```Json
{
  "action": "approve | reject"
}
```

### 共通Response
```Json
{
  "message": "str",
  "status": "pending_member | pending_coach | approved | rejected"
}
```

---

## 4. 部員管理

---

### 4.1 部員作成

### POST /api/users

### 認証
必要

### ロール
coach | director

### Request
```JSON
{
  "email": "EmailStr",
  "name": "str",
  "grade": "int",
  "password": "str",
  "role": "str"
}
```

### Response
```JSON
{
  "message": "str"
}
```

---

### 4.2 部員一覧取得

### GET /api/users?role=member

### 認証
必要

### ロール
manager | coach | director

### Request
```JSON
{
}
```

### Response
```JSON
{
  "user_id": "int",
  "email": "EmailStr",
  "memberName": "str",
  "grade": "int",
  "role": "str"
}
```

### 4.3 部員ステータス更新

### PATCH /api/users/{user_id}/status

### 認証
必要

### ロール
coach | director

### Request
```JSON
{
  "status": "retired | withdrawn"
}
```

### Response
```JSON
{
  "message": "str"
}
```

---

## 5. 測定記録管理

---
### 5.1 測定記録登録
### POST /api/measurements

### 認証
必要

### ロール
manager

### Request
```JSON
{
  "user_id": "int",
  "measurement_date": "date",
  "sprint_50m": "float",
  "base_running": "float",
  "throwing_distance": "float",
  "pitch_speed": "float",
  "batting_speed": "float",
  "swing_speed": "float",
  "bench_press": "float",
  "squat": "float",
}
```

### Response
```JSON
{
  "measurement_id": "int",
  "message": "str"
}
```

### 5.2 測定記録取得
### GET /api/measurements

### 認証
必要（全ロール）

### 備考
- バックエンドでJWTトークンのロールを検証し返却データを制御する
  - member：自身の測定記録のみ返す
  - manager | coach | director：全部員の測定記録を返す

### Request
```JSON
{
}
```

### Response
```JSON
{
    "measurements": [
    {
      "measurement_id": "int",
      "user_id": "int",
      "name": "str",
      "grade": "int",
      "measurement_date": "date",
      "sprint_50m": "float",
      "base_running": "float",
      "throwing_distance": "float",
      "pitch_speed": "float",
      "batting_speed": "float",
      "swing_speed": "float",
      "bench_press": "float",
      "squat": "float",
      "status": "pending_member | pending_coach | approved | rejected"
    }
  ]
}
```



### 備考
- 測定記録の閲覧・グラフ表示の両方で使用する
- グラフ描画はフロントエンド側で処理する
- 初回アクセス時に全データを一括取得する
- 本番運用時はデータ量に応じてページネーション対応を検討する
```
