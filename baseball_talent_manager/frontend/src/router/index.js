import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      meta: { requiresAuth: true },
      component: { render: () => null },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
      meta: { requiresGuest: true },
    },

    // マネージャールート
    {
      path: "/manager",
      meta: { requiresAuth: true, role: "manager" },
      children: [
        {
          path: "dashboard",
          name: "manager-dashboard",
          component: () => import("@/views/manager/DashboardView.vue"),
          meta: {
            title: "ダッシュボード",
            breadcrumbs: [{ name: "ダッシュボード" }],
          },
        },
        {
          path: "record",
          name: "manager-record",
          component: () =>
            import("@/views/manager/MeasurementResultSubmit.vue"),
          meta: {
            title: "測定結果の入力",
            breadcrumbs: [{ name: "ダッシュボード", to: "/manager/dashboard" }],
          },
        },
        {
          path: "status",
          name: "manager-status",
          component: () => import("@/views/manager/MeasurementStatusList.vue"),
          meta: {
            title: "承認依頼中のステータス確認",
            breadcrumbs: [{ name: "ダッシュボード", to: "/manager/dashboard" }],
          },
        },
      ],
    },

    // 部員ルート
    {
      path: "/member",
      meta: { requiresAuth: true, role: "member" },
      children: [
        {
          path: "dashboard",
          name: "member-dashboard",
          component: () => import("@/views/shared/DashboardView.vue"),
          meta: {
            title: "ダッシュボード",
            breadcrumbs: [{ name: "ダッシュボード" }],
          },
        },
        {
          path: "review",
          name: "member-review",
          component: () => import("@/components/MeasurementResultReview.vue"),
          meta: {
            title: "測定結果の確認と承認",
            breadcrumbs: [{ name: "ダッシュボード", to: "/member/dashboard" }],
          },
        },
        {
          path: "history",
          name: "member-history",
          component: () => import("@/components/MeasurementResultList.vue"),
          meta: {
            title: "測定記録の閲覧",
            breadcrumbs: [{ name: "ダッシュボード", to: "/member/dashboard" }],
          },
        },
      ],
    },

    // コーチルート
    {
      path: "/coach",
      meta: { requiresAuth: true, role: "coach" },
      children: [
        {
          path: "dashboard",
          name: "coach-dashboard",
          component: () => import("@/views/shared/DashboardView.vue"),
          meta: {
            title: "ダッシュボード",
            breadcrumbs: [{ name: "ダッシュボード" }],
          },
        },
        {
          path: "review",
          name: "coach-review",
          component: () => import("@/components/MeasurementResultReview.vue"),
          meta: {
            title: "測定結果の確認と承認",
            breadcrumbs: [{ name: "ダッシュボード", to: "/coach/dashboard" }],
          },
        },
        {
          path: "history",
          name: "coach-history",
          component: () => import("@/components/MeasurementResultList.vue"),
          meta: {
            title: "測定記録の閲覧",
            breadcrumbs: [{ name: "ダッシュボード", to: "/coach/dashboard" }],
          },
        },

        {
          path: "members",
          name: "coach-members",
          component: () => import("@/components/MemberManagement.vue"),
          meta: {
            title: "部員管理",
            breadcrumbs: [{ name: "ダッシュボード", to: "/coach/dashboard" }],
          },
        },
        {
          path: "members/create",
          name: "coach-member-create",
          component: () => import("@/components/MemberCreate.vue"),
          meta: {
            title: "部員作成",
            breadcrumbs: [{ name: "部員管理", to: "/coach/members" }],
          },
        },
        {
          path: "members/retire",
          name: "coach-member-retire",
          component: () => import("@/components/MemberRetire.vue"),
          meta: {
            title: "部員退部・引退処理",
            breadcrumbs: [{ name: "部員管理", to: "/coach/members" }],
          },
        },
      ],
    },

    // 監督ルート
    {
      path: "/director",
      meta: { requiresAuth: true, role: "director" },
      children: [
        {
          path: "dashboard",
          name: "director-dashboard",
          component: () => import("@/views/shared/DashboardView.vue"),
          meta: {
            title: "ダッシュボード",
            breadcrumbs: [{ name: "ダッシュボード" }],
          },
        },
        {
          path: "history",
          name: "director-history",
          component: () => import("@/components/MeasurementResultList.vue"),
          meta: {
            title: "測定記録の閲覧",
            breadcrumbs: [
              { name: "ダッシュボード", to: "/director/dashboard" },
            ],
          },
        },
        {
          path: "members",
          name: "director-members",
          component: () => import("@/components/MemberManagement.vue"),
          meta: {
            title: "部員管理",
            breadcrumbs: [
              { name: "ダッシュボード", to: "/director/dashboard" },
            ],
          },
        },
        {
          path: "members/create",
          name: "director-member-create",
          component: () => import("@/components/MemberCreate.vue"),
          meta: {
            title: "部員作成",
            breadcrumbs: [{ name: "部員管理", to: "/director/members" }],
          },
        },
        {
          path: "members/retire",
          name: "director-member-retire",
          component: () => import("@/components/MemberRetire.vue"),
          meta: {
            title: "部員退部・引退処理",
            breadcrumbs: [{ name: "部員管理", to: "/director/members" }],
          },
        },
      ],
    },
    // === 404 ===
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("@/views/NotFoundView.vue"),
    },
  ],
});

// ナビゲーションガード
router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();

  // ログイン画面では初期化しない
  if (!authStore.isInitialized && to.name !== "login") {
    await authStore.initAuth();
  }

  // 未ログインで認証必須ページ
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login" };
  }

  // ログイン済みでゲスト専用ページ
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    const role = authStore.role;
    if (role === "manager") return "/manager/dashboard";
    if (role === "member") return "/member/dashboard";
    if (role === "coach") return "/coach/dashboard";
    if (role === "director") return "/director/dashboard";
    return "/";
  }

  // ルートアクセス時の振り分け
  if (to.path === "/") {
    if (!authStore.isAuthenticated) return "/login";
    const role = authStore.role;
    if (role === "manager") return "/manager/dashboard";
    if (role === "member") return "/member/dashboard";
    if (role === "coach") return "/coach/dashboard";
    if (role === "director") return "/director/dashboard";
    return "/login";
  }

  // ロール別アクセス制御
  if (to.meta.role && authStore.role !== to.meta.role) {
    const role = authStore.role;
    if (role === "manager") return "/manager/dashboard";
    if (role === "member") return "/member/dashboard";
    if (role === "coach") return "/coach/dashboard";
    if (role === "director") return "/director/dashboard";
    return "/login";
  }
});

export default router;
