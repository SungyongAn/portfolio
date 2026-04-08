<template>
  <div class="container mt-4">
    <div
      class="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-2"
    >
      <h2 class="mb-0 flex-shrink-0">退部・引退履歴</h2>

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

    <!-- 部員一覧テーブル -->
    <div class="card shadow-sm">
      <div class="card-body p-0">
        <table class="table mb-0">
          <thead class="table-light">
            <tr>
              <th>部員名</th>
              <th>学年</th>
              <th>ステータス</th>
              <th>退部 / 引退日</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in paginatedData" :key="m.user_id">
              <td>{{ m.name }}</td>
              <td>{{ m.grade ?? "-" }}</td>
              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-secondary': m.status === 'withdrawn',
                    'bg-warning text-dark': m.status === 'retired',
                  }"
                >
                  {{ formatStatus(m.status) }}
                </span>
              </td>
              <td>
                {{ formatDate(m.status_changed_at) }}
              </td>
            </tr>

            <tr v-if="paginatedData.length === 0">
              <td colspan="4" class="text-center text-muted py-3">
                該当するデータがありません
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

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
import { getUsers } from "@/services/userService.js";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";
import MemberFilterBar from "@/components/member/MemberFilterBar.vue";

const route = useRoute();
const router = useRouter();

const allMembers = ref([]);

/* -----------------------------
   初期データ取得
----------------------------- */
onMounted(async () => {
  try {
    const res = await getUsers("member");
    allMembers.value = res.data.users;
  } catch (e) {
    console.error("ユーザー取得失敗", e);
  }
});

/* -----------------------------
   非activeのみ（履歴）
----------------------------- */
const historyMembers = computed(() =>
  allMembers.value.filter((m) => m.status !== "active"),
);

/* -----------------------------
   フィルタ
----------------------------- */
const filterName = ref(route.query.name || "");
const filterGrade = ref(route.query.grade || "");

const filteredMembers = computed(() => {
  return historyMembers.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" || m.grade === Number(filterGrade.value);

    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    return gradeMatch && nameMatch;
  });
});

/* -----------------------------
   ソート
----------------------------- */
const sortKey = ref(route.query.sort || "grade");
const sortOrder = ref(route.query.order || "asc");

const toggleOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

const compareValues = (a, b, key, order = "asc") => {
  const valA = a[key];
  const valB = b[key];

  if (!isNaN(valA) && !isNaN(valB)) {
    return order === "asc"
      ? Number(valA) - Number(valB)
      : Number(valB) - Number(valA);
  }

  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

const sortedMembers = computed(() =>
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
   表示フォーマット
----------------------------- */
const formatStatus = (status) => {
  if (status === "retired") return "引退";
  if (status === "withdrawn") return "退部";
  return status;
};

const formatDate = (dateStr) => {
  if (!dateStr) return "-";

  const date = new Date(dateStr);
  return date.toLocaleDateString("ja-JP");
};

/* -----------------------------
   リセット
----------------------------- */
const resetFilters = () => {
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
   リセットボタン制御
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
