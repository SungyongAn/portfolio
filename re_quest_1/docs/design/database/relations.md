# relations.md

# リレーション設計

## 1. ER概要

```text
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

# 2. departments

## リレーション

| 関連テーブル | 関係  |
| ------------ | ----- |
| users        | 1対多 |
| projects     | 1対多 |

---

# 3. users

## リレーション

| 関連テーブル  | 関係  |
| ------------- | ----- |
| departments   | 多対1 |
| projects      | 1対多 |
| tasks         | 1対多 |
| worklogs      | 1対多 |
| notifications | 1対多 |

---

# 4. projects

## リレーション

| 関連テーブル        | 関係  |
| ------------------- | ----- |
| departments         | 多対1 |
| users(applicant_id) | 多対1 |
| users(owner_id)     | 多対1 |
| project_budgets     | 1対1  |
| tasks               | 1対多 |
| notifications       | 1対多 |

---

# 5. project_budgets

## リレーション

| 関連テーブル | 関係  |
| ------------ | ----- |
| projects     | 1対1  |
| worklogs     | 1対多 |
| expenses     | 1対多 |

---

# 6. tasks

## リレーション

| 関連テーブル       | 関係  |
| ------------------ | ----- |
| projects           | 多対1 |
| users(assignee_id) | 多対1 |
| worklogs           | 1対多 |

---

# 7. worklogs

## リレーション

| 関連テーブル    | 関係  |
| --------------- | ----- |
| project_budgets | 多対1 |
| tasks           | 多対1 |
| users           | 多対1 |

---

# 8. expenses

## リレーション

| 関連テーブル    | 関係  |
| --------------- | ----- |
| project_budgets | 多対1 |

---

# 9. notifications

## リレーション

| 関連テーブル | 関係  |
| ------------ | ----- |
| users        | 多対1 |
| projects     | 多対1 |

---

# 10. 主なリレーション一覧

```text
departments 1 ── * users
departments 1 ── * projects

users 1 ── * projects(applicant_id)
users 1 ── * projects(owner_id)
users 1 ── * tasks(assignee_id)
users 1 ── * worklogs
users 1 ── * notifications

projects 1 ── 1 project_budgets
projects 1 ── * tasks
projects 1 ── * notifications

project_budgets 1 ── * worklogs
project_budgets 1 ── * expenses

tasks 1 ── * worklogs
```

---

# 11. Entity Framework Core対応方針

## Navigation Property

Entity Framework Coreでは、各EntityにNavigation Propertyを定義する。

例：

```csharp
public class Project
{
    public long Id { get; set; }

    public ICollection<Task> Tasks { get; set; } = [];

    public ProjectBudget? ProjectBudget { get; set; }
}
```

---

## Fluent API

複雑なリレーションは `OnModelCreating()` で定義する。

例：

```csharp
modelBuilder.Entity<Project>()
    .HasOne(p => p.ProjectBudget)
    .WithOne(b => b.Project)
    .HasForeignKey<ProjectBudget>(b => b.ProjectId);
```

---

# 12. 第1段階方針

既存 `quest_1` のリレーション構造を維持する。

変更しない内容

- テーブル間の関係
- 主キー
- 外部キー
- 1対1構造
- 1対多構造

移植完了後に必要に応じて見直しを行う。

```

```
