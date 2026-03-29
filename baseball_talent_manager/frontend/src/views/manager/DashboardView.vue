<template>
  <div class="container mt-4">
    <h2 class="mb-4">ダッシュボード</h2>

    <div class="row g-4">
      <!-- 測定結果の入力 / 承認依頼 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>測定結果の入力/承認依頼</h5>
            <router-link :to="`/manager/record`" class="btn btn-primary mt-3">
              測定結果の入力
            </router-link>
          </div>
        </div>
      </div>

      <!-- 承認依頼中のステータス確認 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>承認依頼中のステータス確認</h5>
            <router-link :to="`/manager/status`" class="btn btn-warning mt-3">
              承認依頼中のステータス確認
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 通知サマリー -->
    <div class="row g-4 mt-1">
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="mb-3">通知サマリー</h5>

            <!-- ステータス件数 -->
            <div class="d-flex flex-wrap gap-3 mb-3">
              <span class="badge bg-danger"> 否認: {{ rejectedCount }} </span>
              <span class="badge bg-warning text-dark">
                部員承認待ち: {{ pendingMemberCount }}
              </span>
              <span class="badge bg-info text-dark">
                コーチ承認待ち: {{ pendingCoachCount }}
              </span>
            </div>

            <!-- 新着通知 -->
            <div v-if="notificationStore.notifications.length > 0">
              <div
                v-for="(n, index) in notificationStore.notifications.slice(
                  0,
                  5,
                )"
                :key="index"
                class="alert alert-secondary py-2 mb-2"
              >
                {{ n.message }}
              </div>
            </div>

            <div v-else class="text-muted">新着通知はありません</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useNotificationStore } from "@/stores/notification";
import { getMeasurements } from "@/services/measurementService";

const notificationStore = useNotificationStore();
const measurements = ref([]);

const fetchMeasurements = async () => {
  try {
    const res = await getMeasurements();
    measurements.value = res.data.measurements ?? [];
  } catch (e) {
    measurements.value = [];
  }
};

onMounted(fetchMeasurements);

// 通知受信時にデータを再取得
watch(() => notificationStore.notifications.length, fetchMeasurements);

const rejectedCount = computed(
  () => measurements.value.filter((m) => m.status === "rejected").length,
);

const pendingMemberCount = computed(
  () => measurements.value.filter((m) => m.status === "pending_member").length,
);

const pendingCoachCount = computed(
  () => measurements.value.filter((m) => m.status === "pending_coach").length,
);
</script>
