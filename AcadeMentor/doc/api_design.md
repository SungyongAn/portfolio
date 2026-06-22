# AcadeMentor API設計書

2026年5月

---

## 1. 設計方針

- **ベースURL**：`https://api.acade-mentor.app`
- **フレームワーク**：Python / FastAPI
- **認証方式**：JWT（Bearer Token）
- **データ形式**：JSON（ファイルアップロードはmultipart/form-data）
- **文字コード**：UTF-8

### 共通レスポンス形式

| ステータスコード | 意味 |
|---|---|
| 200 | 成功 |
| 201 | 作成成功 |
| 202 | 受付完了（非同期処理開始） |
| 400 | リクエスト不正（バリデーションエラー） |
| 401 | 認証エラー（トークンなし・期限切れ） |
| 403 | 権限エラー（アクセス不可） |
| 404 | リソースが存在しない |
| 500 | サーバーエラー |

### 認証が必要なエンドポイント

全リクエストのヘッダーに以下を付与する。

```
Authorization: Bearer {access_token}
```

---

## 2. エンドポイント一覧

| グループ | メソッド | エンドポイント | 認証 | 説明 |
|---|---|---|---|---|
| 認証 | POST | /api/auth/register | 不要 | 新規登録 |
| 認証 | POST | /api/auth/login | 不要 | ログイン |
| 認証 | POST | /api/auth/logout | 共通 | ログアウト |
| 認証 | POST | /api/auth/refresh | 共通 | トークン更新 |
| ユーザー | GET | /api/users/me | 共通 | 自分のプロフィール取得 |
| ユーザー | GET | /api/users/children | 保護者 | 子ども一覧取得 |
| ユーザー | POST | /api/users/children | 保護者 | 子どもの追加・紐付け |
| ユーザー | DELETE | /api/users/children/{child_id} | 保護者 | 子どもとの紐付け解除 |
| 過去問 | GET | /api/past-exams | 保護者 | 過去問一覧取得 |
| 過去問 | POST | /api/past-exams | 保護者 | 過去問アップロード＋AI分析開始 |
| 過去問 | GET | /api/past-exams/{id} | 保護者 | 過去問詳細・AI分析結果取得 |
| 過去問 | DELETE | /api/past-exams/{id} | 保護者 | 過去問削除 |
| 問題 | POST | /api/questions/generate | 子ども | 問題をAIで生成してDBに保存 |
| 問題 | GET | /api/questions/{id} | 子ども | 問題詳細取得 |
| 問題 | GET | /api/questions/{id}/explanation | 子ども | 解説・ポイント取得 |
| 回答 | POST | /api/answers | 子ども | 回答送信・採点・unit_stats更新 |
| 回答 | GET | /api/answers/history | 子ども | 回答履歴一覧取得 |
| 進捗 | GET | /api/progress/summary | 子ども | サマリー取得（ホーム画面用） |
| 進捗 | GET | /api/progress/units | 子ども | 単元別正答率一覧取得 |
| 進捗 | GET | /api/progress/calendar | 子ども | 学習カレンダーデータ取得 |
| 進捗 | GET | /api/progress/parent/{child_id} | 保護者 | 保護者向け進捗データ取得 |
| 進捗 | GET | /api/progress/parent/{child_id}/screen-time | 保護者 | 画面別滞在時間取得 |
| 画面ログ | POST | /api/screen-logs/enter | 子ども | 画面遷移時のログ記録 |
| 画面ログ | PUT | /api/screen-logs/{id}/leave | 子ども | 画面離脱時のログ更新 |

---

## 3. エンドポイント詳細

### 3-1. 認証 /api/auth

---

#### POST /api/auth/register　新規登録

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "parent",
  "name": "たろう"
}
```

**Response 201**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "parent",
  "name": "たろう",
  "created_at": "2026-05-22T10:00:00Z"
}
```

**エラー**
- 400：メール重複・バリデーションエラー

---

#### POST /api/auth/login　ログイン

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response 200**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "role": "parent",
    "name": "たろう"
  }
}
```

**エラー**
- 401：メールアドレスまたはパスワードが正しくない

---

#### POST /api/auth/refresh　トークン更新

**Request Header**
```
Authorization: Bearer {access_token}
```

**Response 200**
```json
{
  "access_token": "new_jwt_token",
  "token_type": "bearer"
}
```

**エラー**
- 401：トークンが無効または期限切れ

---

### 3-2. ユーザー /api/users

---

#### GET /api/users/me　自分のプロフィール取得

**Response 200**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "parent",
  "name": "たろう",
  "created_at": "2026-05-22T10:00:00Z"
}
```

---

#### GET /api/users/children　紐付けられた子ども一覧取得（保護者のみ）

**Response 200**
```json
{
  "children": [
    {
      "child_id": "uuid",
      "name": "たろう",
      "nickname": "たろうくん",
      "is_primary": true
    },
    {
      "child_id": "uuid",
      "name": "はなこ",
      "nickname": "はなちゃん",
      "is_primary": true
    }
  ]
}
```

---

#### POST /api/users/children　子どもアカウントの追加・紐付け（保護者のみ）

**Request Body**
```json
{
  "child_email": "child@example.com",
  "nickname": "たろうくん",
  "is_primary": true
}
```

**Response 201**
```json
{
  "relation_id": "uuid",
  "child_id": "uuid",
  "name": "たろう",
  "nickname": "たろうくん",
  "is_primary": true,
  "created_at": "2026-05-22T10:00:00Z"
}
```

**エラー**
- 404：子どものメールアドレスが存在しない
- 403：roleがchildでない

---

#### DELETE /api/users/children/{child_id}　子どもとの紐付け解除（保護者のみ）

**Response 200**
```json
{
  "message": "紐付けを解除しました"
}
```

**エラー**
- 404：紐付けが存在しない

---

### 3-3. 過去問 /api/past-exams

---

#### GET /api/past-exams　アップロード済み過去問一覧取得（保護者のみ）

**Query Parameters**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| child_id | uuid | ✅ | 対象の子どものID |
| question_type | string | ❌ | calc / shape / text / special |
| exam_year | integer | ❌ | 試験年度 |

**Response 200**
```json
{
  "past_exams": [
    {
      "id": "uuid",
      "question_type": "calc",
      "exam_year": 2024,
      "file_name": "2024_calc.pdf",
      "analysis_status": "done",
      "analysis_result": {
        "units": ["分数の計算", "四則混合"],
        "difficulty": "medium_hard"
      },
      "created_at": "2026-05-10T10:00:00Z"
    }
  ]
}
```

---

#### POST /api/past-exams　過去問アップロード＋AI分析開始（保護者のみ）

**Request（multipart/form-data）**

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| file | file | ✅ | PDF / PNG / JPG（最大50MB） |
| child_id | uuid | ✅ | 対象の子どものID |
| question_type | string | ✅ | calc / shape / text / special |
| exam_year | integer | ✅ | 試験年度 |

**Response 202**
```json
{
  "id": "uuid",
  "analysis_status": "analyzing",
  "message": "アップロード完了。AI分析を開始しました。"
}
```

**補足**
- 202（Accepted）を返しAI分析は非同期で実行
- 分析完了後にanalysis_statusをdoneに更新

**エラー**
- 400：ファイル形式・サイズ不正

---

#### GET /api/past-exams/{id}　過去問詳細・AI分析結果取得（保護者のみ）

**Response 200**
```json
{
  "id": "uuid",
  "question_type": "calc",
  "exam_year": 2024,
  "file_name": "2024_calc.pdf",
  "analysis_status": "done",
  "analysis_result": {
    "units": ["分数の計算", "四則混合"],
    "difficulty": "medium_hard",
    "frequency": {
      "分数の計算": 8,
      "四則混合": 3
    },
    "notes": "分数と小数の混合計算が頻出"
  },
  "created_at": "2026-05-10T10:00:00Z"
}
```

**エラー**
- 404：過去問が存在しない
- 403：他の保護者の過去問へのアクセス不可

---

#### DELETE /api/past-exams/{id}　過去問削除（保護者のみ）

**Response 200**
```json
{
  "message": "過去問を削除しました"
}
```

**補足**
- 関連するquestionsレコードも合わせて削除する

---

### 3-4. 問題 /api/questions

---

#### POST /api/questions/generate　問題をAIで生成してDBに保存（子どものみ）

**Request Body**
```json
{
  "mode": "auto",
  "question_type": "text",
  "unit": "旅人算",
  "count": 10
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| mode | string | ✅ | auto（おまかせ）/ manual（種別指定） |
| question_type | string | ❌ | modeがmanualの場合のみ指定 |
| unit | string | ❌ | 単元名（任意） |
| count | integer | ✅ | 生成問題数（5 / 10 / 15 / 20） |

**Response 201**
```json
{
  "questions": [
    {
      "id": "uuid",
      "question_type": "text",
      "unit": "旅人算",
      "difficulty": "medium",
      "question_text": "A君は時速4kmで...",
      "answer_unit": "km",
      "created_at": "2026-05-22T10:00:00Z"
    }
  ]
}
```

**補足**
- modeがautoの場合はunit_statsの弱点データをもとにAIが種別・単元を自動選択

---

#### GET /api/questions/{id}　問題詳細取得（子どものみ）

**Response 200**
```json
{
  "id": "uuid",
  "question_type": "text",
  "unit": "旅人算",
  "difficulty": "medium",
  "question_text": "A君は時速4kmで...",
  "answer_unit": "km"
}
```

**補足**
- 正解（correct_answer）はセキュリティのためレスポンスに含めない

---

#### GET /api/questions/{id}/explanation　解説・ポイント取得（子どものみ）

**Response 200**
```json
{
  "correct_answer": "15",
  "answer_unit": "km",
  "explanation": [
    {
      "step": 1,
      "title": "2人の速さを確認する",
      "description": "反対方向に歩くので合計になります",
      "formula": "4 + 6 = 10 km/時"
    },
    {
      "step": 2,
      "title": "時間を単位変換する",
      "description": "30分 = 0.5時間",
      "formula": "1時間30分 = 1.5時間"
    },
    {
      "step": 3,
      "title": "距離を求める",
      "description": "距離 = 速さ × 時間",
      "formula": "10 × 1.5 = 15km"
    }
  ],
  "point": "反対方向は速さの合計、同方向は差を使います"
}
```

**補足**
- answer_logsに回答済みレコードがあることを確認してからレスポンスを返す

---

### 3-5. 回答 /api/answers

---

#### POST /api/answers　回答送信・採点・unit_stats更新（子どものみ）

**Request Body**
```json
{
  "question_id": "uuid",
  "user_answer": "15",
  "time_spent_sec": 48
}
```

**Response 200**
```json
{
  "answer_log_id": "uuid",
  "is_correct": true,
  "correct_answer": "15",
  "answer_unit": "km",
  "unit_stats": {
    "question_type": "text",
    "unit": "旅人算",
    "total_count": 22,
    "correct_count": 13,
    "accuracy_rate": 0.5909
  }
}
```

**補足**
- 採点後にunit_statsをリアルタイム更新
- time_spent_secが600秒超の場合は異常値として除外しDBには保存しない

---

#### GET /api/answers/history　回答履歴一覧取得（子どものみ）

**Query Parameters**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| date | string | ❌ | 日付絞り込み（例：2026-05-22） |
| question_type | string | ❌ | calc / shape / text / special |
| limit | integer | ❌ | 取得件数（デフォルト：20） |
| offset | integer | ❌ | オフセット（デフォルト：0） |

**Response 200**
```json
{
  "total": 160,
  "answers": [
    {
      "answer_log_id": "uuid",
      "question_id": "uuid",
      "question_type": "text",
      "unit": "旅人算",
      "user_answer": "15",
      "is_correct": true,
      "time_spent_sec": 48,
      "answered_at": "2026-05-22T10:05:00Z"
    }
  ]
}
```

---

### 3-6. 進捗 /api/progress

---

#### GET /api/progress/summary　サマリー取得（子ども向けホーム画面用）

**Query Parameters**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| date | string | ❌ | 対象日（デフォルト：今日） |

**Response 200**
```json
{
  "today": {
    "answer_count": 18,
    "accuracy_rate": 0.78,
    "is_studied": true
  },
  "streak_days": 7,
  "total_answer_count": 160,
  "weak_units": [
    {
      "question_type": "shape",
      "unit": "複合図形の面積",
      "accuracy_rate": 0.48
    },
    {
      "question_type": "special",
      "unit": "旅人算",
      "accuracy_rate": 0.52
    }
  ]
}
```

---

#### GET /api/progress/units　単元別正答率一覧取得（子ども向け進捗画面用）

**Query Parameters**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| question_type | string | ❌ | calc / shape / text / special |
| sort | string | ❌ | accuracy_asc（デフォルト）/ accuracy_desc |

**Response 200**
```json
{
  "type_summary": {
    "calc": 0.88,
    "shape": 0.48,
    "text": 0.72,
    "special": 0.52
  },
  "units": [
    {
      "question_type": "shape",
      "unit": "複合図形の面積",
      "total_count": 25,
      "correct_count": 12,
      "accuracy_rate": 0.48,
      "accuracy_rate_prev_week": 0.43,
      "last_practiced_at": "2026-05-22T10:00:00Z"
    }
  ]
}
```

---

#### GET /api/progress/calendar　学習カレンダーデータ取得（子ども向け進捗画面用）

**Query Parameters**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| weeks | integer | ❌ | 取得週数（デフォルト：4） |

**Response 200**
```json
{
  "calendar": [
    {
      "date": "2026-05-22",
      "answer_count": 18,
      "level": 3
    },
    {
      "date": "2026-05-21",
      "answer_count": 0,
      "level": 0
    }
  ]
}
```

**補足**
- levelは回答数に応じて0（なし）〜3（多い）の4段階で返す

---

#### GET /api/progress/parent/{child_id}　保護者向け子どもの進捗データ取得（保護者のみ）

**Query Parameters**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| period | string | ❌ | week / month / all（デフォルト：month） |

**Response 200**
```json
{
  "child": { "id": "uuid", "name": "たろう" },
  "summary": {
    "study_time_sec": 16320,
    "answer_count": 160,
    "accuracy_rate": 0.72,
    "streak_days": 7,
    "prev_period_accuracy_rate": 0.69
  },
  "weekly_study_time": [
    { "day": "Mon", "study_time_sec": 1080 },
    { "day": "Tue", "study_time_sec": 1440 },
    { "day": "Wed", "study_time_sec": 0 },
    { "day": "Thu", "study_time_sec": 720 },
    { "day": "Fri", "study_time_sec": 1920 },
    { "day": "Sat", "study_time_sec": 1200 },
    { "day": "Sun", "study_time_sec": 0 }
  ],
  "type_accuracy": {
    "calc": 0.88,
    "shape": 0.48,
    "text": 0.72,
    "special": 0.52
  },
  "weak_units": [
    {
      "question_type": "shape",
      "unit": "複合図形の面積",
      "accuracy_rate": 0.48,
      "accuracy_rate_prev_week": 0.43
    }
  ],
  "alerts": [
    {
      "type": "accuracy_down",
      "unit": "旅人算",
      "message": "旅人算の正答率が先週より5%下がっています"
    }
  ]
}
```

**エラー**
- 403：紐付けのない子どものデータへのアクセス不可

---

#### GET /api/progress/parent/{child_id}/screen-time　画面別滞在時間取得（保護者のみ）

**Query Parameters**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| period | string | ❌ | week / month / all（デフォルト：month） |

**Response 200**
```json
{
  "screen_time": {
    "exercise": 13860,
    "explanation": 2460,
    "progress": 780,
    "home": 480
  },
  "avg_time_per_answer_sec": 100
}
```

---

### 3-7. 画面ログ /api/screen-logs

---

#### POST /api/screen-logs/enter　画面遷移時のログ記録（子どものみ）

**Request Body**
```json
{
  "screen_name": "exercise"
}
```

**Response 201**
```json
{
  "screen_log_id": "uuid",
  "screen_name": "exercise",
  "entered_at": "2026-05-22T10:00:00Z"
}
```

**補足**
- フロントエンドが画面遷移時に自動で呼び出す
- 返却されたscreen_log_idをフロント側で保持する

---

#### PUT /api/screen-logs/{id}/leave　画面離脱時のログ更新（子どものみ）

**Path Parameter**
- `id`：enterで返却されたscreen_log_id

**Response 200**
```json
{
  "screen_log_id": "uuid",
  "screen_name": "exercise",
  "entered_at": "2026-05-22T10:00:00Z",
  "left_at": "2026-05-22T10:24:00Z",
  "duration_sec": 1440
}
```

**補足**
- フロントエンドがページ離脱時（beforeunload）に自動で呼び出す

---

## 4. 未確定事項

| 項目 | 内容 |
|---|---|
| ファイル保存先 | 過去問ファイルはDBには保存せずOracle Cloud Object Storageに保存する方針。詳細は実装フェーズで検討 |
| AI分析の非同期処理 | POST /api/past-examsのAI分析はバックグラウンドタスクで実行。完了通知の方法（ポーリング or WebSocket）は実装フェーズで検討 |
| レートリミット | Claude API呼び出しの頻度制限。実装フェーズで検討 |