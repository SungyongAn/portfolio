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

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
    return
  }

  if (to.path === '/') {
    const role = authStore.role

    if (role === 'admin') {
      next('/admin/users')
    } else if (role === 'teacher') {
      next('/teacher/dashboard')
    } else if (role === 'student') {
      next('/student/dashboard')
    } else {
      next('/login')
    }
    return
  }

  next()
})

export default router