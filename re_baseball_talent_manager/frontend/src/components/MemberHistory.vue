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

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { getUsers } from "@/services/userService";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";
import MemberFilterBar from "@/components/member/MemberFilterBar.vue";

// 型
import type { User, UserStatus } from "@/services/userService";

const route = useRoute();
const router = useRouter();

/* -----------------------------
   クエリヘルパー
----------------------------- */
const getQueryString = (value: unknown): string => {
  return typeof value === "string" ? value : "";
};

/* -----------------------------
   データ
----------------------------- */
const allMembers = ref<User[]>([]);

/* -----------------------------
   初期データ取得
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
   非activeのみ（履歴）
----------------------------- */
const historyMembers = computed<User[]>(() =>
  allMembers.value.filter((m) => m.status !== "active")
);

/* -----------------------------
   フィルタ
----------------------------- */
const filterName = ref<string>(getQueryString(route.query.name));
const filterGrade = ref<string>(getQueryString(route.query.grade));

const filteredMembers = computed<User[]>(() => {
  return historyMembers.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" ||
      m.grade === Number(filterGrade.value);

    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    return gradeMatch && nameMatch;
  });
});

/* -----------------------------
   ソート
----------------------------- */
const sortKey = ref<keyof User>(
  (getQueryString(route.query.sort) as keyof User) || "grade"
);

const sortOrder = ref<"asc" | "desc">(
  getQueryString(route.query.order) === "desc" ? "desc" : "asc"
);

const toggleOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

const compareValues = (
  a: User,
  b: User,
  key: keyof User,
  order: "asc" | "desc" = "asc"
): number => {
  const valA = a[key];
  const valB = b[key];

  // 数値
  if (typeof valA === "number" && typeof valB === "number") {
    return order === "asc" ? valA - valB : valB - valA;
  }

  // 日付（status_changed_atなど想定）
  if (key === "status_changed_at") {
    return order === "asc"
      ? new Date(valA as string).getTime() -
          new Date(valB as string).getTime()
      : new Date(valB as string).getTime() -
          new Date(valA as string).getTime();
  }

  // 文字列
  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

const sortedMembers = computed<User[]>(() =>
  [...filteredMembers.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value)
  )
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
const formatStatus = (status: UserStatus): string => {
  if (status === "retired") return "引退";
  if (status === "inactive") return "退部"; // ←ここ修正ポイント
  return status;
};

const formatDate = (dateStr: string | null): string => {
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
watch(
  [filterName, filterGrade, sortKey, sortOrder, pageSize],
  () => {
    currentPage.value = 1;

    router.replace({
      query: {
        name: filterName.value || undefined,
        grade: filterGrade.value || undefined,
        sort: sortKey.value,
        order: sortOrder.value,
        pageSize:
          pageSize.value !== 10 ? pageSize.value : undefined,
      },
    });
  }
);

/* -----------------------------
   リセットボタン制御
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