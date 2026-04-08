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

<script setup lang="ts">
import { computed } from "vue";

/* -----------------------------
   Props（省略形）
----------------------------- */

const props = defineProps<{
  modelValue: number;
  totalPages: number;
  pageSize: number;
}>();

/* -----------------------------
   Emits
----------------------------- */

const emit = defineEmits<{
  (e: "update:modelValue", value: number): void;
  (e: "update:pageSize", value: number): void;
}>();

/* -----------------------------
   PageSize（v-model用）
----------------------------- */

const localPageSize = computed<number>({
  get: () => props.pageSize,
  set: (val) => emit("update:pageSize", Number(val)),
});
</script>
