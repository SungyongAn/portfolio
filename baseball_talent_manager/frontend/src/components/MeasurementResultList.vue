<template>
  <div class="container mt-4">
    <!-- ヘッダー / ソート・フィルタ -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">測定結果の閲覧</h2>

      <div class="d-flex gap-2 align-items-center">
        <!-- ソート項目 -->
        <select v-model="sortKey" class="form-select form-select-sm">
          <option value="measurement_date">計測日</option>
          <option v-if="isStaff" value="name">部員名</option>
          <option v-if="isStaff" value="grade">学年</option>
          <option value="sprint_50m">50m走</option>
          <option value="base_running">ベースランニング</option>
          <option value="throwing_distance">遠投</option>
          <option value="pitch_speed">球速</option>
          <option value="batting_speed">打球速度</option>
          <option value="swing_speed">スイング速度</option>
          <option value="bench_press">ベンチプレス</option>
          <option value="squat">スクワット</option>
        </select>

        <!-- 昇順 / 降順 -->
        <button
          @click="toggleOrder"
          class="btn btn-outline-primary btn-sm text-nowrap"
        >
          {{ sortOrder === "asc" ? "昇順 ↑" : "降順 ↓" }}
        </button>

        <!-- 名前フィルタ -->
        <input
          v-model="filterName"
          type="text"
          placeholder="名前検索"
          class="form-control form-control-sm ms-3"
        />

        <!-- 計測日フィルタ -->
        <select
          v-model="filterMeasurementDate"
          class="form-select form-select-sm ms-3"
        >
          <option value="">計測日（全て）</option>
          <option v-for="date in availableDates" :key="date" :value="date">
            {{ date }}
          </option>
        </select>

        <!-- 学年フィルタ -->
        <select v-model="filterGrade" class="form-select form-select-sm">
          <option value="">学年（全て）</option>
          <option value="1">1年</option>
          <option value="2">2年</option>
          <option value="3">3年</option>
        </select>

        <!-- リセット -->
        <button
          @click="resetFilters"
          :disabled="isResetDisabled"
          class="btn btn-outline-secondary btn-sm ms-2 text-nowrap"
        >
          リセット
        </button>
      </div>
    </div>

    <!-- データなし表示 -->
    <div v-if="measurements.length === 0" class="alert alert-info">
      測定結果はありません
    </div>

    <!-- テーブル表示 -->
    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <!-- ヘッダー -->
        <thead class="table-light">
          <tr>
            <th v-if="isStaff" style="white-space: nowrap">部員名</th>
            <th v-if="isStaff" style="white-space: nowrap">学年</th>
            <th style="white-space: nowrap">計測日</th>
            <th style="white-space: nowrap">50m走 (sec)</th>
            <th style="white-space: nowrap">ベースランニング (sec)</th>
            <th style="white-space: nowrap">遠投 (m)</th>
            <th style="white-space: nowrap">ストレート球速 (km/h)</th>
            <th style="white-space: nowrap">打球速度 (km/h)</th>
            <th style="white-space: nowrap">スイング速度 (km/h)</th>
            <th style="white-space: nowrap">ベンチプレス (kg)</th>
            <th style="white-space: nowrap">スクワット (kg)</th>
          </tr>
        </thead>

        <!-- ボディ -->
        <tbody>
          <tr
            v-for="measurement in paginatedData"
            :key="measurement.measurement_id"
          >
            <td v-if="isStaff">{{ measurement.name }}</td>
            <td v-if="isStaff">{{ measurement.grade }}年</td>
            <td>{{ measurement.measurement_date }}</td>
            <td>{{ measurement.sprint_50m }}</td>
            <td>{{ measurement.base_running }}</td>
            <td>{{ measurement.throwing_distance }}</td>
            <td>{{ measurement.pitch_speed }}</td>
            <td>{{ measurement.batting_speed }}</td>
            <td>{{ measurement.swing_speed }}</td>
            <td>{{ measurement.bench_press }}</td>
            <td>{{ measurement.squat }}</td>
          </tr>
        </tbody>
      </table>

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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { getMeasurements } from "@/services/measurementService.js";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";

/* -----------------------------
   ルーター・認証情報
----------------------------- */
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const role = computed(() => authStore.role);
const isStaff = computed(() =>
  ["manager", "coach", "director"].includes(role.value),
);

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

<style>
.table th,
.table td {
  text-align: center;
  vertical-align: middle;
}
</style>
