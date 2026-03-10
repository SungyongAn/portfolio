<template>
  <div class="container mt-4">
    <!-- ページタイトル -->
    <h2 class="mb-4">測定結果の確認/承認</h2>

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
            <th>計測日</th>

            <th v-for="field in MEASUREMENT_FIELDS" :key="field.key">
              {{ field.label }}
            </th>

            <th>承認の有無</th>
          </tr>
        </thead>

        <!-- データ -->
        <tbody>
          <tr
            v-for="measurement in measurements"
            :key="measurement.measurement_id"
          >
            <td v-if="isCoach">
              {{ measurement.name }}（{{ measurement.grade }}年）
            </td>

            <td>{{ measurement.measurement_date }}</td>

            <td v-for="field in MEASUREMENT_FIELDS" :key="field.key">
              {{ measurement[field.key] }}
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
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { dummyMeasurements } from "@/dummyData";

const authStore = useAuthStore();

const role = computed(() => authStore.role);

const isCoach = computed(() => role.value === "coach");

const MEASUREMENT_FIELDS = [
  {
    key: "sprint_50m",
    label: "50m走 (sec)",
  },
  {
    key: "base_running",
    label: "ベースランニング (sec)",
  },
  {
    key: "throwing_distance",
    label: "遠投 (m)",
  },
  {
    key: "pitch_speed",
    label: "ストレート球速 (km/h)",
  },
  {
    key: "batting_speed",
    label: "打球速度 (km/h)",
  },
  {
    key: "swing_speed",
    label: "スイング速度 (km/h)",
  },
  {
    key: "bench_press",
    label: "ベンチプレス (kg)",
  },
  {
    key: "squat",
    label: "スクワット (kg)",
  },
];

const APPROVE_STATUS = {
  member: "pending_coach",
  coach: "approved",
};

const measurements = computed(() => {
  if (role.value === "member") {
    return dummyMeasurements.filter(
      (m) => m.user_id === authStore.userId && m.status === "pending_member",
    );
  }

  if (role.value === "coach") {
    return dummyMeasurements.filter((m) => m.status === "pending_coach");
  }

  return [];
});

const hasMeasurements = computed(() => measurements.value.length > 0);

// ステータス更新
const updateStatus = (measurementId, newStatus) => {
  const target = dummyMeasurements.find(
    (m) => m.measurement_id === measurementId,
  );

  if (!target) return;

  target.status = newStatus;
};

const handleApprove = (measurementId) => {
  updateStatus(measurementId, APPROVE_STATUS[role.value]);
};

const handleReject = (measurementId) => {
  updateStatus(measurementId, "rejected");
};
</script>
