# 教師担当設計書（Teacher Assignment Design）

本ドキュメントは、教師の担当情報（担任・教科・学年主任等）の
データ設計およびバリデーション設計方針を整理するものである。

本設計は CHANGELOG（2026/01/20〜2026/02/06）の設計変更を統合した結果である。

---

## 1. 背景

当初設計では、教師の教科情報を文字列で保持していたが、
以下の課題があった。

- 表記揺れが発生する
- 拡張（有効/無効管理）が困難
- 検索・集計が複雑

---

## 2. 設計方針

- 教師の担当情報は **正規化されたマスタ構造**で管理する
- 担当種別（assignment_type）によって **必須項目を変える**
- DB 制約ではなく **Service 層で意味的整合性を担保**する
- **1人の教師が複数の割当を持つことを許可**する
- 複数割当がある場合、**優先順位ルール**に基づいて代表割当を決定する

---

## 3. テーブル構成

### 3.1 subjects（教科マスタ）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | INT | 主キー |
| name | VARCHAR(50) | 教科名（UNIQUE） |
| is_active | BOOLEAN | 有効/無効管理 |

### 3.2 teacher_assignments

| カラム | 型 | 説明 |
|--------|-----|------|
| id | INT | 主キー |
| teacher_id | INT | 教師ID（users.id） |
| assignment_type | ENUM | 担当種別 |
| grade_id | INT | 学年ID（NULL可） |
| class_id | INT | クラスID（NULL可） |
| subject_id | INT | 教科ID（NULL可） |
| is_primary | BOOLEAN | 主担当フラグ |

**複合ユニーク制約:**
- (teacher_id, assignment_type, grade_id, class_id, subject_id)
  - 同一の組み合わせの重複登録を防止

---

## 4. assignment_type 別設計

### 4.1 homeroom（担任）

- **grade_id：必須**
- **class_id：必須**
- subject_id：NULL
- **is_primary：1クラスにつき1人のみ TRUE**
- 同じクラスに複数の担任が割り当てられる場合、1人だけが is_primary = TRUE

### 4.2 subject（教科担当）

- **grade_id：必須**
- **class_id：必須**
- **subject_id：必須**
- is_primary：同じ教科の担当が複数いる場合の主担当を示す

### 4.3 grade_head（学年主任）

- **grade_id：必須**
- class_id：NULL
- subject_id：NULL
- is_primary：通常は TRUE（1学年に1人）

### 4.4 administrator（管理的役割）

- grade_id：NULL
- class_id：NULL
- subject_id：NULL
- is_primary：N/A

---

## 5. 複数割当の扱い

### 5.1 複数割当の例

1人の教師が以下のような複数の役割を持つことが可能：
```
teacher_id: 101
割当1: assignment_type=homeroom, grade_id=1, class_id=1, is_primary=TRUE  # 1年A組担任
割当2: assignment_type=subject, grade_id=1, class_id=2, subject_id=3      # 1年B組数学担当
割当3: assignment_type=grade_head, grade_id=1                              # 1学年主任
```

### 5.2 データモデルの責務分離

#### TeacherAssignmentSummary（事実データモデル）
- 教師が持つ**すべての割当の事実データ**を表現
- 1人の教師につき、複数のインスタンスが存在する
- **用途**: 詳細表示、編集画面、権限チェック
```python
class TeacherAssignmentSummary:
    assignment_type: str
    grade_id: int | None
    grade_name: str | None
    class_id: int | None
    class_name: str | None
    subject_id: int | None
    subject_name: str | None
    is_primary: bool
```

#### UserPrimaryAssignment（代表割当モデル）
- 複数割当の中から**優先順位ルールに基づき1件を選択**した代表割当
- **用途**: ユーザー一覧表示、ログイン時の初期ロール判定
```python
class UserPrimaryAssignment:
    assignment_type: str
    grade_id: int | None
    grade_name: str | None
    class_id: int | None
    class_name: str | None
    subject_id: int | None
    subject_name: str | None
```

---

## 6. 代表割当の決定ロジック

### 6.1 優先順位ルール

`resolve_teacher_primary_assignment()` 関数により、以下の優先順位で代表割当を決定：

1. **is_primary = TRUE の割当を優先**
2. is_primary が複数ある場合、**assignment_type の優先順位**：
   - `homeroom`（担任）> `grade_head`（学年主任）> `subject`（教科担当）> `administrator`
3. 同じ assignment_type が複数ある場合：
   - grade_id の昇順（低学年優先）
   - class_id の昇順（若いクラス番号優先）

### 6.2 実装場所

- `services/teacher_service.py` の `resolve_teacher_primary_assignment()`
- ログイン処理、ユーザー一覧取得処理から呼び出される
- フロントエンド側にロジックを持たせない設計

---

## 7. バリデーション設計

### 7.1 DB層の責務
- 外部キー整合性の保証
- 複合ユニーク制約による重複防止

### 7.2 Service層の責務
- assignment_type ごとの必須項目チェック
- is_primary フラグの一意性チェック（担任・学年主任）
- 意味的整合性の保証

### 7.3 バリデーションルール
```python
def validate_teacher_assignment(assignment):
    if assignment.type == "homeroom":
        assert assignment.grade_id is not None
        assert assignment.class_id is not None
        assert assignment.subject_id is None
        # 同じクラスに is_primary=True は1人まで
        
    elif assignment.type == "subject":
        assert assignment.grade_id is not None
        assert assignment.class_id is not None
        assert assignment.subject_id is not None
        
    elif assignment.type == "grade_head":
        assert assignment.grade_id is not None
        assert assignment.class_id is None
        assert assignment.subject_id is None
        # 同じ学年に is_primary=True は1人まで
        
    elif assignment.type == "administrator":
        assert assignment.grade_id is None
        assert assignment.class_id is None
        assert assignment.subject_id is None
```

---

## 8. API レスポンス設計

### 8.1 ログインレスポンス（LoginResponse）
```json
{
  "user": {
    "id": 101,
    "email": "teacher@example.com",
    "role": "teacher",
    "teacher_assignments": [
      {
        "assignment_type": "homeroom",
        "grade_name": "1年",
        "class_name": "A組",
        "is_primary": true
      },
      {
        "assignment_type": "subject",
        "grade_name": "1年",
        "class_name": "B組",
        "subject_name": "数学",
        "is_primary": false
      }
    ],
    "primary_assignment": {
      "assignment_type": "homeroom",
      "grade_name": "1年",
      "class_name": "A組"
    }
  }
}
```

### 8.2 管理者ユーザー一覧（AdminUserListResponse）
```json
{
  "users": [
    {
      "id": 101,
      "role": "teacher",
      "teacher_assignments": [...],  // 全割当
      "primary_assignment": {        // 代表割当
        "assignment_type": "homeroom",
        "grade_name": "1年",
        "class_name": "A組"
      }
    }
  ]
}
```

---

## 9. フロントエンド実装ガイドライン

### 9.1 一覧表示
- `primary_assignment` を使用
- ロール表示には `assignment_type` を日本語変換して表示

### 9.2 詳細表示・編集
- `teacher_assignments` （配列）を使用
- すべての割当を表示・編集可能にする

### 9.3 権限判定
- `teacher_assignments` 内を検索
- 例：「このクラスの担任か？」→ assignments 内に該当する homeroom があるかチェック

---

## 10. CHANGELOG との対応関係

| 日付 | 内容 |
|------|------|
| 2026/01/20 | 表示ロジック改善（`assignment_type` に基づく role 変換） |
| 2026/01/22 | `subjects` テーブル追加、文字列管理廃止 |
| 2026/02/05 | 複数割当対応、`TeacherAssignmentSummary` / `UserPrimaryAssignment` 分離 |
| 2026/02/05 | `resolve_teacher_primary_assignment()` 追加、優先順位ルール明示化 |
| 2026/02/06 | `LoginResponse` / `AdminUserListResponse` に `primary_assignment` 追加 |

---

## 11. 関連ドキュメント

- [ログインレスポンス設計](./login-response-design.md) - ログイン時のデータ構造詳細
- [認証設計](./auth-design.md) - トークン管理・認証アーキテクチャ

---