import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
})

// リクエストインターセプター（トークン追加）
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.accessToken

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => Promise.reject(error)
)

// レスポンスインターセプター（エラーハンドリング）
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const authStore = useAuthStore()
      
      // リフレッシュトークンを使って再試行
      const success = await authStore.refreshAccessToken()
      
      if (success) {
        // 元のリクエストを再実行
        originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
        return api(originalRequest)
      } else {
        // リフレッシュ失敗時はログアウト
        authStore.logout()
      }
    }
    
    return Promise.reject(error)
  }
)

// === 認証API ===
export const authAPI = {
  login: (email, password) => api.post('/api/auth/login', { email, password }),
  refreshToken: () => api.post('/api/auth/refresh'),
  logout: () => api.post('/api/auth/logout'),
  getMe: () => api.get('/api/auth/me')
}

// === 連絡帳API ===
export const journalAPI = {
  submit: (data) => api.post('/api/journals/', data),
  getHistory: (limit = 50, offset = 0) => 
    api.get(`/api/journals/history?limit=${limit}&offset=${offset}`),
  getToday: () => api.get('/api/journals/today'),
  getSuggestedDate: () => api.get('/api/journals/suggested-date'),
  getDetail: (id) => api.get(`/api/journals/${id}`),
  markAsRead: (id) => api.put(`/api/journals/${id}/read`)
}

// === 教師API ===
export const teacherAPI = {
  getMyClasses: () => api.get('/api/teachers/my-classes'),
  getClassSubmissions: (classId, date) => 
    api.get(`/api/teachers/classes/${classId}/submissions`, { params: { submission_date: date } }),
  getClassJournals: (classId, date) => 
    api.get(`/api/teachers/classes/${classId}/journals`, { params: { submission_date: date } }),
  getDashboard: () => api.get('/api/teachers/dashboard'),
  getUnreadJournals: () => api.get('/api/teachers/unread-journals')
}

// ===管理者API===
export const adminAPI = {
  // ユーザー管理
  getUsers: (params) => api.get('/api/users/', { params }),
  getUserById: (id) => api.get(`/api/users/${id}`),
  createUser: (data) => api.post('/api/users/', data),
  updateUser: (id, data) => api.put(`/api/users/${id}`, data),
  deleteUser: (id) => api.delete(`/api/users/${id}`),
  getStudentsByClass: (classId) => api.get(`/api/users/students/by-class/${classId}`),
  
  // クラス・学年管理
  getGrades: () => api.get('/api/admin/grades'),
  getClasses: (gradeId) => api.get(`/api/admin/grades/${gradeId}/classes`),
  getAllClasses: () => api.get('/api/admin/classes'),
  createClass: (data) => api.post('/api/admin/classes', data),
  updateClass: (id, data) => api.put(`/api/admin/classes/${id}`, data),
  deleteClass: (id) => api.delete(`/api/admin/classes/${id}`),
  
  // クラス割当
  assignStudentToClass: (data) => api.post('/api/admin/assign-student', data),
  assignTeacherToClass: (data) => api.post('/api/admin/assign-teacher', data),
  
  // 統計情報
  getStats: () => api.get('/api/admin/stats')
}

export const userAPI = {
  create: (data) => adminAPI.createUser(data),
  getAll: (params) => adminAPI.getUsers(params),
  getById: (id) => adminAPI.getUserById(id),
  update: (id, data) => adminAPI.updateUser(id, data),
  delete: (id) => adminAPI.deleteUser(id),
  getStudentsByClass: (classId) => adminAPI.getStudentsByClass(classId)
}

export default api