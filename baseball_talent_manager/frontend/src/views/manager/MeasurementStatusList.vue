<template>
  <div class="container mt-4">
    <!-- ページタイトル -->
    <h2 class="mb-4">承認フロー ステータス一覧</h2>

    <!-- データなし -->
    <div v-if="measurements.length === 0" class="alert alert-info">
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
          <tr v-for="measurement in measurements" :key="measurement.measurement_id">
            <td>{{ measurement.name }}</td>
            <td>{{ measurement.grade }}年</td>
            <td>{{ measurement.measurement_date }}</td>
            <td>
              <span :class="['badge', statusConfig[measurement.status].badge]">
                {{ statusConfig[measurement.status].label }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { dummyMeasurements } from "@/dummyData";

// 測定記録一覧
const measurements = ref([]);

// ステータスの表示名・バッジカラー定義
const statusConfig = {
  approved: { label: "承認済み", badge: "bg-success" },
  pending_member: { label: "部員承認待ち", badge: "bg-warning text-dark" },
  pending_coach: { label: "コーチ承認待ち", badge: "bg-primary" },
  rejected: { label: "否認", badge: "bg-danger" },
};

// 測定記録一覧取得
onMounted(() => {
  measurements.value = dummyMeasurements;
});
</script>
