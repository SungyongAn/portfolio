import api from './api'

export const adminAPI = {
  getUsers(params) {
    return api.get('/api/users', { params })
  },
  deleteUser(userId) {
    return api.delete(`/api/users/${userId}`)
  }
}
