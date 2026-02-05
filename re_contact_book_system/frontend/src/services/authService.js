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
  auth.student_class = res.data.student_class ?? null
  auth.primary_assignment = res.data.primary_assignment ?? null
  auth.teacher_assignments = res.data.teacher_assignments ?? []
}


export async function refreshAccessToken() {
  try {
    const res = await api.post('/api/auth/refresh')

    const { access_token, expires_in } = res.data

    const auth = useAuthStore()
    auth.accessToken = access_token
    auth.tokenExpiry = Date.now() + expires_in * 1000

    return true
  } catch (error) {
    if (error.response?.status === 401) {
      // 未ログインは正常系
      return false
    }
    throw error
  }
}

export async function logout() {
  try {
    await api.post('/api/auth/logout')
  } catch (e) {
    // 無視
  }
}

// 名前付き export まとめ
export const authAPI = {
  login,
  refreshAccessToken,
  logout,
}
