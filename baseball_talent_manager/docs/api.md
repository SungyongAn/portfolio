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
{}
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
{}
```

### Response
```JSON
{
  "message": "logged out"
}
```

---

## 3. 承認フロー管理

---

### 3.1 承認フロー発行（マネージャー→部員への確認依頼）

### POST /api/measurements/{measurement_id}/submit

### 認証
必要

### ロール
manager

### 説明
測定記録を部員確認待ち状態にする

### Request
```JSON
{}
```

### Response
```JSON
{
  "measurement_id": "int",
  "message": "str"
}
```

---

### 3.2 部員承認・否認

### PATCH /api/measurements/{measurement_id}/member-approve

### 認証
必要

### ロール
member

### 説明
部員が承認または否認する

---

### 3.3 コーチ最終承認・否認

### PATCH /api/measurements/{measurement_id}/coach-approve

### 認証
必要

### ロール
coach

### 説明
コーチが最終承認または否認する

---

### 3.2・3.3 共通Request
```JSON
{
  "action": "approve | reject"
}
```

### 共通Response
```JSON
{
  "message": "str",
  "status": "pending_member | pending_coach | approved | rejected"
}
```

---

### 3.4 承認済みレコードの確認済みマーク

### PATCH /api/measurements/{measurement_id}/confirm

### 認証
必要

### ロール
manager

### 説明
- `approved` ステータスのレコードを確認済みとしてマークする
- `manager_confirmed` を `true` に更新し、`MeasurementStatusList` から非表示にする
- 既に確認済みのレコードに対しては400エラーを返す

### Request
```JSON
{}
```

### Response
```JSON
{
  "message": "str",
  "status": "approved"
}
```

### エラー
- 対象レコードが存在しない（404）
- ステータスが `approved` 以外（400）
- 既に確認済み（400）

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
{}
```

### Response
```JSON
{
  "user_id": "int",
  "email": "EmailStr",
  "name": "str",
  "grade": "int",
  "role": "str"
}
```

---

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

### 備考
- 同一部員・同一計測日の重複チェックを実施
- `rejected` ステータスのレコードが存在する場合は上書き更新して `draft` に戻す
- `draft` / `pending_member` / `pending_coach` / `approved` の場合は400エラーを返す

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
  "squat": "float"
}
```

### Response
```JSON
{
  "measurement_id": "int",
  "message": "str"
}
```

---

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
{}
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
      "status": "draft | pending_member | pending_coach | approved | rejected",
      "manager_confirmed": "bool"
    }
  ]
}
```

---

### 5.3 測定記録全件取得（可視化用）

### GET /api/measurements/all

### 認証
必要（全ロール）

### 備考
- ロールに関わらず全部員の測定記録を返す
- 可視化ダッシュボードのグラフ描画用途
- アクセス制御はバックエンド側で実施

### Request
```JSON
{}
```

### Response
5.2 と同じ形式

---

## 6. リアルタイム通知

---

### 6.1 WebSocket接続

### WebSocket /ws/notifications

### 認証
クエリパラメータでAccess Tokenを渡す

```
ws://host/ws/notifications?token={access_token}
```

### 説明
- 接続時にJWTトークンを検証し、ユーザーを特定する
- 承認フローのステータス変化をリアルタイムに通知する
- WebSocketはHTTPヘッダーを使用できないため、クエリパラメータでトークンを渡す方式を採用

### 通知イベント一覧

| イベント | 通知先 | type フィールド |
|---------|--------|---------------|
| マネージャーが承認フロー発行 | 対象部員 | `approval_requested` |
| 部員が承認 | コーチ全員 | `approval_requested` |
| コーチが承認 | マネージャー全員・対象部員 | `approved` |
| コーチが否認 | マネージャー全員・対象部員 | `rejected` |

### 通知メッセージ形式
```JSON
{
  "type": "approval_requested | approved | rejected",
  "message": "str"
}
```

### 備考
- PoCのシングルワーカー構成では問題なく動作する
- 本番運用時の複数ワーカー構成ではRedis Pub/Subなどのメッセージブローカーの導入が必要

---

## 7. AIアドバイス

---

### 7.1 AIアドバイス取得

### POST /api/advice/{user_id}

### 認証
必要

### ロール
coach | director

### 説明
指定した部員の全測定記録をもとにGemini APIがアドバイスを生成する

### Request
```JSON
{}
```

### Response
```JSON
{
  "user_id": "int",
  "name": "str",
  "advice": "str"
}
```

### エラー
- 対象ユーザーが存在しない（404）
- 測定記録が存在しない（404）
- Gemini APIのレート制限超過（429）