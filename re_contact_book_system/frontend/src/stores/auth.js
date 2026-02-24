import { defineStore } from 'pinia'
import * as authAPI from '@/services/authService'
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
        const data = await authAPI.login(email, password)
        console.log('store login data:', data)
        this.accessToken = data.access_token
        this.tokenExpiry = Date.now() + data.expires_in * 1000
        this.role = data.role
        this.userId = data.user_id
        this.userName = data.name
        this.student_class = data.student_class ?? null
        this.primary_assignment = data.primary_assignment ?? null
        this.teacher_assignments = data.teacher_assignments ?? []
        console.log('after set state:', {
          accessToken: this.accessToken,
          role: this.role,
          userName: this.userName,
          primary_assignment:this.primary_assignment.assignment_type
        })

        this.updateActivity()
        this.startInactivityTimer()
      
        return true
      } catch (error) {
        console.error('ログインエラー:', error)
        throw error
      }
    },

    async refreshAccessToken() {
      const data = await authAPI.refreshAccessToken()
      
      if (!data) {
        return false
      }

      // ← ここでstateを更新
      this.accessToken = data.access_token
      this.tokenExpiry = Date.now() + data.expires_in * 1000
    
      return true
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
