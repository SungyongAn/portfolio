// src/services/authService.js
import api from './api'

export async function login(email, password) {
  const res = await api.post('/api/auth/login', { email, password })
  return res.data  // ← データを返すだけ
}

export async function refreshAccessToken() {
  try {
    const res = await api.post('/api/auth/refresh')
    return res.data  // ← データを返すだけ
  } catch (error) {
    if (error.response?.status === 401) {
      return null
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

export const authAPI = {
  login,
  refreshAccessToken,
  logout,
}