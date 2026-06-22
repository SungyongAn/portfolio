# budget_api.md

# 予算API設計

## 1. 概要

本ドキュメントは、`re_quest1` における予算・工数・経費関連APIを定義する。

対象機能は以下とする。

* 予算取得
* 予算更新
* 工数登録
* 工数更新
* 工数削除
* 経費登録
* 経費更新
* 経費削除

第1段階では、既存 `quest_1` の予算管理仕様を維持し、
React + ASP.NET Core 版で同等の挙動を再現する。

---

## 2. 予算取得API

## Endpoint

```text
GET /api/projects/{id}/budget
```

---

## Path Parameter

| 項目 | 型    | 説明   |
| -- | ---- | ---- |
| id | long | 案件ID |

---

## Response

```json
{
  "id": 1,
  "project_id": 1,
  "budget_amount": 1000000,
  "unit_price": 800000,
  "planned_months": 1.25,
  "actual_months": 0.8,
  "actual_cost": 640000,
  "expense_cost": 50000,
  "total_actual": 690000,
  "consumption_rate": 69.0
}
```

---

## 3. 予算更新API

## Endpoint

```text
PUT /api/projects/{id}/budget
```

---

## Path Parameter

| 項目 | 型    | 説明   |
| -- | ---- | ---- |
| id | long | 案件ID |

---

## Request

```json
{
  "budget_amount": 1000000,
  "unit_price": 800000,
  "planned_months": 1.25
}
```

---

## Response

```json
{
  "success": true
}
```

---

## 4. 工数登録API

## Endpoint

```text
POST /api/worklogs
```

---

## Request

```json
{
  "project_budget_id": 1,
  "task_id": 1,
  "user_id": 3,
  "actual_months": 0.1,
  "work_date": "2026-05-01",
  "memo": "設計作業"
}
```

---

## Response

```json
{
  "id": 1
}
```

---

## 5. 工数更新API

## Endpoint

```text
PUT /api/worklogs/{id}
```

---

## Path Parameter

| 項目 | 型    | 説明   |
| -- | ---- | ---- |
| id | long | 工数ID |

---

## Request

```json
{
  "actual_months": 0.2,
  "work_date": "2026-05-02",
  "memo": "設計作業更新"
}
```

---

## Response

```json
{
  "success": true
}
```

---

## 6. 工数削除API

## Endpoint

```text
DELETE /api/worklogs/{id}
```

---

## Path Parameter

| 項目 | 型    | 説明   |
| -- | ---- | ---- |
| id | long | 工数ID |

---

## Response

```json
{
  "success": true
}
```

---

## 7. 経費登録API

## Endpoint

```text
POST /api/expenses
```

---

## Request

```json
{
  "project_budget_id": 1,
  "title": "クラウド利用料",
  "amount": 30000,
  "expense_date": "2026-05-01",
  "memo": "検証環境利用料"
}
```

---

## Response

```json
{
  "id": 1
}
```

---

## 8. 経費更新API

## Endpoint

```text
PUT /api/expenses/{id}
```

---

## Path Parameter

| 項目 | 型    | 説明   |
| -- | ---- | ---- |
| id | long | 経費ID |

---

## Request

```json
{
  "title": "クラウド利用料",
  "amount": 50000,
  "expense_date": "2026-05-02",
  "memo": "検証環境利用料更新"
}
```

---

## Response

```json
{
  "success": true
}
```

---

## 9. 経費削除API

## Endpoint

```text
DELETE /api/expenses/{id}
```

---

## Path Parameter

| 項目 | 型    | 説明   |
| -- | ---- | ---- |
| id | long | 経費ID |

---

## Response

```json
{
  "success": true
}
```

---

## 10. 集計項目

予算情報では以下の値を扱う。

| 項目               | 内容    |
| ---------------- | ----- |
| budget_amount    | 予算額   |
| unit_price       | 人月単価  |
| planned_months   | 予定人月  |
| actual_months    | 実績人月  |
| actual_cost      | 実績工数費 |
| expense_cost     | 経費合計  |
| total_actual     | 実績合計  |
| consumption_rate | 予算消化率 |

---

## 11. 計算方針

## 実績工数費

```text
actual_cost = actual_months * unit_price
```

---

## 実績合計

```text
total_actual = actual_cost + expense_cost
```

---

## 予算消化率

```text
consumption_rate = total_actual / budget_amount * 100
```

---

## 12. CPI計算

CPIはダッシュボードやアラート判定で使用する。

```text
CPI = progress / consumption_rate
```

---

## 13. バリデーション

## 予算

| 項目             | 条件     |
| -------------- | ------ |
| budget_amount  | 0以上    |
| unit_price     | 0以上    |
| planned_months | 0より大きい |

---

## 工数

| 項目            | 条件     |
| ------------- | ------ |
| actual_months | 0より大きい |
| work_date     | 必須     |

---

## 経費

| 項目           | 条件  |
| ------------ | --- |
| title        | 必須  |
| amount       | 0以上 |
| expense_date | 必須  |

---

## 14. 認可方針

## APPLICANT

* 自案件の予算情報を参照可能
* 原則として工数・経費の登録は不可

---

## DEPT_MANAGER

* 自部門案件の予算情報を参照可能
* 自部門案件の予算管理が可能

---

## HQ_MANAGER

* 全案件の予算情報を参照可能
* 全案件の予算管理が可能

---

## TASK_MEMBER

* 担当案件に紐づく工数登録が可能
* 担当外案件の工数登録は不可

---

## 15. IDOR対策

予算・工数・経費操作時は、必ず対象案件へのアクセス権限を確認する。

```text
Budget / Worklog / Expense 取得
 ↓

Project取得
 ↓

PermissionService
 ↓

権限確認
 ↓

許可
または
403
```

---

## 16. Controller

```text
BudgetController
WorklogController
ExpenseController
```

---

## 17. Service

```text
BudgetService
WorklogService
ExpenseService
PermissionService
```

---

## 18. Repository

```text
BudgetRepository
WorklogRepository
ExpenseRepository
ProjectRepository
```

---

## 19. エラーレスポンス

## 権限不足

```json
{
  "detail": "Forbidden"
}
```

Status:

```text
403 Forbidden
```

---

## データなし

```json
{
  "detail": "Budget not found"
}
```

Status:

```text
404 Not Found
```

---

## バリデーションエラー

```json
{
  "detail": "Validation Error"
}
```

Status:

```text
422 Validation Error
```

---

## 20. 第1段階方針

既存PoCの予算管理仕様を維持する。

変更しない内容

* APIパス
* 予算計算方針
* 工数管理
* 経費管理
* CPI計算
* 権限制御
* IDOR対策

---

## 21. 今後の改善候補

移植完了後、以下を検討する。

* 工数入力履歴の詳細化
* 経費カテゴリ追加
* 予算変更履歴
* 承認済み予算の変更制御
* CPI計算の共通化
* 金額計算ロジックのテスト強化
* 小数計算の丸め方針明確化

---

## 22. まとめ

予算APIでは、案件ごとの予算・工数・経費を管理する。

第1段階では既存PoCの仕様を維持し、
React + ASP.NET Core 版で同等の予実管理を再現する。
