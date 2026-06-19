import { TaskStatus } from "@/api/models/TaskStatus";


export const TASK_STATUS_LABEL: Record<TaskStatus, string> = {
  TODO: "未着手",
  IN_PROGRESS: "進行中",
  IN_REVIEW: "レビュー中",
  DONE: "完了",
};

export const TASK_STATUS_TYPE: Record<TaskStatus, string> = {
  TODO: "info",
  IN_PROGRESS: "primary",
  IN_REVIEW: "warning",
  DONE: "success",
};

// ── WF工程定義 ─────────────────────────────

export const WATERFALL_PHASES = [
  "要件定義",
  "基本設計",
  "詳細設計",
  "実装",
  "単体テスト",
  "結合テスト",
  "総合テスト",
  "リリース",
] as const;

// ── WF工程順 ─────────────────────────────

export const PHASE_ORDER: Record<string, number> = {
  調査: 1,

  要件定義: 2,

  基本設計: 3,

  詳細設計: 4,

  実装: 5,

  単体テスト: 6,

  結合テスト: 7,

  総合テスト: 8,

  受入テスト: 9,

  リリース: 10,

  運用準備: 11,
};
