import { defineStore } from 'pinia'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null, // アクセストークンはメモリのみ
    tokenExpiry: null, // メモリのみ
    role: null, // メモリのみ
    userName: null, // メモリのみ
    userId: null, // メモリのみ
    lastActivity: Date.now(),
    inactivityTimer: null,
    eventListeners: [] // クリーンアップ用
  }),

  getters: {
    isAuthenticated() {
      return !!this.accessToken && !this.isTokenExpired
    },
    
    isTokenExpired(state) {
      if (!state.tokenExpiry) return true
      return Date.now() > state.tokenExpiry
    }
  },

  actions: {
    async login(email, password) {
      try {
        const response = await authAPI.login(email, password)
        const data = response.data

        // トークンを保存（メモリのみ）
        this.accessToken = data.access_token
        this.role = data.role
        this.userName = data.name
        this.userId = data.user_id
        
        // 有効期限を計算（expires_in は秒単位）
        const expiryTime = Date.now() + (data.expires_in * 1000)
        this.tokenExpiry = expiryTime

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
        const response = await authAPI.refreshToken()
        const data = response.data

        // 新しいアクセストークンを保存（メモリのみ）
        this.accessToken = data.access_token
        const expiryTime = Date.now() + (data.expires_in * 1000)
        this.tokenExpiry = expiryTime

        return true
      } catch (error) {
        console.error('トークンリフレッシュエラー:', error)
        this.logout()
        return false
      }
    },

    startInactivityTimer() {
      const INACTIVITY_TIMEOUT = 30 * 60 * 1000 // 30分

      // 既存のタイマーとリスナーをクリア
      this.clearInactivityTimer()

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

      // イベントリスナーを登録し、参照を保存
      const events = ['mousemove', 'keypress', 'click', 'scroll', 'touchstart']
      events.forEach(eventName => {
        window.addEventListener(eventName, resetTimer)
        this.eventListeners.push({ eventName, handler: resetTimer })
      })

      // 初回タイマー開始
      resetTimer()
    },

    clearInactivityTimer() {
      // タイマーをクリア
      if (this.inactivityTimer) {
        clearTimeout(this.inactivityTimer)
        this.inactivityTimer = null
      }

      // イベントリスナーを削除
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
        // サーバー側のログアウトAPI呼び出し（リフレッシュトークンの無効化）
        await authAPI.logout()
      } catch (error) {
        console.error('ログアウトAPIエラー:', error)
      } finally {
        // タイマーとリスナーをクリア
        this.clearInactivityTimer()

        // 状態をクリア
        this.accessToken = null
        this.tokenExpiry = null
        this.role = null
        this.userName = null
        this.userId = null
        this.lastActivity = Date.now()

        // ログインページへリダイレクト
        window.location.href = '/login'
      }
    },

    // アプリ起動時の初期化
    async initialize() {
      // リフレッシュトークン（HttpOnly Cookie）が存在する場合のみトークン更新を試行
      try {
        await this.refreshAccessToken()
        this.startInactivityTimer()
        return true
      } catch (error) {
        // リフレッシュトークンがない、または無効な場合は何もしない
        // ログイン画面への遷移はルーターガードで処理
        return false
      }
    }
  }
})