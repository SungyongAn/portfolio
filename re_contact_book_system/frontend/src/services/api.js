import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http:////127.0.0.1:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// リクエストインターセプター（トークン追加）
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// レスポンスインターセプター（エラーハンドリング）
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 認証エラー時はログアウト
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// === 認証API ===
export const authAPI = {
  login: (email, password) => api.post('/api/auth/login', { email, password }),
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

// === ユーザー管理API ===
export const userAPI = {
  create: (data) => api.post('/api/users/', data),
  getAll: (role, limit = 100, offset = 0) => 
    api.get('/api/users/', { params: { role, limit, offset } }),
  getById: (id) => api.get(`/api/users/${id}`),
  update: (id, data) => api.put(`/api/users/${id}`, data),
  delete: (id) => api.delete(`/api/users/${id}`),
  getStudentsByClass: (classId) => api.get(`/api/users/students/by-class/${classId}`)
}

export default api