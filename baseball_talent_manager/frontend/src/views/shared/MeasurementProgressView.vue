<template>
  <div class="container mt-4">
    <div
      class="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-2"
    >
      <h2 class="mb-0">測定登録状況</h2>

      <!-- 年月ピッカー -->
      <input type="month" v-model="selectedMonth" class="form-control w-auto" />
    </div>

    <!-- 一覧テーブル -->
    <div class="card shadow-sm">
      <div class="card-body p-0">
        <table class="table mb-0">
          <thead class="table-light">
            <tr>
              <th>部員名</th>
              <th>学年</th>
              <th>登録状況</th>
              <th>ステータス</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="m in displayData" :key="m.user_id">
              <td>{{ m.name }}</td>
              <td>{{ m.grade ?? "-" }}</td>

              <!-- 登録状況 -->
              <td>
                <span
                  class="badge"
                  :class="m.isRegistered ? 'bg-success' : 'bg-secondary'"
                >
                  {{ m.isRegistered ? "登録済み" : "未登録" }}
                </span>
              </td>

              <!-- 承認ステータス -->
              <td>
                <span
                  v-if="m.isRegistered"
                  class="badge"
                  :class="getStatusClass(m.status)"
                >
                  {{ formatStatus(m.status) }}
                </span>
                <span v-else class="text-muted">-</span>
              </td>
            </tr>

            <tr v-if="displayData.length === 0">
              <td colspan="4" class="text-center text-muted py-3">
                データがありません
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
import { ref, computed, onMounted } from "vue";
import { getUsers } from "@/services/userService.js";
import { getAllMeasurements } from "@/services/measurementService.js";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";

/* -----------------------------
   state
----------------------------- */
const members = ref([]);
const measurements = ref([]);
const selectedMonth = ref("");

/* -----------------------------
   初期化
----------------------------- */
onMounted(async () => {
  try {
    // 当月セット
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, "0");
    selectedMonth.value = `${yyyy}-${mm}`;

    // データ取得
    const [userRes, measurementRes] = await Promise.all([
      getUsers("member"),
      getAllMeasurements(),
    ]);

    members.value = userRes.data.users;
    measurements.value = measurementRes.data.measurements;
  } catch (e) {
    console.error("初期データ取得失敗", e);
  }
});

/* -----------------------------
   対象月の測定データ
----------------------------- */
const filteredMeasurements = computed(() => {
  return measurements.value.filter((m) =>
    m.measurement_date.startsWith(selectedMonth.value),
  );
});

/* -----------------------------
   突き合わせ（ここがコア）
----------------------------- */
const mergedData = computed(() => {
  return members.value
    .filter((member) => member.status === "active")
    .map((member) => {
      const record = filteredMeasurements.value.find(
        (m) => m.user_id === member.user_id,
      );
      return {
        ...member,
        isRegistered: !!record,
        status: record?.status || null,
      };
    });
});

/* -----------------------------
   ソート（任意：学年順）
----------------------------- */
const sortedData = computed(() => {
  return [...mergedData.value].sort((a, b) => {
    return (a.grade || 0) - (b.grade || 0);
  });
});

/* -----------------------------
   ページネーション
----------------------------- */
const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedData);

pageSize.value = 10;

const displayData = paginatedData;

/* -----------------------------
   表示用
----------------------------- */
const formatStatus = (status) => {
  if (status === "draft") return "入力済み（未依頼）";
  if (status === "pending_member") return "部員承認待ち";
  if (status === "pending_coach") return "コーチ承認待ち";
  if (status === "approved") return "承認済み";
  if (status === "rejected") return "否認";
  return "-";
};

const getStatusClass = (status) => {
  if (status === "approved") return "bg-success";
  if (status === "pending_member") return "bg-warning text-dark";
  if (status === "pending_coach") return "bg-primary";
  if (status === "rejected") return "bg-danger";
  return "bg-secondary";
};
</script>
