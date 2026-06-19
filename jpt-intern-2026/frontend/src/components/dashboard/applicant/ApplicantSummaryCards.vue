<template>
  <div class="summary-cards">
    <el-card
      class="summary-card info"
      shadow="hover"
      @click="handleCardClick('pending')"
    >
      <div class="card-title">申請中</div>
      <div class="card-value">
        {{ applicantSummary?.pending ?? 0 }}<span>件</span>
      </div>
      <div class="card-desc">部門・本部承認待ち</div>
    </el-card>

    <el-card
      class="summary-card rejected"
      shadow="hover"
      @click="handleCardClick('rejected')"
    >
      <div class="card-title">却下</div>
      <div class="card-value">
        {{ applicantSummary?.rejected ?? 0 }}<span>件</span>
      </div>
      <div class="card-desc">差し戻し・再確認が必要</div>
    </el-card>

    <el-card
      class="summary-card danger"
      shadow="hover"
      @click="handleCardClick('risk')"
    >
      <div class="card-title">注意・危険</div>
      <div class="card-value">
        {{ summary.riskProjectCount }}<span>件</span>
      </div>
      <div class="card-desc">確認が必要な案件</div>
    </el-card>

    <el-card
      class="summary-card budget"
      shadow="hover"
      @click="handleCardClick('budget')"
    >
      <div class="card-title">予算消費率</div>
      <div class="card-value">
        {{ summary.totalConsumptionRate }}<span>%</span>
      </div>
      <div class="card-desc">
        実績 {{ formatCurrency(summary.totalActual) }} / 予算
        {{ formatCurrency(summary.totalBudget) }}
      </div>
    </el-card>

    <el-card
      class="summary-card draft"
      shadow="hover"
      @click="handleCardClick('draft')"
    >
      <div class="card-title">下書き</div>
      <div class="card-value">
        {{ applicantSummary?.draft ?? 0 }}<span>件</span>
      </div>
      <div class="card-desc">未申請の保存案件</div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import type { ApplicantSummary, DashboardSummary } from "@/api/dashboard";

defineProps<{
  summary: DashboardSummary;
  applicantSummary: ApplicantSummary | null;
}>();

const emit = defineEmits<{
  (
    e: "select-filter",
    filter: "pending" | "draft" | "rejected" | "risk" | "budget",
  ): void;
}>();

const handleCardClick = (
  filter: "pending" | "draft" | "rejected" | "risk" | "budget",
) => {
  emit("select-filter", filter);
};

const formatCurrency = (value?: number) => {
  const amount = value ?? 0;

  if (amount >= 100000000) {
    return `${Math.round(amount / 100000000)}億円`;
  }

  if (amount >= 10000) {
    return `${Math.round(amount / 10000)}万円`;
  }

  return `${amount.toLocaleString()}円`;
};
</script>

<style scoped>
.summary-cards {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.summary-card {
  min-width: 220px;
  flex: 0 0 220px;
}

.card-title {
  font-size: 13px;
  color: #606266;
}

.card-value {
  margin-top: 12px;
  font-size: 32px;
  font-weight: 700;
  color: #222;
}

.card-value span {
  margin-left: 4px;
  font-size: 13px;
  font-weight: 500;
  color: #606266;
}

.card-desc {
  margin-top: 8px;
  font-size: 11px;
  color: #909399;
}

.summary-card.info {
  background: #f0f5ff;
  border-color: #adc6ff;
}

.summary-card.draft {
  background: #f4f4f5;
  border-color: #dcdfe6;
}

.summary-card.rejected {
  background: #fff1f0;
  border-color: #ffccc7;
}

.summary-card.danger {
  background: #fff1f0;
  border-color: #ffccc7;
}

.summary-card.budget {
  background: #fff7e6;
  border-color: #ffd591;
}
</style>
