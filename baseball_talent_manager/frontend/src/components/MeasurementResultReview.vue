<template>
  <div class="container mt-4">
    <h2 v-if="!isCoach" class="mb-4">測定結果の確認/承認</h2>
    <div
      v-if="isCoach"
      class="d-flex justify-content-between align-items-center mb-4"
    >
      <h2 class="mb-4">測定結果の確認/承認</h2>

      <div class="d-flex flex-wrap gap-2 align-items-center">
        <!-- ソート項目 -->
        <select v-model="sortKey" class="form-select form-select-sm w-auto">
          <option value="name">部員名</option>
          <option value="grade">学年</option>
          <option value="measurement_date">計測日</option>
        </select>

        <!-- 昇順 / 降順 -->
        <button
          class="btn btn-outline-secondary btn-sm"
          @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
        >
          {{ sortOrder === "asc" ? "昇順" : "降順" }}
        </button>

        <!-- 名前検索 -->
        <input
          v-model="filterName"
          type="text"
          class="form-control form-control-sm w-auto"
          placeholder="部員名"
        />

        <!-- 学年 -->
        <select v-model="filterGrade" class="form-select form-select-sm w-auto">
          <option value="">全学年</option>
          <option value="1">1年</option>
          <option value="2">2年</option>
          <option value="3">3年</option>
        </select>

        <!-- 計測日 -->
        <select
          v-model="filterMeasurementDate"
          class="form-select form-select-sm w-auto"
        >
          <option value="">全期間</option>
          <option v-for="date in availableDates" :key="date" :value="date">
            {{ date }}
          </option>
        </select>

        <!-- リセット -->
        <button class="btn btn-outline-danger btn-sm" @click="resetFilters">
          リセット
        </button>
      </div>
    </div>

    <!-- データなし -->
    <div v-if="!hasMeasurements" class="alert alert-info">
      承認依頼はありません
    </div>

    <!-- テーブル -->
    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <!-- ヘッダー -->
        <thead class="table-light">
          <tr>
            <th v-if="isCoach">部員名</th>
            <th v-if="isCoach">学年</th>
            <th>計測日</th>

            <th
              v-for="field in MEASUREMENT_FIELDS"
              :key="field.key"
              class="break"
            >
              {{ field.label }} ({{ field.unit }})
            </th>

            <th>承認の有無</th>
          </tr>
        </thead>

        <!-- データ -->
        <tbody>
          <tr
            v-for="measurement in paginatedData"
            :key="measurement.measurement_id"
          >
            <td v-if="isCoach">
              {{ measurement.name }}
            </td>
            <td v-if="isCoach">{{ measurement.grade }}年</td>
            <td>{{ measurement.measurement_date }}</td>
            <td
              v-for="field in MEASUREMENT_FIELDS"
              :key="`${measurement.measurement_id}-${field.key}`"
            >
              {{ measurement[field.key] }} {{ field.unit }}
            </td>
            <td>
              <div class="d-flex flex-wrap gap-2">
                <button
                  @click="handleApprove(measurement.measurement_id)"
                  class="btn btn-primary"
                  type="button"
                >
                  承認
                </button>

                <button
                  @click="handleReject(measurement.measurement_id)"
                  class="btn btn-danger"
                  type="button"
                >
                  否認
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ページネーション / 件数選択 -->
    <div class="d-flex justify-content-between align-items-center mt-3">
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
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";

import {
  getMeasurements,
  memberApprove,
  coachApprove,
} from "@/services/measurementService.js";

/* -----------------------------
   ステート
----------------------------- */
const allMeasurements = ref([]);

/*フィルタ */
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
   ソート設定
----------------------------- */
const sortKey = ref("measurement_date");
const sortOrder = ref("asc");

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

  // 文字列判定
  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

const filteredMeasurements = computed(() => {
  // コーチ以外はそのまま
  if (!isCoach.value) return measurements.value;

  return measurements.value.filter((m) => {
    // 名前（部分一致）
    const matchName =
      !filterName.value ||
      (m.name ?? "").toLowerCase().includes(filterName.value.toLowerCase());

    // 学年
    const matchGrade =
      !filterGrade.value || String(m.grade) === String(filterGrade.value);

    // 計測日（YYYY-MM一致）
    const matchDate =
      !filterMeasurementDate.value ||
      m.measurement_date.startsWith(filterMeasurementDate.value);

    return matchName && matchGrade && matchDate;
  });
});

/* ソート */
const sortedMeasurements = computed(() => {
  return [...filteredMeasurements.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value),
  );
});

const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMeasurements);

// 表示データがあるか
const hasMeasurements = computed(() => sortedMeasurements.value.length > 0);

// 登録済み計測年月（重複なし）
const availableDates = computed(() => {
  const dates = measurements.value.map((m) => m.measurement_date.slice(0, 7));
  return [...new Set(dates)].sort();
});

const resetFilters = () => {
  filterName.value = "";
  filterGrade.value = "";
  filterMeasurementDate.value = "";
  sortKey.value = "measurement_date";
  sortOrder.value = "asc";
};

/* 承認 / 否認*/
const handleApprove = async (measurementId) => {
  if (role.value === "member") {
    await memberApprove(measurementId, "approve");
  } else if (role.value === "coach") {
    await coachApprove(measurementId, "approve");
  }
  await fetchMeasurements();
};

const handleReject = async (measurementId) => {
  if (role.value === "member") {
    await memberApprove(measurementId, "reject");
  } else if (role.value === "coach") {
    await coachApprove(measurementId, "reject");
  }
  await fetchMeasurements();
};

watch(
  [filterName, filterGrade, filterMeasurementDate, sortKey, sortOrder],
  () => {
    currentPage.value = 1;
  },
);
</script>

<style>
.table th,
.table td {
  text-align: center;
  vertical-align: middle;
}
.table th {
  white-space: nowrap;
}
</style>
