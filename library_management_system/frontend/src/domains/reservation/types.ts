export type ReservationStatus =
  | 'waiting'
  | 'ready'
  | 'cancelled'

export interface Reservation {
  id: number
  book_id: number
  book_title: string
  book_barcode: string
  user_id: number
  user_name: string
  status: ReservationStatus
  queue_position: number | null
  reserved_at: string
  ready_at: string | null
  expires_at: string | null
}