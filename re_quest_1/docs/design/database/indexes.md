# indexes.md

# インデックス・制約・命名方針

## 1. 概要

本ドキュメントは、`re_quest1` のデータベースにおける以下の方針を定義する。

- インデックス
- 制約
- バリデーション
- 命名規則

第1段階では、既存 `quest_1` のDB設計を維持しながら、
ASP.NET Core / Entity Framework Core で再実装する。

---

# 2. インデックス方針

検索・絞り込み・認可判定で利用するカラムにはインデックスを設定する。

## 方針

- ログイン検索に使うカラムに設定する
- ロール別・部門別検索に使うカラムに設定する
- 案件一覧の絞り込みに使うカラムに設定する
- タスク一覧や期限超過判定に使うカラムに設定する
- 通知取得や未読件数取得に使うカラムに設定する

---

# 3. users

## インデックス対象

| カラム        | 理由         |
| ------------- | ------------ |
| email         | ログイン検索 |
| role          | ロール別検索 |
| department_id | 部門別検索   |

## 一意制約

| カラム | 理由                         |
| ------ | ---------------------------- |
| email  | ログインIDとして利用するため |

---

# 4. projects

## インデックス対象

| カラム        | 理由             |
| ------------- | ---------------- |
| status        | ステータス別検索 |
| department_id | 部門別検索       |
| applicant_id  | 申請者別検索     |
| owner_id      | 責任者別検索     |

---

# 5. tasks

## インデックス対象

| カラム      | 理由             |
| ----------- | ---------------- |
| project_id  | 案件別検索       |
| assignee_id | 担当者別検索     |
| status      | ステータス別検索 |
| due_date    | 期限超過判定     |

---

# 6. notifications

## インデックス対象

| カラム     | 理由               |
| ---------- | ------------------ |
| user_id    | ユーザー別通知取得 |
| is_read    | 未読件数取得       |
| created_at | 新着順表示         |

---

# 7. project_budgets

## 一意制約

| カラム     | 理由                           |
| ---------- | ------------------------------ |
| project_id | 1案件につき予算情報は1件のため |

---

# 8. 外部キー制約

主要な関連には外部キー制約を設定する。

## 対象例

| テーブル        | カラム            | 参照先             |
| --------------- | ----------------- | ------------------ |
| users           | department_id     | departments.id     |
| projects        | department_id     | departments.id     |
| projects        | applicant_id      | users.id           |
| projects        | owner_id          | users.id           |
| project_budgets | project_id        | projects.id        |
| tasks           | project_id        | projects.id        |
| tasks           | assignee_id       | users.id           |
| worklogs        | project_budget_id | project_budgets.id |
| worklogs        | task_id           | tasks.id           |
| worklogs        | user_id           | users.id           |
| expenses        | project_budget_id | project_budgets.id |
| notifications   | user_id           | users.id           |
| notifications   | project_id        | projects.id        |

---

# 9. NOT NULL制約

業務上必須となる項目には `NOT NULL` を設定する。

## 例

| テーブル      | カラム        |
| ------------- | ------------- |
| users         | name          |
| users         | email         |
| users         | password_hash |
| users         | role          |
| projects      | name          |
| projects      | status        |
| projects      | department_id |
| projects      | applicant_id  |
| tasks         | title         |
| tasks         | status        |
| notifications | user_id       |
| notifications | type          |
| notifications | title         |
| notifications | message       |

---

# 10. バリデーション方針

DB制約だけでなく、アプリケーション側でも入力値検証を行う。

---

## projects

| 項目           | 条件        |
| -------------- | ----------- |
| name           | 必須        |
| budget_amount  | 0以上       |
| planned_months | 0より大きい |
| progress       | 0〜100      |

---

## project_budgets

| 項目           | 条件        |
| -------------- | ----------- |
| budget_amount  | 0以上       |
| unit_price     | 0以上       |
| planned_months | 0より大きい |

---

## tasks

| 項目     | 条件   |
| -------- | ------ |
| title    | 必須   |
| progress | 0〜100 |

---

## worklogs

| 項目          | 条件        |
| ------------- | ----------- |
| actual_months | 0より大きい |

---

## expenses

| 項目   | 条件  |
| ------ | ----- |
| amount | 0以上 |

---

# 11. 命名方針

## DB

既存構成に合わせ、スネークケースを維持する。

例：

```text id="l24s70"
project_budgets
department_id
created_at
```

---

## C# Entity

C# 側では PascalCase を使用する。

例：

```text id="0qejby"
ProjectBudget
DepartmentId
CreatedAt
```

---

## DTO

Request / Response DTO は用途が分かる名称にする。

例：

```text id="exm5h3"
ProjectCreateRequest
ProjectUpdateRequest
ProjectResponse
DashboardResponse
```

---

# 12. Entity Framework Core対応方針

## インデックス

EF Coreでは `OnModelCreating()` または属性でインデックスを定義する。

例：

```csharp id="vfc7xv"
modelBuilder.Entity<User>()
    .HasIndex(u => u.Email)
    .IsUnique();
```

---

## 外部キー

リレーションは `OnModelCreating()` で明示的に定義する。

例：

```csharp id="3d35ak"
modelBuilder.Entity<Project>()
    .HasOne(p => p.Department)
    .WithMany(d => d.Projects)
    .HasForeignKey(p => p.DepartmentId);
```

---

# 13. 第1段階方針

第1段階では、既存DB設計から大きな変更は行わない。

## 変更しない内容

- テーブル名
- カラム名
- 主キー
- 外部キー
- ロール値
- ステータス値

---

# 14. 今後の改善候補

移植完了後、以下を検討する。

- 論理削除カラム追加
- 監査ログテーブル追加
- enumの正式導入
- 複合インデックスの追加
- 承認履歴テーブルの追加
- 通知テンプレートテーブルの追加
- パフォーマンス確認後のインデックス最適化

---

# 15. まとめ

本設計では、既存PoCのDB構造を維持しつつ、
ASP.NET Core / Entity Framework Core で安全に移植できる構成を優先する。

インデックス・制約・バリデーションは、検索性・整合性・安全性を確保するために設定する。
