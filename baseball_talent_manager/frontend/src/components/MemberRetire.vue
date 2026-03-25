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

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { updateUserStatus, getUsers } from "@/services/userService.js";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";
import MemberConfirmModal from "@/components/member/MemberConfirmModal.vue";
import MemberFilterBar from "@/components/member/MemberFilterBar.vue";
import MemberTable from "@/components/member/MemberTable.vue";

const route = useRoute();
const router = useRouter();
const allMembers = ref([]);

onMounted(async () => {
  try {
    const res = await getUsers("member");
    allMembers.value = res.data.users;
  } catch (e) {
    console.error("ユーザー取得失敗", e);
  }
});

// activeな部員のみ表示
const activeMembers = computed(() =>
  allMembers.value.filter((m) => m.status === "active"),
);

// モーダル制御
const showModal = ref(false);
const selectedMember = ref(null);
const actionType = ref("");
const successMessage = ref("");

const closeModal = () => {
  showModal.value = false;
  selectedMember.value = null;
  actionType.value = "";
};

const openModal = (member, type) => {
  selectedMember.value = member;
  actionType.value = type;
  showModal.value = true;
};

const handleProcess = async () => {
  try {
    const label = actionType.value === "retired" ? "引退" : "退部";

    await updateUserStatus(selectedMember.value.user_id, actionType.value);

    const res = await getUsers("member");
    allMembers.value = res.data.users;

    successMessage.value = `${selectedMember.value.name}さんを${label}処理しました`;
    closeModal();
  } catch (e) {
    console.error("更新失敗", e);
  }
};

// ソート関数化（可読性向上）
const compareValues = (a, b, key, order = "asc") => {
  const valA = a[key];
  const valB = b[key];

  // 数値判定
  if (!isNaN(valA) && !isNaN(valB)) {
    return order === "asc"
      ? Number(valA) - Number(valB)
      : Number(valB) - Number(valA);
  }

  // 文字列判定（日本語対応）
  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

/* -----------------------------
   フィルタ
----------------------------- */
const filterName = ref(route.query.name || "");
const filterGrade = ref(route.query.grade || "");

// フィルタ適用
const filteredMembers = computed(() => {
  return activeMembers.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" || m.grade === Number(filterGrade.value);

    // 大文字小文字を無視する場合はこちらを使用可能
    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    return gradeMatch && nameMatch;
  });
});

/* -----------------------------
   ソート情報
----------------------------- */
const sortKey = ref(route.query.sort || "grade");
const sortOrder = ref(route.query.order || "asc");

const toggleOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

const sortedMembers = computed(() =>
  [...filteredMembers.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value),
  ),
);

const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMembers);

pageSize.value = Number(route.query.pageSize) || 10;

/* -----------------------------
   フィルタ・ソート・ページリセット
----------------------------- */
const resetFilters = () => {
  sortKey.value = "grade";
  sortOrder.value = "asc";
  filterName.value = "";
  filterGrade.value = "";
  currentPage.value = 1;
};
/* -----------------------------
   URL更新
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
   リセットボタン無効判定
----------------------------- */
const isResetDisabled = computed(() => {
  return (
    !filterName.value &&
    !filterGrade.value &&
    sortKey.value === "grade" &&
    sortOrder.value === "asc"
  );
});
</script>
