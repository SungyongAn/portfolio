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
      <div v-if="activeTab === 'teamTrend'">
        <TeamTrendChart />
      </div>

      <div v-if="activeTab === 'playerTrend'">
        <PlayerTrendChart />
      </div>

      <div v-if="activeTab === 'radar'">
        <RadarChart />
      </div>

      <div v-if="activeTab === 'ranking'">
        <RankingTable />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import TeamTrendChart from "@/components/visualization/TeamTrendChart.vue";
import PlayerTrendChart from "@/components/visualization/PlayerTrendChart.vue";
import RadarChart from "@/components/visualization/RadarChart.vue";
import RankingTable from "@/components/visualization/RankingTable.vue";

const authStore = useAuthStore();

const role = computed(() => authStore.role);

// タブ定義
const tabs = [
  { key: "teamTrend", label: "チームの成長推移", roles: ["coach", "director"] },
  {
    key: "playerTrend",
    label: "個人の成長推移",
    roles: ["coach", "director", "member"],
  },
  { key: "radar", label: "能力比較", roles: ["coach", "director"] },
  {
    key: "ranking",
    label: "チーム内順位",
    roles: ["coach", "director", "member"],
  },
];

// ロールによる表示制御
const visibleTabs = computed(() =>
  tabs.filter((tab) => tab.roles.includes(role.value)),
);

// 初期タブ
const activeTab = ref(visibleTabs.value[0]?.key || "");
</script>
