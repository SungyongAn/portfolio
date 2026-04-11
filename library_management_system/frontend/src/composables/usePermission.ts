// ============================================================
// composables/usePermission.ts  —  操作可否チェック
// ============================================================

import { computed } from "vue";
import type { Loan, Reservation, InterLibraryRequest } from "@/types";
import {
  LOAN_LIMIT,
  RESERVATION_CANCELLABLE_STATUSES,
  INTERLIBRARY_CANCELLABLE_STATUSES,
} from "@/constants";

/**
 * 対象ユーザーの貸出・予約状況をもとに操作可否を返す。
 * 自分自身の操作にも、代理操作時の対象生徒にも使用する。
 *
 * @param loans        対象ユーザーの貸出中リスト
 * @param interLibraries 対象ユーザーの図書館間貸出リスト（到着済含む貸出中扱い）
 */
export function usePermission(
  loans: () => Loan[],
  interLibraries: () => InterLibraryRequest[],
) {
  // ── 貸出中冊数（図書館間貸出を含む） ─────────────────────────
  const activeLoanCount = computed(() => {
    const normalLoans = loans().filter((l) => l.returned_at === null).length;
    // arrived（到着済・手元にある）も貸出中として数える
    const ilLoans = interLibraries().filter(
      (il) => il.status === "arrived",
    ).length;
    return normalLoans + ilLoans;
  });

  // ── 延滞中フラグ ─────────────────────────────────────────────
  const hasOverdue = computed(() =>
    loans().some((l) => l.returned_at === null && l.is_overdue),
  );

  // ── 貸出上限チェック ─────────────────────────────────────────
  const isLoanLimitReached = computed(
    () => activeLoanCount.value >= LOAN_LIMIT,
  );

  // ── 新規貸出・予約が可能か ────────────────────────────────────
  /** 貸出上限未満かつ延滞なし */
  const canBorrow = computed(
    () => !isLoanLimitReached.value && !hasOverdue.value,
  );

  /** 予約可否（貸出と同じ条件） */
  const canReserve = computed(() => canBorrow.value);

  // ── 予約キャンセル可否 ────────────────────────────────────────
  const canCancelReservation = (reservation: Reservation): boolean =>
    RESERVATION_CANCELLABLE_STATUSES.includes(reservation.status);

  // ── 図書館間貸出キャンセル可否 ────────────────────────────────
  const canCancelInterLibrary = (il: InterLibraryRequest): boolean =>
    INTERLIBRARY_CANCELLABLE_STATUSES.includes(il.status);

  // ── 制限理由メッセージ ────────────────────────────────────────
  /** 貸出・予約不可の場合の表示メッセージ。可能な場合は null */
  const borrowBlockReason = computed((): string | null => {
    if (hasOverdue.value)
      return "延滞中の資料があります。返却後にご利用ください。";
    if (isLoanLimitReached.value)
      return `貸出上限（${LOAN_LIMIT}冊）に達しています。`;
    return null;
  });

  return {
    activeLoanCount,
    hasOverdue,
    isLoanLimitReached,
    canBorrow,
    canReserve,
    canCancelReservation,
    canCancelInterLibrary,
    borrowBlockReason,
  };
}
