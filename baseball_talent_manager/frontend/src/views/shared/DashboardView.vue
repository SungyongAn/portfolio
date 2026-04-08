<template>
  <div class="container mt-4">
    <h2 class="mb-4">ダッシュボード</h2>

    <div class="row g-4">
      <!-- 測定確認 / 承認 -->
      <div v-if="isMember || isCoach" class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>測定結果の確認 / 承認</h5>
            <router-link :to="`/${role}/review`" class="btn btn-primary mt-3">
              測定結果の確認
            </router-link>
          </div>
        </div>
      </div>

      <!-- 測定記録閲覧 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>測定記録の閲覧</h5>
            <router-link
              :to="`/${role}/history`"
              class="btn btn-outline-primary mt-3"
            >
              測定記録一覧を見る
            </router-link>
          </div>
        </div>
      </div>

      <!-- 部員管理 -->
      <div v-if="isCoach || isDirector" class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>部員の管理</h5>
            <router-link :to="`/${role}/members`" class="btn btn-warning mt-3">
              管理画面へ
            </router-link>
          </div>
        </div>
      </div>

      <!-- 可視化ダッシュボード -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>可視化ダッシュボード</h5>
            <router-link
              :to="`/${role}/chart`"
              class="btn btn-outline-success mt-3"
            >
              グラフを見る
            </router-link>
          </div>
        </div>
      </div>

      <!-- 測定登録状況（コーチ・監督のみ） -->
      <div v-if="isCoach || isDirector" class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>測定登録状況</h5>
            <router-link
              :to="`/${role}/progress`"
              class="btn btn-outline-info mt-3"
            >
              登録状況を確認
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <!-- 通知サマリー -->
    <div v-if="!isDirector" class="row g-4 mt-1">
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="mb-3">通知サマリー</h5>

            <!-- 部員向け -->
            <div v-if="isMember">
              <div v-if="hasPendingMember" class="alert alert-warning mb-0">
                承認依頼があります
              </div>
              <div v-else class="text-muted">承認依頼はありません</div>
            </div>

            <!-- コーチ向け -->
            <div v-else-if="isCoach">
              <span class="badge bg-info text-dark">
                承認待ち件数: {{ pendingCoachCount }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useNotificationStore } from "@/stores/notification";
import { getMeasurements } from "@/services/measurementService";

const authStore = useAuthStore();
const notificationStore = useNotificationStore();

const role = computed(() => authStore.role);
const isMember = computed(() => authStore.isMember);
const isCoach = computed(() => authStore.isCoach);
const isDirector = computed(() => authStore.isDirector);

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

// 部員：承認待ちがあるか
const hasPendingMember = computed(() =>
  measurements.value.some((m) => m.status === "pending_member"),
);

// コーチ：承認待ち件数
const pendingCoachCount = computed(
  () => measurements.value.filter((m) => m.status === "pending_coach").length,
);
</script>
