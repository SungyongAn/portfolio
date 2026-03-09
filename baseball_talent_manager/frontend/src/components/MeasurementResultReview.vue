<template>
  <div class="container mt-4">
    <!-- ページタイトル -->
    <h2 class="mb-4">測定結果の確認/承認</h2>

    <!-- データなし -->
    <div v-if="measurements.length === 0" class="alert alert-info">
      承認依頼はありません
    </div>

    <!-- テーブル形式 -->
    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th v-if="role === 'coach'">部員名</th>
            <th>計測日</th>
            <th>50m走 (sec)</th>
            <th>ベースランニング (sec)</th>
            <th>遠投 (m)</th>
            <th>ストレート球速 (km/h)</th>
            <th>打球速度 (km/h)</th>
            <th>スイング速度 (km/h)</th>
            <th>ベンチプレス (kg)</th>
            <th>スクワット (kg)</th>
            <th>承認の有無</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="measurement in measurements"
            :key="measurement.measurement_id"
          >
            <td v-if="role === 'coach'">
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
            <td>
              <div class="d-flex flex-wrap gap-2">
                <button
                  @click="handleApprove(measurement.measurement_id)"
                  type="button"
                  class="btn btn-primary"
                >
                  承認
                </button>
                <button
                  @click="handleReject(measurement.measurement_id)"
                  type="button"
                  class="btn btn-danger"
                >
                  否認
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { dummyMeasurements } from "@/dummyData";

const authStore = useAuthStore();
const role = authStore.role;
const measurements = ref([]);

onMounted(() => {
  if (role === "member") {
    measurements.value = dummyMeasurements.filter(
      (m) => m.user_id === authStore.userId && m.status === "pending_member",
    );
  } else if (role === "coach") {
    measurements.value = dummyMeasurements.filter(
      (m) => m.status === "pending_coach",
    );
  }
});

// 承認処理（ボタン押下時に実行）
const handleApprove = (measurementId) => {
  const target = dummyMeasurements.find(
    (m) => m.measurement_id === measurementId,
  );
  if (role === "member") {
    target.status = "pending_coach";
  } else if (role === "coach") {
    target.status = "approved";
  }
  // 画面の一覧から該当レコードを除外
  measurements.value = measurements.value.filter(
    (m) => m.measurement_id !== measurementId,
  );
};

// 否認処理（ボタン押下時に実行）
const handleReject = (measurementId) => {
  const target = dummyMeasurements.find(
    (m) => m.measurement_id === measurementId,
  );
  target.status = "rejected";
  // 画面の一覧から該当レコードを除外
  measurements.value = measurements.value.filter(
    (m) => m.measurement_id !== measurementId,
  );
};
</script>
