<template>
  <div class="container mt-4">
    <h2 class="mb-4">分析・可視化</h2>

    <!-- タブナビゲーション -->
    <ul class="nav nav-tabs mb-3">
      <li v-for="tab in visibleTabs" :key="tab.key" class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </li>
    </ul>

    <!-- タブコンテンツ -->
    <div class="tab-content">
      <div v-if="activeTab === 'trend'">
        <TrendChartView :measurements="allMeasurements" />
      </div>

      <div v-if="activeTab === 'radar'">
        <RadarChart :measurements="allMeasurements" />
      </div>

      <div v-if="activeTab === 'ranking'">
        <RankingTable :measurements="allMeasurements" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { getAllMeasurements } from "@/services/measurementService.js";
import TrendChartView from "@/components/visualization/TrendChartView.vue";
// @ts-ignore
import RadarChart from "@/components/visualization/RadarChart.vue";
import RankingTable from "@/components/visualization/RankingTable.vue";
import type { Measurement } from "@/services/measurementService";
import type { Role } from "@/stores/auth";

const authStore = useAuthStore();
const role = computed(() => authStore.role);

const allMeasurements = ref<Measurement[]>([]);

onMounted(async () => {
  const res = await getAllMeasurements();
  allMeasurements.value = res.data.measurements.filter(
    (m: Measurement) => m.status === "approved",  // 明示的に型付け
  );
});

const tabs = [
  { key: "trend", label: "成長推移", roles: ["coach", "director", "member"] },
  { key: "radar", label: "能力比較", roles: ["coach", "director"] },
  { key: "ranking", label: "チーム内順位", roles: ["coach", "director", "member"] },
] as const;

type Tab = (typeof tabs)[number];

const visibleTabs = computed(() => {
  if (!role.value) return [];
  return tabs.filter((tab) =>
    (tab.roles as readonly string[]).includes(role.value!)  // ← 修正
  );
});

const activeTab = ref<Tab["key"]>(visibleTabs.value[0]?.key || "trend");
</script>