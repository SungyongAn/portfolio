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

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { getMeasurements } from "@/services/measurementService";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";
import MeasurementFilterBar from "@/components/measurement/MeasurementFilterBar.vue";
import MeasurementTable from "@/components/measurement/MeasurementTable.vue";

// 型
import type { Measurement } from "@/services/measurementService";
import type { Role } from "@/stores/auth";

/* -----------------------------
   ルーター・認証情報
----------------------------- */
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const role = computed<Role | null>(() => authStore.role);

// ✅ Role型を使う
const staffRoles: Role[] = ["manager", "coach", "director"];

const isStaff = computed<boolean>(() =>
  role.value ? staffRoles.includes(role.value) : false
);

/* -----------------------------
  クエリ取得ヘルパー
----------------------------- */
const getQueryString = (value: unknown): string => {
  return typeof value === "string" ? value : "";
};

/* -----------------------------
  フィルタ
----------------------------- */
const filterName = ref<string>(getQueryString(route.query.name));
const filterGrade = ref<string>(getQueryString(route.query.grade));
const filterMeasurementDate = ref<string>(
  getQueryString(route.query.date)
);

/* -----------------------------
   ソート情報
----------------------------- */
const sortKey = ref<string>(
  getQueryString(route.query.sort) || "measurement_date"
);

const sortOrder = ref<"asc" | "desc">(
  getQueryString(route.query.order) === "desc" ? "desc" : "asc"
);

const toggleOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

/* -----------------------------
   データ取得
----------------------------- */
const allMeasurements = ref<Measurement[]>([]);

onMounted(async () => {
  const res = await getMeasurements();
  allMeasurements.value = res.data.measurements;
});

/* -----------------------------
   データ加工
----------------------------- */

// 1. ロールに応じたデータ選別
const measurements = computed<Measurement[]>(() => {
  if (role.value === "member") {
    return allMeasurements.value.filter(
      (m) =>
        m.user_id === authStore.userId &&
        m.status === "approved"
    );
  }
  if (isStaff.value) {
    return allMeasurements.value.filter(
      (m) => m.status === "approved"
    );
  }
  return [];
});

// 2. 登録済み年月
const availableDates = computed<string[]>(() => {
  const dates = measurements.value.map((m) =>
    m.measurement_date.slice(0, 7)
  );
  return [...new Set(dates)].sort();
});

// 3. フィルタ
const filteredMeasurements = computed<Measurement[]>(() => {
  return measurements.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" ||
      m.grade === Number(filterGrade.value);

    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    const measurementDateMatch =
      filterMeasurementDate.value === "" ||
      m.measurement_date.includes(filterMeasurementDate.value);

    return gradeMatch && nameMatch && measurementDateMatch;
  });
});

/* -----------------------------
   ソート
----------------------------- */
const compareValues = (
  a: Measurement,
  b: Measurement,
  key: keyof Measurement,
  order: "asc" | "desc" = "asc"
): number => {
  const valA = a[key];
  const valB = b[key];

  // 数値
  if (typeof valA === "number" && typeof valB === "number") {
    return order === "asc" ? valA - valB : valB - valA;
  }

  // 日付
  if (key === "measurement_date") {
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

const sortedMeasurements = computed<Measurement[]>(() =>
  [...filteredMeasurements.value].sort((a, b) =>
    compareValues(a, b, sortKey.value as keyof Measurement, sortOrder.value)
  )
);

const hasMeasurements = computed<boolean>(
  () => sortedMeasurements.value.length > 0
);

/* -----------------------------
   ページネーション
----------------------------- */
const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMeasurements);

/* -----------------------------
   リセット
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
   URL同期
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
        pageSize:
          pageSize.value !== 10 ? pageSize.value : undefined,
      },
    });
  }
);

/* -----------------------------
   リセット無効判定
----------------------------- */
const isResetDisabled = computed<boolean>(() => {
  return (
    !filterName.value &&
    !filterGrade.value &&
    !filterMeasurementDate.value &&
    sortKey.value === "measurement_date" &&
    sortOrder.value === "asc"
  );
});
</script>