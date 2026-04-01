<template>
  <div class="card p-3">
    <h5 class="mb-3">ランキング</h5>

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

    <!-- テーブル -->
    <div v-if="ranking.length" class="table-responsive">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>順位</th>
            <th>氏名</th>
            <th>学年</th>
            <th>記録</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in ranking"
            :key="row.user_id"
            :class="{ 'table-primary': isMe(row.user_id) }"
          >
            <td>{{ row.rank }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.grade }}</td>
            <td>{{ formatValue(row.value) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="alert alert-info">データがありません</div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRankingData } from "@/composables/useRankingData.js";
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";
import { useAuthStore } from "@/stores/auth";

// props
const props = defineProps({
  measurements: {
    type: Array,
    default: () => [],
  },
});

// composable
const { getRanking } = useRankingData(computed(() => props.measurements));

// store
const authStore = useAuthStore();

// 選択項目
const selectedField = ref(MEASUREMENT_FIELDS[0]?.key || "");

// ランキングデータ
const ranking = computed(() => getRanking(selectedField.value));

// 自分判定
const isMe = (userId) => {
  return authStore.userId === userId;
};

// 表示フォーマット（最低限）
const formatValue = (value) => {
  if (value == null) return "-";
  return Number(value).toFixed(2);
};
</script>
