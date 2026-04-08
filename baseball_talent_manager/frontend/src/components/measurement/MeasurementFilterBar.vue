<template>
  <div class="d-flex flex-wrap gap-2 align-items-center">
    <!-- ソート -->
    <select
      class="form-select form-select-sm w-auto"
      :value="sortKey"
      @change="$emit('update:sortKey', $event.target.value)"
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
      @input="$emit('update:filterName', $event.target.value)"
    />

    <!-- 計測日 -->
    <select
      class="form-select form-select-sm w-auto"
      :value="filterMeasurementDate"
      @change="$emit('update:filterMeasurementDate', $event.target.value)"
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
      @change="$emit('update:filterGrade', $event.target.value)"
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

<script setup>
defineProps({
  sortKey: String,
  sortOrder: String,
  filterName: String,
  filterGrade: String,
  filterMeasurementDate: String,
  availableDates: Array,
  isStaff: Boolean,
  isResetDisabled: Boolean,
});

defineEmits([
  "update:sortKey",
  "update:filterName",
  "update:filterGrade",
  "update:filterMeasurementDate",
  "toggleOrder",
  "reset",
]);
</script>
