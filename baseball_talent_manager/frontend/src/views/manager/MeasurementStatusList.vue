<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-4">承認フロー ステータス一覧</h2>

      <div class="d-flex gap-2 align-items-center">
        <!-- ソート項目 -->
        <select v-model="sortKey" class="form-select form-select-sm">
          <option value="name">部員名</option>
          <option value="grade">学年</option>
          <option value="status">ステータス</option>
          <option value="measurement_date">計測日</option>
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

        <!-- 学年フィルタ -->
        <select v-model="filterGrade" class="form-select form-select-sm">
          <option value="">学年（全て）</option>
          <option value="1">1年</option>
          <option value="2">2年</option>
          <option value="3">3年</option>
        </select>

        <!-- ステータスフィルタ -->
        <select v-model="filterStatus" class="form-select form-select-sm">
          <option value="">ステータス</option>
          <option value="approved">承認済み</option>
          <option value="pending_member">部員承認待ち</option>
          <option value="pending_coach">コーチ承認待ち</option>
          <option value="rejected">否認</option>
        </select>

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
    <!-- データなし -->
    <div v-if="!hasMeasurements" class="alert alert-info">
      測定記録がありません
    </div>

    <!-- テーブル形式 -->
    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th>部員名</th>
            <th>学年</th>
            <th>計測日</th>
            <th>ステータス</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="measurement in paginatedData"
            :key="measurement.measurement_id"
          >
            <td>{{ measurement.name }}</td>
            <td>{{ measurement.grade }}年</td>
            <td>{{ measurement.measurement_date }}</td>
            <td>
              <span :class="['badge', getStatus(measurement.status).badge]">
                {{ getStatus(measurement.status).label }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ページネーション / 件数選択 -->
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
/* -----------------------------
   インポート
----------------------------- */
import { ref, computed, onMounted, watch } from "vue";
import { getMeasurements } from "@/services/measurementService.js";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";
import { useNotificationStore } from "@/stores/notification";

/* -----------------------------
   ルーター・リアクティブ変数
----------------------------- */
const route = useRoute();
const router = useRouter();
const notificationStore = useNotificationStore();

const measurements = ref([]);

/*フィルタ */
const filterName = ref(route.query.name || "");
const filterGrade = ref(route.query.grade || "");
const filterStatus = ref(route.query.status || "");
const filterMeasurementDate = ref(route.query.date || "");

/* ソート情報 */
const sortKey = ref(route.query.sort || "measurement_date");
const sortOrder = ref(route.query.order || "asc");

/* -----------------------------
   定数
----------------------------- */
const statusConfig = {
  draft: { label: "入力済み（未依頼）", badge: "bg-secondary" },
  approved: { label: "承認済み", badge: "bg-success" },
  pending_member: { label: "部員承認待ち", badge: "bg-warning text-dark" },
  pending_coach: { label: "コーチ承認待ち", badge: "bg-primary" },
  rejected: { label: "否認", badge: "bg-danger" },
};

/* -----------------------------
   computed系（依存順に）
----------------------------- */

// フィルタ適用
const filteredMeasurements = computed(() =>
  measurements.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" || m.grade === Number(filterGrade.value);

    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    const statusMatch =
      filterStatus.value === "" || m.status === filterStatus.value;

    const measurementDateMatch =
      filterMeasurementDate.value === "" ||
      m.measurement_date.includes(filterMeasurementDate.value);

    return gradeMatch && nameMatch && statusMatch && measurementDateMatch;
  }),
);

// ソート用比較関数
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

// ソート済みデータ
const sortedMeasurements = computed(() =>
  [...filteredMeasurements.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value),
  ),
);

const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMeasurements);

// URLから初期値
pageSize.value = Number(route.query.pageSize) || 10;

// 表示データがあるか
const hasMeasurements = computed(() => paginatedData.value.length > 0);

// 登録済み計測年月（重複なし）
const availableDates = computed(() => {
  const dates = measurements.value.map((m) => m.measurement_date.slice(0, 7));
  return [...new Set(dates)].sort();
});

// リセットボタン無効判定
const isResetDisabled = computed(
  () =>
    !filterName.value &&
    !filterGrade.value &&
    !filterStatus.value &&
    !filterMeasurementDate.value &&
    sortKey.value === "measurement_date" &&
    sortOrder.value === "asc",
);

/* -----------------------------
   メソッド系
----------------------------- */

// ステータス表示用
const getStatus = (status) =>
  statusConfig[status] ?? { label: "不明", badge: "bg-secondary" };

// ソート順切替
const toggleOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

// フィルタ・ソート・ページリセット
const resetFilters = () => {
  sortKey.value = "measurement_date";
  sortOrder.value = "asc";
  filterName.value = "";
  filterGrade.value = "";
  filterStatus.value = "";
  filterMeasurementDate.value = "";
  currentPage.value = 1;
};

/* -----------------------------
   副作用系
----------------------------- */

// データ取得
onMounted(async () => {
  const res = await getMeasurements();
  measurements.value = res.data.measurements;
});

// URL更新（queryパラメータ反映）
watch(
  [
    filterName,
    filterGrade,
    filterStatus,
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
        status: filterStatus.value || undefined,
        date: filterMeasurementDate.value || undefined,
        sort: sortKey.value,
        order: sortOrder.value,
        pageSize: pageSize.value !== 10 ? pageSize.value : undefined,
      },
    });
  },
);

// 通知受信時のwatch（独立して追加）
watch(
  () => notificationStore.notifications.length,
  async () => {
    const res = await getMeasurements();
    measurements.value = res.data.measurements ?? [];
  },
);
</script>
