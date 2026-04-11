import type { ReservationStatus } from './types'

export const RESERVATION_STATUS = {
  WAITING: 'waiting',
  READY: 'ready',
  CANCELLED: 'cancelled',
} as const satisfies Record<string, ReservationStatus>

export const RESERVATION_STATUS_LABEL: Record<ReservationStatus, string> = {
  waiting: '順番待ち',
  ready: '準備完了',
  cancelled: 'キャンセル済',
}

/** Bootstrap badge クラス */
export const RESERVATION_STATUS_COLOR: Record<ReservationStatus, string> = {
  waiting: 'bg-warning text-dark',
  ready: 'bg-success',
  cancelled: 'bg-secondary',
}

export const RESERVATION_CANCELLABLE_STATUSES: ReservationStatus[] = [
  RESERVATION_STATUS.WAITING,
  RESERVATION_STATUS.READY,
]