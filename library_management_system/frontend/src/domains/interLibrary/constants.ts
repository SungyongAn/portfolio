import type { InterLibraryStatus } from "./types";

export const INTERLIBRARY_STATUS = {
  PENDING: "pending",
  CONFIRMED: "confirmed",
  SHIPPED: "shipped",
  ARRIVED: "arrived",
  CANCELLED: "cancelled",
} as const satisfies Record<string, InterLibraryStatus>;

export const INTERLIBRARY_STATUS_LABEL: Record<InterLibraryStatus, string> = {
  pending: "受付中",
  confirmed: "配送確定",
  shipped: "発送済",
  arrived: "到着済",
  cancelled: "キャンセル済",
};

/** Bootstrap badge クラス */
export const INTERLIBRARY_STATUS_COLOR: Record<InterLibraryStatus, string> = {
  pending: "bg-info text-dark",
  confirmed: "bg-primary",
  shipped: "bg-warning text-dark",
  arrived: "bg-success",
  cancelled: "bg-secondary",
};

export const INTERLIBRARY_CANCELLABLE_STATUSES: InterLibraryStatus[] = [
  INTERLIBRARY_STATUS.PENDING,
  INTERLIBRARY_STATUS.CONFIRMED,
];

/** 締切曜日（0=日, 1=月, ..., 5=金, 6=土） */
export const INTERLIBRARY_DEADLINE_DAY = 5;

/** 締切時刻（時・24時間表記） */
export const INTERLIBRARY_DEADLINE_HOUR = 15;
