# component_design.md

# コンポーネント設計

## 1. 概要

本ドキュメントは、`re_quest1` の React フロントエンドにおけるコンポーネント設計を定義する。

第1段階では既存Vue版のコンポーネント構成を維持し、Reactコンポーネントへ移植する。

---

# 2. 基本方針

## 方針

- UI部品をコンポーネント化する
- 画面ロジックはPageまたはHookへ分離する
- 共通部品は `components/common` に配置する
- 機能固有部品は `features` 配下へ配置する
- 過度なコンポーネント分割は行わない

---

# 3. コンポーネント分類

```text
components/
├─ common
├─ dialogs
├─ drawers
├─ charts
└─ gantt
```

---

# 4. 共通コンポーネント

## 配置

```text
components/common/
```

---

## 想定コンポーネント

| コンポーネント | 用途             |
| -------------- | ---------------- |
| Loading        | ローディング表示 |
| ErrorMessage   | エラー表示       |
| EmptyState     | データなし表示   |
| Pagination     | ページネーション |
| ConfirmDialog  | 確認ダイアログ   |
| PageHeader     | 画面ヘッダー     |

---

# 5. Dialogコンポーネント

## 配置

```text
components/dialogs/
```

---

## 想定コンポーネント

| コンポーネント           | 用途           |
| ------------------------ | -------------- |
| NotificationDetailDialog | 通知詳細       |
| TaskDetailDialog         | タスク詳細     |
| ConfirmDialog            | 確認ダイアログ |

---

## 方針

- Dialog開閉状態は親コンポーネントで管理する
- Dialog内では状態を持ちすぎない

---

# 6. Drawerコンポーネント

## 配置

```text
components/drawers/
```

---

## 想定コンポーネント

| コンポーネント      | 用途         |
| ------------------- | ------------ |
| ProjectCreateDrawer | 案件申請     |
| NotificationDrawer  | モバイル通知 |

---

## 方針

- 一覧画面を維持したまま操作する
- 画面遷移を減らす

---

# 7. Chartコンポーネント

## 配置

```text
components/charts/
```

---

## 想定コンポーネント

| コンポーネント        | 用途       |
| --------------------- | ---------- |
| DepartmentBudgetChart | 部門別予算 |
| ProjectStatusChart    | 案件状況   |
| RiskProjectChart      | リスク案件 |

---

# 8. Ganttコンポーネント

## 配置

```text
components/gantt/
```

---

## 想定コンポーネント

| コンポーネント | 用途           |
| -------------- | -------------- |
| GanttChart     | ガントチャート |
| GanttTaskRow   | タスク行       |
| GanttHeader    | 日付ヘッダー   |

---

# 9. ダッシュボードコンポーネント

## 配置

```text
features/dashboard/components/
```

---

## 想定構成

```text
dashboard/
├─ SummaryCards
├─ ProjectListPanel
├─ TodayTasksPanel
├─ AlertPanel
├─ ApplicantDashboard
├─ DeptManagerDashboard
├─ HqManagerDashboard
└─ TaskMemberDashboard
```

---

# 10. 案件管理コンポーネント

## 配置

```text
features/projects/components/
```

---

## 想定構成

```text
projects/
├─ ProjectTable
├─ ProjectCard
├─ ProjectForm
├─ ProjectDetail
├─ ProjectStatusBadge
└─ ProjectCreateDrawer
```

---

# 11. タスク管理コンポーネント

## 配置

```text
features/tasks/components/
```

---

## 想定構成

```text
tasks/
├─ TaskTable
├─ TaskForm
├─ TaskDetailDialog
├─ TaskStatusBadge
└─ TaskProgressBar
```

---

# 12. 予算管理コンポーネント

## 配置

```text
features/budget/components/
```

---

## 想定構成

```text
budget/
├─ BudgetSummary
├─ BudgetTable
├─ WorklogTable
├─ ExpenseTable
└─ ConsumptionRateBadge
```

---

# 13. 通知コンポーネント

## 配置

```text
features/notifications/components/
```

---

## 想定構成

```text
notifications/
├─ NotificationPopover
├─ NotificationDrawer
├─ NotificationList
├─ NotificationItem
└─ NotificationDetailDialog
```

---

# 14. レイアウトコンポーネント

## 配置

```text
layouts/
```

---

## 想定構成

```text
layouts/
├─ MainLayout
├─ DashboardLayout
├─ AuthLayout
├─ Sidebar
└─ Header
```

---

# 15. Props設計方針

## 方針

- Propsは必要最小限にする
- 巨大なオブジェクトを渡しすぎない
- イベントは callback として渡す
- 状態管理はStoreまたは親で行う

---

## 例

```typescript
type ProjectTableProps = {
  projects: Project[];
  loading: boolean;
  onSelect: (id: number) => void;
};
```

---

# 16. Vue版との対応

| Vue        | React       |
| ---------- | ----------- |
| props      | props       |
| emit       | callback    |
| computed   | useMemo     |
| watch      | useEffect   |
| ref        | useRef      |
| composable | custom hook |

---

# 17. 第1段階方針

第1段階では既存Vue版の構成を維持する。

変更しない内容

- ダッシュボード構成
- Dialog構成
- Drawer構成
- 通知UI構成
- ガントチャート構成

---

# 18. 今後の改善候補

移植完了後に検討する。

- Atomic Design導入
- Compound Component化
- Storybook導入
- UIライブラリ共通化
- Component Test追加
- 再利用性向上

---

# 19. まとめ

React版では、

```text
common
dashboard
projects
tasks
budget
notifications
```

を中心にコンポーネントを構成する。

第1段階では既存Vue版のUI構造を維持し、同等の画面を再現する。
