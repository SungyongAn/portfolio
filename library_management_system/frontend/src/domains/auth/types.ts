import type { Role } from '@/domains/user/types'

/** ログイン済みユーザー情報（JWTペイロード相当） */
export interface AuthUser {
  id: number
  name: string
  email: string
  role: Role
  is_committee: boolean
  school_id: number | null
  school_name: string
}

/** ログインAPIレスポンス */
export interface LoginResponse {
  access_token: string
  token_type: 'bearer'
  user: AuthUser
}