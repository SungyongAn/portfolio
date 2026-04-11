export type Role = 'student' | 'librarian' | 'admin'

export interface User {
  id: number
  email: string
  name: string
  role: Role
  is_committee: boolean
  school_id: number | null
  school_name: string
  grade: number | null
  class_name: string | null
  barcode: string | null
}