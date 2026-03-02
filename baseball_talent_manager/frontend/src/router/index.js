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

    // マネージャールート
    {
      path: '/manager',
      meta: { requiresAuth: true, role: 'manager' },
      children: [
        {
          path: 'dashboard',
          name: 'manager-dashboard',
          component: () => import('@/views/manager/DashboardView.vue'),
          meta: {
            title: 'ダッシュボード',
            breadcrumbs: [
              { name: 'ダッシュボード' }
            ]
          }
        },
        {
          path: 'submit',
          name: 'manager-submit',
          component: () => import('@/views/manager/MeasurementResultSubmit.vue'),
          meta: {
            title: '測定結果の入力',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/manager/dashboard' }
            ]
          }
        },
        {
          path: 'statuslist',
          name: 'manager-unread',
          component: () => import('@/views/manager/MeasurementStatusList.vue'),
          meta: {
            title: '承認依頼中のステータス確認',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/manager/dashboard' }
            ]
          }
        }
      ]
    },

    // 部員ルート
    {
      path: '/member',
      meta: { requiresAuth: true, role: 'member' },
      children: [
        {
          path: 'dashboard',
          name: 'member-dashboard',
          component: () => import('@/views/shared/DashboardView.vue'),
          meta: {
            title: 'ダッシュボード',
            breadcrumbs: [
              { name: 'ダッシュボード' }
            ]
          }
        },
        {
          path: 'resultreview',
          name: 'member-resultreview',
          component: () => import('@/components/MeasurementResultReview.vue'),
          meta: {
            title: '測定結果の確認と承認',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/member/dashboard' }
            ]
          }
        },
        {
          path: 'history',
          name: 'member-history',
          component: () => import('@/components/MeasurementResultList.vue'),
          meta: {
            title: '測定記録の閲覧',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/shared/dashboard' }
            ]
          }
        }
      ]
    },

    // コーチルート
    {
      path: '/coach',
      meta: { requiresAuth: true, role: 'coach' },
      children: [
        {
          path: 'dashboard',
          name: 'coach-dashboard',
          component: () => import('@/views/shared/DashboardView.vue'),
          meta: {
            title: 'ダッシュボード',
            breadcrumbs: [
              { name: 'ダッシュボード' }
            ]
          }
        },
        {
          path: 'resultreview',
          name: 'coach-resultreview',
          component: () => import('@/components/MeasurementResultReview.vue'),
          meta: {
            title: '測定結果の確認と承認',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/coach/dashboard' }
            ]
          }
        },
        {
          path: 'history',
          name: 'coach-history',
          component: () => import('@/components/MeasurementResultList.vue'),
          meta: {
            title: '測定記録の閲覧',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/coach/dashboard' }
            ]
          },
        },
        {
          path: 'userscreate',
          name: 'coach-users-create',
          component: () => import('@/components/MemberCreate.vue'),
          meta: {
            title: '部員作成',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/coach/dashboard' }
            ]
          }
        },
        {
          path: 'usersretire',
          name: 'coach-users-retire',
          component: () => import('@/components/MemberRetire.vue'),
          meta: {
            title: '部員退部・引退処理',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/coach/dashboard' }
            ]
          }
        }
      ]
    },
    
    // 監督ルート
    {
      path: '/director',
      meta: { requiresAuth: true, role: 'director' },
      children: [
        {
          path: 'dashboard',
          name: 'director-dashboard',
          component: () => import('@/views/shared/DashboardView.vue'),
          meta: {
            title: 'ダッシュボード',
            breadcrumbs: [
              { name: 'ダッシュボード' }
            ]
          }
        },
        {
          path: 'history',
          name: 'director-history',
          component: () => import('@/components/MeasurementResultList.vue'),
          meta: {
            title: '測定記録の閲覧',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/director/dashboard' }
            ]
          },
        },
        {
          path: 'userscreate',
          name: 'director-users-create',
          component: () => import('@/components/MemberCreate.vue'),
          meta: {
            title: '部員作成',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/director/dashboard' }
            ]
          }
        },
        {
          path: 'usersretire',
          name: 'director-users-retire',
          component: () => import('@/components/MemberRetire.vue'),
          meta: {
            title: '部員退部・引退処理',
            breadcrumbs: [
              { name: 'ダッシュボード', to: '/director/dashboard' }
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
    if (role === 'teacher') {
      switch(authStore.teacherRole) {
        case '担任':
        case '副担任':
          return next('/teacher/class-dashboard')
        case '学年主任':
          return next('/teacher/grade-dashboard')
        case '教科担当':
          return next('/teacher/subject-dashboard')
        default:
          return next('/teacher/dashboard')
      }
    }
    if (role === 'student') return next('/student/dashboard')

    next('/login')
    return
  }

  next()
})


export default router