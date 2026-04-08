<template>
  <div class="d-flex flex-wrap gap-2 align-items-center">
    <!-- ソート -->
    <select
      class="form-select form-select-sm w-auto"
      :value="sortKey"
       @change="onSortChange"
    >
      <option value="measurement_date">計測日</option>
      <option v-if="isStaff" value="name">部員名</option>
      <option v-if="isStaff" value="grade">学年</option>
      <option value="sprint_50m">50m走</option>
      <option value="base_running">ベースランニング</option>
      <option value="throwing_distance">遠投</option>
      <option value="pitch_speed">球速</option>
      <option value="batting_speed">打球速度</option>
      <option value="swing_speed">スイング速度</option>
      <option value="bench_press">ベンチプレス</option>
      <option value="squat">スクワット</option>
    </select>

    <!-- 昇降順 -->
    <button
      class="btn btn-outline-primary btn-sm text-nowrap"
      @click="$emit('toggleOrder')"
    >
      {{ sortOrder === "asc" ? "昇順 ↑" : "降順 ↓" }}
    </button>

    <!-- 名前 -->
    <input
      class="form-control form-control-sm w-auto"
      type="text"
      placeholder="名前検索"
      :value="filterName"
      @input="onNameInput" 
    />

    <!-- 計測日 -->
    <select
      class="form-select form-select-sm w-auto"
      :value="filterMeasurementDate"
      @change="onDateChange"
    >
      <option value="">計測日（全て）</option>
      <option v-for="date in availableDates" :key="date" :value="date">
        {{ date }}
      </option>
    </select>

    <!-- 学年 -->
    <select
      class="form-select form-select-sm w-auto"
      :value="filterGrade"
      @change="onGradeChange"
    >
      <option value="">学年（全て）</option>
      <option value="1">1年</option>
      <option value="2">2年</option>
      <option value="3">3年</option>
    </select>

    <!-- リセット -->
    <button
      class="btn btn-outline-danger btn-sm text-nowrap"
      :disabled="isResetDisabled"
      @click="$emit('reset')"
    >
      リセット
    </button>
  </div>
</template>

<script setup lang="ts">
/* -----------------------------
   型定義
----------------------------- */

export type SortKey = 
  | "measurement_date"
  | "name"
  | "grade"
  | "sprint_50m"
  | "base_running"
  | "throwing_distance"
  | "pitch_speed"
  | "batting_speed"
  | "swing_speed"
  | "bench_press"
  | "squat";

type SortOrder = "asc" | "desc";

export type Grade = "" | "1" | "2" | "3";

/* -----------------------------
   Props（省略形）
----------------------------- */

defineProps<{
  sortKey: SortKey;
  sortOrder: SortOrder;
  filterName: string;
  filterGrade: Grade;
  filterMeasurementDate: string;
  availableDates: string[];
  isStaff: boolean;
  isResetDisabled: boolean;
}>();

/* -----------------------------
   Emits
----------------------------- */

const emit = defineEmits<{
  (e: "update:sortKey", value: SortKey): void;
  (e: "update:filterName", value: string): void;
  (e: "update:filterGrade", value: Grade): void;
  (e: "update:filterMeasurementDate", value: string): void;
  (e: "toggleOrder"): void;
  (e: "reset"): void;
}>();

/* -----------------------------
   イベントハンドラ（型安全化）
----------------------------- */

const onSortChange = (e: Event) => {
  const value = (e.target as HTMLSelectElement).value as SortKey;
  emit("update:sortKey", value);
};

const onNameInput = (e: Event) => {
  const value = (e.target as HTMLInputElement).value;
  emit("update:filterName", value);
};

const onDateChange = (e: Event) => {
  const value = (e.target as HTMLSelectElement).value;
  emit("update:filterMeasurementDate", value);
};

const onGradeChange = (e: Event) => {
  const value = (e.target as HTMLSelectElement).value as Grade;
  emit("update:filterGrade", value);
};
</script>