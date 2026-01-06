import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    // === 生徒用ルート ===
    {
      path: '/student',
      name: 'student',
      redirect: '/student/dashboard',
      meta: { requiresAuth: true, role: 'student' },
      children: [
        {
          path: 'dashboard',
          name: 'student-dashboard',
          component: () => import('@/views/student/DashboardView.vue')
        },
        {
          path: 'submit',
          name: 'student-submit',
          component: () => import('@/views/student/SubmitView.vue')
        },
        {
          path: 'history',
          name: 'student-history',
          component: () => import('@/views/student/HistoryView.vue')
        }
      ]
    },
    // === 教師用ルート ===
    {
      path: '/teacher',
      name: 'teacher',
      redirect: '/teacher/dashboard',
      meta: { requiresAuth: true, role: 'teacher' },
      children: [
        {
          path: 'dashboard',
          name: 'teacher-dashboard',
          component: () => import('@/views/teacher/DashboardView.vue')
        },
        {
          path: 'submissions/:classId',
          name: 'teacher-submissions',
          component: () => import('@/views/teacher/SubmissionsView.vue')
        },
        {
          path: 'unread',
          name: 'teacher-unread',
          component: () => import('@/views/teacher/UnreadView.vue')
        }
      ]
    },
    // === 管理者用ルート ===
    {
      path: '/admin',
      name: 'admin',
      redirect: '/admin/users',
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/admin/UserManagementView.vue')
        }
      ]
    },
    // === 404 ===
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue')
    }
  ]
})

// ナビゲーションガード
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const userRole = authStore.role

  // 認証が必要なページ
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      next('/login')
      return
    }

    // ロールチェック
    if (to.meta.role && userRole !== to.meta.role) {
      // 権限がない場合、自分のダッシュボードへリダイレクト
      next(`/${userRole}/dashboard`)
      return
    }
  }

  // ゲスト専用ページ（ログイン済みユーザーはアクセス不可）
  if (to.meta.requiresGuest && isAuthenticated) {
    next(`/${userRole}/dashboard`)
    return
  }

  next()
})

export default router