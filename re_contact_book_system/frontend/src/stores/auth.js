import { defineStore } from 'pinia'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null, // アクセストークンはメモリに保存
    refreshToken: localStorage.getItem('refreshToken') || null,
    tokenExpiry: localStorage.getItem('tokenExpiry')
    ? Number(localStorage.getItem('tokenExpiry'))
    : null,
    role: localStorage.getItem('role') || null,
    userName: localStorage.getItem('userName') || null,
    userId: localStorage.getItem('userId') || null,
    lastActivity: Date.now(),
    inactivityTimer: null
  }),

  getters: {
    isAuthenticated: (state) => {
       return !!state.accessToken || !!state.refreshToken
    },

    isTokenExpired: (state) => {
      if (!state.tokenExpiry) return true
      return Date.now() > state.tokenExpiry
    }
  },

  actions: {
    async login(email, password) {
      try {
        const response = await authAPI.login(email, password)
        const data = response.data

        // トークンを保存
        this.accessToken = data.access_token
        this.refreshToken = data.refresh_token
        this.role = data.role
        this.userName = data.name
        this.userId = data.user_id
        
        // 有効期限を計算（expires_in は秒単位）
        const expiryTime = Date.now() + (data.expires_in * 1000)
        this.tokenExpiry = expiryTime

        // LocalStorageに保存
        localStorage.setItem('refreshToken', data.refresh_token)
        localStorage.setItem('tokenExpiry', expiryTime.toString())
        localStorage.setItem('role', data.role)
        localStorage.setItem('userName', data.name)
        localStorage.setItem('userId', data.user_id.toString())

        // 最終アクティビティ時刻を更新
        this.updateActivity()
        
        // 無操作タイマーを開始
        this.startInactivityTimer()

        return true
      } catch (error) {
        console.error('ログインエラー:', error)
        throw error
      }
    },

    async refreshAccessToken() {
      try {
        const response = await authAPI.refreshToken(this.refreshToken)
        const data = response.data

        // 新しいアクセストークンを保存
        this.accessToken = data.access_token
        const expiryTime = Date.now() + (data.expires_in * 1000)
        this.tokenExpiry = expiryTime

        localStorage.setItem('tokenExpiry', expiryTime.toString())

        return true
      } catch (error) {
        console.error('トークンリフレッシュエラー:', error)
        this.logout()
        return false
      }
    },

    startInactivityTimer() {
      const INACTIVITY_TIMEOUT = 30 * 60 * 1000 // 30分

      // 既存のタイマーをクリア
      if (this.inactivityTimer) {
        clearTimeout(this.inactivityTimer)
      }

      // アクティビティイベントのリスナー
      const resetTimer = () => {
        this.updateActivity()
        
        if (this.inactivityTimer) {
          clearTimeout(this.inactivityTimer)
        }

        this.inactivityTimer = setTimeout(() => {
          console.log('無操作によりログアウトします')
          this.logout()
        }, INACTIVITY_TIMEOUT)
      }

      // イベントリスナーを登録
      window.addEventListener('mousemove', resetTimer)
      window.addEventListener('keypress', resetTimer)
      window.addEventListener('click', resetTimer)
      window.addEventListener('scroll', resetTimer)

      // 初回タイマー開始
      resetTimer()
    },

    updateActivity() {
      this.lastActivity = Date.now()
      localStorage.setItem('lastActivity', this.lastActivity.toString())
    },

    logout() {
      // タイマーをクリア
      if (this.inactivityTimer) {
        clearTimeout(this.inactivityTimer)
      }

      // 状態をクリア
      this.accessToken = null
      this.refreshToken = null
      this.tokenExpiry = null
      this.role = null
      this.userName = null
      this.userId = null

      // LocalStorageをクリア
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('tokenExpiry')
      localStorage.removeItem('role')
      localStorage.removeItem('userName')
      localStorage.removeItem('userId')
      localStorage.removeItem('lastActivity')

      // ログインページへリダイレクト
      window.location.href = '/login'
    },

    // アプリ起動時の初期化
    initialize() {
      // refreshToken があれば、必ず accessToken の再取得を試みる
      if (this.refreshToken) {
        this.refreshAccessToken().then((success) => {
          if (success) {
            this.startInactivityTimer()
          }
        })
      }
    }
  }
})