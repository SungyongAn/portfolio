import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      meta: { requiresAuth: true },
      component: { render: () => null }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    // 生徒ルート
    {
      path: '/student',
      meta: { requiresAuth: true, role: 'student' },
      children: [
        {
          path: 'dashboard',
          name: 'student-dashboard',
          component: () => import('@/views/student/DashboardView.vue'),
          meta: {
            title: 'ダッシュボード',
            breadcrumbs: [
              { name: 'ダッシュボード' }
            ]
          }
        },
        {
          path: 'submit',
          name: 'student-submit',
          component: () => import('@/views/student/SubmitView.vue'),
          meta: {
            title: '連絡帳提出',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/student/dashboard' },
              { name: '連絡帳提出' }
            ]
          }
        },
        {
          path: 'history',
          name: 'student-history',
          component: () => import('@/views/student/HistoryView.vue'),
          meta: {
            title: '過去の記録',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/student/dashboard' },
              { name: '過去の記録' }
            ]
          }
        }
      ]
    },

    // 教師ルート
    {
      path: '/teacher',
      meta: { requiresAuth: true, role: 'teacher' },
      children: [
        {
          path: 'dashboard',
          name: 'teacher-dashboard',
          component: () => import('@/views/teacher/DashboardView.vue'),
          meta: {
            title: 'ダッシュボード',
            breadcrumbs: [
              { name: 'ダッシュボード' }
            ]
          }
        },
        {
          path: 'submissions',
          name: 'teacher-submissions',
          component: () => import('@/views/teacher/SubmissionsView.vue'),
          meta: {
            title: '提出状況',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/teacher/dashboard' },
              { name: '提出状況' }
            ]
          }
        },
        {
          path: 'unread',
          name: 'teacher-unread',
          component: () => import('@/views/teacher/UnreadView.vue'),
          meta: {
            title: '未読連絡帳',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/teacher/dashboard' },
              { name: '未読連絡帳' }
            ]
          }
        }
      ]
    },

    // 管理者ルート
    {
      path: '/admin',
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/admin/UsersView.vue'),
          meta: {
            title: 'ユーザー管理',
            breadcrumbs: [
              { name: 'ユーザー管理' }
            ]
          }
        },
        {
          path: 'users/create',
          name: 'admin-users-create',
          component: () => import('@/views/admin/UserCreateView.vue'),
          meta: {
            title: 'ユーザー作成',
            breadcrumbs: [
              { name: 'ユーザー管理', to: '/admin/users' },
              { name: '新規作成' }
            ]
          }
        },
        {
          path: 'users/:id/edit',
          name: 'admin-users-edit',
          component: () => import('@/views/admin/UserEditView.vue'),
          meta: {
            title: 'ユーザー編集',
            breadcrumbs: [
              { name: 'ユーザー管理', to: '/admin/users' },
              { name: '編集' }
            ]
          }
        },
        {
          path: 'grades',
          name: 'admin-grades',
          component: () => import('@/views/admin/GradesView.vue'),
          meta: {
            title: '学年・クラス管理',
            breadcrumbs: [
              { name: '学年・クラス管理' }
            ]
          }
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
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // ログイン画面では初期化しない
  if (!authStore.isInitialized && to.name !== 'login') {
    await authStore.initAuth()
  }

  // 未ログインで認証必須ページ
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
    return
  }

  // ログイン済みでゲスト専用ページ
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    const role = authStore.role
    if (role === 'admin') return next('/admin/users')
    if (role === 'teacher') return next('/teacher/dashboard')
    if (role === 'student') return next('/student/dashboard')
    return next('/')
  }

   // ルートアクセス時の振り分け
   if (to.path === '/') {
    if (!authStore.isAuthenticated) {
      next('/login')
      return
    }

    const role = authStore.role
    if (role === 'admin') return next('/admin/users')
    if (role === 'teacher') return next('/teacher/dashboard')
    if (role === 'student') return next('/student/dashboard')

    next('/login')
    return
  }

  next()
})


export default router