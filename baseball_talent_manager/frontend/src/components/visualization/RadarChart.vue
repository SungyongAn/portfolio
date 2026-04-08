<template>
  <div class="card p-3">
    <h5 class="mb-3">能力比較</h5>

    <!-- 部員選択（staff想定：複数選択） -->
    <div class="mb-3">
      <label class="form-label">部員選択</label>
      <select v-model="selectedPlayerIds" class="form-select" multiple>
        <option v-for="player in players" :key="player.id" :value="player.id">
          {{ player.name }}
        </option>
      </select>
    </div>

    <!-- チャート -->
    <v-chart :option="chartOption" autoresize style="height: 400px" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import VChart from "vue-echarts";
import { useRadarData } from "@/composables/useRadarData.js";
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";

// ECharts
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { RadarChart } from "echarts/charts";
import { TooltipComponent, LegendComponent } from "echarts/components";

use([CanvasRenderer, RadarChart, TooltipComponent, LegendComponent]);

// props
const props = defineProps({
  measurements: {
    type: Array,
    default: () => [],
  },
});

// composable
const { players, getRadarSeries, getTeamAvgSeries } = useRadarData(
  computed(() => props.measurements),
);

// 選択状態
const selectedPlayerIds = ref([]);

// 初期選択（全員 or 先頭1人など用途に応じて調整可）
watch(
  players,
  (list) => {
    if (!list.length) return;

    // 例：最初は1人だけ選択
    selectedPlayerIds.value = [list[0].id];
  },
  { immediate: true },
);

// チャートデータ生成
const chartOption = computed(() => {
  const indicators = MEASUREMENT_FIELDS.map((field) => ({
    name: field.label,
    max: 100,
  }));

  // 選択選手
  const playerSeries = getRadarSeries(selectedPlayerIds.value);

  // チーム平均
  const teamSeries = getTeamAvgSeries();

  const seriesData =
    selectedPlayerIds.value.length > 0
      ? [...teamSeries, ...playerSeries]
      : teamSeries;

  return {
    tooltip: {},
    legend: {
      data: seriesData.map((s) => s.name),
    },
    radar: {
      indicator: indicators,
    },
    series: [
      {
        type: "radar",
        data: seriesData,
      },
    ],
  };
});
</script>
