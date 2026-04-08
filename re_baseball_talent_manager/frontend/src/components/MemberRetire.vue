<template>
  <div class="container mt-4">
    <div
      class="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-2"
    >
      <h2 class="mb-0 flex-shrink-0">部員退部・引退処理</h2>

      <MemberFilterBar
        :sortKey="sortKey"
        :sortOrder="sortOrder"
        :filterName="filterName"
        :filterGrade="filterGrade"
        :isResetDisabled="isResetDisabled"
        @update:sortKey="sortKey = $event"
        @update:filterName="filterName = $event"
        @update:filterGrade="filterGrade = $event"
        @toggleOrder="toggleOrder"
        @reset="resetFilters"
      />
    </div>

    <!-- 成功メッセージ -->
    <div v-if="successMessage" class="alert alert-success">
      <i class="bi bi-check-circle me-2"></i>
      {{ successMessage }}
    </div>

    <!-- 部員一覧テーブル -->
    <MemberTable
      :members="paginatedData"
      @retire="(member) => openModal(member, 'retired')"
      @withdraw="(member) => openModal(member, 'withdrawn')"
    />

    <!-- 確認モーダル -->
    <MemberConfirmModal
      :show="showModal"
      :member="selectedMember"
      :actionType="actionType"
      @close="closeModal"
      @confirm="handleProcess"
    />

    <!-- ページネーション -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <Pagination
        v-model="currentPage"
        :totalPages="totalPages"
        :pageSize="pageSize"
        @update:pageSize="
          pageSize = $event;
          currentPage = 1;
        "
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { updateUserStatus, getUsers } from "@/services/userService";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";
import MemberConfirmModal from "@/components/member/MemberConfirmModal.vue";
import MemberFilterBar from "@/components/member/MemberFilterBar.vue";
import MemberTable from "@/components/member/MemberTable.vue";

// ✅ 型import
import type { User, UserStatus } from "@/services/userService";
import type { ActionType } from "@/components/member/MemberConfirmModal.vue";

const route = useRoute();
const router = useRouter();

/* -----------------------------
   データ
----------------------------- */
// ✅ 型付け
const allMembers = ref<User[]>([]);

/* -----------------------------
   初期取得
----------------------------- */
onMounted(async (): Promise<void> => {
  try {
    const res = await getUsers("member");
    allMembers.value = res.data.users;
  } catch (e) {
    console.error("ユーザー取得失敗", e);
  }
});

/* -----------------------------
   activeのみ
----------------------------- */
const activeMembers = computed<User[]>(() =>
  allMembers.value.filter((m) => m.status === "active"),
);

/* -----------------------------
   モーダル
----------------------------- */
const showModal = ref<boolean>(false);

// ✅ User | null
const selectedMember = ref<User | null>(null);

// ✅ ActionType
const actionType = ref<ActionType | "">("");

const successMessage = ref<string>("");

const closeModal = (): void => {
  showModal.value = false;
  selectedMember.value = null;
  actionType.value = "";
};

const openModal = (member: User, type: ActionType): void => {
  selectedMember.value = member;
  actionType.value = type;
  showModal.value = true;
};

/* -----------------------------
   処理実行
----------------------------- */
const handleProcess = async (): Promise<void> => {
  if (!selectedMember.value) return;

  try {
    const label = actionType.value === "retired" ? "引退" : "退部";

    // ❗ 修正ポイント：user_id → id
    await updateUserStatus(
      selectedMember.value.id,
      actionType.value as UserStatus,
    );

    const res = await getUsers("member");
    allMembers.value = res.data.users;

    successMessage.value = `${selectedMember.value.name}さんを${label}処理しました`;

    closeModal();
  } catch (e) {
    console.error("更新失敗", e);
  }
};

/* -----------------------------
   ソート
----------------------------- */
const compareValues = (
  a: User,
  b: User,
  key: keyof User,
  order: "asc" | "desc" = "asc",
): number => {
  const valA = a[key];
  const valB = b[key];

  // 数値
  if (typeof valA === "number" && typeof valB === "number") {
    return order === "asc" ? valA - valB : valB - valA;
  }

  // 文字列
  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

/* -----------------------------
   フィルタ
----------------------------- */
const getQueryString = (v: unknown): string => (typeof v === "string" ? v : "");

const filterName = ref<string>(getQueryString(route.query.name));
const filterGrade = ref<string>(getQueryString(route.query.grade));

const filteredMembers = computed<User[]>(() => {
  return activeMembers.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" || m.grade === Number(filterGrade.value);

    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    return gradeMatch && nameMatch;
  });
});

/* -----------------------------
   ソート状態
----------------------------- */
const sortKey = ref<keyof User>(
  (getQueryString(route.query.sort) as keyof User) || "grade",
);

const sortOrder = ref<"asc" | "desc">(
  getQueryString(route.query.order) === "desc" ? "desc" : "asc",
);

const toggleOrder = (): void => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

const sortedMembers = computed<User[]>(() =>
  [...filteredMembers.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value),
  ),
);

/* -----------------------------
   ページネーション
----------------------------- */
const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMembers);

pageSize.value = Number(route.query.pageSize) || 10;

/* -----------------------------
   リセット
----------------------------- */
const resetFilters = (): void => {
  sortKey.value = "grade";
  sortOrder.value = "asc";
  filterName.value = "";
  filterGrade.value = "";
  currentPage.value = 1;
};

/* -----------------------------
   URL同期
----------------------------- */
watch([filterName, filterGrade, sortKey, sortOrder, pageSize], () => {
  currentPage.value = 1;

  router.replace({
    query: {
      name: filterName.value || undefined,
      grade: filterGrade.value || undefined,
      sort: sortKey.value,
      order: sortOrder.value,
      pageSize: pageSize.value !== 10 ? pageSize.value : undefined,
    },
  });
});

/* -----------------------------
   リセット制御
----------------------------- */
const isResetDisabled = computed<boolean>(() => {
  return (
    !filterName.value &&
    !filterGrade.value &&
    sortKey.value === "grade" &&
    sortOrder.value === "asc"
  );
});
</script>
