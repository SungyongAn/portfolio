<template>
  <div class="d-flex justify-content-between align-items-center mt-3">
    <!-- 件数 -->
    <select v-model="localPageSize" class="form-select form-select-sm w-auto">
      <option :value="10">10件</option>
      <option :value="20">20件</option>
      <option :value="50">50件</option>
    </select>

    <!-- ページ操作 -->
    <div class="d-flex align-items-center gap-2 flex-nowrap">
      <button
        class="btn btn-sm btn-outline-secondary"
        :disabled="modelValue === 1"
        @click="$emit('update:modelValue', modelValue - 1)"
      >
        ←
      </button>

      <span style="white-space: nowrap">
        {{ modelValue }} / {{ totalPages }}
      </span>

      <button
        class="btn btn-sm btn-outline-secondary"
        :disabled="modelValue === totalPages"
        @click="$emit('update:modelValue', modelValue + 1)"
      >
        →
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  modelValue: Number, // currentPage
  totalPages: Number,
  pageSize: Number,
});

const emit = defineEmits(["update:modelValue", "update:pageSize"]);

const localPageSize = computed({
  get: () => props.pageSize,
  set: (val) => emit("update:pageSize", val),
});
</script>
