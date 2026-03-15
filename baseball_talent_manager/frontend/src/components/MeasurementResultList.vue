<template>
  <div class="container mt-4">
    <!-- ページタイトル -->
    <h2 class="mb-4">測定結果の閲覧</h2>

    <!-- データなし -->
    <div v-if="measurements.length === 0" class="alert alert-info">
      測定結果はありません
    </div>

    <!-- テーブル形式 -->
    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th v-if="isStaff">部員名</th>
            <th>計測日</th>
            <th>50m走 (sec)</th>
            <th>ベースランニング (sec)</th>
            <th>遠投 (m)</th>
            <th>ストレート球速 (km/h)</th>
            <th>打球速度 (km/h)</th>
            <th>スイング速度 (km/h)</th>
            <th>ベンチプレス (kg)</th>
            <th>スクワット (kg)</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="measurement in measurements"
            :key="measurement.measurement_id"
          >
            <td v-if="isStaff">
              {{ measurement.name }}（{{ measurement.grade }}年）
            </td>
            <td>{{ measurement.measurement_date }}</td>
            <td>
              {{ measurement.sprint_50m }}
            </td>
            <td>
              {{ measurement.base_running }}
            </td>
            <td>
              {{ measurement.throwing_distance }}
            </td>
            <td>
              {{ measurement.pitch_speed }}
            </td>
            <td>
              {{ measurement.batting_speed }}
            </td>
            <td>
              {{ measurement.swing_speed }}
            </td>
            <td>
              {{ measurement.bench_press }}
            </td>
            <td>
              {{ measurement.squat }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { getMeasurements } from "@/services/measurementService.js";

const allMeasurements = ref([]);

onMounted(async () => {
  const res = await getMeasurements();
  allMeasurements.value = res.data.measurements;
});

const authStore = useAuthStore();
const role = computed(() => authStore.role);

const isStaff = computed(() =>
  ["manager", "coach", "director"].includes(role.value),
);

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
</script>
