import type { BookStatus } from './types'

export const BOOK_STATUS = {
  AVAILABLE: 'available',
  LOANED: 'loaned',
  RESERVED: 'reserved',
  INTER_LIBRARY: 'inter_library',
  DISCARDED: 'discarded',
} as const satisfies Record<string, BookStatus>

export const BOOK_STATUS_LABEL: Record<BookStatus, string> = {
  available: '貸出可',
  loaned: '貸出中',
  reserved: '予約済',
  inter_library: '図書館間貸出中',
  discarded: '廃棄済',
}

/** Bootstrap badge クラス（例: <span :class="['badge', BOOK_STATUS_COLOR[book.status]]"> ） */
export const BOOK_STATUS_COLOR: Record<BookStatus, string> = {
  available: 'bg-success',
  loaned: 'bg-warning text-dark',
  reserved: 'bg-info text-dark',
  inter_library: 'bg-primary',
  discarded: 'bg-secondary',
}