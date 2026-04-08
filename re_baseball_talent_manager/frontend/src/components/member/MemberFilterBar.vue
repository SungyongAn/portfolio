<template>
  <div class="d-flex gap-2 align-items-center flex-wrap">
    <!-- ソート項目 -->
    <select
      :value="sortKey"
      @change="onChangeSortKey"
      class="form-select form-select-sm w-auto"
    >
      <option value="name">部員名</option>
      <option value="grade">学年</option>
    </select>

    <!-- 昇順 / 降順 -->
    <button
      @click="emit('toggleOrder')"
      class="btn btn-outline-primary btn-sm text-nowrap"
    >
      {{ sortOrder === "asc" ? "昇順 ↑" : "降順 ↓" }}
    </button>

    <!-- 名前フィルタ -->
    <input
      :value="filterName"
      @input="onInputName"
      type="text"
      placeholder="名前検索"
      class="form-control form-control-sm w-auto"
    />

    <!-- 学年フィルタ -->
    <select
      :value="filterGrade"
      @change="onChangeGrade"
      class="form-select form-select-sm w-auto"
    >
      <option value="">学年（全て）</option>
      <option value="1">1年</option>
      <option value="2">2年</option>
      <option value="3">3年</option>
    </select>

    <!-- リセット -->
    <button
      @click="emit('reset')"
      :disabled="isResetDisabled"
      class="btn btn-outline-secondary btn-sm text-nowrap"
    >
      リセット
    </button>
  </div>
</template>

<script setup lang="ts">
/* -----------------------------
  型定義
----------------------------- */

// ソートキー
type SortKey = "name" | "grade";

// ソート順
type SortOrder = "asc" | "desc";

/* -----------------------------
  Props
----------------------------- */
const props = defineProps<{
  sortKey: SortKey;
  sortOrder: SortOrder;
  filterName: string;
  filterGrade: string | number | "";
  isResetDisabled: boolean;
}>();

/* -----------------------------
  Emits
----------------------------- */
const emit = defineEmits<{
  (e: "update:sortKey", value: SortKey): void;
  (e: "update:filterName", value: string): void;
  (e: "update:filterGrade", value: string | number): void;
  (e: "toggleOrder"): void;
  (e: "reset"): void;
}>();

/* -----------------------------
  イベントハンドラ
  ※ $event.target.value は型が弱いので補強
----------------------------- */
const onChangeSortKey = (e: Event) => {
  const value = (e.target as HTMLSelectElement).value as SortKey;
  emit("update:sortKey", value);
};

const onInputName = (e: Event) => {
  const value = (e.target as HTMLInputElement).value;
  emit("update:filterName", value);
};

const onChangeGrade = (e: Event) => {
  const value = (e.target as HTMLSelectElement).value;
  emit("update:filterGrade", value);
};
</script>
