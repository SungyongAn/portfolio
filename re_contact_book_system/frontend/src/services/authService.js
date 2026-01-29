// src/services/authService.js
import api from './api'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

export async function login(email, password) {
  const res = await api.post('/api/auth/login', { email, password })

  const auth = useAuthStore()
  auth.accessToken = res.data.access_token
  auth.tokenExpiry = Date.now() + res.data.expires_in * 1000
  auth.role = res.data.role
  auth.userId = res.data.user_id
  auth.userName = res.data.name
}


export async function refreshAccessToken() {
  const res = await api.post('/api/auth/refresh')
  const { access_token, expires_in } = res.data

  const auth = useAuthStore()
  auth.accessToken = access_token
  auth.tokenExpiry = Date.now() + expires_in * 1000
}

export async function logout() {
  try {
    await api.post('/api/auth/logout')
  } catch (e) {
    // 無視
  }

  const auth = useAuthStore()
  auth.accessToken = null
  auth.userId = null
  auth.userName = null
  auth.role = null
  auth.tokenExpiry = null
  router.push('/login')
}

// 名前付き export まとめ
export const authAPI = {
  login,
  refreshAccessToken,
  logout,
}
