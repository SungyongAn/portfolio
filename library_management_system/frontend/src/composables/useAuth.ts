// ============================================================
// composables/useAuth.ts  —  認証状態・ロール判定
// ============================================================

import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { ROLES } from "@/constants";

export function useAuth() {
  const authStore = useAuthStore();

  // ── ログイン状態 ────────────────────────────────────────────
  const isLoggedIn = computed(() => authStore.isLoggedIn);
  const currentUser = computed(() => authStore.user);

  // ── ロール判定 ───────────────────────────────────────────────
  const isStudent = computed(() => currentUser.value?.role === ROLES.STUDENT);

  const isCommittee = computed(
    () =>
      currentUser.value?.role === ROLES.STUDENT &&
      currentUser.value?.is_committee === true,
  );

  const isLibrarian = computed(
    () => currentUser.value?.role === ROLES.LIBRARIAN,
  );

  const isAdmin = computed(() => currentUser.value?.role === ROLES.ADMIN);

  // ── 代理操作権限 ─────────────────────────────────────────────
  /** 他生徒への代理操作が可能か（figure委員 or 司書） */
  const canProxy = computed(() => isCommittee.value || isLibrarian.value);

  // ── 所属校 ───────────────────────────────────────────────────
  const schoolId = computed(() => currentUser.value?.school_id ?? null);
  const schoolName = computed(() => currentUser.value?.school_name ?? "");

  // ── 表示名 ───────────────────────────────────────────────────
  const displayName = computed(() => {
    if (!currentUser.value) return "";
    if (isCommittee.value) return `${currentUser.value.name}（図書委員）`;
    return currentUser.value.name;
  });

  return {
    isLoggedIn,
    currentUser,
    isStudent,
    isCommittee,
    isLibrarian,
    isAdmin,
    canProxy,
    schoolId,
    schoolName,
    displayName,
  };
}
