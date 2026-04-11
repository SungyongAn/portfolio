export type BookStatus =
  | 'available'
  | 'loaned'
  | 'reserved'
  | 'inter_library'
  | 'discarded'

export interface Book {
  id: number
  barcode: string
  title: string
  author: string
  publisher: string
  ndc: string
  isbn: string
  school_id: number
  school_name: string
  status: BookStatus
  location: string
}