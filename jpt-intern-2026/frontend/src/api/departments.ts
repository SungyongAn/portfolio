import apiClient from './client'

export type Department = {
  id: number
  name: string
}

export const departmentsAPI = {
  getDepartments() {
    return apiClient.get<Department[]>('/api/departments')
  },
}