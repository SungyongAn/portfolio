<template>
  <div class="card p-3">
    <h5 class="mb-3">推移グラフ</h5>
    <v-chart :option="chartOption" autoresize style="height: 400px" />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { LineChart } from "echarts/charts";
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

// 型
import type { EChartsOption } from "echarts";

/* -----------------------------
  ECharts
----------------------------- */
use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
]);

/* -----------------------------
  型定義
----------------------------- */
type SeriesItem = {
  name: string;
  data: number[];
};

/* -----------------------------
  Props
----------------------------- */
const props = defineProps<{
  series: SeriesItem[];
  labels: string[];
  unit?: string;
}>();

/* -----------------------------
  chart option
----------------------------- */
const chartOption = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: "axis",
    valueFormatter: (value: number) =>
      props.unit ? `${value} ${props.unit}` : value,
  },
  legend: {
    data: props.series.map((s) => s.name),
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true,
  },
  xAxis: {
    type: "category",
    data: props.labels,
  },
  yAxis: {
    type: "value",
  },
  series: props.series.map((s) => ({
    name: s.name,
    type: "line",
    data: s.data,
    smooth: true,
  })),
}));
</script>