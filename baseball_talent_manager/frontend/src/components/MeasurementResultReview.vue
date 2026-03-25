<template>
  <div class="container mt-4">
    <!-- ヘッダー -->
    <div
      class="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-2"
    >
      <h2 class="mb-0">測定結果の確認/承認</h2>

      <!-- コーチのみフィルタ表示 -->
      <MeasurementFilterBar
        v-if="isCoach"
        :sortKey="sortKey"
        :sortOrder="sortOrder"
        :filterName="filterName"
        :filterGrade="filterGrade"
        :filterMeasurementDate="filterMeasurementDate"
        :availableDates="availableDates"
        :isStaff="true"
        :isResetDisabled="isResetDisabled"
        @update:sortKey="sortKey = $event"
        @update:filterName="filterName = $event"
        @update:filterGrade="filterGrade = $event"
        @update:filterMeasurementDate="filterMeasurementDate = $event"
        @toggleOrder="toggleOrder"
        @reset="resetFilters"
      />
    </div>

    <!-- データなし -->
    <div v-if="!hasMeasurements" class="alert alert-info">
      承認依頼はありません
    </div>

    <!-- テーブル -->
    <MeasurementTable
      v-else
      :measurements="paginatedData"
      :isStaff="isCoach"
      :showActions="true"
      :submittingId="submittingId"
      @approve="handleApprove"
      @reject="handleReject"
    />

    <!-- ページネーション -->
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
import { usePagination } from "@/composables/usePagination";

import Pagination from "@/components/Pagination.vue";
import MeasurementFilterBar from "@/components/measurement/MeasurementFilterBar.vue";
import MeasurementTable from "@/components/measurement/MeasurementTable.vue";

import {
  getMeasurements,
  memberApprove,
  coachApprove,
} from "@/services/measurementService.js";

/* -----------------------------
   ステート
----------------------------- */
const allMeasurements = ref([]);

/* フィルタ */
const filterName = ref("");
const filterGrade = ref("");
const filterMeasurementDate = ref("");

/* -----------------------------
   認証・権限
----------------------------- */
const authStore = useAuthStore();
const role = computed(() => authStore.role);
const isCoach = computed(() => role.value === "coach");

/* -----------------------------
   データ取得
----------------------------- */
const fetchMeasurements = async () => {
  try {
    const res = await getMeasurements();
    allMeasurements.value = res.data.measurements;
  } catch (error) {
    console.error(error);
    alert("データの取得に失敗しました");
  }
};

onMounted(fetchMeasurements);

/* -----------------------------
   role別フィルタ
----------------------------- */
const measurements = computed(() => {
  if (role.value === "member") {
    return allMeasurements.value.filter(
      (m) => m.user_id === authStore.userId && m.status === "pending_member",
    );
  }
  if (role.value === "coach") {
    return allMeasurements.value.filter((m) => m.status === "pending_coach");
  }
  return [];
});

/* -----------------------------
   ソート
----------------------------- */
const sortKey = ref("measurement_date");
const sortOrder = ref("asc");

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

  if (key === "measurement_date") {
    return order === "asc"
      ? new Date(valA) - new Date(valB)
      : new Date(valB) - new Date(valA);
  }

  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

/* -----------------------------
   フィルタ
----------------------------- */
const filteredMeasurements = computed(() => {
  if (!isCoach.value) return measurements.value;

  return measurements.value.filter((m) => {
    const matchName =
      !filterName.value ||
      (m.name ?? "").toLowerCase().includes(filterName.value.toLowerCase());

    const matchGrade =
      !filterGrade.value || String(m.grade) === String(filterGrade.value);

    const matchDate =
      !filterMeasurementDate.value ||
      m.measurement_date.startsWith(filterMeasurementDate.value);

    return matchName && matchGrade && matchDate;
  });
});

/* -----------------------------
   ソート適用
----------------------------- */
const sortedMeasurements = computed(() =>
  [...filteredMeasurements.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value),
  ),
);

/* -----------------------------
   ページネーション
----------------------------- */
const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMeasurements);

const hasMeasurements = computed(() => sortedMeasurements.value.length > 0);

/* -----------------------------
   フィルタ用データ
----------------------------- */
const availableDates = computed(() => {
  const dates = measurements.value.map((m) => m.measurement_date.slice(0, 7));
  return [...new Set(dates)].sort();
});

const isResetDisabled = computed(() => {
  return (
    !filterName.value &&
    !filterGrade.value &&
    !filterMeasurementDate.value &&
    sortKey.value === "measurement_date" &&
    sortOrder.value === "asc"
  );
});

const resetFilters = () => {
  filterName.value = "";
  filterGrade.value = "";
  filterMeasurementDate.value = "";
  sortKey.value = "measurement_date";
  sortOrder.value = "asc";
  currentPage.value = 1;
};

/* -----------------------------
   承認 / 否認
----------------------------- */
// 二重クリック防止
const submittingId = ref(null);

const handleAction = async (id, action) => {
  if (submittingId.value) return;

  submittingId.value = id;
  try {
    if (role.value === "member") {
      await memberApprove(id, action);
    } else {
      await coachApprove(id, action);
    }

    await fetchMeasurements();
  } catch (error) {
    console.error(error);
    alert(`${action === "approve" ? "承認" : "否認"}に失敗しました`);
  } finally {
    submittingId.value = null;
  }
};

const handleApprove = (id) => handleAction(id, "approve");
const handleReject = (id) => handleAction(id, "reject");

/* -----------------------------
   ページリセット
----------------------------- */
watch(
  [filterName, filterGrade, filterMeasurementDate, sortKey, sortOrder],
  () => {
    currentPage.value = 1;
  },
);
</script>
