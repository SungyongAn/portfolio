import type { Role } from './types'

export const ROLES = {
  STUDENT: 'student',
  LIBRARIAN: 'librarian',
  ADMIN: 'admin',
} as const satisfies Record<string, Role>

export const ROLE_LABEL: Record<Role, string> = {
  student: '生徒',
  librarian: '司書',
  admin: '管理者',
}

export const COMMITTEE_LABEL = '図書委員'