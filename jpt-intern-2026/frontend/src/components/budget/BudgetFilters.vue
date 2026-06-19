<template>
  <div class="header-actions">
    <el-input
      v-model="keywordModel"
      placeholder="案件名で検索"
      clearable
      :empty-values="[null]"
      style="width: 240px"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>

    <el-select
      v-model="statusFilterModel"
      placeholder="ステータス"
      clearable
      :empty-values="[null]"
      :value-on-clear="null"
    >
      <el-option label="承認済み" value="APPROVED" />
      <el-option label="進行中" value="IN_PROGRESS" />
      <el-option label="完了" value="COMPLETED" />
    </el-select>

    <el-select
      v-if="showDepartmentFilter"
      v-model="departmentFilterModel"
      placeholder="部門"
      clearable
      :empty-values="[null]"
      :value-on-clear="null"
    >
      <el-option
        v-for="dept in departments"
        :key="dept.id"
        :label="dept.name"
        :value="dept.id"
      />
    </el-select>

    <el-select
      v-model="budgetFilterModel"
      placeholder="予算帯"
      clearable
      :empty-values="[null]"
      :value-on-clear="null"
    >
      <el-option label="〜500万円" value="low" />
      <el-option label="500万〜1,000万円" value="mid" />
      <el-option label="1,000万円〜" value="high" />
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { Search } from "@element-plus/icons-vue";
import type { Department } from "@/api/departments";

type BudgetFilter = "low" | "mid" | "high" | null;

defineProps<{
  departments: Department[];
  showDepartmentFilter: boolean;
}>();

const keywordModel = defineModel<string>("keyword", { required: true });
const statusFilterModel = defineModel<string>("statusFilter", {
  required: true,
});
const departmentFilterModel = defineModel<number | null>("departmentFilter", {
  required: true,
});
const budgetFilterModel = defineModel<BudgetFilter>("budgetFilter", {
  required: true,
});
</script>

<style scoped>
.header-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
</style>
