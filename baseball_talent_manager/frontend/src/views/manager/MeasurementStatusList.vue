<template>
  <div class="container mt-4">
    <!-- ページタイトル -->
    <h2 class="mb-4">承認フロー ステータス一覧</h2>

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
            v-for="measurement in measurements"
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
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { getMeasurements } from "@/services/measurementService.js";

const measurements = ref([]);

onMounted(async () => {
  const res = await getMeasurements();
  measurements.value = res.data.measurements;
});

const hasMeasurements = computed(() => measurements.value.length > 0);

const statusConfig = {
  approved: { label: "承認済み", badge: "bg-success" },
  pending_member: { label: "部員承認待ち", badge: "bg-warning text-dark" },
  pending_coach: { label: "コーチ承認待ち", badge: "bg-primary" },
  rejected: { label: "否認", badge: "bg-danger" },
};

const getStatus = (status) => {
  return (
    statusConfig[status] ?? {
      label: "不明",
      badge: "bg-secondary",
    }
  );
};
</script>
