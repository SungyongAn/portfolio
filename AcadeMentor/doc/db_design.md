# AcadeMentor DB設計書

2026年5月

---

## 1. 設計方針

- **DB種別**：PostgreSQL
- **ORM**：SQLAlchemy（Python/FastAPI）
- **ホスティング**：Oracle Cloud
- **ID形式**：全テーブルでUUIDを使用
- **複数子ども対応**：保護者と子どもの紐付けを中間テーブル（parent_child_relations）で管理

---

## 2. テーブル一覧

| テーブル名 | 説明 |
|---|---|
| users | ユーザー（保護者・子ども共通） |
| parent_child_relations | 保護者と子どもの紐付け |
| past_exams | 過去問アップロード情報 |
| questions | AIが生成したオリジナル問題 |
| answer_logs | 子どもの回答履歴 |
| unit_stats | 単元別正答率の集計 |
| screen_logs | 画面別滞在時間のログ |

---

## 3. テーブル定義

### 3-1. users（ユーザー）

保護者・子どもを1テーブルで管理する。`role`カラムで種別を判定する。

| カラム名 | 型 | NOT NULL | 説明 |
|---|---|---|---|
| id | UUID | ✅ | ユーザーID（PK） |
| email | VARCHAR(255) | ✅ | メールアドレス（一意） |
| password_hash | VARCHAR(255) | ✅ | パスワード（ハッシュ） |
| role | ENUM('child','parent') | ✅ | 利用者種別 |
| name | VARCHAR(100) | ✅ | 表示名 |
| created_at | TIMESTAMP | ✅ | 登録日時 |
| updated_at | TIMESTAMP | ✅ | 更新日時 |

**インデックス**
- `email`：一意インデックス

---

### 3-2. parent_child_relations（保護者・子ども紐付け）

保護者と子どもの関係をN対Mで管理する中間テーブル。

| カラム名 | 型 | NOT NULL | 説明 |
|---|---|---|---|
| id | UUID | ✅ | 紐付けID（PK） |
| parent_id | UUID | ✅ | 保護者のユーザーID（FK: users.id） |
| child_id | UUID | ✅ | 子どものユーザーID（FK: users.id） |
| nickname | VARCHAR(100) | ❌ | 保護者が設定する子どもの呼び名 |
| is_primary | BOOLEAN | ✅ | 主担当保護者かどうか（デフォルト: true） |
| created_at | TIMESTAMP | ✅ | 紐付け日時 |

**インデックス**
- `(parent_id, child_id)`：複合一意インデックス（同じ組み合わせの重複を防ぐ）
- `parent_id`：保護者IDでの検索用
- `child_id`：子どもIDでの検索用

**ユースケース**
- 保護者1人が子ども2人を管理 → parent_child_relationsに2レコード追加
- 父・母それぞれが同じ子どもを確認 → child_idが同じレコードを2つ登録（is_primaryで主担当を識別）
- 保護者ダッシュボードで子どもを切り替え → parent_idで絞り込んで子ども一覧を取得

---

### 3-3. past_exams（過去問）

保護者がアップロードした過去問の情報とAI分析結果を管理する。

| カラム名 | 型 | NOT NULL | 説明 |
|---|---|---|---|
| id | UUID | ✅ | 過去問ID（PK） |
| parent_id | UUID | ✅ | アップロードした保護者ID（FK: users.id） |
| child_id | UUID | ✅ | 対象の子どものID（FK: users.id） |
| question_type | ENUM('calc','shape','text','special') | ✅ | 問題種別 |
| exam_year | INTEGER | ✅ | 試験年度 |
| file_name | VARCHAR(255) | ✅ | 元ファイル名 |
| analysis_status | ENUM('pending','analyzing','done') | ✅ | AI分析ステータス |
| analysis_result | JSONB | ❌ | AI分析結果（傾向・単元・難易度） |
| created_at | TIMESTAMP | ✅ | アップロード日時 |

**analysis_resultのJSON構造例**
```json
{
  "units": ["分数の計算", "小数のかけ算", "四則混合"],
  "difficulty": "medium_hard",
  "frequency": {
    "分数の計算": 8,
    "小数のかけ算": 5,
    "四則混合": 3
  },
  "notes": "分数と小数の混合計算が頻出"
}
```

**インデックス**
- `parent_id`：保護者IDでの検索用
- `child_id`：子どもIDでの検索用

---

### 3-4. questions（問題）

AIが生成したオリジナル問題を管理する。

| カラム名 | 型 | NOT NULL | 説明 |
|---|---|---|---|
| id | UUID | ✅ | 問題ID（PK） |
| past_exam_id | UUID | ✅ | 元の過去問ID（FK: past_exams.id） |
| question_type | ENUM('calc','shape','text','special') | ✅ | 問題種別 |
| unit | VARCHAR(100) | ✅ | 単元名（例：旅人算） |
| difficulty | ENUM('easy','medium','hard') | ✅ | 難易度 |
| question_text | TEXT | ✅ | 問題文（AI生成） |
| correct_answer | VARCHAR(255) | ✅ | 正解 |
| answer_unit | VARCHAR(50) | ❌ | 単位（cm²・kmなど） |
| explanation | JSONB | ✅ | ステップ解説 |
| point | TEXT | ✅ | この問題のポイント |
| created_at | TIMESTAMP | ✅ | 生成日時 |

**explanationのJSON構造例**
```json
[
  {
    "step": 1,
    "title": "2人の速さを確認する",
    "description": "反対方向に歩くので、離れる速さは2人の速さの合計になります。",
    "formula": "4 + 6 = 10 km/時"
  },
  {
    "step": 2,
    "title": "時間を単位変換する",
    "description": "1時間30分を時間単位に直します。",
    "formula": "1時間30分 = 1.5時間"
  },
  {
    "step": 3,
    "title": "距離を求める",
    "description": "距離 = 速さ × 時間 の公式を使います。",
    "formula": "10 × 1.5 = 15km"
  }
]
```

**インデックス**
- `past_exam_id`：過去問IDでの検索用
- `(question_type, unit)`：種別・単元での絞り込み用

---

### 3-5. answer_logs（回答履歴）

子どもの回答履歴を記録する。学習時間の計測にも使用する。

| カラム名 | 型 | NOT NULL | 説明 |
|---|---|---|---|
| id | UUID | ✅ | 回答履歴ID（PK） |
| child_id | UUID | ✅ | 回答した子どものID（FK: users.id） |
| question_id | UUID | ✅ | 問題ID（FK: questions.id） |
| user_answer | VARCHAR(255) | ✅ | 子どもの回答 |
| is_correct | BOOLEAN | ✅ | 正解かどうか |
| time_spent_sec | INTEGER | ✅ | 回答にかかった秒数 |
| answered_at | TIMESTAMP | ✅ | 回答日時 |

**補足**
- `time_spent_sec`は問題表示から回答送信までの秒数を計測
- 600秒（10分）以上の場合は異常値として除外する

**インデックス**
- `child_id`：子どもIDでの検索用
- `(child_id, answered_at)`：子どもの日別集計用
- `question_id`：問題IDでの検索用

---

### 3-6. unit_stats（単元別集計）

子どもの単元別正答率を集計して保持する。回答履歴から都度集計するのではなく、回答のたびに更新する。

| カラム名 | 型 | NOT NULL | 説明 |
|---|---|---|---|
| id | UUID | ✅ | 集計ID（PK） |
| child_id | UUID | ✅ | 子どものID（FK: users.id） |
| question_type | ENUM('calc','shape','text','special') | ✅ | 問題種別 |
| unit | VARCHAR(100) | ✅ | 単元名 |
| total_count | INTEGER | ✅ | 累計回答数（デフォルト: 0） |
| correct_count | INTEGER | ✅ | 正解数（デフォルト: 0） |
| accuracy_rate | DECIMAL(5,4) | ✅ | 正答率（0.0000〜1.0000） |
| last_practiced_at | TIMESTAMP | ✅ | 最終練習日時 |
| updated_at | TIMESTAMP | ✅ | 更新日時 |

**インデックス**
- `(child_id, accuracy_rate)`：苦手単元の抽出用
- `(child_id, question_type)`：種別別集計用

---

### 3-7. screen_logs（画面滞在ログ）

子どもの画面別滞在時間を記録する。保護者ダッシュボードの「画面別滞在時間」表示に使用する。

| カラム名 | 型 | NOT NULL | 説明 |
|---|---|---|---|
| id | UUID | ✅ | ログID（PK） |
| child_id | UUID | ✅ | 子どものID（FK: users.id） |
| screen_name | ENUM('home','exercise','explanation','progress') | ✅ | 画面名 |
| entered_at | TIMESTAMP | ✅ | 画面遷移した日時 |
| left_at | TIMESTAMP | ❌ | 画面を離れた日時 |
| duration_sec | INTEGER | ❌ | 滞在秒数（left_at確定後に計算） |

**インデックス**
- `(child_id, entered_at)`：子どもの日別・月別集計用

---

## 4. テーブル間のリレーション

```
users（parent）  ──N対M──  users（child）
                    ↑
          parent_child_relations

users（parent）  ──1対N──  past_exams
users（child）   ──1対N──  past_exams
past_exams       ──1対N──  questions
users（child）   ──1対N──  answer_logs
questions        ──1対N──  answer_logs
users（child）   ──1対N──  unit_stats
users（child）   ──1対N──  screen_logs
```

---

## 5. 未確定事項

| 項目 | 内容 |
|---|---|
| unit_statsの更新タイミング | 回答送信ごとにリアルタイム更新 or バッチ処理で定期更新。API設計フェーズで検討 |
| past_examsのファイル保存先 | ファイル本体はDBには保存せずOracle Cloud Object Storageに保存する方針。詳細はAPI設計フェーズで検討 |
| screen_logsの保持期間 | データ量が増えるため一定期間後にアーカイブまたは削除する方針。容量設計フェーズで検討 |