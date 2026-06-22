# validation_design.md

# Validation設計

## 1. 概要

本ドキュメントは、`re_quest1` の ASP.NET Core Web API における入力値検証方針を定義する。

第1段階では、既存 `quest_1` で実装した Pydantic スキーマの入力値検証を、ASP.NET Core の DTO / DataAnnotations へ移植する。

---

# 2. 目的

Validationの目的は以下である。

- 不正な入力値をAPI側で拒否する
- フロントエンド制御だけに依存しない
- API直接リクエスト時の不正入力を防ぐ
- DB整合性を保つ
- セキュリティリスクを下げる

---

# 3. 基本方針

## 方針

- Request DTOで入力値検証を行う
- 必須項目には `Required` を設定する
- 数値範囲には `Range` を設定する
- 文字列長には `StringLength` を設定する
- 業務的な判定はService層で行う
- DB制約だけに依存しない

---

# 4. Validation実施場所

## Controller / DTO

形式的な入力値検証を行う。

例：

- 必須
- 文字列長
- 数値範囲
- 日付形式

---

## Service

業務的な入力値検証を行う。

例：

- ステータス遷移可否
- 承認可能状態か
- 担当者が存在するか
- 対象案件にアクセス可能か

---

# 5. Project Validation

## 対象DTO

```text
ProjectCreateRequest
ProjectUpdateRequest
```

---

## 検証項目

| 項目           | 条件           |
| -------------- | -------------- |
| name           | 必須           |
| budget_amount  | 0以上          |
| planned_months | 0より大きい    |
| progress       | 0〜100         |
| start_date     | end_date以前   |
| end_date       | start_date以降 |

---

## 補足

案件名は空文字を許可しない。

---

# 6. ProjectBudget Validation

## 対象DTO

```text
BudgetUpdateRequest
```

---

## 検証項目

| 項目           | 条件        |
| -------------- | ----------- |
| budget_amount  | 0以上       |
| unit_price     | 0以上       |
| planned_months | 0より大きい |

---

# 7. Task Validation

## 対象DTO

```text
TaskCreateRequest
TaskUpdateRequest
```

---

## 検証項目

| 項目       | 条件                 |
| ---------- | -------------------- |
| title      | 必須                 |
| progress   | 0〜100               |
| status     | TaskStatusのいずれか |
| start_date | due_date以前         |
| due_date   | start_date以降       |

---

## 補足

TASK_MEMBERは自分の担当タスクのみ更新可能とする。

この判定はValidationではなく、PermissionServiceで行う。

---

# 8. Worklog Validation

## 対象DTO

```text
WorklogCreateRequest
WorklogUpdateRequest
```

---

## 検証項目

| 項目          | 条件                                         |
| ------------- | -------------------------------------------- |
| actual_months | 0より大きい                                  |
| work_date     | 必須                                         |
| task_id       | 存在する場合は対象タスクへのアクセス権が必要 |

---

# 9. Expense Validation

## 対象DTO

```text
ExpenseCreateRequest
ExpenseUpdateRequest
```

---

## 検証項目

| 項目         | 条件  |
| ------------ | ----- |
| title        | 必須  |
| amount       | 0以上 |
| expense_date | 必須  |

---

# 10. Approval Validation

## 対象DTO

```text
ApprovalRequest
RejectRequest
```

---

## 検証項目

| 項目       | 条件           |
| ---------- | -------------- |
| comment    | 任意           |
| project_id | 存在する案件ID |

---

## 業務検証

| 処理     | 条件                           |
| -------- | ------------------------------ |
| 部門承認 | PENDING_DEPTのみ               |
| 本部承認 | PENDING_HQのみ                 |
| 却下     | PENDING_DEPT または PENDING_HQ |
| 着手     | APPROVEDのみ                   |
| 完了     | IN_PROGRESSのみ                |

---

# 11. Notification Validation

## 対象DTO

```text
NotificationReadRequest
```

---

## 検証項目

| 項目            | 条件                 |
| --------------- | -------------------- |
| notification_id | 存在する通知ID       |
| user_id         | ログインユーザー本人 |

---

# 12. DataAnnotations例

## Required

```csharp
[Required]
public string Name { get; set; } = string.Empty;
```

---

## Range

```csharp
[Range(0, double.MaxValue)]
public decimal BudgetAmount { get; set; }
```

---

## Progress

```csharp
[Range(0, 100)]
public int Progress { get; set; }
```

---

# 13. 業務Validation例

## ステータス遷移

```text
現在ステータス
 ↓

操作内容
 ↓

許可される遷移か確認
 ↓

許可
または
ValidationException
```

---

# 14. エラーレスポンス

## バリデーションエラー

```json
{
  "detail": "Validation Error"
}
```

---

## Status

```text
422 Validation Error
```

---

# 15. Controllerでの扱い

ControllerではDTOを受け取り、ModelStateの検証結果を利用する。

## 方針

- DTOで形式検証
- Serviceで業務検証
- 例外はMiddlewareで共通レスポンス化

---

# 16. Serviceでの扱い

Serviceでは業務ルールに基づくValidationを行う。

## 例

- 承認可能ステータスか
- 完了可能ステータスか
- 対象データが存在するか
- 操作者に権限があるか

---

# 17. DB制約との関係

ValidationはDB制約の前段として機能する。

## 方針

- 入力値はDTOで検証する
- 整合性はDB制約でも守る
- Serviceで業務的なルールを守る

---

# 18. 第1段階方針

既存PoCのValidationルールを維持する。

変更しない内容

- name必須
- progress 0〜100
- budget_amount 0以上
- unit_price 0以上
- planned_months 0より大きい
- actual_months 0より大きい
- expense amount 0以上

---

# 19. 今後の改善候補

移植完了後に検討する。

- FluentValidation導入
- バリデーションメッセージ統一
- 多言語対応
- フロントエンドとの共通スキーマ管理
- OpenAPIとの連携
- Zodとの整合性確保

---

# 20. まとめ

ValidationはAPIの安全性とデータ整合性を守るために実施する。

第1段階では既存PoCで強化した入力値検証をASP.NET CoreのDTO / DataAnnotationsで再現する。
