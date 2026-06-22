# directory_structure.md

# ディレクトリ構成設計

## 1. 概要

本ドキュメントは、`re_quest1` の React フロントエンドにおけるディレクトリ構成を定義する。

第1段階では既存Vue版の責務を維持しつつ、Reactの一般的な構成へ移植する。

---

# 2. ディレクトリ構成

```text
frontend/
│
├─ public/
│
├─ src/
│
├─ api/
│
├─ assets/
│
├─ components/
│
├─ features/
│
├─ hooks/
│
├─ layouts/
│
├─ pages/
│
├─ routes/
│
├─ stores/
│
├─ types/
│
├─ utils/
│
├─ App.tsx
│
└─ main.tsx
```

---

# 3. src/api

## 役割

API通信処理を管理する。

---

## 構成例

```text
api/
├─ authApi.ts
├─ dashboardApi.ts
├─ projectApi.ts
├─ taskApi.ts
├─ budgetApi.ts
└─ notificationApi.ts
```

---

## 方針

- APIごとにファイル分割する
- fetch処理は apiClient に集約する
- UIから直接fetchしない

---

# 4. src/assets

## 役割

静的ファイルを管理する。

---

## 対象

```text
images
icons
fonts
```

---

# 5. src/components

## 役割

共通コンポーネントを管理する。

---

## 例

```text
components/
├─ common/
├─ dialogs/
├─ drawers/
├─ charts/
└─ gantt/
```

---

## 共通部品例

```text
Loading
ConfirmDialog
Pagination
EmptyState
ErrorMessage
```

---

# 6. src/features

## 役割

機能単位で管理する。

---

## 構成例

```text
features/
├─ auth/
├─ dashboard/
├─ projects/
├─ tasks/
├─ budget/
└─ notifications/
```

---

## 例

```text
projects/
├─ components/
├─ hooks/
├─ services/
├─ types/
└─ pages/
```

---

# 7. src/hooks

## 役割

カスタムHookを管理する。

---

## 例

```text
hooks/
├─ useAuth.ts
├─ useDashboard.ts
├─ useProjects.ts
├─ useTasks.ts
└─ useNotifications.ts
```

---

# 8. src/layouts

## 役割

画面共通レイアウトを管理する。

---

## 例

```text
layouts/
├─ MainLayout.tsx
├─ DashboardLayout.tsx
└─ AuthLayout.tsx
```

---

# 9. src/pages

## 役割

ルーティング対象画面を管理する。

---

## 例

```text
pages/
├─ LoginPage.tsx
├─ DashboardPage.tsx
├─ ProjectDetailPage.tsx
├─ ApprovalPage.tsx
├─ BudgetPage.tsx
└─ TaskPage.tsx
```

---

# 10. src/routes

## 役割

React Routerを管理する。

---

## 例

```text
routes/
├─ AppRoutes.tsx
├─ ProtectedRoute.tsx
└─ RoleRoute.tsx
```

---

# 11. src/stores

## 役割

Zustand Storeを管理する。

---

## 例

```text
stores/
├─ authStore.ts
├─ dashboardStore.ts
└─ notificationStore.ts
```

---

# 12. src/types

## 役割

TypeScript型定義を管理する。

---

## 例

```text
types/
├─ auth.ts
├─ dashboard.ts
├─ project.ts
├─ task.ts
├─ budget.ts
└─ notification.ts
```

---

# 13. src/utils

## 役割

共通処理を管理する。

---

## 例

```text
utils/
├─ apiClient.ts
├─ date.ts
├─ currency.ts
├─ permissions.ts
└─ constants.ts
```

---

# 14. Vue版との対応

| Vue版       | React版    |
| ----------- | ---------- |
| views       | pages      |
| components  | components |
| composables | hooks      |
| stores      | stores     |
| services    | api        |
| router      | routes     |
| types       | types      |

---

# 15. 実装方針

第1段階では過度な機能分割は行わない。

優先事項

```text
動作再現
↓
責務分離
↓
最適化
```

---

# 16. 今後の改善候補

移植完了後に検討する。

- Feature First構成への完全移行
- Atomic Design導入
- Storybook導入
- React Query導入
- Zustand Slice化
- Monorepo化

---

# 17. まとめ

React版では、

```text
api
components
pages
stores
routes
```

を中心に構成し、既存Vue版の責務を維持したまま移植を行う。

第1段階では、構成の美しさよりも既存PoCとの互換性を優先する。
