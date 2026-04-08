<template>
  <div class="container mt-4">
    <div
      class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-4"
    >
      <!-- タイトル -->
      <h2 class="mb-0 flex-shrink-0">測定結果の閲覧</h2>

      <!-- フィルタ -->
      <div class="ms-auto">
        <MeasurementFilterBar
          :sortKey="sortKey"
          :sortOrder="sortOrder"
          :filterName="filterName"
          :filterGrade="filterGrade"
          :filterMeasurementDate="filterMeasurementDate"
          :availableDates="availableDates"
          :isStaff="isStaff"
          :isResetDisabled="isResetDisabled"
          @update:sortKey="sortKey = $event"
          @update:filterName="filterName = $event"
          @update:filterGrade="filterGrade = $event"
          @update:filterMeasurementDate="filterMeasurementDate = $event"
          @toggleOrder="toggleOrder"
          @reset="resetFilters"
        />
      </div>
    </div>

    <div v-if="!hasMeasurements" class="alert alert-info">
      測定結果はありません
    </div>

    <MeasurementTable v-else :measurements="paginatedData" :isStaff="isStaff" />

    <div class="d-flex justify-content-center mt-3">
      <Pagination
        v-if="hasMeasurements"
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
import { useAuthStore } from "@/stores/auth";
import { getMeasurements } from "@/services/measurementService.js";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";
import MeasurementFilterBar from "@/components/measurement/MeasurementFilterBar.vue";
import MeasurementTable from "@/components/measurement/MeasurementTable.vue";

/* -----------------------------
   ルーター・認証情報
----------------------------- */
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const role = computed(() => authStore.role);
const staffRoles = ["manager", "coach", "director"];

const isStaff = computed(() => staffRoles.includes(role.value));

/* -----------------------------
  フィルタ
----------------------------- */
const filterName = ref(route.query.name || "");
const filterGrade = ref(route.query.grade || "");
const filterMeasurementDate = ref(route.query.date || "");

/* -----------------------------
   ソート情報
----------------------------- */
const sortKey = ref(route.query.sort || "measurement_date");
const sortOrder = ref(route.query.order || "asc");
const toggleOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

/* -----------------------------
   データ取得
----------------------------- */
const allMeasurements = ref([]);

onMounted(async () => {
  const res = await getMeasurements();
  allMeasurements.value = res.data.measurements;
});

/* -----------------------------
   元データからフィルタ・ソート・ページネーション
   依存関係順に整理
----------------------------- */

// 1. ロールに応じたデータ選別
const measurements = computed(() => {
  if (role.value === "member") {
    return allMeasurements.value.filter(
      (m) => m.user_id === authStore.userId && m.status === "approved",
    );
  }
  if (isStaff.value) {
    return allMeasurements.value.filter((m) => m.status === "approved");
  }
  return [];
});

// 2. 登録済みの計測年月を重複なしで取得
const availableDates = computed(() => {
  const dates = measurements.value.map(
    (m) => m.measurement_date.slice(0, 7), // "2025-08-01" → "2025-08"
  );
  return [...new Set(dates)].sort();
});

// 3. フィルタ適用
const filteredMeasurements = computed(() => {
  return measurements.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" || m.grade === Number(filterGrade.value);

    // 大文字小文字を無視する場合はこちらを使用可能
    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    const measurementDateMatch =
      filterMeasurementDate.value === "" ||
      m.measurement_date.includes(filterMeasurementDate.value);

    return gradeMatch && nameMatch && measurementDateMatch;
  });
});

// 4. ソート関数化（可読性向上）
const compareValues = (a, b, key, order = "asc") => {
  const valA = a[key];
  const valB = b[key];

  // 数値判定
  if (!isNaN(valA) && !isNaN(valB)) {
    return order === "asc"
      ? Number(valA) - Number(valB)
      : Number(valB) - Number(valA);
  }

  // 日付判定
  if (key === "measurement_date") {
    return order === "asc"
      ? new Date(valA) - new Date(valB)
      : new Date(valB) - new Date(valA);
  }

  // 文字列判定（日本語対応）
  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

const sortedMeasurements = computed(() =>
  [...filteredMeasurements.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value),
  ),
);

const hasMeasurements = computed(() => sortedMeasurements.value.length > 0);

const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMeasurements);

/* -----------------------------
   フィルタ・ソート・ページリセット
----------------------------- */
const resetFilters = () => {
  sortKey.value = "measurement_date";
  sortOrder.value = "asc";
  filterName.value = "";
  filterGrade.value = "";
  filterMeasurementDate.value = "";
  currentPage.value = 1;
};

/* -----------------------------
   URL更新
----------------------------- */
watch(
  [
    filterName,
    filterGrade,
    filterMeasurementDate,
    sortKey,
    sortOrder,
    pageSize,
  ],
  () => {
    currentPage.value = 1;
    router.replace({
      query: {
        name: filterName.value || undefined,
        grade: filterGrade.value || undefined,
        date: filterMeasurementDate.value || undefined,
        sort: sortKey.value,
        order: sortOrder.value,
        pageSize: pageSize.value !== 10 ? pageSize.value : undefined,
      },
    });
  },
);

/* -----------------------------
   リセットボタン無効判定
----------------------------- */
const isResetDisabled = computed(() => {
  return (
    !filterName.value &&
    !filterGrade.value &&
    !filterMeasurementDate.value &&
    sortKey.value === "measurement_date" &&
    sortOrder.value === "asc"
  );
});
</script>
