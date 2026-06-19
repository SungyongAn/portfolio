import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { UserRole } from "@/api/models/UserRole";

//  meta型拡張
declare module "vue-router" {
  interface RouteMeta {
    requiresAuth?: boolean;
    requiresGuest?: boolean;
    roles?: UserRole[];
    title?: string;
    breadcrumbs?: { name: string; to?: string }[];
  }
}

//  routes定義
const routes: RouteRecordRaw[] = [
  // ログイン
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/auth/LoginView.vue"),
    meta: { requiresGuest: true, title: "ログイン" },
  },

  // ダッシュボード
  {
    path: "/",
    name: "dashboard",
    component: () => import("@/views/DashboardView.vue"),
    meta: {
      requiresAuth: true,
      title: "ダッシュボード",
      breadcrumbs: [{ name: "ダッシュボード" }],
    },
  },

  // 案件
  {
    path: "/projects",
    name: "projects",
    component: () => import("@/views/projects/ProjectListView.vue"),
    meta: {
      requiresAuth: true,
      title: "案件一覧",
      breadcrumbs: [{ name: "ダッシュボード", to: "/" }, { name: "案件一覧" }],
    },
  },
  {
    path: "/projects/new",
    name: "project-new",
    component: () => import("@/views/projects/ProjectNewView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.APPLICANT],
      title: "案件申請",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "案件申請" },
      ],
    },
  },
  {
    path: "/projects/create",
    name: "project-create-legacy",
    component: () => import("@/views/NotFoundView.vue"),
    meta: {
      requiresAuth: true,
      title: "404",
    },
  },
  {
    path: "/projects/:projectId",
    name: "project-detail",
    component: () => import("@/views/projects/ProjectDetailView.vue"),
    meta: {
      requiresAuth: true,
      title: "案件詳細",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "案件詳細" },
      ],
    },
  },

  // 承認・却下
  {
    path: "/projects/:projectId/approval",
    name: "project-approval",
    component: () => import("@/views/approval/ApprovalView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.DEPT_MANAGER, UserRole.HQ_MANAGER],
      title: "承認・却下",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "承認・却下" },
      ],
    },
  },

  // タスク
  {
    path: "/projects/:projectId/tasks/new",
    name: "task-new",
    component: () => import("@/views/tasks/TaskFormView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.APPLICANT],
      title: "タスク登録",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "タスク登録" },
      ],
    },
  },
  {
    path: "/members/tasks",
    name: "member-tasks",
    component: () => import("@/views/members/MemberTaskView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.DEPT_MANAGER],
      title: "メンバータスク状況",
    },
  },

  // 予算管理
  {
    path: "/projects/:projectId/budget",
    name: "budget",
    component: () => import("@/views/budget/BudgetView.vue"),
    meta: {
      requiresAuth: true,
      title: "予算管理",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "予算管理" },
      ],
    },
  },
  {
    path: "/projects/:projectId/budget/worklogs/new",
    name: "worklog-new",
    component: () => import("@/views/budget/WorklogFormView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.APPLICANT],
      title: "工数実績入力",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "予算管理", to: "/projects/:projectId/budget" },
        { name: "工数実績入力" },
      ],
    },
  },
  {
    path: "/projects/:projectId/budget/worklogs/:worklogId/edit",
    name: "worklog-edit",
    component: () => import("@/views/budget/WorklogFormView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.APPLICANT],
      title: "工数実績編集",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "予算管理" },
        { name: "工数実績編集" },
      ],
    },
  },
  {
    path: "/projects/:projectId/budget/expenses/new",
    name: "expense-new",
    component: () => import("@/views/budget/ExpenseFormView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.APPLICANT],
      title: "直接経費入力",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "予算管理", to: "/projects/:projectId/budget" },
        { name: "直接経費入力" },
      ],
    },
  },
  {
    path: "/projects/:projectId/budget/expenses/:expenseId/edit",
    name: "expense-edit",
    component: () => import("@/views/budget/ExpenseFormView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.APPLICANT],
      title: "直接経費編集",
      breadcrumbs: [
        { name: "ダッシュボード", to: "/" },
        { name: "案件一覧", to: "/projects" },
        { name: "予算管理" },
        { name: "直接経費編集" },
      ],
    },
  },

  {
    path: "/budget",
    name: "budget-list",
    component: () => import("@/views/budget/BudgetListView.vue"),
    meta: {
      requiresAuth: true,
      roles: [UserRole.HQ_MANAGER, UserRole.DEPT_MANAGER],
      title: "予算管理",
    },
  },

  // 通知
  {
    path: "/notifications",
    name: "notifications",
    component: () => import("@/views/NotificationView.vue"),
    meta: {
      requiresAuth: true,
      title: "通知一覧",
      breadcrumbs: [{ name: "ダッシュボード", to: "/" }, { name: "通知一覧" }],
    },
  },

  // 404
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/views/NotFoundView.vue"),
  },
];

//  router生成
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

//  ナビゲーションガード
router.beforeEach(async (to) => {
  const authStore = useAuthStore();

  // 初期化（初回のみ）
  if (!authStore.isInitialized) {
    await authStore.initAuth();
  }

  // タイトル設定
  if (to.meta.title) {
    document.title = `${to.meta.title} | 開発管理システム`;
  }

  // 認証ガード
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { path: "/login" };
  }

  // ロール別アクセス制御
  if (
    to.meta.roles &&
    authStore.role &&
    !to.meta.roles.includes(authStore.role)
  ) {
    return { path: "/" };
  }

  // ログイン済みのログイン画面アクセス防止
  if (to.path === "/login" && authStore.isAuthenticated) {
    return { path: "/" };
  }
});

export default router;
