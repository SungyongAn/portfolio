export type InterLibraryStatus =
  | 'pending'
  | 'confirmed'
  | 'shipped'
  | 'arrived'
  | 'cancelled'

export interface InterLibraryRequest {
  id: number
  book_id: number
  book_title: string
  book_barcode: string
  from_school_id: number
  from_school_name: string
  to_school_id: number
  to_school_name: string
  user_id: number
  user_name: string
  status: InterLibraryStatus
  requested_at: string
  shipped_at: string | null
  arrived_at: string | null
}