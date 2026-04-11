// ============================================================
// composables/useLoanStatus.ts  —  貸出状態の表示変換
// ============================================================

import { computed } from "vue";
import type { Loan } from "@/types";
import { LOAN_PERIOD_DAYS } from "@/constants";

/**
 * 1件の貸出情報をもとに表示用の派生値を返す。
 *
 * @param loan 対象の貸出レコード（リアクティブな getter を渡す）
 */
export function useLoanStatus(loan: () => Loan) {
  // ── 残日数 ───────────────────────────────────────────────────
  const remainingDays = computed(() => {
    const due = new Date(loan().due_date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    due.setHours(0, 0, 0, 0);
    return Math.floor(
      (due.getTime() - today.getTime()) / (1000 * 60 * 60 * 24),
    );
  });

  // ── 延滞中フラグ ─────────────────────────────────────────────
  const isOverdue = computed(
    () => loan().returned_at === null && remainingDays.value < 0,
  );

  // ── 返却期限が近い（3日以内） ─────────────────────────────────
  const isDueSoon = computed(
    () =>
      !isOverdue.value &&
      loan().returned_at === null &&
      remainingDays.value <= 3,
  );

  // ── 残日数の表示ラベル ────────────────────────────────────────
  const remainingLabel = computed(() => {
    if (loan().returned_at !== null) return "返却済";
    if (isOverdue.value) return `${Math.abs(remainingDays.value)}日超過`;
    if (remainingDays.value === 0) return "本日返却期限";
    return `残${remainingDays.value}日`;
  });

  // ── Bootstrap テキストカラークラス ────────────────────────────
  const remainingColorClass = computed(() => {
    if (loan().returned_at !== null) return "text-secondary";
    if (isOverdue.value) return "text-danger fw-bold";
    if (isDueSoon.value) return "text-warning";
    return "text-body";
  });

  // ── 返却期限の表示（YYYY/MM/DD） ──────────────────────────────
  const dueDateLabel = computed(() => {
    const due = new Date(loan().due_date);
    return due.toLocaleDateString("ja-JP", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  });

  return {
    remainingDays,
    isOverdue,
    isDueSoon,
    remainingLabel,
    remainingColorClass,
    dueDateLabel,
  };
}

// ============================================================
// ユーティリティ：貸出日から返却期限日を算出
// ============================================================

/**
 * 貸出日（ISO 8601文字列）から返却期限日（ISO 8601文字列）を返す。
 * ダミーデータ生成時に使用する。
 */
export function calcDueDate(loanedAt: string): string {
  const date = new Date(loanedAt);
  date.setDate(date.getDate() + LOAN_PERIOD_DAYS);
  return date.toISOString();
}
