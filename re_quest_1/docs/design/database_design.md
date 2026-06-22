# database_design.md

# データベース設計書

## 1. 概要

本ドキュメントは、`re_quest1` におけるデータベース設計の概要を定義する。

既存の `quest_1` で利用していた MySQL のテーブル構成を基準とし、
第1段階ではテーブル構成・カラム構成を大きく変更せず、
ASP.NET Core / Entity Framework Core で再実装する。

---

## 2. 使用DB

```text id="9o40ms"
MySQL 8
```

---

## 3. 設計方針

第1段階では、既存PoCのDB構造を原則維持する。

### 維持する内容

- テーブル構成
- 主キー
- 外部キー
- カラム名
- ステータス値
- ロール値
- 初期データ構成

### 変更を避ける内容

- テーブル統合
- テーブル分割
- カラム名変更
- リレーション変更
- ステータス値変更
- ロール値変更

---

## 4. 詳細設計

詳細は以下のファイルを参照する。

| ファイル                | 内容                         |
| ----------------------- | ---------------------------- |
| `database/tables.md`    | テーブル・カラム設計         |
| `database/relations.md` | ER概要・リレーション設計     |
| `database/indexes.md`   | インデックス・制約・命名方針 |
| `database/seed_data.md` | 初期データ方針               |

---

## 5. DB設計の全体像

```text id="mmrgms"
departments
  └─ users
        ├─ projects
        │     ├─ project_budgets
        │     │     ├─ worklogs
        │     │     └─ expenses
        │     └─ tasks
        │
        └─ notifications
```

---

## 6. 主要テーブル

| テーブル名      | 概要         |
| --------------- | ------------ |
| departments     | 部門情報     |
| users           | ユーザー情報 |
| projects        | 案件情報     |
| project_budgets | 案件予算情報 |
| tasks           | タスク情報   |
| worklogs        | 工数情報     |
| expenses        | 経費情報     |
| notifications   | 通知情報     |

---

## 7. EF Core 実装方針

ASP.NET Core 版では Entity Framework Core を使用する。

### 方針

- Entity クラスでテーブル構造を表現する
- DbContext でリレーションを定義する
- EF Core Migrations でスキーマ変更を管理する
- 第1段階では既存DB構造を優先し、過度な設計変更は行わない

---

## 8. 命名方針

詳細は `database/indexes.md` を参照する。

### DB

既存構成に合わせ、スネークケースを維持する。

例：

```text id="kym7av"
project_budgets
department_id
created_at
```

### C# Entity

C# 側では PascalCase を使用する。

例：

```text id="wdl4od"
ProjectBudget
DepartmentId
CreatedAt
```

---

## 9. 移植時の注意点

- 既存DB構造との差分を増やさない
- 既存APIレスポンスに影響するカラム名は維持する
- decimal 型の精度に注意する
- 日付型と日時型を明確に分ける
- 外部キー削除時の挙動を明確にする
- enum 値は文字列として扱い、既存値を維持する

---

## 10. 今後の改善候補

第1段階の移植完了後、以下を検討する。

- enum の正式導入
- 論理削除カラムの追加
- 監査ログテーブルの追加
- 承認履歴テーブルの追加
- 通知テンプレート管理
- タスク依存関係管理
- 工数入力履歴の詳細化
- 金額計算ロジックのDB依存削減

---

## 11. まとめ

第1段階では、既存 `quest_1` のDB構造を維持し、
ASP.NET Core / Entity Framework Core で同等のデータ管理を再現する。

DB設計の改善は移植完了後に行い、まずは既存PoCと同じ挙動を実現することを優先する。
