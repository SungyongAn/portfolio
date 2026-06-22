# routing_design.md

# ルーティング設計

## 1. 概要

本ドキュメントは、`re_quest1` の React フロントエンドにおけるルーティング設計を定義する。

既存Vue版のURL構成・画面遷移を維持し、React Routerで再実装する。

---

# 2. 使用技術

```text
React Router
```

---

# 3. 基本方針

第1段階では既存Vue版のルーティングを維持する。

変更しない内容

- URL構成
- 画面遷移
- 認証ガード
- ロール別アクセス制御
- Query Parameter による表示切替

---

# 4. ルート一覧

| パス                      | 画面              | 認証 | 概要               |
| ------------------------- | ----------------- | ---- | ------------------ |
| `/login`                  | LoginPage         | 不要 | ログイン画面       |
| `/`                       | DashboardPage     | 必要 | ダッシュボード     |
| `/?view=projects`         | DashboardPage     | 必要 | 案件一覧表示       |
| `/?action=create-project` | DashboardPage     | 必要 | 案件申請Drawer表示 |
| `/projects/:id`           | ProjectDetailPage | 必要 | 案件詳細           |
| `/approvals`              | ApprovalPage      | 必要 | 承認画面           |
| `/budget`                 | BudgetListPage    | 必要 | 予算一覧           |
| `/members/tasks`          | TaskFormPage      | 必要 | メンバータスク     |

---

# 5. 認証ガード

認証が必要な画面では `ProtectedRoute` を使用する。

## 方針

- 未ログインの場合は `/login` へ遷移する
- ログイン済みの場合は対象画面を表示する
- 認証状態は `authStore` から取得する

---

## ProtectedRoute例

```text
ProtectedRoute
 ├─ DashboardPage
 ├─ ProjectDetailPage
 ├─ ApprovalPage
 ├─ BudgetListPage
 └─ TaskFormPage
```

---

# 6. ロール別ルーティング

ロールによってアクセス可能な画面を制御する。

## APPLICANT

| パス                      | 可否 |
| ------------------------- | ---- |
| `/`                       | ○    |
| `/?view=projects`         | ○    |
| `/?action=create-project` | ○    |
| `/projects/:id`           | ○    |
| `/approvals`              | ×    |
| `/budget`                 | △    |
| `/members/tasks`          | ×    |

---

## DEPT_MANAGER

| パス              | 可否 |
| ----------------- | ---- |
| `/`               | ○    |
| `/?view=projects` | ○    |
| `/projects/:id`   | ○    |
| `/approvals`      | ○    |
| `/budget`         | ○    |
| `/members/tasks`  | ×    |

---

## HQ_MANAGER

| パス              | 可否 |
| ----------------- | ---- |
| `/`               | ○    |
| `/?view=projects` | ○    |
| `/projects/:id`   | ○    |
| `/approvals`      | ○    |
| `/budget`         | ○    |
| `/members/tasks`  | ×    |

---

## TASK_MEMBER

| パス              | 可否 |
| ----------------- | ---- |
| `/`               | ○    |
| `/?view=projects` | △    |
| `/projects/:id`   | ○    |
| `/approvals`      | ×    |
| `/budget`         | △    |
| `/members/tasks`  | ○    |

---

# 7. Query Parameter設計

## 案件一覧表示

```text
/?view=projects
```

DashboardPage内で案件一覧パネルを表示する。

---

## 案件申請Drawer表示

```text
/?action=create-project
```

DashboardPage内で案件申請Drawerを開く。

---

# 8. 案件詳細

```text
/projects/:id
```

## 処理

```text
URLからid取得
 ↓

ProjectDetailPage
 ↓

projectApi.getProject(id)
 ↓

表示
```

---

# 9. 404対応

存在しないルートの場合は、NotFoundPageを表示する。

## 方針

- 未定義パスは NotFoundPage
- 認証切れの場合は LoginPage
- 権限不足の場合は ForbiddenPage または DashboardPage へ戻す

---

# 10. AppRoutes構成

```text
routes/
├─ AppRoutes.tsx
├─ ProtectedRoute.tsx
└─ RoleRoute.tsx
```

---

# 11. AppRoutes責務

- ルーティング定義
- 認証ガード適用
- ロールガード適用
- NotFound処理

---

# 12. ProtectedRoute責務

- 認証状態確認
- 未ログイン時のリダイレクト
- 認証済み画面の表示

---

# 13. RoleRoute責務

- ロール別アクセス可否判定
- 権限不足時の処理
- メニュー表示制御との整合性維持

---

# 14. Vue RouterからReact Routerへの対応

| Vue Router        | React Router         |
| ----------------- | -------------------- |
| router/index.ts   | routes/AppRoutes.tsx |
| meta.requiresAuth | ProtectedRoute       |
| meta.roles        | RoleRoute            |
| route.params.id   | useParams            |
| route.query       | useSearchParams      |
| router.push       | useNavigate          |

---

# 15. 第1段階方針

既存Vue版のURL構成を維持する。

変更しない内容

- `/`
- `/login`
- `/projects/:id`
- `/approvals`
- `/budget`
- `/members/tasks`
- `/?view=projects`
- `/?action=create-project`

---

# 16. 今後の改善候補

移植完了後に検討する。

- URL設計の再整理
- 案件一覧専用ページ化
- 申請ページ専用URL化
- Nested Routes導入
- Layout Route導入
- 権限不足画面の改善
- Query Parameter管理の共通化

---

# 17. まとめ

React版では React Router を使用し、既存Vue版のURL構成・画面遷移を維持する。

第1段階では、ルーティング改善よりも既存PoCとの互換性を優先する。
