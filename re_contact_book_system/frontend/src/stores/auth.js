import { defineStore } from 'pinia'
import { authAPI } from '@/services/authService'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    tokenExpiry: null,
    role: null,
    userName: null,
    userId: null,
    student_class: null,
    primary_assignment: null,
    teacher_assignments: [],  
    isInitialized: false,
    lastActivity: Date.now(),
    inactivityTimer: null,
    eventListeners: [],

    roleMap: {
      student: '生徒',
      teacher: '教師',
      admin: '管理者'
    }
  }),

  getters: {
    isAuthenticated() {
      return !!this.accessToken && !this.isTokenExpired
    },

    isTokenExpired(state) {
      if (!state.tokenExpiry) return true
      return Date.now() > state.tokenExpiry
    },

    maybeLoggedIn(state) {
      return !!state.accessToken || !!state.tokenExpiry
    },

    studentGrade() {
      return this.student_class?.grade_number ?? null
   },

    studentClassName() {
      return this.student_class?.class_name ?? null
    },

    primaryAssignmentType() {
      return this.primary_assignment?.assignment_type ?? null
    },

    primaryAssignmentGrade() {
      return this.primary_assignment?.grade_number ?? null
    },

    primaryAssignmentClass() {
      return this.primary_assignment?.class_name ?? null
    },

    teacherAssignments() {
      return this.teacher_assignments ?? []
    }, 

    displayRole() {
      return this.role ? this.roleMap[this.role] || this.role : null
    },
    
    isStudent() {
      return this.role === 'student'
    },

    isTeacher() {
      return this.role === 'teacher'
    },

    isAdmin() {
      return this.role === 'admin'
    }
  },

  actions: {
    async login(email, password) {
      try {
        // authService は認証専用サービス
        // API 呼び出しと同時に authStore を直接更新する責務を持つ
        // （認証状態はアプリ内で一意なため）
        await authAPI.login(email, password)
        this.updateActivity()
        this.startInactivityTimer()
        return true
      } catch (error) {
        console.error('ログインエラー:', error)
        throw error
      }
    },

    async initAuth() {
      if (!this.maybeLoggedIn) {
        this.isInitialized = true
        return
      }

      const refreshed = await this.refreshAccessToken()

      if (refreshed) {
        this.startInactivityTimer()
      }

      this.isInitialized = true
    },

    startInactivityTimer() {
      const INACTIVITY_TIMEOUT = 30 * 60 * 1000 // 30分

      this.clearInactivityTimer()

      const resetTimer = () => {
        this.updateActivity()
        if (this.inactivityTimer) clearTimeout(this.inactivityTimer)

        this.inactivityTimer = setTimeout(() => {
          console.log('無操作によりログアウトします')
          this.logout()
        }, INACTIVITY_TIMEOUT)
      }

      const events = ['mousemove', 'keypress', 'click', 'scroll', 'touchstart']
      events.forEach(eventName => {
        window.addEventListener(eventName, resetTimer)
        this.eventListeners.push({ eventName, handler: resetTimer })
      })

      resetTimer()
    },

    clearInactivityTimer() {
      if (this.inactivityTimer) {
        clearTimeout(this.inactivityTimer)
        this.inactivityTimer = null
      }

      this.eventListeners.forEach(({ eventName, handler }) => {
        window.removeEventListener(eventName, handler)
      })
      this.eventListeners = []
    },

    updateActivity() {
      this.lastActivity = Date.now()
    },

    async logout() {
      try {
        await authAPI.logout()
      } catch (e) {
        // エラー無視
      }

      this.clearInactivityTimer()
      this.accessToken = null
      this.tokenExpiry = null
      this.role = null
      this.userName = null
      this.userId = null
      this.student_class = null
      this.primary_assignment = null
      this.teacher_assignments = []

      // ルーティング
      router.push('/login')
    }
  }
})
