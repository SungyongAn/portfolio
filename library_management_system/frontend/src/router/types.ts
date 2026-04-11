// ============================================================
// router/types.ts  —  ルートメタフィールドの型拡張
// ============================================================

import type { Role } from "@/types";

declare module "vue-router" {
  interface RouteMeta {
    /** true のとき未ログインでのみアクセス可（ログイン済みはダッシュボードへ） */
    requiresGuest?: boolean;
    /** true のときログイン必須 */
    requiresAuth?: boolean;
    /** アクセスを許可するロールの配列。未指定の場合は全ロール許可 */
    roles?: Role[];
    /** true のとき is_committee: true の生徒のみアクセス可 */
    requiresCommittee?: boolean;
    /** ページタイトル */
    title?: string;
  }
}
