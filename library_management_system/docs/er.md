# ER図・テーブル設計

## ER図

```
schools
  id (PK)
  name
  ┃
  ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ↓                               ↓
users                           books
  id (PK)                         id (PK)
  school_id (FK → schools)        school_id (FK → schools)
  email                           barcode (UNIQUE)
  name                            title
  role                            author
  password_hash                   isbn
  is_active                       ndc
  created_at                      publisher
  updated_at                      published_year
                                  status
                                  created_at
                                  updated_at
  ↓                               ↓
  ┣━━━━━━━━━━━━━━━┓               ┣━━━━━━━━━━━━━━━┓
  ↓               ↓               ↓               ↓
loans         reservations    loans         inter_library_requests
  id (PK)         id (PK)         id (PK)         id (PK)
  book_id(FK)     book_id(FK)     user_id(FK)     book_id (FK → books)
  user_id(FK)     user_id(FK)     ...             from_school_id (FK → schools)
  loaned_at       queue_order                     to_school_id (FK → schools)
  due_at          status                          requested_user_id (FK → users)
  returned_at     expires_at                      status
  created_at      created_at                      deadline
  updated_at      updated_at                      shipped_at
                                                  received_at
                                                  created_at
                                                  updated_at
```

---

## テーブル定義

### schools（学校）

| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | INT AUTO_INCREMENT | NOT NULL | 主キー |
| name | VARCHAR(100) | NOT NULL | 学校名 |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

---

### users（ユーザー）

| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | INT AUTO_INCREMENT | NOT NULL | 主キー |
| school_id | INT | NOT NULL | 所属校（FK → schools.id） |
| email | VARCHAR(255) | NOT NULL | メールアドレス（UNIQUE） |
| name | VARCHAR(100) | NOT NULL | 氏名 |
| role | ENUM('student','librarian','admin') | NOT NULL | ロール |
| password_hash | VARCHAR(255) | NOT NULL | Argon2ハッシュ |
| grade | TINYINT | NULL | 学年（studentのみ。1〜3） |
| class_name | VARCHAR(20) | NULL | クラス（studentのみ。例：A, B, 1組） |
| is_committee | TINYINT(1) | NOT NULL DEFAULT 0 | 図書委員フラグ（studentのみ有効。1:図書委員） |
| is_active | TINYINT(1) | NOT NULL | 有効フラグ（1:有効, 0:削除済） |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

**インデックス**
- UNIQUE: email
- INDEX: school_id
- INDEX: role

---

### books（資料）

| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | INT AUTO_INCREMENT | NOT NULL | 主キー |
| school_id | INT | NOT NULL | 所蔵校（FK → schools.id） |
| barcode | VARCHAR(50) | NOT NULL | バーコードID（UNIQUE） |
| title | VARCHAR(500) | NOT NULL | タイトル |
| author | VARCHAR(255) | NULL | 著者 |
| isbn | VARCHAR(20) | NULL | ISBN |
| ndc | VARCHAR(10) | NULL | NDC分類番号 |
| publisher | VARCHAR(255) | NULL | 出版社 |
| published_year | YEAR | NULL | 出版年 |
| status | ENUM('available','on_loan','reserved','disposed','inter_library') | NOT NULL | 貸出状態 |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

**インデックス**
- UNIQUE: barcode
- INDEX: school_id
- INDEX: status
- INDEX: ndc
- FULLTEXT: title, author（全文検索用）

---

### loans（貸出記録）

| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | INT AUTO_INCREMENT | NOT NULL | 主キー |
| book_id | INT | NOT NULL | 資料ID（FK → books.id） |
| user_id | INT | NOT NULL | 借りた生徒（FK → users.id） |
| loaned_at | DATETIME | NOT NULL | 貸出日時 |
| due_at | DATE | NOT NULL | 返却期限（貸出から2週間） |
| returned_at | DATETIME | NULL | 返却日時（NULL=未返却） |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

**インデックス**
- INDEX: book_id
- INDEX: user_id
- INDEX: returned_at（未返却検索用）
- INDEX: due_at（リマインド処理用）

---

### reservations（予約・順番待ち）

| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | INT AUTO_INCREMENT | NOT NULL | 主キー |
| book_id | INT | NOT NULL | 資料ID（FK → books.id） |
| user_id | INT | NOT NULL | 予約者（FK → users.id） |
| queue_order | INT | NOT NULL | 順番（1=次の予約者） |
| status | ENUM('waiting','ready','cancelled','completed') | NOT NULL | 予約状態 |
| notified_at | DATETIME | NULL | 準備完了通知日時 |
| expires_at | DATETIME | NULL | 自動キャンセル期限（notified_atから7日） |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

**インデックス**
- INDEX: book_id, queue_order
- INDEX: user_id
- INDEX: status
- INDEX: expires_at（自動キャンセル処理用）

---

### inter_library_requests（図書館間貸出）

| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | INT AUTO_INCREMENT | NOT NULL | 主キー |
| book_id | INT | NOT NULL | 資料ID（FK → books.id） |
| from_school_id | INT | NOT NULL | 送り出し校（FK → schools.id） |
| to_school_id | INT | NOT NULL | 受け取り校（FK → schools.id） |
| requested_user_id | INT | NOT NULL | 予約した生徒（FK → users.id） |
| status | ENUM('pending','confirmed','shipped','received','on_loan','returned','cancelled') | NOT NULL | 処理状態 |
| deadline | DATE | NOT NULL | 締め切り金曜日の日付 |
| shipped_at | DATETIME | NULL | 発送日時（金曜回収時） |
| received_at | DATETIME | NULL | 受取登録日時 |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

**インデックス**
- INDEX: book_id
- INDEX: from_school_id
- INDEX: to_school_id
- INDEX: requested_user_id
- INDEX: status
- INDEX: deadline（締め切り処理用）

---

### password_reset_tokens（パスワードリセットトークン）

| カラム名 | 型 | NULL | 説明 |
|---------|-----|------|------|
| id | INT AUTO_INCREMENT | NOT NULL | 主キー |
| user_id | INT | NOT NULL | 対象ユーザー（FK → users.id） |
| token | VARCHAR(255) | NOT NULL | リセットトークン（UNIQUE・ランダム生成） |
| expires_at | DATETIME | NOT NULL | 有効期限（発行から30分） |
| used_at | DATETIME | NULL | 使用日時（NULL=未使用） |
| created_at | DATETIME | NOT NULL | 作成日時 |

**インデックス**
- UNIQUE: token
- INDEX: user_id
- INDEX: expires_at（期限切れトークン削除用）

**補足**
- トークンは1回使用後に`used_at`を記録し、以降は無効とする
- 期限切れ・使用済みトークンは定期的に削除する

---

## ステータス管理方針

PoCのためシンプルな`status`カラム管理を採用する。

### books.status 遷移

```
available ──→ on_loan ──→ available
    │                         ↑
    └──→ reserved ────────────┘
    │         │
    │         └──→ inter_library（予約済み資料が図書館間貸出に回る場合）
    │
    └──→ inter_library（図書館間貸出中）
    │
    └──→ disposed（廃棄）
```

### reservations.status 遷移

```
waiting ──→ ready ──→ completed
    │            │
    └────────────┴──→ cancelled
```

### inter_library_requests.status 遷移

```
pending ──→ confirmed ──→ shipped ──→ received ──→ on_loan ──→ returned
    │             │
    └─────────────┴──→ cancelled
```

> `cancelled`への遷移は`pending`・`confirmed`のみ可能。`shipped`以降はキャンセル不可。

---

## 採番ルール（バーコード統合方針）

各校のバーコードIDが重複する可能性があるため、新システムでは以下のルールで採番する。

- フォーマット：`{学校コード2桁}-{連番6桁}`
- 例：A高校の1冊目 → `01-000001`
- 既存バーコードは`old_barcode`カラムに保持し、移行後に新採番を適用する