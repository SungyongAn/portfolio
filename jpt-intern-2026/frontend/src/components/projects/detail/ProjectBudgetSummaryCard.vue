<template>
  <el-card class="project-budget-summary-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>予算サマリ</span>

        <div class="header-actions">
          <el-button
            v-if="canOpenBudget"
            size="small"
            @click="$emit('open-budget')"
          >
            詳細
          </el-button>

          <el-button link @click="collapsed = !collapsed">
            <el-icon>
              <ArrowUp v-if="!collapsed" />
              <ArrowDown v-else />
            </el-icon>
          </el-button>
        </div>
      </div>
    </template>

    <el-descriptions v-if="budget && !collapsed" :column="4" border>
      <el-descriptions-item label="予算額">
        {{ formatCurrency(budget.budget_amount) }}
      </el-descriptions-item>

      <el-descriptions-item label="実績額">
        {{ formatCurrency(budget.actual_amount) }}
      </el-descriptions-item>

      <el-descriptions-item label="金額消化率">
        <div class="rate-cell">
          <el-progress
            :percentage="budgetUsageRate"
            :stroke-width="8"
            :show-text="false"
          />
          <span>{{ budgetUsageRate }}%</span>
        </div>
      </el-descriptions-item>

      <el-descriptions-item label="残予算">
        {{ formatCurrency(remainingAmount) }}
      </el-descriptions-item>

      <el-descriptions-item label="計画工数">
        {{ budget.planned_months ?? 0 }} 人月
      </el-descriptions-item>

      <el-descriptions-item label="人月単価">
        {{ formatCurrency(budget.unit_price) }}
      </el-descriptions-item>
    </el-descriptions>

    <el-empty
      v-else-if="!budget"
      description="予算情報が登録されていません"
      :image-size="80"
    />
  </el-card>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArrowUp, ArrowDown } from "@element-plus/icons-vue";

import type { ProjectBudgetResponse } from "@/api/models/ProjectBudgetResponse";

const props = defineProps<{
  budget: ProjectBudgetResponse | null;
  canOpenBudget?: boolean;
}>();

defineEmits<{
  (e: "open-budget"): void;
}>();

const collapsed = ref(false);

const budgetAmount = computed(() => {
  return props.budget?.budget_amount ?? 0;
});

const actualAmount = computed(() => {
  return props.budget?.actual_amount ?? 0;
});

const remainingAmount = computed(() => {
  return budgetAmount.value - actualAmount.value;
});

const budgetUsageRate = computed(() => {
  if (props.budget?.consumption_rate != null) {
    return Math.round(props.budget.consumption_rate);
  }

  if (budgetAmount.value <= 0) {
    return 0;
  }

  return Math.round((actualAmount.value / budgetAmount.value) * 100);
});

const formatCurrency = (value?: number | null) => {
  if (value == null) return "-";

  return `${value.toLocaleString("ja-JP")} 円`;
};
</script>

<style scoped>
.project-budget-summary-card {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rate-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rate-cell :deep(.el-progress) {
  flex: 1;
  min-width: 80px;
}
</style>
