<template>
  <div class="container mt-4">
    <h2 class="mb-4">推移分析</h2>

    <!-- 測定項目選択 -->
    <div class="mb-3">
      <label class="form-label">測定項目</label>
      <select v-model="selectedField" class="form-select">
        <option
          v-for="field in MEASUREMENT_FIELDS"
          :key="field.key"
          :value="field.key"
        >
          {{ field.label }}
        </option>
      </select>
    </div>

    <!-- 部員選択（staffのみ） -->
    <div v-if="isStaff" class="mb-3">
      <label class="form-label">部員選択</label>
      <select v-model="selectedPlayerId" class="form-select">
        <option v-for="player in players" :key="player.id" :value="player.id">
          {{ player.name }}
        </option>
      </select>
    </div>

    <!-- タブ -->
    <ul class="nav nav-tabs mb-3">
      <!-- ★ staffのみ -->
      <li v-if="isStaff" class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'teamTrend' }"
          @click="activeTab = 'teamTrend'"
        >
          チーム推移
        </button>
      </li>

      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'playerTrend' }"
          @click="activeTab = 'playerTrend'"
        >
          個人推移
        </button>
      </li>
    </ul>

    <!-- チーム推移 -->
    <div v-if="activeTab === 'teamTrend'">
      <TrendChart
        :series="teamTrend.series"
        :labels="teamTrend.labels"
        :unit="selectedFieldUnit"
      />
    </div>

    <!-- 個人推移 -->
    <div v-if="activeTab === 'playerTrend'">
      <TrendChart
        :series="playerTrend.series"
        :labels="playerTrend.labels"
        :unit="selectedFieldUnit"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useTrendData } from "@/composables/useTrendData";
import TrendChart from "@/components/visualization/TrendChart.vue";
import { useAuthStore } from "@/stores/auth";
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";

// 型
import type { Measurement } from "@/services/measurementService";
import type { MeasurementFieldKey } from "@/constants/measurementFields";
import type { Player, TrendSeries } from "@/composables/useTrendData";

/* -----------------------------
  Props
----------------------------- */
const props = defineProps<{
  measurements: Measurement[];
}>();

/* -----------------------------
  store
----------------------------- */
const authStore = useAuthStore();
const isStaff = computed(() => authStore.isStaff);

/* -----------------------------
  composable
----------------------------- */
const { players, getTrendSeries } = useTrendData(
  computed(() => props.measurements)
);

/* -----------------------------
  状態管理
----------------------------- */
type ActiveTab = "teamTrend" | "playerTrend";

const activeTab = ref<ActiveTab>(
  isStaff.value ? "teamTrend" : "playerTrend"
);

const selectedField = ref<MeasurementFieldKey>(
  MEASUREMENT_FIELDS[0]?.key as MeasurementFieldKey
);

const selectedPlayerId = ref<number | null>(null);

/* -----------------------------
  初期選択
----------------------------- */
watch(
  players,
  (list) => {
    if (!list.length) return;

    selectedPlayerId.value = isStaff.value
      ? list[0].id
      : authStore.userId;
  },
  { immediate: true }
);

/* -----------------------------
  unit
----------------------------- */
const selectedFieldUnit = computed((): string => {
  const field = MEASUREMENT_FIELDS.find(
    (f) => f.key === selectedField.value
  );
  return field?.unit || "";
});

/* -----------------------------
  チーム推移
----------------------------- */
const teamTrend = computed<TrendSeries>(() =>
  getTrendSeries({
    fieldKey: selectedField.value,
  })
);

/* -----------------------------
  個人推移
----------------------------- */
const playerTrend = computed<TrendSeries>(() => {
  if (!selectedPlayerId.value) {
    return { series: [], labels: [] };
  }

  return getTrendSeries({
    fieldKey: selectedField.value,
    userId: selectedPlayerId.value,
  });
});
</script>