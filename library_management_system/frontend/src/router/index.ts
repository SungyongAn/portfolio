// ============================================================
// router/index.ts  —  ルーティング設定
// ============================================================

import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { LOGIN_ROUTE } from "@/constants";

// ── ルート定義 ────────────────────────────────────────────────

const routes: RouteRecordRaw[] = [
  // ── 未ログイン専用 ──────────────────────────────────────────
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/LoginView.vue"),
    meta: { requiresGuest: true, title: "ログイン" },
  },
  {
    path: "/password-reset/request",
    name: "PasswordResetRequest",
    component: () => import("@/views/PasswordResetRequestView.vue"),
    meta: { requiresGuest: true, title: "パスワードリセット申請" },
  },
  {
    path: "/password-reset/confirm",
    name: "PasswordResetConfirm",
    component: () => import("@/views/PasswordResetConfirmView.vue"),
    meta: { requiresGuest: true, title: "パスワードリセット実行" },
  },

  // ── 全ロール共通（要ログイン） ───────────────────────────────
  {
    path: "/books",
    name: "BookSearch",
    component: () => import("@/views/BookSearchView.vue"),
    meta: { requiresAuth: true, title: "資料検索" },
  },
  {
    path: "/books/:id",
    name: "BookDetail",
    component: () => import("@/views/BookDetailView.vue"),
    meta: { requiresAuth: true, title: "資料詳細" },
  },
  {
    path: "/password/change",
    name: "PasswordChange",
    component: () => import("@/views/PasswordChangeView.vue"),
    meta: { requiresAuth: true, title: "パスワード変更" },
  },

  // ── 生徒・図書委員 ──────────────────────────────────────────
  {
    path: "/dashboard",
    name: "StudentDashboard",
    component: () => import("@/views/student/DashboardView.vue"),
    meta: { requiresAuth: true, roles: ["student"], title: "ダッシュボード" },
  },
  {
    path: "/mypage",
    name: "MyPage",
    component: () => import("@/views/student/MyPageView.vue"),
    meta: { requiresAuth: true, roles: ["student"], title: "マイページ" },
  },
  {
    path: "/loans/checkout",
    name: "LoanCheckout",
    component: () => import("@/views/LoanCheckoutView.vue"),
    meta: {
      requiresAuth: true,
      roles: ["student", "librarian"],
      title: "貸出処理",
    },
  },
  {
    path: "/loans/return",
    name: "LoanReturn",
    component: () => import("@/views/LoanReturnView.vue"),
    meta: {
      requiresAuth: true,
      roles: ["student", "librarian"],
      title: "返却処理",
    },
  },
  {
    path: "/loan-management",
    name: "LoanManagementCommittee",
    component: () => import("@/views/student/LoanManagementView.vue"),
    meta: {
      requiresAuth: true,
      roles: ["student"],
      requiresCommittee: true,
      title: "貸出管理",
    },
  },

  // ── 司書 ────────────────────────────────────────────────────
  {
    path: "/librarian/dashboard",
    name: "LibrarianDashboard",
    component: () => import("@/views/librarian/DashboardView.vue"),
    meta: {
      requiresAuth: true,
      roles: ["librarian"],
      title: "ダッシュボード（司書）",
    },
  },
  {
    path: "/librarian/books",
    name: "BookManagement",
    component: () => import("@/views/librarian/BookManagementView.vue"),
    meta: { requiresAuth: true, roles: ["librarian"], title: "資料管理" },
  },
  {
    path: "/librarian/transfer",
    name: "TransferReceive",
    component: () => import("@/views/librarian/TransferReceiveView.vue"),
    meta: {
      requiresAuth: true,
      roles: ["librarian"],
      title: "送付リスト・受取登録",
    },
  },
  {
    path: "/librarian/loan-management",
    name: "LoanManagementLibrarian",
    component: () => import("@/views/librarian/LoanManagementView.vue"),
    meta: {
      requiresAuth: true,
      roles: ["librarian"],
      title: "貸出管理（司書）",
    },
  },

  // ── 管理者 ──────────────────────────────────────────────────
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: () => import("@/views/admin/DashboardView.vue"),
    meta: {
      requiresAuth: true,
      roles: ["admin"],
      title: "ダッシュボード（管理者）",
    },
  },
  {
    path: "/admin/students",
    name: "StudentAccountManagement",
    component: () => import("@/views/admin/StudentAccountView.vue"),
    meta: { requiresAuth: true, roles: ["admin"], title: "生徒アカウント管理" },
  },

  // ── リダイレクト ────────────────────────────────────────────
  {
    path: "/",
    redirect: LOGIN_ROUTE,
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: LOGIN_ROUTE,
  },
];

// ── ルーターインスタンス ──────────────────────────────────────

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// ── ナビゲーションガード ──────────────────────────────────────

router.beforeEach((to) => {
  const authStore = useAuthStore();

  // 未ログイン専用ルート：ログイン済みならダッシュボードへ
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    return authStore.defaultRoute;
  }

  // 要ログインルート：未ログインならログインページへ
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return { name: "Login", query: { redirect: to.fullPath } };
  }

  // ロール制限チェック
  if (to.meta.roles && authStore.user) {
    const allowedRoles = to.meta.roles as string[];
    if (!allowedRoles.includes(authStore.user.role)) {
      return authStore.defaultRoute;
    }
  }

  // 図書委員限定ルートのチェック
  if (to.meta.requiresCommittee && authStore.user) {
    if (!authStore.user.is_committee) {
      return authStore.defaultRoute;
    }
  }
});

// ── ページタイトル更新 ────────────────────────────────────────

router.afterEach((to) => {
  const title = to.meta.title as string | undefined;
  document.title = title ? `${title} | 図書館システム` : "図書館システム";
});

export default router;
