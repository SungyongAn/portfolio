import { defineStore } from 'pinia'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
    userName: localStorage.getItem('userName') || null,
    userId: localStorage.getItem('userId') || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  getters: {
    isStudent: (state) => state.role === 'student',
    isTeacher: (state) => state.role === 'teacher',
    isAdmin: (state) => state.role === 'admin'
  },

  actions: {
    async login(email, password) {
      try {
        const response = await authAPI.login(email, password)
        const { token, role, name, user_id } = response.data

        // 状態を保存
        this.token = token
        this.role = role
        this.userName = name
        this.userId = user_id
        this.isAuthenticated = true

        // LocalStorageに保存
        localStorage.setItem('token', token)
        localStorage.setItem('role', role)
        localStorage.setItem('userName', name)
        localStorage.setItem('userId', user_id)

        return { success: true, role }
      } catch (error) {
        console.error('Login error:', error)
        return { 
          success: false, 
          message: error.response?.data?.detail || 'ログインに失敗しました' 
        }
      }
    },

    logout() {
      // 状態をクリア
      this.token = null
      this.role = null
      this.userName = null
      this.userId = null
      this.isAuthenticated = false

      // LocalStorageをクリア
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('userName')
      localStorage.removeItem('userId')
    },

    async fetchUserInfo() {
      try {
        const response = await authAPI.getMe()
        const { name, role, id } = response.data
        
        this.userName = name
        this.role = role
        this.userId = id
        
        localStorage.setItem('userName', name)
        localStorage.setItem('role', role)
        localStorage.setItem('userId', id)
      } catch (error) {
        console.error('Failed to fetch user info:', error)
        this.logout()
      }
    }
  }
})