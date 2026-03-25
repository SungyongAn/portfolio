<template>
  <div class="d-flex gap-2 align-items-center flex-wrap">
    <!-- ソート項目 -->
    <select
      :value="sortKey"
      @change="$emit('update:sortKey', $event.target.value)"
      class="form-select form-select-sm w-auto"
    >
      <option value="name">部員名</option>
      <option value="grade">学年</option>
    </select>

    <!-- 昇順 / 降順 -->
    <button
      @click="$emit('toggleOrder')"
      class="btn btn-outline-primary btn-sm text-nowrap"
    >
      {{ sortOrder === "asc" ? "昇順 ↑" : "降順 ↓" }}
    </button>

    <!-- 名前フィルタ -->
    <input
      :value="filterName"
      @input="$emit('update:filterName', $event.target.value)"
      type="text"
      placeholder="名前検索"
      class="form-control form-control-sm w-auto"
    />

    <!-- 学年フィルタ -->
    <select
      :value="filterGrade"
      @change="$emit('update:filterGrade', $event.target.value)"
      class="form-select form-select-sm w-auto"
    >
      <option value="">学年（全て）</option>
      <option value="1">1年</option>
      <option value="2">2年</option>
      <option value="3">3年</option>
    </select>

    <!-- リセット -->
    <button
      @click="$emit('reset')"
      :disabled="isResetDisabled"
      class="btn btn-outline-secondary btn-sm text-nowrap"
    >
      リセット
    </button>
  </div>
</template>

<script setup>
defineProps({
  sortKey: String,
  sortOrder: String,
  filterName: String,
  filterGrade: [String, Number],
  isResetDisabled: Boolean,
});

defineEmits([
  "update:sortKey",
  "update:filterName",
  "update:filterGrade",
  "toggleOrder",
  "reset",
]);
</script>
