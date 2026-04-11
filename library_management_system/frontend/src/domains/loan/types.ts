export interface Loan {
  id: number
  book_id: number
  book_title: string
  book_barcode: string
  user_id: number
  user_name: string
  loaned_at: string
  due_date: string
  returned_at: string | null
  is_overdue: boolean
}