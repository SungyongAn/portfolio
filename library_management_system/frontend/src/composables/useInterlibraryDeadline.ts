// ============================================================
// composables/useInterlibraryDeadline.ts  —  図書館間貸出 締切判定
// ============================================================

import { computed } from "vue";
import {
  INTERLIBRARY_DEADLINE_DAY,
  INTERLIBRARY_DEADLINE_HOUR,
} from "@/constants";

export function useInterlibraryDeadline() {
  // ── 現在が締切時間内か ────────────────────────────────────────
  /**
   * true  → 今週の受付中（金曜15:00前）
   * false → 締切済（金曜15:00以降・土日・月〜木も含む次週待ち）
   */
  const isWithinDeadline = computed(() => {
    const now = new Date();
    const day = now.getDay(); // 0=日 〜 6=土
    const hour = now.getHours();

    if (day < INTERLIBRARY_DEADLINE_DAY) return true;
    if (day === INTERLIBRARY_DEADLINE_DAY && hour < INTERLIBRARY_DEADLINE_HOUR)
      return true;
    return false;
  });

  // ── 次回締切日時 ──────────────────────────────────────────────
  /** 次の金曜15:00を Date で返す */
  const nextDeadline = computed(() => {
    const now = new Date();
    const day = now.getDay();

    // 今週の金曜15:00をまず算出
    const daysUntilFriday = (INTERLIBRARY_DEADLINE_DAY - day + 7) % 7;
    const friday = new Date(now);
    friday.setDate(now.getDate() + daysUntilFriday);
    friday.setHours(INTERLIBRARY_DEADLINE_HOUR, 0, 0, 0);

    // すでに今週の金曜15:00を過ぎていたら来週に繰り越す
    if (friday <= now) {
      friday.setDate(friday.getDate() + 7);
    }

    return friday;
  });

  // ── 次回締切日時の表示ラベル ──────────────────────────────────
  const nextDeadlineLabel = computed(() =>
    nextDeadline.value.toLocaleString("ja-JP", {
      month: "long",
      day: "numeric",
      weekday: "short",
      hour: "2-digit",
      minute: "2-digit",
    }),
  );

  // ── 資料詳細画面で表示するメッセージ ─────────────────────────
  const deadlineMessage = computed(() =>
    isWithinDeadline.value
      ? null
      : `今週の受付は締め切りました。次回受付：${nextDeadlineLabel.value}`,
  );

  return {
    isWithinDeadline,
    nextDeadline,
    nextDeadlineLabel,
    deadlineMessage,
  };
}
